"""
==============================================================================
ScamShield-VN: 2-Tier Cascaded AI Router (PhoBERT Fast-Path + Dynamic Cloud LLM)
==============================================================================
Author: ScamShield Core Engineering Team
Description:
    Core Cascaded Orchestrator implementing the Accuracy-Latency-Cost Trilemma solution:
    - Tier 1 (Fast-Path Local CPU): PhoBERT ONNX (latency < 65ms, cost $0)
    - Threshold Routing (tau = 0.90): High confidence routes directly.
    - Tier 2 (Slow-Path Cloud Fallback): Dynamic Model Registry calls Gemini Lite/Standard
      only for ambiguous/low-confidence instances (~15-20% traffic).
==============================================================================
"""

import time
import json
import logging
from typing import Dict, List, Optional, Any
from .model_registry import ModelRegistry
from .local_classifier import LocalPhoBERTClassifier

logger = logging.getLogger("ScamShield.TwoTierRouter")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s", datefmt="%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


SYSTEM_PROMPT_TIER_2 = """Bạn là chuyên gia an ninh mạng ScamShield-VN chuyên phân tích và phát hiện tin nhắn lừa đảo tiếng Việt (SMS, Zalo, Telegram, Facebook).
Nhiệm vụ của bạn là phân tích sâu ngữ cảnh tin nhắn được gửi đến và trả về kết quả định dạng JSON thuần túy (không kèm markdown format).

Cấu trúc JSON bắt buộc:
{
    "is_scam": true/false,
    "confidence": 0.0 - 1.0,
    "scam_type": "Mạo danh ngân hàng / Giả mạo cơ quan công an / Tuyển dụng CTV / Lừa đảo trúng thưởng / Đầu tư tài chính / Không phải lừa đảo",
    "risk_level": "LOW" / "MEDIUM" / "HIGH" / "CRITICAL",
    "explanation": "Giải thích ngắn gọn 1-2 câu lý do nhận định và thủ đoạn tâm lý của đối tượng"
}
"""


class TwoTierRouter:
    """
    2-Tier Cascaded Router for Real-Time Scam Message Classification.
    """

    def __init__(
        self,
        confidence_threshold: float = 0.90,
        api_key: Optional[str] = None,
        config_path: Optional[str] = None,
        tier1_temperature: float = 1.30,
        tier1_cost_alpha: float = 5.0,
    ):
        """
        Initialize the 2-Tier Router.

        Args:
            confidence_threshold: Confidence threshold (tau) for Tier 1 -> Tier 2 escalation. Default 0.90.
            api_key: Gemini API Key for Tier 2 fallback.
            config_path: Path to YAML config for dynamic model registry.
            tier1_temperature: Temperature Scaling parameter for Tier 1.
            tier1_cost_alpha: WBCE penalty alpha for Tier 1.
        """
        self.tau = confidence_threshold
        self.tier1_classifier = LocalPhoBERTClassifier(
            temperature=tier1_temperature,
            cost_alpha=tier1_cost_alpha,
        )
        self.tier2_registry = ModelRegistry(
            api_key=api_key,
            config_path=config_path,
            auto_discover=True,
        )
        logger.info(f"TwoTierRouter Initialized. Fallback Threshold (tau) = {self.tau:.2f}")

    def classify(self, message: str, force_tier2: bool = False) -> Dict[str, Any]:
        """
        Process and classify an incoming message through the 2-Tier Architecture.

        Args:
            message: Raw Vietnamese message text.
            force_tier2: Force escalation to Tier 2 regardless of Tier 1 confidence.

        Returns:
            dict containing final classification, detailed Tier 1 & Tier 2 telemetry,
            routing rationale, latency, and cost breakdown.
        """
        start_overall = time.perf_counter()

        # -------------------------------------------------------------
        # Step 1: Execute Tier 1 Local Fast-Path (PhoBERT CPU)
        # -------------------------------------------------------------
        t1_result = self.tier1_classifier.predict(message)
        t1_confidence = t1_result["confidence"]
        t1_is_sure = (t1_confidence >= self.tau)

        tier1_summary = {
            "label": t1_result["label"],
            "class_id": t1_result["class_id"],
            "confidence": t1_confidence,
            "scam_prob": t1_result["calibrated_scam_prob"],
            "ham_prob": round(1.0 - t1_result["calibrated_scam_prob"], 4),
            "latency_ms": t1_result["latency_ms"],
            "cost_usd": 0.0,
            "is_sure": t1_is_sure,
            "status": "CONFIDENT" if t1_is_sure else "UNSURE",
            "matched_cues": t1_result.get("matched_cues", []),
            "reason": (
                f"Độ tin cậy Tầng 1 ({t1_confidence*100:.1f}%) >= Ngưỡng an toàn ({self.tau*100:.0f}%) -> Rất tự tin."
                if t1_is_sure
                else f"Độ tin cậy Tầng 1 ({t1_confidence*100:.1f}%) < Ngưỡng an toàn ({self.tau*100:.0f}%) -> Vùng phân vân / không chắc chắn."
            ),
        }

        # -------------------------------------------------------------
        # Case A: Fast-Path Direct Exit (Tier 1 is Confident >= tau)
        # -------------------------------------------------------------
        if t1_is_sure and not force_tier2:
            total_elapsed_ms = (time.perf_counter() - start_overall) * 1000
            routing_reason = (
                f"Độ tin cậy Tầng 1 đạt {t1_confidence*100:.1f}% >= {self.tau*100:.0f}% (Ngưỡng an toàn). "
                f"Phản hồi trực tiếp tại thiết bị, KHÔNG cần gọi Cloud LLM (Tiết kiệm 100% chi phí và tối ưu độ trễ)."
            )
            return {
                "message": message,
                "final_label": t1_result["label"],
                "final_confidence": t1_confidence,
                "is_scam": (t1_result["label"] == "SCAM"),
                "scam_type": "Detected by Tier 1 Heuristic/Pattern" if t1_result["label"] == "SCAM" else "Legitimate Message",
                "risk_level": "HIGH" if t1_result["label"] == "SCAM" else "LOW",
                "explanation": f"Xử lý trực tiếp bởi Tier 1 (PhoBERT Local Fast-Path) với độ tự tin {t1_confidence*100:.1f}% >= {self.tau*100:.0f}%.",
                "routing_path": "TIER_1_DIRECT_FASTPATH",
                "routing_reason": routing_reason,
                "tier_used": "Tier 1 (Local CPU PhoBERT)",
                "model_name": "PhoBERT-base-v2-INT8",
                "tier1_telemetry": tier1_summary,
                "tier2_telemetry": {
                    "status": "SKIPPED",
                    "reason": "FastPath satisfied; no cloud escalation needed.",
                },
                "total_latency_ms": round(total_elapsed_ms + t1_result["latency_ms"], 2),
                "total_cost_usd": 0.0,
                "escalated": False,
            }

        # -------------------------------------------------------------
        # Case B: Escalate to Tier 2 (Dynamic Cloud Fallback)
        # Reason: Ambiguous case (Confidence < tau) or forced audit
        # -------------------------------------------------------------
        fallback_trigger = "FORCED_AUDIT" if force_tier2 else f"LOW_CONFIDENCE ({t1_confidence*100:.1f}% < {self.tau*100:.0f}%)"
        routing_reason = (
            f"Tầng 1 phân vân ({t1_confidence*100:.1f}% < {self.tau*100:.0f}%), rơi vào vùng rủi ro bỏ sót lừa đảo (FNR). "
            f"Kích hoạt Tầng 2 (Cloud LLM) để phân tích ngữ cảnh xã hội và bẫy thao túng tâm lý sâu."
        )
        logger.info(f"Escalating message to Tier 2 Cloud LLM. Reason: {fallback_trigger}")

        t2_response = self.tier2_registry.generate_content(
            prompt=f"Hãy phân tích tin nhắn sau:\n\n{message}",
            tier="lite",
            system_instruction=SYSTEM_PROMPT_TIER_2,
            temperature=0.1,
        )

        # Parse Tier 2 output
        if t2_response.get("success"):
            try:
                raw_text = t2_response["text"].strip()
                # Clean possible markdown wrapping
                if raw_text.startswith("```json"):
                    raw_text = raw_text.replace("```json", "", 1).rstrip("` \n")
                elif raw_text.startswith("```"):
                    raw_text = raw_text.replace("```", "", 1).rstrip("` \n")

                parsed = json.loads(raw_text)
                is_scam = parsed.get("is_scam", False)
                final_label = "SCAM" if is_scam else "HAM"
                final_conf = float(parsed.get("confidence", 0.95))
                scam_type = parsed.get("scam_type", "Phân tích ngữ cảnh sâu")
                risk_level = parsed.get("risk_level", "HIGH" if is_scam else "LOW")
                explanation = parsed.get("explanation", "Phân tích ngữ cảnh sâu bởi Cloud LLM.")

                total_elapsed_ms = (time.perf_counter() - start_overall) * 1000 + t1_result["latency_ms"]

                # Estimated cost for Lite model (~$0.075 / 1M input tokens, ~$0.30 / 1M output tokens -> ~$0.00005 per request)
                estimated_cost = 0.00005

                return {
                    "message": message,
                    "final_label": final_label,
                    "final_confidence": round(final_conf, 4),
                    "is_scam": is_scam,
                    "scam_type": scam_type,
                    "risk_level": risk_level,
                    "explanation": explanation,
                    "routing_path": "TIER_2_CLOUD_FALLBACK",
                    "routing_reason": routing_reason,
                    "tier_used": f"Tier 2 (Cloud {t2_response['tier'].upper()})",
                    "model_name": t2_response["model_used"],
                    "tier1_telemetry": tier1_summary,
                    "tier2_telemetry": {
                        "status": "EXECUTED",
                        "model": t2_response["model_used"],
                        "tier": t2_response["tier"],
                        "confidence": round(final_conf, 4),
                        "scam_type": scam_type,
                        "explanation": explanation,
                        "latency_ms": round(t2_response["latency_ms"], 2),
                        "cost_usd": estimated_cost,
                        "fallback_trigger": fallback_trigger,
                    },
                    "total_latency_ms": round(total_elapsed_ms + t2_response["latency_ms"], 2),
                    "total_cost_usd": estimated_cost,
                    "escalated": True,
                }
            except Exception as e:
                logger.error(f"Failed to parse Tier 2 LLM JSON output: {e}. Falling back to Tier 1 prediction.")

        # If Tier 2 failed or API key not present, graceful fallback to Tier 1 decision
        total_elapsed_ms = (time.perf_counter() - start_overall) * 1000 + t1_result["latency_ms"]
        err_msg = t2_response.get("error", "OFFLINE")
        return {
            "message": message,
            "final_label": t1_result["label"],
            "final_confidence": t1_confidence,
            "is_scam": (t1_result["label"] == "SCAM"),
            "scam_type": "Tier 1 Fallback (Tier 2 Offline)",
            "risk_level": "MEDIUM" if t1_result["label"] == "SCAM" else "LOW",
            "explanation": f"Tier 2 không khả dụng ({err_msg}). Hệ thống sử dụng kết quả dự đoán của Tier 1 ({t1_confidence*100:.1f}%).",
            "routing_path": "TIER_1_GRACEFUL_DEGRADATION",
            "routing_reason": f"Tầng 1 phân vân ({t1_confidence*100:.1f}%), nhưng Tầng 2 Cloud tạm thời không khả dụng ({err_msg}) -> Duy trì hoạt động với kết quả Tầng 1.",
            "tier_used": "Tier 1 (Graceful Degradation Mode)",
            "model_name": "PhoBERT-base-v2-INT8",
            "tier1_telemetry": tier1_summary,
            "tier2_telemetry": {
                "status": "FAILED_OR_OFFLINE",
                "error": err_msg,
                "fallback_trigger": fallback_trigger,
            },
            "total_latency_ms": round(total_elapsed_ms, 2),
            "total_cost_usd": 0.0,
            "escalated": True,
        }

    def classify_batch(self, messages: List[str]) -> List[Dict[str, Any]]:
        """Classify a batch of messages and record metrics."""
        return [self.classify(msg) for msg in messages]
