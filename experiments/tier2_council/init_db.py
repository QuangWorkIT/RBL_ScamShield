# -*- coding: utf-8 -*-
"""
==============================================================================
ScamShield Tier-2 Council: Database Initialization Script
==============================================================================
Location: experiments/tier2_council/init_db.py
Description:
    Initializes SQLite database `benchmark.db` within the experiment directory.
    Loads model catalog, official observations, and exact pricing matrices.
==============================================================================
"""

import os
import sys
import json
import sqlite3
import logging
from typing import Dict, Any

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s]: %(message)s")
logger = logging.getLogger("Tier2InitDB")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "benchmark.db")
SEED_PATH = os.path.join(BASE_DIR, "benchmark-seed.json")


def create_schema(conn: sqlite3.Connection):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS models (
        model_id TEXT PRIMARY KEY,
        provider TEXT NOT NULL,
        context_limit_tokens INTEGER,
        context_semantics TEXT,
        max_output_tokens INTEGER,
        thinking TEXT,
        free_api_tier BOOLEAN,
        free_rpm INTEGER,
        free_tpm INTEGER,
        free_rpd INTEGER,
        access_status TEXT,
        spec_source_url TEXT,
        checked_at TEXT,
        ttft_p50_ms REAL,
        ttft_p95_ms REAL,
        output_tokens_per_second REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        price_id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_id TEXT NOT NULL,
        service_tier TEXT NOT NULL DEFAULT 'standard',
        currency TEXT NOT NULL DEFAULT 'USD',
        unit TEXT NOT NULL DEFAULT 'per_1M_tokens',
        input_uncached REAL NOT NULL,
        output_billable REAL NOT NULL,
        context_band TEXT,
        observed_on TEXT,
        effective_from TEXT,
        effective_to TEXT,
        source_url TEXT,
        FOREIGN KEY (model_id) REFERENCES models (model_id)
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_prices_model ON prices (model_id);")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS benchmark_observations (
        obs_id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_id TEXT NOT NULL,
        benchmark TEXT NOT NULL,
        score REAL,
        unit TEXT,
        source_url TEXT,
        checked_at TEXT,
        evidence_class TEXT,
        effort TEXT,
        tools TEXT,
        harness TEXT,
        attempts TEXT,
        notes TEXT,
        FOREIGN KEY (model_id) REFERENCES models (model_id)
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_obs_model_bench ON benchmark_observations (model_id, benchmark);")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pilot_runs (
        run_id TEXT PRIMARY KEY,
        task_id TEXT NOT NULL,
        sample_id TEXT,
        task_role TEXT,
        model_id TEXT NOT NULL,
        attempt INTEGER DEFAULT 1,
        ttft_ms REAL,
        total_duration_ms REAL,
        input_tokens INTEGER,
        output_tokens INTEGER,
        reasoning_tokens INTEGER DEFAULT 0,
        cost_usd REAL,
        raw_prompt TEXT,
        raw_output TEXT,
        predicted_label TEXT,
        gold_label TEXT,
        is_correct BOOLEAN,
        confidence REAL,
        error_code TEXT,
        prompt_hash TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (model_id) REFERENCES models (model_id)
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_runs_model_task ON pilot_runs (model_id, task_role);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_runs_sample ON pilot_runs (sample_id);")

    conn.commit()


def populate_data(conn: sqlite3.Connection):
    cursor = conn.cursor()

    if os.path.exists(SEED_PATH):
        with open(SEED_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        for m in data.get("models", []):
            cursor.execute("""
            INSERT OR REPLACE INTO models (
                model_id, provider, context_limit_tokens, context_semantics,
                max_output_tokens, thinking, free_api_tier, free_rpm,
                free_tpm, free_rpd, access_status, spec_source_url,
                checked_at, ttft_p50_ms, ttft_p95_ms, output_tokens_per_second
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                m.get("model_id"), m.get("provider"), m.get("context_limit_tokens"),
                m.get("context_semantics"), m.get("max_output_tokens"), m.get("thinking"),
                1 if m.get("free_api_tier") else 0, m.get("free_rpm"), m.get("free_tpm"),
                m.get("free_rpd"), m.get("access_status"), m.get("spec_source_url"),
                m.get("checked_at"), m.get("ttft_p50_ms"), m.get("ttft_p95_ms"),
                m.get("output_tokens_per_second")
            ))

        for obs in data.get("benchmark_observations", []):
            cursor.execute("""
            INSERT INTO benchmark_observations (
                model_id, benchmark, score, unit, source_url, checked_at,
                evidence_class, effort, tools, harness, attempts, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                obs.get("model_id"), obs.get("benchmark"), obs.get("score"),
                obs.get("unit"), obs.get("source_url"), obs.get("checked_at"),
                obs.get("evidence_class"), obs.get("effort"), obs.get("tools"),
                obs.get("harness"), obs.get("attempts"), obs.get("notes")
            ))

    # Add custom active models
    active_models = [
        ("claude-sonnet-5", "Anthropic", 1000000, "combined", 128000, "adaptive", 0, None, None, None, "vibi.top active", "https://vibi.top", "2026-10-18"),
        ("claude-opus-5", "Anthropic", 1000000, "combined", 128000, "adaptive", 0, None, None, None, "vibi.top active", "https://vibi.top", "2026-10-18"),
    ]
    for am in active_models:
        cursor.execute("INSERT OR REPLACE INTO models (model_id, provider, context_limit_tokens, context_semantics, max_output_tokens, thinking, free_api_tier, free_rpm, free_tpm, free_rpd, access_status, spec_source_url, checked_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", am)

    # Ingest verified prices (matching vibi.top dashboard and Google official)
    cursor.execute("DELETE FROM prices;")
    verified_rates = [
        ("gpt-6.1-sol", 1.50, 6.30, "standard", "vibi.top dashboard"),
        ("gpt-6-sol", 1.50, 6.30, "standard", "vibi.top dashboard"),
        ("claude-sonnet-5", 2.75, 13.75, "standard", "vibi.top dashboard"),
        ("claude-opus-5", 6.60, 33.00, "standard", "vibi.top dashboard"),
        ("claude-opus-5-5", 10.00, 50.00, "standard", "vibi.top dashboard"),
        ("claude-fable-5-1", 11.00, 55.00, "standard", "vibi.top dashboard"),
        ("gemini-3.5-flash-lite", 0.30, 2.50, "standard", "Google AI Studio"),
        ("gemini-3.8-flash", 0.75, 3.75, "standard", "Google AI Studio"),
        ("gemini-4-argon", 2.00, 10.00, "standard", "Google AI Studio"),
    ]
    for m_id, inp, out, band, src in verified_rates:
        cursor.execute("""
        INSERT INTO prices (model_id, input_uncached, output_billable, context_band, source_url)
        VALUES (?, ?, ?, ?, ?)
        """, (m_id, inp, out, band, src))

    conn.commit()


def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        create_schema(conn)
        populate_data(conn)
        logger.info(f"Database benchmark.db successfully initialized at: {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
