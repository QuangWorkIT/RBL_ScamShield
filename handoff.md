# 🤝 PROJECT HANDOFF & EXPERIMENT CONTINUITY GUIDE
### Project: ScamShield-VN — Evidence-Grounded Vietnamese Scam & Phishing Detection Platform
> **File:** `handoff.md`  
> **Last Updated:** 2026-10-20 17:35:00 (UTC+7)  
> **Status:** Standardized 3-Label Framework, RQ Refactored, Ablation & P-Single Ready for Live API Runs  
> **Lead Researcher:** Nguyễn Trung Hiếu (PL / LR)  
> **Target Conference:** ICITT (Call for Papers Submission)  
> **Git Branch:** `feat/master-slr-synthesis`  

---

## 1. Executive Summary & Context of Previous Session

In the previous session, we audited the codebase against the latest feedback from the Mentor and completed 4 core technical milestones:
1. **Standardized 3-Label Output Schema:** Replaced all legacy/temporary labels (`SCAM`, `HAM`, `SUSPICIOUS_REVIEW`) across [`pipeline/forensic_council.py`](file:///C:/Users/USER/RBL_ScamShield/pipeline/forensic_council.py), [`pipeline/two_tier_router.py`](file:///C:/Users/USER/RBL_ScamShield/pipeline/two_tier_router.py), and [`config/council_registry.yaml`](file:///C:/Users/USER/RBL_ScamShield/config/council_registry.yaml) with:
   - **`SCAM-RISK`** (High/Critical risk of smishing/fraud)
   - **`LOW-RISK`** (Legitimate transactional or regular service notification)
   - **`UNKNOWN`** (Ambiguous boundary: $0.40 \le P < 0.60$ or unresolved agent contradiction)
2. **Research Questions (RQ) Scope Update & Rejection of Condorcet:**
   - **RQ3 (Human-Centric Utility Study) has been officially removed** from the ICITT paper scope to focus 100% on system performance, Pareto frontier trade-offs, and multi-agent consensus reliability.
   - **Condorcet Jury Theorem was completely expunged** from [`team-synthesis/proposal_amendment_v1.1.md`](file:///C:/Users/USER/RBL_ScamShield/team-synthesis/proposal_amendment_v1.1.md), [`RBL_FRAMEWORK.md`](file:///C:/Users/USER/RBL_ScamShield/RBL_FRAMEWORK.md), and [`paper/claims.md`](file:///C:/Users/USER/RBL_ScamShield/paper/claims.md). Replaced with mathematical foundation on **Correlated Error Mitigation** (*Kim et al., ICML 2025; Smit et al., ICML 2024; Ladha, 1992*).
3. **Occam's 3-Agent Council Selection:** Confirmed decision to **keep the Public Defender Advocate** (0% False Positive Rate on legitimate banking OTPs) while consolidating technical and linguistic roles.
4. **Backend PII Masking Note:** Confirmed that data redaction per Article 25 Decree 13/2023/NĐ-CP is handled at the backend server level.
5. **Created New Benchmark Runners:**
   - [`experiments/tier2_council/runner_p_single.py`](file:///C:/Users/USER/RBL_ScamShield/experiments/tier2_council/runner_p_single.py): Baseline Single LLM with Structured Forensic Prompt (*Wang et al., ACL 2024*).
   - [`experiments/tier2_council/runner_ablation_3v5.py`](file:///C:/Users/USER/RBL_ScamShield/experiments/tier2_council/runner_ablation_3v5.py): Dynamic Ablation Runner (5-Agent vs. 3-Agent with Defender vs. 3-Agent Naive) with automated paired McNemar tests.

---

## 2. Primary Objective for the Incoming Conversation

👉 **RUN THE EMPIRICAL BENCHMARKS USING LIVE MODEL APIS**  
The scripts are fully functional with offline fallback heuristics, but the next conversation needs to run them with **live external LLM API calls** (Google Gemini, OpenAI / Anthropic via `vibi.top` proxy) to generate the official empirical tables and statistical significance figures for the ICITT paper manuscript.

---

## 3. Environment & API Configuration

The project root has a `.env` file containing the necessary API credentials:

```bash
# Location: C:\Users\USER\RBL_ScamShield\.env
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
VIBI_BASE_URL=https://vibi.top/v1
```

*Both `pipeline/forensic_council.py`, `runner_p_single.py`, and `runner_ablation_3v5.py` automatically load `.env` via `python-dotenv`.*

### Pre-Flight API Health Check (Run First in New Session)
Run this single-line verification to confirm API access before executing large batches:

```powershell
python -c "
import os, httpx
from dotenv import load_dotenv
load_dotenv('.env')
key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('VIBI_BASE_URL', 'https://vibi.top/v1')
headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
body = {'model': 'gpt-6.1-sol', 'messages': [{'role': 'user', 'content': 'Test ping'}], 'max_tokens': 5}
r = httpx.post(f'{base_url}/chat/completions', headers=headers, json=body, timeout=10.0)
print('Vibi/OpenAI API Status:', r.status_code, '| Response:', r.json().get('choices', [{}])[0].get('message', {}).get('content'))
"
```

---

## 4. Step-by-Step Live Experiment Execution Protocol

Execute the following 4 stages sequentially:

### Stage 1: P-single Baseline on Live API
Evaluates a single state-of-the-art model (`gpt-6.1-sol` or `gemini-1.5-pro`) using the multi-axial Structured Forensic Prompt (*Wang et al., ACL 2024*).

```powershell
# 1. Smoke test (5 samples)
python experiments/tier2_council/runner_p_single.py --limit 5 --model gpt-6.1-sol

# 2. Full Forensic Challenge Suite (117 samples)
python experiments/tier2_council/runner_p_single.py --model gpt-6.1-sol

# Outputs saved to:
# - experiments/tier2_council/reports/REPORT_P_SINGLE_BASELINE.md
# - experiments/tier2_council/reports/p_single_results.json
```

---

### Stage 2: 3-Agent vs. 5-Agent Council Ablation on Live API
Evaluates the 3 experimental arms:
- **Arm 1:** Full 5-Agent Council
- **Arm 2:** 3-Agent Council with Public Defender (Proposed Occam configuration)
- **Arm 3:** 3-Agent Council Naive (without Defender, to isolate Defender's impact)

```powershell
# 1. Smoke test (5 samples)
python experiments/tier2_council/runner_ablation_3v5.py --limit 5

# 2. Full Forensic Challenge Suite (117 samples)
python experiments/tier2_council/runner_ablation_3v5.py

# Outputs saved to:
# - experiments/tier2_council/reports/REPORT_ABLATION_3V5.md
# - experiments/tier2_council/reports/ablation_3v5_matrix.json
```

*Note on Rate Limits:* The runner handles async calls concurrently. If you encounter rate limits (HTTP 429), the built-in `CircuitBreaker` will automatically wait and cooldown (cooldown 300s, or standby chain fallback).

---

### Stage 3: Multi-Agent Consensus Benchmark (EXP-02)
Runs the 4 arms across the 117 master test suite and logs to SQLite `experiments/tier2_council/consensus_benchmark.db`:

```powershell
python experiments/tier2_council/runner_consensus.py
python experiments/tier2_council/analyze_consensus.py
```

---

### Stage 4: Two-Tier Cascaded System E2E Benchmark (EXP-03)
Runs the full End-to-End benchmark across all **384 samples** (267 Frozen Test Set + 117 Forensic Challenges) across 3 independent iterations with median aggregation and $\tau$ sweep:

```powershell
python experiments/e2e_two_tier/runner_e2e_benchmark.py
```

*Results are logged to `experiments/e2e_two_tier/e2e_benchmark.db` and summarized in `experiments/e2e_two_tier/reports/e2e_summary.csv`.*

---

## 5. Artifact & Codebase Map

```
RBL_ScamShield/
├── pipeline/
│   ├── local_classifier.py        # Tier 1 ViSoBERT inference (<15.8ms CPU, cost $0)
│   ├── forensic_council.py        # Tier 2 Council (3-label schema: SCAM-RISK, LOW-RISK, UNKNOWN)
│   ├── two_tier_router.py         # Cascaded Router connecting Tier 1 & 2 (Standardized labels)
│   └── model_registry.py          # Dynamic LLM API registry
├── config/
│   └── council_registry.yaml      # Consensus rules, role configs, thresholds [0.40, 0.60]
├── visobert_5runs_release/        # [GIT LFS] Model weights & ONNX checkpoints
├── experiments/
│   ├── tier2_council/
│   │   ├── runner_p_single.py     # [NEW] Baseline P-single with Structured Forensic Prompt
│   │   ├── runner_ablation_3v5.py # [NEW] Ablation Study (3-Agent with Defender vs 5-Agent)
│   │   ├── runner_consensus.py    # Consensus evaluation runner
│   │   ├── benchmark.db           # Solo model run cache
│   │   ├── consensus_benchmark.db # Council consensus run records
│   │   └── reports/
│   │       ├── REPORT_P_SINGLE_BASELINE.md
│   │       ├── REPORT_ABLATION_3V5.md
│   │       └── ablation_3v5_matrix.json
│   └── e2e_two_tier/
│       ├── runner_e2e_benchmark.py# 3-run median runner with tau ablation (N=384)
│       ├── e2e_benchmark.db       # SQLite records
│       └── reports/
│           ├── e2e_summary.csv    # Summary matrix
│           └── e2e_ablation.csv   # Ablation sweep matrix
├── paper/
│   ├── claims.md                  # Academic claims mapped to evidence (Claims 1-5)
│   ├── FULL_PAPER_PREVIEW.md      # IEEE paper draft preview
│   └── sections/
│       ├── 01_intro.tex           # Introduction
│       ├── 03_method.tex          # Methodology
│       ├── 04_results.tex         # Results & statistical tables
│       └── 05_discussion.tex      # Discussion & Correlated Errors
└── RBL_FRAMEWORK.md               # Research framework (RQ1 & RQ2 defined, RQ3 removed)
```

---

## 6. Action Items Checklist for Incoming Conversation

- [ ] **Step 1:** Verify API connectivity with `Vibi/OpenAI` and `Gemini` via pre-flight health check.
- [ ] **Step 2:** Run `runner_p_single.py` with live API and confirm metric logging.
- [ ] **Step 3:** Run `runner_ablation_3v5.py` with live API; confirm McNemar test result ($p$-value) and FPR suppression on Arm 2.
- [ ] **Step 4:** Integrate the final live API metrics into `paper/sections/04_results.tex` (Table of 3-Agent vs. 5-Agent vs. P-single vs. ViSoBERT T1).
- [ ] **Step 5:** Finalize `paper/sections/05_discussion.tex` addressing:
  - Error de-correlation (*Kim et al., ICML 2025*).
  - Anti-Alarm Fatigue via Public Defender (-0.25 veto).
  - Vietnamese data protection compliance (Article 25, Decree 13/2023/NĐ-CP).
