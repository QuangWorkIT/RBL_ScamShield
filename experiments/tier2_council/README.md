# 🔬 ScamShield Tier-2 Forensic Council Empirical Benchmark

> **Module:** `experiments/tier2_council/`  
> **Repository:** `RBL_ScamShield`  
> **Evaluation Suite:** 117 Verified Multi-Aspect Forensic Samples  
> **Tested Models:** `gemini-3.5-flash-lite`, `gemini-3.8-flash`, `gpt-6.1-sol`, `claude-sonnet-5`

---

## 1. Structure Overview

```
experiments/tier2_council/
├── .env                              # API keys (Protected by .gitignore)
├── init_db.py                        # Initializes SQLite benchmark.db with verified prices
├── runner.py                         # High-performance async runner (Non-stream vibi.top + Gemini direct)
├── analyze_runs.py                   # Computes F1, precision, recall, FPR, latency, cost per success
├── benchmark-seed.json               # Seed catalog and official observations
├── data/
│   ├── master_test_suite.jsonl       # Compiled 117-sample evaluation benchmark
│   └── tasks/                        # Deliverables from the 4 team specialists
│       ├── task_cyber_url.jsonl
│       ├── role_soc_eng.json
│       ├── task_vn_teencode.json
│       └── master_evaluation_benchmark_bank_defender_30.jsonl
└── reports/
    ├── REPORT_TIER2_COUNCIL_BENCHMARK.md  # Comprehensive visual report
    ├── competency_matrix.csv              # Machine-readable evaluation matrix
    ├── competency_matrix.json             # Structured JSON matrix
    └── usage_log.csv                      # Microsecond telemetry usage log
```

---

## 2. Reproduction & Execution Commands

### Step 1: Initialize Database
```bash
python experiments/tier2_council/init_db.py
```

### Step 2: Run Full Benchmark (or Smoke Test)
```bash
# Run all 117 samples across candidate models
python experiments/tier2_council/runner.py --models gemini-3.5-flash-lite gpt-6.1-sol claude-sonnet-5 --suite experiments/tier2_council/data/master_test_suite.jsonl

# Or run with sample limit (e.g., first 10 items)
python experiments/tier2_council/runner.py --models gemini-3.5-flash-lite gpt-6.1-sol --limit 10
```

### Step 3: Generate Analysis Report & Competency Matrix
```bash
python experiments/tier2_council/analyze_runs.py
```
View the final report at: `reports/REPORT_TIER2_COUNCIL_BENCHMARK.md`
