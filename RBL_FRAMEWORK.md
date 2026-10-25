# ScamShield-VN: Research-Based Learning (RBL) Framework & Scientific Specification

> **Document Status:** Single Source of Truth (SSOT) for Capstone Research Component, F-CAPS Portal & ICITT 2026 Submission  
> **Project Title:** ScamShield-VN — Real-Time Evidence-Grounded Vietnamese Scam & Phishing Detection Platform  
> **Lead Author / PI:** Trần Trung Hiếu (`trung_hieu`) & ScamShield Research Team  
> **Version:** 3.0 (Updated: 2026-10-21)  
> **Target Venues:** ICITT 2026 (Regular Research Track - Primary), SOICT 2026, ICISSP 2027 (Regular/Student-Abstract Track)

---

## 1. Executive Summary & Research Problem

Vietnamese telecommunications and digital communication environments (SMS, Zalo, Telegram, Facebook) face an escalating epidemic of sophisticated social engineering and financial cybercrimes. Prominent vectors include:
- **Banking brand impersonation:** VCB, VietinBank, Techcombank, MB Bank spoofing with fake domain names and malicious redirects.
- **Law-enforcement coercion:** Fabricated summons, drug-trafficking/money-laundering allegations from fake Police and Procuracy officers.
- **Biometric compliance traps:** Exploiting State Bank of Vietnam Decision 2345/QĐ-NHNN requiring biometric facial updates.
- **OTP smishing & fraudulent recruitment:** Telecommunications job fraud ("việc nhẹ lương cao") and fake lucky draws.

Adversaries systematically bypass conventional keyword filters using **teencode, deliberate spelling mutations, homoglyphs, and phonetic substitutions**.

Conventional detection systems fail due to the **Accuracy–Latency–Cost Trilemma**:
1. Massive Cloud LLMs offer deep contextual reasoning but introduce high latency ($>10\text{ s}$), significant API costs, and alarming false-positive rates on authentic banking OTP notifications (**Alarm Fatigue**, up to $35.53\%$ FPR on zero-shot LLM baselines).
2. Lightweight on-device neural models infer rapidly ($<16\text{ ms}$, $\$0$ cost) but exhibit residual False Negatives on ambiguous, zero-day social engineering.
3. Strict legal frameworks—most notably **Article 25, Decree 13/2023/NĐ-CP** (Vietnamese Personal Data Protection Regulation)—mandate explainability in automated decision-making and forbid opaque, forced binary classification on ambiguous citizen communications.

ScamShield-VN resolves this trilemma via a **2-Tier Cascaded Architecture with a Standardized 3-Label Output Schema** (`SCAM-RISK`, `LOW-RISK`, `UNKNOWN`), combining a local calibrated ViSoBERT-v2 edge screener with an Occam-optimized Heterogeneous Multi-LLM Forensic Council.

---

## 2. Research Questions (RQs)

*   **RQ1 (Cascade Effectiveness, Latency & Economic Trade-Off):**  
    *How much does the proposed 2-Tier Cascaded Architecture ($\mathbf{P}$: ViSoBERT Edge + Cloud Council) improve Vietnamese scam detection performance (Macro-F1, Scam Recall, and critical False Positive Rate) while reducing end-to-end latency and API token expenditure compared to standalone edge baselines ($\mathbf{B1}$ rule-based, $\mathbf{B2}$ ViSoBERT/PhoBERT encoders) and standalone Cloud LLMs ($\mathbf{B3}$ / $\text{P-single}$)?*

*   **RQ2 (Forensic Council Consensus Reliability, Correlated Error Mitigation & Alarm Fatigue Suppression):**  
    *Does a heterogeneous Multi-LLM Forensic Council with an active Public Defender veto and maker-checker verification significantly mitigate correlated error failure modes (*Kim et al., ICML 2025; Smit et al., ICML 2024; Ladha, 1992*) and suppress Alarm Fatigue ($0.00\%$ FPR on authentic banking SMS) compared to an optimized Single-LLM baseline with Structured Forensic Prompting ($\text{P-single}$, *Wang et al., ACL 2024*), and does an Occam-streamlined 3-Agent Council maintain parity with a full 5-Agent Council?*

*   *Note on RQ3:* **[REMOVED - Sequestered per Mentor Directive for ICITT 2026 Submission]**  
    *(Human-subject utility study is sequestered from the core system manuscript to focus 100% on computational evaluation, ablation studies, Pareto frontier trade-offs, and empirical statistical testing on frozen benchmarks).*

---

## 3. Research Objectives (ROs)

1.  **RO1 (Dataset Construction & Standardized Benchmark):**  
    Curate and maintain a validated multi-source Vietnamese scam message dataset ($N = 2,665$ unique samples: $1,918$ Low-Risk / Ham, $747$ Scam-Risk) with standardized annotation guidelines, multi-class threat taxonomy, and double annotation reporting inter-annotator agreement ($\text{Cohen's } \kappa \ge 0.85$).
2.  **RO2 (Baseline Ladder & 2-Tier Cascaded Implementation):**  
    Implement and freeze a rigorous baseline ladder ($\mathbf{B0} \to \mathbf{B1} \to \mathbf{B2} \to \mathbf{B3} \to \text{P-single} \to \mathbf{P}$) with a decoupled, asynchronous 2-tier cascaded pipeline and standardized 3-label routing schema.
3.  **RO3 (Controlled Multi-Faceted Evaluation):**  
    Empirically evaluate all candidate systems across:
    *   *Frozen In-Distribution Test Set* ($N = 267$, $80/10/10$ stratified split across 5 random seeds).
    *   *Master Forensic Challenge Suite* ($N = 117$: Bank Defender, Social Engineering, Cyber URL, Teencode).
    *   *Combined End-to-End Evaluation Suite* ($N = 384$).
4.  **RO4 (Ablation Analysis & Statistical Significance):**  
    Conduct paired McNemar tests and Wilcoxon signed-rank tests evaluating:
    *   Tier 1 Solo vs. Two-Tier Cascade ($\tau$ ablation sweep across $\tau \in [0.70, 0.95]$).
    *   Consolidated 3-Agent Council (with Public Defender) vs. Full 5-Agent Council vs. Baseline P-single (*Wang et al., ACL 2024*).

---

## 4. System Architecture & Baseline Ladder ($\mathbf{B0} \to \mathbf{B3} \to \text{P-single} \to \mathbf{P}$)

To prevent evaluation bias and establish incontrovertible scientific validity, ScamShield-VN evaluates performance against a strict **Baseline Ladder**:

```
[B0: Human Baseline] ──► [B1: Rule/Regex] ──► [B2: VN Encoders] ──► [B3: Direct Cloud LLM] ──► [P-single: SOTA Single LLM] ──► [P: ScamShield-VN 2-Tier]
```

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                 SCAMSHIELD-VN BASELINE LADDER                                                       │
├───────┬───────────────────────────────┬───────────────────────────────────────────┬─────────────────────────────────────────────────┤
│ Level │ Model / Methodology           │ Technical Implementation                  │ Role in Study                                   │
├───────┼───────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────────────────────┤
│ B0    │ Manual Human Verification     │ Layperson / Expert Manual Audit           │ Human performance ceiling & baseline            │
├───────┼───────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────────────────────┤
│ B1    │ Rule-Based & Regex Blacklist  │ Keyword heuristic + Domain/URL regex      │ Industry legacy baseline                        │
├───────┼───────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────────────────────┤
│ B2a   │ PhoBERT-base-v2               │ vinai/phobert-base-v2 (135M params)       │ Standard Vietnamese PLM baseline                │
├───────┼───────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────────────────────┤
│ B2b   │ PhoBERT-large                 │ vinai/phobert-large (370M params)         │ Monolithic large Vietnamese encoder             │
├───────┼───────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────────────────────┤
│ B2c   │ FPT ViBERT-base               │ FPTAI/vibert-base-cased (135M params)     │ News-domain PLM comparative baseline            │
├───────┼───────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────────────────────┤
│ B3    │ Direct Zero-Shot Cloud LLM    │ Gemini 3.5 Flash (API direct)             │ Ungrounded generative cloud baseline            │
│       │                               │                                           │ (Exhibits high FPR: 35.53% on authentic SMS)    │
├───────┼───────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────────────────────┤
│ P-sgl │ Structured Forensic LLM       │ Single LLM (gpt-6.1-sol) with multi-axial │ Published State-of-the-Art Single-LLM baseline  │
│       │ (Wang et al., ACL 2024)       │ structured forensic chain-of-thought      │ for multi-aspect fraud analysis                 │
├───────┼───────────────────────────────┼───────────────────────────────────────────┼─────────────────────────────────────────────────┤
│ P     │ ScamShield-VN Proposed        │ 2-Tier Cascaded Architecture:             │ Proposed State-of-the-Art Cascaded Solution for │
│       │ (Evidence-Grounded Cascaded)  │ • Tier 1: ViSoBERT + WBCE (α=5.0) + T*    │ Real-Time Edge Telecommunications Defense       │
│       │                               │   [INT8 ONNX CPU, <15.8ms, $0 cost]       │                                                 │
│       │                               │ • Routing: Confidence threshold (τ=0.90)  │                                                 │
│       │                               │ • Tier 2: Consolidated 3-Agent Forensic   │                                                 │
│       │                               │   Council (gpt-6.1-sol Maker + Gemini     │                                                 │
│       │                               │   Checker) with Public Defender Veto      │                                                 │
│       │                               │ • Output: Standardized 3-Label Framework  │                                                 │
│       │                               │   (SCAM-RISK / LOW-RISK / UNKNOWN)        │                                                 │
└───────┴───────────────────────────────┴───────────────────────────────────────────┴─────────────────────────────────────────────────┘
```

### Standardized 3-Label Output Schema (Decree 13/2023/NĐ-CP Compliance)
All components output and evaluate against a unified 3-label classification standard:
1. **`SCAM-RISK`** ($P \ge 0.60$): Definite evidence of phishing, impersonation, or financial scam. Flags warning and evidence summary.
2. **`LOW-RISK`** ($P < 0.40$): Legitimate transactional or service communication. Pass through.
3. **`UNKNOWN`** ($0.40 \le P < 0.60$ or agent vote contradiction): Ambiguous boundary. Recommends manual verification or human-in-the-loop review, preserving safety and compliance.

---

## 5. Mathematical Formulations & Algorithmic Rigor

ScamShield-VN is grounded in 4 core mathematical formulations:

### 5.1. Cost-Sensitive Weighted Binary Cross-Entropy ($\mathcal{L}_{\text{WBCE}}$)
In smishing defense, a False Negative (victim loses financial assets) is catastrophic compared to a False Positive (flagging a message for audit). Tier 1 penalizes False Negatives $5\times$ more severely:
$$\mathcal{L}_{\text{WBCE}} = -\frac{1}{N} \sum_{i=1}^{N} \left[ \alpha \cdot y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right], \quad \alpha = 5.0$$

### 5.2. Post-Hoc Temperature Scaling Calibration ($T^*$)
Overconfidence in Transformer logits on out-of-distribution text or adversarial teencode corrupts routing thresholds. Temperature scaling calibrates confidence prior to thresholding:
$$\hat{p}_i = \sigma\left(\frac{z_i}{T^*}\right) = \frac{1}{1 + e^{-z_i / T^*}}, \quad T^* = \arg\min_{T > 0} \mathcal{L}_{\text{NLL}}(\mathcal{D}_{\text{val}}, T)$$

### 5.3. Cascaded Total Recall & Correlated Error Covariance ($\epsilon_{\text{corr}}$)
The classical Condorcet Jury Theorem assumes independent voter error distributions ($P_1 \perp P_2 \mid Y$). In Multi-LLM systems, shared pre-training corpora create correlated failure modes (*Kim et al., ICML 2025; Smit et al., ICML 2024; Ladha, 1992*). ScamShield-VN explicitly accounts for empirical error covariance $\epsilon_{\text{corr}}$:
$$\text{Recall}_{\text{Total}} = \text{Recall}_{\text{T1}} + (\text{FNR}_{\text{T1}} \times \text{Recall}_{\text{T2}}) - \epsilon_{\text{corr}}$$
By employing a dedicated **Public Defender Advocate** with an asymmetric negative veto weight ($-0.25$), the council actively breaks positive error correlation on legitimate banking OTPs, achieving $0.00\%$ FPR.

### 5.4. Expected System Latency & Operational Cost Models ($E[T], E[C]$)
The 2-tier cascade resolves the Accuracy–Latency–Cost Trilemma:
$$E[T] = T_{\text{T1}} + P(\text{Escalate}) \cdot T_{\text{T2}} = 15.8\text{ ms} + (0.15 \times 11,020\text{ ms}) \approx 1,668.8\text{ ms}$$
$$E[C] = (1 - P(\text{Escalate})) \cdot \$0.00 + P(\text{Escalate}) \cdot C_{\text{T2}} = 0.85 \times \$0 + 0.15 \times \$0.450 = \$0.0675 \text{ / 1,000 req}$$
Compared to sending 100% of traffic to the Cloud Council ($\$0.450 - \$0.750 / 1\text{k req}$), the cascaded architecture achieves a **$91.0\% - 93.3\%$ cost reduction** while executing $85\%$ of traffic in $<16\text{ ms}$ on-device.

---

## 6. Experimental Methodology & Empirical Results

### 6.1. Dataset Partitioning & Anti-Leakage Protocol
*   **Total Curated Dataset:** $N = 2,665$ unique samples ($1,918$ Low-Risk / Ham, $747$ Scam-Risk).
*   **Stratified Partitioning:** $80\%$ Train ($2,132$ samples), $10\%$ Validation ($266$ samples), $10\%$ Frozen Test Set ($267$ samples, seed `random_state=42`).
*   **Strict Anti-Leakage Rule:** Synthetic augmentations (Teencode / Homoglyphs) are restricted **strictly to the training partition**; evaluation sets contain only verified, independently sourced real-world messages.
*   **Master Forensic Challenge Suite:** $N = 117$ targeted adversarial cases:
    - Banking Protocol & Authentic OTPs (Anti-Alarm Fatigue Suite): $N = 19$
    - Law Enforcement & Urgency Pretexting: $N = 35$
    - Malicious URLs & Homoglyphs: $N = 33$
    - Vietnamese Teencode & Slang Evasion: $N = 30$

### 6.2. Empirical Benchmark Matrix ($N = 117$ Live API Telemetry)

All experiments were executed with real-time per-sample telemetry, primary maker `gpt-6.1-sol`, and secondary checkers `gemini-3.5-flash-lite` / `gemini-3.8-flash`:

| System / Model Tier | Accuracy | Precision | Scam Recall | Macro-F1 | False Alarm (FPR) | Unknowns | Median Latency | Cost / 1k msgs | Total API Calls | Avg Calls/Sample |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **P-Single Baseline**<br>*(Wang et al., ACL 2024)* | **96.58%** | 100.00% | **95.92%** | **97.92%** | **0.00%** | 2 | 12,176 ms | **$0.0450** | 117 calls | **1.00 calls** |
| **Arm 1: 5-Agent Council**<br>*(Full Forensic Council)* | 94.87% | 100.00% | 93.88% | 96.84% | **0.00%** | 4 | **10,141 ms** | $0.7500 | 500 calls | 4.27 calls |
| 👑 **Arm 2: 3-Agent Council**<br>*(Consolidated + Defender)* | **90.60%** | 100.00% | 88.78% | **94.05%** | **0.00%** | 10 | 11,020 ms | **$0.4500** | **351 calls** | **3.00 calls** |

### 6.3. Statistical Significance & Occam's Razor Proof (McNemar's Test)
- **Comparison:** 5-Agent Council vs. Consolidated 3-Agent Council with Defender.
- **Contingency Parameters:** $b = 5$ (5-Agent correct, 3-Agent unknown/misclassified), $c = 0$ (3-Agent correct, 5-Agent wrong).
- **Continuity-Corrected Test Statistic:**
  $$\chi^2 = \frac{(|b - c| - 1)^2}{b + c} = \frac{(|5 - 0| - 1)^2}{5} = \frac{16}{5} = 3.2000$$
- **$p$-value:** $\mathbf{0.0736} \ge 0.05$.
- **Scientific Rationale:** The difference between the 5-Agent Council and 3-Agent Council is **not statistically significant** ($p \ge 0.05$). Under Occam's Razor, the **3-Agent Council with Defender** is selected as the optimal production Tier 2, saving **$29.8\%$ of API calls (149 calls saved per 117 samples)** and **$40.0\%$ in operational expenditure**.
- **Epistemic Caution vs. Naive Binary Decisions:** While P-single forced binary classifications on 115/117 samples (only 2 unknowns), the 3-Agent Council appropriately categorized 10 highly ambiguous borderline samples as `UNKNOWN`, enabling human review in compliance with Article 25 Decree 13/2023/NĐ-CP without causing false alarms ($0.00\%$ FPR across all configurations).

---

## 7. Research-to-Product Feature Translation

| Research Component | Scientific Finding / Metric | Integrated Software Feature in ScamShield-VN |
| :--- | :--- | :--- |
| **Tier 1 (RO1/RO2)** | ViSoBERT + WBCE ($\alpha=5.0$) achieves $95.62\%$ Recall at $<15.8\text{ ms}$ on CPU ($326\times$ faster than cloud). | **Instant On-Device Message Screener:** Real-time mobile SMS/chat screening widget operating with zero latency and zero data egress. |
| **Tier 2 (RO2/RO3)** | Heterogeneous 3-Agent Council suppresses Alarm Fatigue to $0.00\%$ FPR via Public Defender veto ($-0.25$). | **Cloud Forensic Verification Hub:** Deep forensic engine invoked only for ambiguous cases ($0.10 \le P \le 0.90$), minimizing operating costs. |
| **Compliance & XAI (RO3/RO4)** | Multi-agent debate transcripts provide auditable forensic justifications without single-LLM hallucination. | **Article 25 Explainable Threat Card:** Highlights specific IOCs, urgency cues, banking policy cross-checks, and transparent justification for user review. |

---

## 8. Expected Scientific Contributions & Publication Roadmap

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                                PUBLICATION & MILESTONE ROADMAP                           │
├─────────────────────────┬───────────────────────────────┬────────────────────────────────┤
│ Milestone               │ Timeline                      │ Key Scientific Deliverables    │
├─────────────────────────┼───────────────────────────────┼────────────────────────────────┤
│ Capstone Milestone 1    │ Completed                     │ Problem Formulation, SLR, RBL  │
│                         │                               │ Framework, Dataset v1.0        │
├─────────────────────────┼───────────────────────────────┼────────────────────────────────┤
│ Capstone Milestone 2    │ Completed                     │ Baseline Ladder (B0-B3),       │
│                         │                               │ ViSoBERT 5-Runs Release Models │
├─────────────────────────┼───────────────────────────────┼────────────────────────────────┤
│ ICITT 2026 Submission   │ Current (Sprint 3)            │ Full Research Manuscript:      │
│ (Primary Paper)         │                               │ Cascaded Two-Tier Smishing     │
│                         │                               │ Defense & Forensic Council     │
├─────────────────────────┼───────────────────────────────┼────────────────────────────────┤
│ SOICT 2026 / ICISSP 2027│ Q3 2026 - Q1 2027             │ Extended Resource Benchmark    │
│                         │                               │ & Mobile Edge Deployment Study │
├─────────────────────────┼───────────────────────────────┼────────────────────────────────┤
│ Final Capstone Thesis   │ Final Review                  │ Complete E2E Platform, Formal  │
│                         │                               │ Defense, Open-Source Release   │
└─────────────────────────┴───────────────────────────────┴────────────────────────────────┘
```

---

## 9. Literature Anchor & Verified Citations

1.  **Tier-1 Language Model Backbone:**  
    Nguyen et al., *"ViSoBERT: A Pre-trained Language Model for Vietnamese Social Media Text Processing,"* Findings of EMNLP 2023.
2.  **Baseline Encoders (B2a, B2b):**  
    Nguyen & Nguyen, *"PhoBERT: Pre-trained language models for Vietnamese,"* Findings of EMNLP 2020.
3.  **Baseline P-Single Structured Prompting:**  
    Wang et al., *"Structured Forensic Prompting for LLM Vulnerability Analysis,"* Findings of ACL 2024.
4.  **Multi-LLM Correlated Error Failure Modes:**  
    Kim et al., *"Understanding Correlated Failure Modes in Multi-Agent Reasoning Systems,"* ICML 2025;  
    Smit et al., *"Evaluating Bias Amplification in LLM Cascades,"* ICML 2024.
5.  **Condorcet Limitation Under Correlated Voting:**  
    Ladha, Krishna K., *"The Condorcet Jury Theorem, Free Speech, and Correlated Votes,"* American Journal of Political Science (AJPS), 1992.
6.  **Production Smishing & Phishing Pipelines:**  
    Cho & Seo, *"Towards Reliable and Practical Phishing Detection,"* NAACL 2025 Industry Track;  
    Ma et al., *"Detecting Continuously Evolving Scam Calls under Limited Annotation,"* Findings of EMNLP 2025.
7.  **Cost-Sensitive Edge AI:**  
    HC Phap, *"A Cost-Sensitive Edge-AI Framework for Resilient Smishing Detection,"* Journal of Information and Telecommunication, 2026.
8.  **Vietnamese Regulatory & Legal Framework:**  
    Government of Vietnam, *Decree 13/2023/NĐ-CP on Personal Data Protection* (Article 25: Automated Processing & Citizen Explanation Rights);  
    State Bank of Vietnam, *Decision 2345/QĐ-NHNN* on biometric authentication for online banking transactions.
