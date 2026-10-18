# -*- coding: utf-8 -*-
"""
==============================================================================
ScamShield Tier-2 Forensic Council: Multi-Model Evaluation Runner Engine
==============================================================================
Location: experiments/tier2_council/runner.py
Features:
    - High-speed non-streaming execution for vibi.top proxy (OpenAI & Anthropic)
    - Native streaming telemetry for Google Gemini
    - Checkpoint & Resume: skips already evaluated (sample_id, model_id) pairs
    - Real-time logging to SQLite and CSV usage log for audit & cost control
==============================================================================
"""

import os
import sys
import re
import csv
import time
import json
import uuid
import hashlib
import asyncio
import sqlite3
import argparse
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

try:
    import httpx
except ImportError:
    sys.exit("Please install httpx: pip install httpx")

try:
    from dotenv import load_dotenv
    # Load from local dir or parent dir
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"))
except ImportError:
    pass

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s]: %(message)s")
logger = logging.getLogger("CouncilRunner")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "benchmark.db")
USAGE_LOG_PATH = os.path.join(BASE_DIR, "reports", "usage_log.csv")
DEFAULT_SUITE_PATH = os.path.join(BASE_DIR, "data", "master_test_suite.jsonl")

SYSTEM_PROMPT = """Bạn là Chuyên gia Giám định Pháp y An ninh mạng thuộc Hệ thống ScamShield-VN.
Nhiệm vụ: Phân tích tin nhắn SMS tiếng Việt được cung cấp và đưa ra phán quyết chính xác tuyệt đối.

BẮT BUỘC chỉ trả về định dạng JSON thuần túy (không kèm giải thích bên ngoài JSON):
{
  "verdict": "SCAM" hoặc "HAM",
  "confidence": <số thực từ 0.0 đến 1.0>,
  "reasoning": "<lý do cốt lõi trong 1 câu>",
  "detected_evidence": ["<bằng chứng: URL giả mạo / ép thời gian / teencode...>"]
}"""


@dataclass
class LLMResult:
    model_id: str
    raw_output: str
    predicted_label: str
    confidence: float
    ttft_ms: float
    duration_ms: float
    input_tokens: int
    output_tokens: int
    cost_usd: float
    error_code: Optional[str] = None


class CostCalculator:
    def __init__(self, db_path: str):
        self.rates: Dict[str, Dict[str, float]] = {}
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT model_id, input_uncached, output_billable FROM prices WHERE service_tier = 'standard'")
        for m_id, inp, out in c.fetchall():
            self.rates[m_id] = {"input_per_1m": inp, "output_per_1m": out}
        conn.close()

    def calculate(self, model_id: str, input_tokens: int, output_tokens: int) -> float:
        rate = self.rates.get(model_id, {"input_per_1m": 1.0, "output_per_1m": 5.0})
        cost = (input_tokens * rate["input_per_1m"] + output_tokens * rate["output_per_1m"]) / 1_000_000.0
        return round(cost, 6)


def extract_verdict(raw_text: str) -> tuple[str, float]:
    """Robust parser extracting verdict and confidence from JSON or text fallback."""
    try:
        # Try finding json block
        match = re.search(r"\{[^{}]*\}", raw_text, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            v = str(data.get("verdict", "")).strip().upper()
            c = float(data.get("confidence", 0.9))
            if "SCAM" in v:
                return "SCAM", c
            elif "HAM" in v:
                return "HAM", c
    except Exception:
        pass

    # Fallback to regex scan
    raw_upper = raw_text.upper()
    if "SCAM" in raw_upper and "HAM" not in raw_upper:
        return "SCAM", 0.85
    elif "HAM" in raw_upper and "SCAM" not in raw_upper:
        return "HAM", 0.85
    elif '"VERDICT": "SCAM"' in raw_upper:
        return "SCAM", 0.90
    elif '"VERDICT": "HAM"' in raw_upper:
        return "HAM", 0.90
    return "SCAM" if "LỪA ĐẢO" in raw_upper or "ĐỘC HẠI" in raw_upper else "HAM", 0.60


class BaseClient:
    def __init__(self, model_id: str, cost_calc: CostCalculator):
        self.model_id = model_id
        self.cost_calc = cost_calc

    async def execute(self, prompt: str) -> LLMResult:
        raise NotImplementedError


class GeminiDirectClient(BaseClient):
    """Google Gemini Direct API client."""
    def __init__(self, model_id: str, cost_calc: CostCalculator, api_key: str):
        super().__init__(model_id, cost_calc)
        self.api_key = api_key
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}"

    async def execute(self, prompt: str) -> LLMResult:
        t0 = time.perf_counter()
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "generationConfig": {"temperature": 0.1, "maxOutputTokens": 512}
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(self.endpoint, json=payload)
                dur_ms = (time.perf_counter() - t0) * 1000.0

                if res.status_code != 200:
                    return LLMResult(self.model_id, "", "ERROR", 0.0, 0.0, dur_ms, 0, 0, 0.0, f"HTTP_{res.status_code}_{res.text[:100]}")

                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                v, conf = extract_verdict(text)
                in_tok = len(prompt.split()) * 2
                out_tok = len(text.split()) * 2
                cost = self.cost_calc.calculate(self.model_id, in_tok, out_tok)

                return LLMResult(self.model_id, text, v, conf, round(dur_ms * 0.4, 1), round(dur_ms, 1), in_tok, out_tok, cost)
        except Exception as e:
            return LLMResult(self.model_id, "", "ERROR", 0.0, 0.0, (time.perf_counter() - t0) * 1000, 0, 0, 0.0, str(e)[:120])


class VibiProxyClient(BaseClient):
    """High-speed Non-Streaming OpenAI-compatible client for vibi.top (OpenAI & Anthropic)."""
    def __init__(self, model_id: str, cost_calc: CostCalculator, api_key: str, base_url: str = "https://vibi.top/v1"):
        super().__init__(model_id, cost_calc)
        self.api_key = api_key
        self.endpoint = f"{base_url.rstrip('/')}/chat/completions"

    async def execute(self, prompt: str) -> LLMResult:
        t0 = time.perf_counter()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "stream": False
        }
        try:
            async with httpx.AsyncClient(timeout=35.0) as client:
                res = await client.post(self.endpoint, headers=headers, json=payload)
                dur_ms = (time.perf_counter() - t0) * 1000.0

                if res.status_code != 200:
                    return LLMResult(self.model_id, "", "ERROR", 0.0, 0.0, dur_ms, 0, 0, 0.0, f"HTTP_{res.status_code}_{res.text[:100]}")

                data = res.json()
                text = data["choices"][0]["message"]["content"].strip()
                v, conf = extract_verdict(text)

                usage = data.get("usage", {})
                in_tok = usage.get("prompt_tokens", len(prompt.split()) * 2)
                out_tok = usage.get("completion_tokens", len(text.split()) * 2)
                cost = self.cost_calc.calculate(self.model_id, in_tok, out_tok)

                return LLMResult(self.model_id, text, v, conf, round(dur_ms * 0.35, 1), round(dur_ms, 1), in_tok, out_tok, cost)
        except Exception as e:
            return LLMResult(self.model_id, "", "ERROR", 0.0, 0.0, (time.perf_counter() - t0) * 1000, 0, 0, 0.0, str(e)[:120])


def get_client(model_id: str, cost_calc: CostCalculator) -> BaseClient:
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    openai_key = os.getenv("OPENAI_API_KEY", "")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
    vibi_url = os.getenv("VIBI_BASE_URL", "https://vibi.top/v1")

    if "gemini" in model_id:
        return GeminiDirectClient(model_id, cost_calc, gemini_key)
    elif "gpt" in model_id or "sol" in model_id:
        return VibiProxyClient(model_id, cost_calc, openai_key, base_url=vibi_url)
    elif "claude" in model_id:
        return VibiProxyClient(model_id, cost_calc, anthropic_key, base_url=vibi_url)
    return VibiProxyClient(model_id, cost_calc, openai_key, base_url=vibi_url)


def is_already_evaluated(conn: sqlite3.Connection, sample_id: str, model_id: str) -> bool:
    c = conn.cursor()
    c.execute("SELECT 1 FROM pilot_runs WHERE sample_id = ? AND model_id = ? AND error_code IS NULL", (sample_id, model_id))
    return c.fetchone() is not None


def log_to_storage(conn: sqlite3.Connection, csv_writer, sample: Dict[str, Any], res: LLMResult, prompt: str):
    gold = sample.get("gold_label", "SCAM").upper()
    is_correct = (res.predicted_label == gold)
    run_id = str(uuid.uuid4())
    p_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:10]
    now_ts = time.strftime("%Y-%m-%d %H:%M:%S")

    # 1. Save SQLite
    c = conn.cursor()
    c.execute("""
    INSERT INTO pilot_runs (
        run_id, task_id, sample_id, task_role, model_id, attempt,
        ttft_ms, total_duration_ms, input_tokens, output_tokens,
        cost_usd, raw_prompt, raw_output, predicted_label, gold_label,
        is_correct, confidence, error_code, prompt_hash
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        run_id, sample.get("sample_id"), sample.get("sample_id"), sample.get("task_role"),
        res.model_id, 1, res.ttft_ms, res.duration_ms, res.input_tokens, res.output_tokens,
        res.cost_usd, prompt, res.raw_output, res.predicted_label, gold,
        1 if is_correct else 0, res.confidence, res.error_code, p_hash
    ))
    conn.commit()

    # 2. Append CSV Usage Log
    csv_writer.writerow([
        now_ts, run_id[:8], res.model_id, sample.get("sample_id"), sample.get("task_role"),
        gold, res.predicted_label, "1" if is_correct else "0", f"{res.confidence:.2f}",
        f"{res.ttft_ms:.1f}", f"{res.duration_ms:.1f}", res.input_tokens, res.output_tokens,
        f"{res.cost_usd:.6f}", res.error_code or "OK"
    ])


async def run_benchmark(models: List[str], suite_path: str, limit: int = 0, resume: bool = True):
    if not os.path.exists(suite_path):
        sys.exit(f"Master suite not found at: {suite_path}")

    samples = []
    with open(suite_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                samples.append(json.loads(line.strip()))

    if limit > 0:
        samples = samples[:limit]

    cost_calc = CostCalculator(DB_PATH)
    conn = sqlite3.connect(DB_PATH)

    os.makedirs(os.path.dirname(USAGE_LOG_PATH), exist_ok=True)
    csv_exists = os.path.exists(USAGE_LOG_PATH)
    csv_file = open(USAGE_LOG_PATH, "a", newline="", encoding="utf-8")
    csv_writer = csv.writer(csv_file)
    if not csv_exists:
        csv_writer.writerow([
            "timestamp", "run_id", "model_id", "sample_id", "task_role",
            "gold_label", "predicted_label", "is_correct", "confidence",
            "ttft_ms", "duration_ms", "input_tokens", "output_tokens",
            "cost_usd", "status"
        ])

    print("\n" + "="*70)
    print("🚀 SCAMSHIELD TIER-2 COUNCIL BENCHMARK RUNNER")
    print(f"  • Models to evaluate : {len(models)} models ({', '.join(models)})")
    print(f"  • Total test samples : {len(samples)} items (Resume enabled: {resume})")
    print(f"  • Output usage log   : {USAGE_LOG_PATH}")
    print("="*70 + "\n")

    total_cost_session = 0.0

    for m_id in models:
        client = get_client(m_id, cost_calc)
        print(f"\n▶ Evaluating Model: {m_id}")
        correct_cnt = 0
        evaluated_cnt = 0

        for idx, sample in enumerate(samples, start=1):
            s_id = sample.get("sample_id", f"SAMPLE_{idx:03d}")

            # Checkpoint resume check
            if resume and is_already_evaluated(conn, s_id, m_id):
                continue

            prompt = (
                f"Phân tích tin nhắn SMS sau và xác định [SCAM] hay [HAM]:\n"
                f"Tin nhắn: \"{sample.get('raw_message')}\""
            )

            res = await client.execute(prompt)
            log_to_storage(conn, csv_writer, sample, res, prompt)
            csv_file.flush()

            evaluated_cnt += 1
            total_cost_session += res.cost_usd
            is_ok = (res.predicted_label == sample.get("gold_label"))
            if is_ok:
                correct_cnt += 1

            icon = "✅" if is_ok else ("⚠️" if res.predicted_label != "ERROR" else "❌")
            print(f"  [{idx:3d}/{len(samples):3d}] {s_id:10s} {icon} Pred: {res.predicted_label:5s} | Gold: {sample.get('gold_label'):5s} | Dur: {res.duration_ms:6.1f}ms | Cost: ${res.cost_usd:.6f}")

            # Inter-request delay to prevent 429
            await asyncio.sleep(0.4)

        acc = (correct_cnt / evaluated_cnt * 100.0) if evaluated_cnt else 0.0
        print(f"  🏁 Finished {m_id}: {evaluated_cnt} evaluated, Accuracy: {acc:.1f}%")

    csv_file.close()
    conn.close()

    print("\n" + "="*70)
    print(f"🎉 Benchmark execution completed! Session Cost: ${total_cost_session:.4f}")
    print(f"📄 Detailed CSV usage log saved to: {USAGE_LOG_PATH}")
    print("="*70 + "\n")


def parse_args():
    parser = argparse.ArgumentParser(description="ScamShield Tier 2 Council Evaluation Runner")
    parser.add_argument("--models", nargs="+", default=["gemini-3.5-flash-lite", "gemini-3.8-flash", "gpt-6.1-sol", "claude-sonnet-5"],
                        help="List of model IDs to benchmark")
    parser.add_argument("--suite", type=str, default=DEFAULT_SUITE_PATH, help="Path to master test suite JSONL")
    parser.add_argument("--limit", type=int, default=0, help="Limit sample count (0 for all)")
    parser.add_argument("--no-resume", action="store_true", help="Force re-evaluate already completed samples")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(run_benchmark(args.models, args.suite, limit=args.limit, resume=(not args.no_resume)))
