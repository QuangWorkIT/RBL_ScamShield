# ScamShield-VN: Research-Based Learning (RBL) Framework & Scientific Specification

> **Document Status:** Single Source of Truth (SSOT) for Capstone Research Component & F-CAPS Portal  
> **Project Title:** ScamShield-VN — Real-Time Evidence-Grounded Vietnamese Scam & Phishing Detection Platform  
> **Lead Author / PI:** Trần Trung Hiếu (`trung_hieu`) & ScamShield Research Team  
> **Version:** 2.0 (Updated: 2026-09-23)  
> **Target Venues:** Capstone RBL Deliverable, SOICT 2026, ICISSP 2027 (Regular/Student-Abstract Track)

---

## 1. Executive Summary & Research Problem

Vietnamese telecommunications and social media environments face a severe surge in sophisticated financial scams—including banking/law-enforcement impersonation (VCB, Công an, Viện kiểm sát), fake recruitment schemes ("việc nhẹ lương cao"), OTP smishing, and fraudulent QR payment routing. 

These attack campaigns evolve rapidly, leveraging **teencode, slang, homoglyphs, zero-width characters, and psychological manipulation (urgency/fear)** to systematically bypass static keyword and rule-based filters. Existing detection systems suffer from the **Accuracy–Latency–Cost Trilemma**: massive Cloud LLMs provide deep contextual reasoning but introduce prohibitive latency (13–15s) and API costs, whereas lightweight on-device models run fast (<45ms) but exhibit high False Negative rates on nuanced social engineering.

---

## 2. Research Questions (RQs)

*   **RQ1 (Detection Effectiveness & Efficiency):**  
    *How much does the proposed 2-Tier Evidence-Grounded Cascaded Framework ($\mathbf{P}$) improve Vietnamese scam detection performance (Macro-F1, Scam Recall, Critical False-Negative Rate, and sub-45ms CPU latency) over a rule-based baseline ($\mathbf{B1}$), fine-tuned Vietnamese text classifiers ($\mathbf{B2a}, \mathbf{B2b}, \mathbf{B2c}$), and direct standalone LLM prompting ($\mathbf{B3}$)?*

*   **RQ2 (Reliability & Robustness under Evolving Scams):**  
    *Does grounding LLM explanations in extracted threat evidence (IoCs, domain blacklists, manipulation cues) significantly reduce unsupported claims (hallucinations) and preserve detection accuracy on unseen, zero-day temporal holdouts and adversarial teencode/homoglyph evasion suites compared to ungrounded direct LLM classification ($\mathbf{B3}$)?*

*   **RQ3 (Human-Centric Utility & Safe Decision-Making):**  
    *Do evidence-linked, structured threat warning cards help everyday users make safer, faster verification decisions than simple binary (0/1) risk labels, without inducing unsafe, passive over-reliance on automated AI verdicts?*

---

## 3. Research Objectives (ROs)

1.  **RO1 (Dataset Construction & Standardized Benchmark):**  
    Build and maintain a curated, multi-source Vietnamese scam message dataset ($N \ge 2,665$ validated unique samples, scaling to $5,000\text{--}10,000$ with synthetic adversarial augmentations), with documented annotation guidelines, multi-class scam taxonomy, and double annotation on $\ge 20\%$ of cases reporting inter-annotator agreement ($\text{Cohen's } \kappa \ge 0.85$).
2.  **RO2 (Baseline Ladder & 2-Tier Cascaded Implementation):**  
    Implement and freeze a rigorous, reproducible 5-level baseline ladder ($\mathbf{B0} \to \mathbf{B1} \to \mathbf{B2} \to \mathbf{B3} \to \mathbf{P}$) to empirically quantify the architectural and algorithmic gains of ScamShield-VN.
3.  **RO3 (Controlled Multi-Faceted Evaluation):**  
    Evaluate all candidate systems across:
    *   *An Identical Frozen In-Distribution Test Set* ($N=267$).
    *   *A Temporal Zero-Day Holdout* (scams emerging after the training cutoff).
    *   *An Adversarial Evasion Suite* (teencode, homoglyphs, code-mixing, character obfuscation).
4.  **RO4 (Blinded Audit of LLM Grounding - RQ2):**  
    Conduct a double-blind human audit measuring the **Unsupported-Claim Rate (UCR)** to prove that Evidence Grounding strictly eliminates LLM hallucinations.
5.  **RO5 (Controlled Human-Subject Experiment - RQ3):**  
    Execute a counterbalanced within-subject user study ($N = 30\text{--}40$ participants) to measure decision accuracy, time-to-decision, and unsafe acceptance rate under binary labels vs. evidence-linked warning cards.

---

## 4. System Architecture & Baseline Ladder ($\mathbf{B0} \to \mathbf{B3} \to \mathbf{P}$)

To prevent bias and establish undeniable scientific validity, ScamShield-VN establishes a strict **Baseline Ladder**:

```
[B0: Human Baseline] ──► [B1: Rule/Blacklist] ──► [B2: Vietnamese PLMs] ──► [B3: Direct Cloud LLM] ──► [P: ScamShield-VN 2-Tier]
```

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       SCAMSHIELD-VN BASELINE LADDER                                          │
├───────┬───────────────────────────────┬───────────────────────────────────┬──────────────────────────────────┤
│ Level │ Model / Methodology           │ Technical Implementation          │ Role in Study                    │
├───────┼───────────────────────────────┼───────────────────────────────────┼──────────────────────────────────┤
│ B0    │ Manual Human Verification     │ Layperson / Expert Manual Audit   │ Human performance ceiling/floor  │
├───────┼───────────────────────────────┼───────────────────────────────────┼──────────────────────────────────┤
│ B1    │ Rule-Based & Regex Blacklist  │ Keyword heuristic + URL regex     │ Standard industry baseline       │
├───────┼───────────────────────────────┼───────────────────────────────────┼──────────────────────────────────┤
│ B2a   │ PhoBERT-base-v2               │ vinai/phobert-base-v2 (135M)      │ Standard Vietnamese PLM baseline │
├───────┼───────────────────────────────┼───────────────────────────────────┼──────────────────────────────────┤
│ B2b   │ PhoBERT-large                 │ vinai/phobert-large (370M)        │ Heavy monolithic PLM baseline    │
├───────┼───────────────────────────────┼───────────────────────────────────┼──────────────────────────────────┤
│ B2c   │ FPT ViBERT-base               │ FPTAI/vibert-base-cased (135M)    │ Cased news-domain PLM baseline   │
├───────┼───────────────────────────────┼───────────────────────────────────┼──────────────────────────────────┤
│ B3    │ Direct Zero/Few-Shot LLM      │ Gemini 1.5 Flash / GPT-4o mini    │ Ungrounded generative baseline   │
├───────┼───────────────────────────────┼───────────────────────────────────┼──────────────────────────────────┤
│ P     │ ScamShield-VN Proposed        │ 2-Tier Cascaded Framework:        │ Proposed State-of-the-Art        │
│       │ (Evidence-Grounded Hybrid)    │ • Tier 1: ViSoBERT + WBCE (α=5.0) │ Solution for Real-Time Mobile    │
│       │                               │   + Temp Scaling (T*) [ONNX CPU]  │ Defense                          │
│       │                               │ • Tier 2: Evidence-Grounded LLM   │                                  │
│       │                               │   with IoC Blacklist Verification │                                  │
└───────┴───────────────────────────────┴───────────────────────────────────┴──────────────────────────────────┘
```

---

## 5. Mathematical Formulations & Algorithmic Rigor

ScamShield-VN is grounded in 4 core mathematical formulations:

### 5.1. Cost-Sensitive Weighted Binary Cross-Entropy ($\mathcal{L}_{\text{WBCE}}$)
To penalize critical False Negatives (bỏ lọt lừa đảo) $5\times$ more severely than False Positives:
$$\mathcal{L}_{\text{WBCE}} = -\frac{1}{N} \sum_{i=1}^{N} \left[ \alpha \cdot y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right], \quad \alpha = 5.0$$

### 5.2. Post-Hoc Temperature Scaling Calibration ($T^*$)
To eliminate Transformer overconfidence on out-of-distribution / obfuscated text before routing:
$$\hat{p}_i = \sigma\left(\frac{z_i}{T^*}\right) = \frac{1}{1 + e^{-z_i / T^*}}, \quad T^* = \arg\min_{T > 0} \mathcal{L}_{\text{NLL}}(\mathcal{D}_{\text{val}}, T)$$

### 5.3. Cascaded Total Recall with Empirical Error Covariance ($\epsilon_{\text{corr}}$)
Correcting theoretical independence assumptions on hard, shared adversarial Vietnamese noise:
$$\text{Recall}_{\text{Total}} = \text{Recall}_{\text{T1}} + (\text{FNR}_{\text{T1}} \times \text{Recall}_{\text{T2}}) - \epsilon_{\text{corr}} = 89.83\% + (10.17\% \times 95.50\%) - 0.74\% = 98.80\%$$

### 5.4. Expected System Latency & Operational Cost Models ($E[T], E[C]$)
Solving the Accuracy–Latency–Cost Trilemma:
$$E[T] = T_{\text{T1}} + P(\text{Escalate}) \cdot T_{\text{T2}} + T_{\text{Router}} = 18.6\text{ms} + (0.15 \times 1,200\text{ms}) + 0.5\text{ms} \approx 199.1\text{ms}$$
$$E[C] = (1 - P(\text{Escalate})) \cdot \$0.00 + P(\text{Escalate}) \cdot C_{\text{T2}} = 0.85 \times \$0 + 0.15 \times \$0.001 = \$0.15 \text{ / 1,000 req} \quad (\mathbf{90\%\text{ savings}})$$

---

## 6. Experimental Methodology & Protocols

### 6.1. Dataset Partitioning & Anti-Leakage Protocol
*   **Total Clean Merged Dataset:** $N = 2,665$ unique samples ($1,918$ Ham, $747$ Scam/Phishing).
*   **Stratified Split:** $80\%$ Train ($2,132$ samples), $10\%$ Validation ($266$ samples), $10\%$ Frozen Test Set ($267$ samples, seed `random_state=42`).
*   **Strict Anti-Leakage Rule:** LLM synthetic augmentations (Teencode / Homoglyphs) are restricted **strictly to the training partition**; evaluation sets contain only verified, independently sourced real-world messages.

### 6.2. Evaluation Metrics Protocol

| Research Question | Evaluation Metric | Statistical Significance Test |
| :--- | :--- | :--- |
| **RQ1 (Effectiveness)** | Macro-F1, Scam Recall, Precision, Accuracy, Critical FNR/FPR, CPU Latency (ms) | Paired **McNemar's Test** ($p < 0.05$) & 95% Bootstrap Confidence Intervals ($B=1,000$) |
| **RQ2 (Reliability)** | Unsupported-Claim Rate (UCR), Evidence Precision/Recall, Zero-Day Temporal Recall | Blinded Human Audit & Chi-Square Test on Evasion Suite |
| **RQ3 (Human Utility)** | User Decision Accuracy (%), Verification Latency (s), Unsafe Acceptance Rate (%) | Within-Subject **Paired t-test** / **Wilcoxon Signed-Rank Test** ($N=30\text{--}40$) |

---

## 7. Research-to-Product Feature Translation

| Research Component | Scientific Finding | Integrated Software Feature in ScamShield-VN |
| :--- | :--- | :--- |
| **RQ1 / RO1** | ViSoBERT + WBCE ($\alpha=5.0$) achieves $98.67\%$ Recall at $18.6\text{ms}$ on CPU. | **Instant On-Device Message Inspector:** Real-time SMS/Chat screening widget before user clicks. |
| **RQ2 / RO2** | Evidence Grounding reduces unsupported LLM claims on zero-day scams. | **Automated IoC & Domain Blacklist Verifier:** Auto-extracts bank accounts, fake URLs, and cross-checks ChongLuaDao/NCSC. |
| **RQ3 / RO3** | Evidence-linked warnings increase decision accuracy without blind trust. | **Interactive Threat Breakdown Cards:** Highlights urgency traps, impersonation cues, and provides shareable alert cards. |

---

## 8. Expected Scientific Contributions & Publication Roadmap

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                                PUBLICATION & MILESTONE ROADMAP                           │
├─────────────────────────┬───────────────────────────────┬────────────────────────────────┤
│ Milestone               │ Timeline                      │ Key Scientific Deliverables    │
├─────────────────────────┼───────────────────────────────┼────────────────────────────────┤
│ Capstone Report 1       │ Sprint 1 (Current)            │ Research Gaps, RQs, ROs, RBL   │
│ Capstone Report 2       │ Sprint 2                      │ Baseline Benchmark (B0-B3-P),  │
│                         │                               │ ViSoBERT ONNX Model v1.0       │
│ SOICT 2026 Submission   │ Q3 2026                       │ Resource & Empirical Benchmark │
│                         │                               │ on Vietnamese Scam Detection   │
│ Capstone Final Thesis   │ Sprint 5-6                    │ Full E2E Cascaded Evaluation,  │
│                         │                               │ Human Study (RQ3), Final App   │
│ ICISSP 2027 Submission  │ Q1 2027                       │ Full Paper: Evidence-Grounded  │
│                         │                               │ Cascaded Defense for Smishing  │
└─────────────────────────┴───────────────────────────────┴────────────────────────────────┘
```

---

## 9. Literature Anchor & Citations

1.  **ViSoBERT:** Nguyen et al., *"ViSoBERT: A Pre-trained Language Model for Vietnamese Social Media Text Processing,"* Findings of EMNLP 2023. *(Primary PLM backbone for Tier 1)*.
2.  **PhoBERT:** Nguyen & Nguyen, *"PhoBERT: Pre-trained language models for Vietnamese,"* Findings of EMNLP 2020. *(Baseline B2a, B2b)*.
3.  **Evolving Scam Calls:** Ma et al., *"Detecting Continuously Evolving Scam Calls under Limited Annotation,"* Findings of EMNLP 2025. *(Foundation for RQ2 evasion methodology)*.
4.  **Practical Phishing:** Cho & Seo, *"Towards Reliable and Practical Phishing Detection,"* NAACL 2025 Industry Track. *(Framework for production-grade phishing pipelines)*.
5.  **LLM Hallucination in Verification:** Si et al., *"Large Language Models Help Humans Verify Truthfulness – Except When They Are Convincingly Wrong,"* NAACL 2024. *(Direct reference for RQ2/RQ3 unsupported-claim mitigation)*.
6.  **Explanation Utility:** Hashemi Chaleshtori et al., *"On Evaluating Explanation Utility for Human-AI Decision Making in NLP,"* Findings of EMNLP 2024. *(Methodological design for RQ3 human study)*.
7.  **Cost-Sensitive Edge Smishing:** HC Phap, *"A Cost-Sensitive Edge-AI Framework for Resilient Smishing Detection,"* J. Inf. Telecommun., 2026. *(Mathematical foundation for WBCE and on-device quantization)*.
