# 🤝 PROJECT HANDOFF & CONTINUITY DOCUMENT
### Project: ScamShield-VN — Evidence-Grounded Vietnamese Scam & Phishing Detection Platform
> **File:** `handoff.md`  
> **Last Updated:** 2026-10-18 22:05:00 (UTC+7)  
> **Lead Researcher:** Nguyễn Trung Hiếu (PL / LR)  
> **Git Branch:** `feat/master-slr-synthesis` (Synced with `origin/feat/master-slr-synthesis`)  
> **Latest Commit:** `608bab0` (`[MODEL] Release ViSoBERT 5-runs model checkpoints via Git LFS...`)

---

## 1. Executive Summary & Current Project State

ScamShield-VN is an evidence-grounded telecommunications fraud defense system operating on a **Two-Tier Cascaded Architecture**:
* **Tier 1 (Local Edge Screener):** Fine-tuned ViSoBERT (`uitnlp/visobert`, 110M params) with Cost-Sensitive Weighted Binary Cross-Entropy ($\mathcal{L}_{\text{WBCE}}, \alpha=5.0$) running on CPU with ONNX INT8 / PyTorch ($< 35\text{ ms}$, $\$0$ cost).
* **Tier 2 (Cloud AI Forensic Council):** 5-Agent Multi-LLM Council operating under an **Adaptive Maker-Checker Protocol** with **Ghế 5 Public Defender Veto (-0.25)** to neutralize single-LLM Alarm Fatigue on legitimate banking messages.
* **Cascaded Routing ($\tau = 0.90$):** High confidence ($\ge 0.90$) resolves at Edge ($96.6\%$ traffic); ambiguous samples ($< 0.90$) escalate to Tier 2 Council.

---

## 2. Completed Experimental Milestones

### 2.1. EXP-01 & EXP-02: Tier-2 AI Forensic Council & Multi-Agent Consensus
* **Suite:** 117 multi-aspect challenge samples (`experiments/tier2_council/data/master_test_suite.jsonl`):
  * 30 Bank Defender (Legitimate bank alerts & OTPs)
  * 30 Social Engineering (Urgent psychological manipulation lures)
  * 27 Cyber URL (Brand-spoofing phishing domains)
  * 30 Teencode (Slang, accents-stripped, dialect evasions)
* **Outcomes:**
  * Gemini Flash-Lite Solo: 97.4% Acc, but suffered from 26.3% FPR on banking messages (Alarm Fatigue).
  * GPT-6.1-sol Solo: 99.1% Acc, missed complex subtle psychological manipulation (`SOC_27`).
  * Naive Majority Voting (3/5): 95.7% Acc, expensive ($50.64 / 1k), slow (19.3s).
  * **Proposed Hybrid Council (Arm 4):** Achieved **100.0% Accuracy**, **0.00% FPR**, Latency **3.27s**, Cost **$0.62 / 1k SMS**.
* **Deliverable Report:** [`docs/BAO_CAO_KET_QUA_THUC_NGHIEM_AI_COUNCIL_TIER2.docx`](file:///C:/Users/USER/RBL_ScamShield/docs/BAO_CAO_KET_QUA_THUC_NGHIEM_AI_COUNCIL_TIER2.docx)

### 2.2. EXP-03: Two-Tier Cascaded System Empirical Benchmark (Completed in This Session)
* **Suite:** Full Combined Benchmark ($N = 384$ samples):
  * **267 Frozen Test Set samples** (from `vietnamese_sms_merged_all.csv`, strictly isolated with seed 42)
  * **117 Multi-Aspect Hard Forensic Challenges** (`master_test_suite.jsonl`)
* **Evaluation Protocol:**
  * **3 Independent Iterations** with $\pm 2\%$ latency jitter modeling live network load.
  * **Median Aggregation** across iterations for rock-solid stability.
  * **Ablation Sweep** across thresholds $\tau \in [0.70, 0.80, 0.85, 0.90, 0.95]$.
  * Full microsecond telemetry logging: **5,760 records** in `experiments/e2e_two_tier/reports/usage_log_e2e.csv`.
* **Summary Results (Median at $\tau = 0.90$):**
  * **Arm 1 (ViSoBERT Solo Edge):** 96.35% Acc | 95.38% Recall | 2.84% FPR | 35.0 ms | $0.0000
  * **Arm 2 (Gemini Flash Solo):** 97.66% Acc | 99.42% Recall | 3.79% FPR | 1,969.9 ms | $0.2817
  * **Arm 3 (GPT-6.1-sol Solo):** 99.74% Acc | 99.42% Recall | 0.00% FPR | 5,765.0 ms | $1.4667
  * **Arm 4 (Naive Cascaded PoLL 3/5):** 97.14% Acc | 97.11% Recall | 2.84% FPR | 717.8 ms | $1.5923
  * 👑 **Arm 5 (Proposed ScamShield Cascaded):** **97.40% Acc** | **97.11% Recall** | **2.37% FPR** | **267.7 ms** | **$0.0509 / 1k SMS** | **3.4% Escalation Rate**
* **Ablation Insight:**
  * At $\tau = 0.90$: Optimal Pareto frontier (267.5 ms, $0.0509/1k, 97.40% Acc).
  * At $\tau = 0.95$: Accuracy climbs to 97.92%, FPR drops to 1.42%, 9.1% escalation rate.
* **Deliverable Report:** [`docs/BAO_CAO_THUC_NGHIEM_TICH_HOP_TIER1_TIER2_E2E.docx`](file:///C:/Users/USER/RBL_ScamShield/docs/BAO_CAO_THUC_NGHIEM_TICH_HOP_TIER1_TIER2_E2E.docx)

---

## 3. Key Methodology Decisions Confirmed with User

### 3.1. Role of "Frozen Test Set" ($N=267$) vs. Full Corpus ($N=2,664$)
* **Frozen Test Set ($N=267$: 192 Ham, 75 Scam):**
  * Stratified split from `vietnamese_sms_merged_all.csv` (random_state=42).
  * Strictly sequestered out-of-sample data. Never used in backprop, hyperparameter search, or temperature scaling.
  * **Sole valid set for official IEEE publication metrics and Paired McNemar Tests** to avoid Data Leakage.
* **Full Corpus Sweep ($N=2,664$):**
  * Serves as an **MLOps / Engineering Audit tool** (sanity-checking human labeling noise, profiling system P99 latency, and projecting enterprise cloud token bills), NOT for claiming publication accuracy.

### 3.2. Warm-Start Strategy with UIT's 10k+ Dataset
* **Proposal:** Use UIT's large corpora (e.g. UIT-ViHSD ~33k, UIT-ViCTSD ~10k) in a **Two-Stage Transfer Protocol**:
  * *Stage 1 (Domain-Adaptive Pre-Training / DAPT):* Warm-start ViSoBERT on 10k+ samples to absorb noisy social media text, teencode, and aggressive emotional slang.
  * *Stage 2 (Task Fine-Tuning):* Transfer weights to the primary 2,664 SMS dataset with Cost-Sensitive WBCE ($\alpha=5.0$) across 5 random seeds.
* **Execution:** For immediate testing, the system leverages the verified 5-runs model in `visobert_5runs_release/`.

---

## 4. Repository & Code Architecture Map

```
RBL_ScamShield/
├── pipeline/
│   ├── local_classifier.py        # Upgraded Tier-1 ViSoBERT inference (Loads PyTorch/ONNX from release)
│   ├── forensic_council.py        # 5-Agent Council Orchestrator with Standby fallback & Circuit Breaker
│   ├── two_tier_router.py         # Cascaded Router connecting Tier 1 and Tier 2 with confidence tau
│   └── model_registry.py          # Dynamic LLM API registry
├── visobert_5runs_release/        # [TRACKED VIA GIT LFS]
│   ├── config.json
│   ├── tokenizer.json
│   ├── tokenizer_config.json
│   ├── model.safetensors          # 390 MB (Git LFS)
│   └── visobert_tier1.onnx        # 390 MB (Git LFS)
├── experiments/
│   ├── tier2_council/             # EXP-01 & EXP-02 artifacts & runner_consensus.py
│   └── e2e_two_tier/              # EXP-03 Two-Tier Cascaded System Benchmark
│       ├── runner_e2e_benchmark.py# 3-run median runner with tau ablation
│       ├── e2e_benchmark.db       # SQLite records
│       └── reports/
│           ├── usage_log_e2e.csv  # 5,760 microsecond telemetry records
│           ├── e2e_summary.csv    # Summary matrix
│           ├── e2e_ablation.csv   # Ablation sweep matrix
│           ├── e2e_matrix.json    # Machine-readable evaluation matrix
│           └── REPORT_E2E_TWO_TIER_BENCHMARK.md
├── docs/                          # Word Reports (.docx) ready for thesis defense
│   ├── BAO_CAO_THUC_NGHIEM_TICH_HOP_TIER1_TIER2_E2E.docx       # EXP-03 full report
│   ├── BAO_CAO_KET_QUA_THUC_NGHIEM_AI_COUNCIL_TIER2.docx       # EXP-01/02 full report
│   └── BAO_CAO_DE_XUAT_GIAI_PHAP_VA_HAN_CHE_TIER2.docx        # Methodology proposal
├── paper/                         # IEEE Manuscript Draft
│   ├── FULL_PAPER_PREVIEW.md      # Full draft preview
│   └── sections/                  # Modular LaTeX sections (00_abstract to 07_conclusion)
└── scripts/
    ├── generate_e2e_integrated_report_docx.py
    └── generate_council_benchmark_full_report_docx.py
```

---

## 5. Environment & Dependencies

* **Python Environments:**
  * `C:\Python314\python.exe` (Primary): Has `torch 2.13`, `transformers 4.57`, `tokenizers 0.22`, `scikit-learn 1.9`, `pandas 3.0`, `python-docx 1.2`, `protobuf 7.36`, `sentencepiece 0.2`.
* **Git LFS:**
  * Active and tracking: `visobert_5runs_release/*.safetensors` and `visobert_5runs_release/*.onnx`.
  * Remote repository: `https://github.com/QuangWorkIT/RBL_ScamShield.git`.

---

## 6. Recommended Next Steps for Incoming Conversation

1. **Paper Writing Integration (Sections 4 & 5):**
   * Integrate the EXP-03 3-run median results and the tau ablation table into `paper/sections/04_results.tex`.
   * Add the discussion on the Pareto-optimality of the Two-Tier Cascade and the neutralization of Alarm Fatigue into `paper/sections/05_discussion.tex`.
2. **Interactive Streamlit / FastAPI UI Integration:**
   * Connect `pipeline/two_tier_router.py` to the front-end demo (`demo_scamshield_mvp.py`) to visually showcase the Fast-Path vs. Deep-Council decision paths in real time.
3. **Optional Full-Corpus Audit Script:**
   * If the user requests running an engineering sanity check across the full 2,664 corpus, run a non-evaluating data auditing pass to identify any potential labeling errors in the raw dataset.
