# ScamShield-VN: Evidence-Grounded Vietnamese Scam and Phishing Detection Platform

> **Authors:** Nguyen Trung Hieu, Le Quoc Huy, Hoang Hai Phuc, Phan Tran Hoang Tran, Nguyen Minh Quang  
> **Affiliation:** Department of Software Engineering, FPT University, Ho Chi Minh City, Vietnam  
> **Contact:** `cristand2825@gmail.com`, `{huylq, phuchh, tranpth, quangnm}@fpt.edu.vn`  
> **Status:** Full Manuscript Draft (IEEE Conference Format Preview)

---

## Abstract
Telecommunications scam and phishing campaigns in Vietnam inflict severe financial and social damage, increasingly exploiting localized syntactic nuances such as teencode, slang, and non-diacritic text to bypass keyword filters. However, current defensive solutions either depend on symmetric-loss classifiers that suffer from unacceptable false-negative rates on subtle lures, or rely exclusively on cloud Large Language Models (LLMs) that exhibit severe alarm fatigue and latency bottlenecks. In this work, we conduct an empirical study benchmarking pretrained Vietnamese language models against in-context LLMs, proposing a lightweight edge screener that pairs ViSoBERT with a Cost-Sensitive Weighted Binary Cross-Entropy loss ($\mathcal{L}_{\text{WBCE}}$, $\alpha=5.0$) quantized via ONNX INT8. Evaluated across 5 deterministic random seeds on a frozen benchmark of 2,665 real-world Vietnamese SMS messages ($N=267$ isolated test set), our proposed ViSoBERT model achieves a dominant Scam Recall of $95.62\% \pm 2.25\%$ and Macro-F1 of $92.51\% \pm 2.39\%$, significantly outperforming Gemini 3.5 Flash ($p < 0.0001$, McNemar test) whose precision collapsed to $64.47\%$ due to hyper-vigilant over-flagging, while maintaining an on-device CPU inference latency of $15\text{ ms/message}$ and a $390\text{ MB}$ footprint. These results demonstrate that asymmetric penalty weighting on social-specialized encoders provides Pareto-optimal edge triage, establishing the empirical grounding for a two-tier hybrid defense architecture.

**Keywords:** scam detection, phishing detection, large language models, cost-sensitive learning, Vietnamese NLP, edge AI.

---

## 1. Introduction
Digital telecommunications fraud, smishing (SMS phishing), and impersonation attacks have surged dramatically across Southeast Asia, inflicting estimated damages exceeding hundreds of millions of dollars annually in Vietnam alone. Attackers systematically exploit deceptive social engineering tactics, targeting vulnerable mobile users with fraudulent banking alerts, fake tax arrears notices, and fictitious job opportunities. In Vietnam, this operational landscape is characterized by extensive linguistic evasion tactics: scammers intentionally incorporate colloquial slang, compound teencode abbreviations, irregular spacing, and diacritic-stripped text to circumvent static keyword blacklists and carrier-level regex filters.

Recent advances in natural language processing (NLP) have motivated researchers to deploy deep learning architectures and Large Language Models (LLMs) for message-based cyber defense. Standard transformer-based architectures, including PhoBERT and multilingual variants, have demonstrated competitive overall classification accuracy on benchmark corpora. Simultaneously, prompt-based LLMs such as GPT-4 and Gemini have shown emergent reasoning capabilities in zero-shot and few-shot fraudulent intent classification.

However, in the empirical literature we reviewed, existing systems encounter a critical tripartite bottleneck. First, conventional neural classifiers are universally trained under symmetric loss functions (such as unweighted cross-entropy), treating false positives (misidentifying a legitimate message as scam) and catastrophic false negatives (failing to intercept a scam message that causes financial ruin) as mathematically identical. Second, state-of-the-art cloud LLMs suffer from severe "alarm fatigue": hyper-vigilant prompting causes precision to collapse as benign promotional and transactional notifications are mistakenly flagged. Third, cloud API calls incur multi-second latencies ($3\text{--}6\text{ seconds/message}$) and recurring monetary costs, violating the strict sub-second latency and offline privacy constraints required for mobile edge deployment.

To resolve these challenges, this paper presents an evidence-grounded empirical study and architectural solution. Our primary contributions are summarized as follows:
* **Rigorous Multi-Seed Benchmark:** We establish a standardized benchmark on $2,665$ real-world Vietnamese SMS messages ($N=267$ isolated frozen test set) across 5 deterministic random seeds, comparing fine-tuned Vietnamese language models (PhoBERT-base, PhoBERT-large, FPT ViBERT) against few-shot cloud LLMs (Gemini 3.5 Flash).
* **Cost-Sensitive Social Media Modeling:** We fine-tune ViSoBERT under a Cost-Sensitive Weighted Binary Cross-Entropy loss ($\mathcal{L}_{\text{WBCE}}$, $\alpha=5.0$), demonstrating a dominant Scam Recall of $95.62\% \pm 2.25\%$ and Macro-F1 of $92.51\% \pm 2.39\%$.
* **Statistical and Pareto Profiling:** Through McNemar's paired tests and deployment profiling, we establish that ViSoBERT attains Pareto-optimality over large-scale encoders ($3.8\times$ smaller than PhoBERT-large) while operating at $\approx 15\text{ ms/message}$ on consumer CPU hardware.
* **Two-Tier Architecture Grounding:** Based on the empirical breakdown of single-LLM precision collapse, we formulate an evidence-backed two-tier triage pipeline transitioning ambiguous edge samples to a specialized multi-agent forensic council.

---

## 2. Related Work
To systematically situate our contribution within the broader literature, we synthesize 40 peer-reviewed investigations into three dominant research themes.

### 2.1 Theme 1: Traditional Machine Learning and Rule-Based Filtering
Early investigations into telecommunications spam detection predominantly evaluated classical shallow algorithms including Support Vector Machines (SVM), Naive Bayes (NB), and ensemble tree structures paired with TF-IDF or Bag-of-Words feature representations. However, shallow classifiers degrade precipitously when encountering out-of-vocabulary teencode, deliberate orthographic obfuscations, and adversarial synonym replacements commonly engineered by modern cyber syndicates. Furthermore, static rule-based heuristics fail to model long-range semantic dependencies and contextual urgency.

### 2.2 Theme 2: Pretrained Language Models for Vietnamese NLP
The emergence of transformer-based architectures revolutionized low-resource natural language understanding. For the Vietnamese linguistic space, PhoBERT established foundational benchmarks for syllable-level contextual embeddings. Nguyen-Xuan et al. introduced a mixed-language dual-encoder reaching an F1-score of $0.94$ on code-mixed social media lures, while Cam and Binh achieved $86.47\%$ accuracy utilizing PhoBERT on Vietnamese email spam. Nevertheless, a critical shared deficiency across existing Vietnamese transformer applications is their reliance on standard unweighted cross-entropy loss. Because spam and scam instances represent an extreme minority in genuine traffic, symmetric loss optimization biases decision thresholds toward majority benign classes, yielding unacceptably high false-negative rates on subtle, indirect fraud scenarios.

### 2.3 Theme 3: LLMs and Edge-Deployed Small Language Models
Recent initiatives have explored Large Language Models and on-device Small Language Models (SLMs) for threat triage. Zhou et al. benchmarked leading commercial models (GPT-4o, Claude, Gemini) on SMS fraud, finding that fraud recall fluctuated widely between $64.16\%$ and $90.13\%$ while benign recall dropped as low as $12.81\%$ due to severe over-flagging. In contrast, edge-oriented frameworks such as QuishingShield and knowledge distillation pipelines have targeted low-latency mobile inference, reporting CPU execution times under $50\text{ ms}$. Nonetheless, these architectures have focused almost exclusively on English corpora and fail to integrate cost-asymmetric penalty functions tailored to the nuances of Vietnamese social media text.

| Study | Language | Model / Architecture | Evaluation Dataset | Key Metric | Primary Limitation / Research GAP |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Tuấn et al. (2023) | Vietnamese | PhoBERT, CNN, LSTM | Multi-accent SMS ($N\approx 3,000$) | Acc: $95.56\%$ | Evaluated symmetric loss; no cost-sensitive penalty. |
| Nguyen-Xuan (2026) | Viet-Eng | MLTEA Dual-Encoder | Code-mixed Phishing | F1: $0.940$ | Cloud-scale architecture; high latency for edge. |
| Cam \& Binh (2026) | Vietnamese | PhoBERT, BiLSTM | VNSED Email Corpus | Acc: $86.47\%$ | Lacks social slang vocabulary; high false negatives. |
| Zhou et al. (2026) | Multilingual | GPT-4o, Claude, Gemini | FraudSMSWalker ($N\approx 4,000$) | Recall: $64.16\text{--}90.13\%$ | Extreme false positives (benign recall $<30.25\%$). |
| Banda et al. (2026) | English | Llama-3.2-3B Mobile | QR/Text Lures ($N=4,200$) | Latency: $45\text{ ms}$ | English only; heavy RAM footprint ($>2\text{ GB}$). |
| Phap et al. (2026) | English | BiGRU + MaskedPool + WBCE | UCI \& LSDST ($N=5,574$) | Latency: $0.25\text{ ms}$ | Recurrent model; lacks transformer contextual semantics. |
| **This Work** | **Vietnamese** | **ViSoBERT + WBCE ($\alpha=5.0$)** | **Merged SMS ($N=2,665$)** | **Recall: $95.62\%$** | **Pareto-optimal edge detection: $15\text{ ms}$, $390\text{ MB}$, INT8.** |

---

## 3. Methodology

### 3.1 Benchmark Dataset and Frozen Test Partition
We curated a unified corpus of $2,665$ genuine Vietnamese telecommunications messages by merging verified public repositories, community reports from ChongLuaDao, and national cybersecurity warning feeds (`data/raw/vietnamese_sms_merged_all.csv`). The corpus consists of $1,918$ benign messages ($72.0\%$) and $747$ confirmed scam instances ($28.0\%$). 

* **Training and Validation Partition ($90\%$):** $2,398$ messages.
* **Frozen Test Partition ($10\%$):** Exactly **$N = 267$ messages** ($192$ Ham, $75$ Scam).
* Inter-Annotator Agreement: Cohen's $\kappa = 0.88$.

### 3.2 Cost-Sensitive Loss Formulation ($\mathcal{L}_{\text{WBCE}}$)
To impose an explicit inductive bias favoring recall on deceptive samples:
$$\mathcal{L}_{\text{WBCE}} = -\frac{1}{N} \sum_{i=1}^{N} \left[ \alpha \cdot y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right]$$
where $\alpha = 5.0$ exerts a 5-fold steeper penalty gradient for false negatives.

### 3.3 ONNX Runtime Export and Edge Quantization
Exported via `opset_version=18` with dynamic axes. Resulting file `visobert_tier1.onnx` occupies $390\text{ MB}$ with an average inference latency of $\approx 15.8\text{ ms/msg}$ on CPU.

### 3.4 Two-Tier Architecture and Multi-Agent Council
* **Tier 1 (Edge Screener):** ViSoBERT on-device. If $P(\hat{y}) \ge 0.90 \rightarrow$ Immediate verdict ($< 15\text{ ms}$, handles $85\%$ of traffic).
* **Tier 2 (Forensic Council Escalation):** If confidence $P < 0.90 \rightarrow$ Routed to 5-Agent Council: Forensic Lead, Psycholinguistic, Cyber Threat, Financial Fraud, and Public Defender (Devil's Advocate).

---

## 4. Empirical Results

### 4.1 Comparative Benchmark Across 5 Independent Runs
Evaluated on the isolated Frozen Test Partition ($N=267$ messages):

| Model Configuration | Role / Category | Parameters | Accuracy (%) | Precision (%) | Scam Recall (%) | Macro-F1 (%) | Size / Latency |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **ViSoBERT + WBCE ($\alpha=5.0$)** | **Proposed (Tier 1 Edge)** | **110M** | **$95.65 \pm 1.54$** | **$89.79 \pm 5.15$** | **$95.62 \pm 2.25$** | **$92.51 \pm 2.39$** | **390 MB / 15.8 ms** |
| PhoBERT-large | Baseline B2.3 | 370M | $95.95 \pm 1.57$ | $93.13 \pm 3.17$ | $92.33 \pm 3.44$ | $92.70 \pm 2.87$ | 1,480 MB / 54.2 ms |
| FPT ViBERT-base | Baseline B2.2 | 124M | $95.04 \pm 1.11$ | $90.10 \pm 4.12$ | $92.60 \pm 2.84$ | $91.25 \pm 1.81$ | 480 MB / 18.2 ms |
| PhoBERT-base-v2 | Baseline B2.1 | 135M | $95.11 \pm 0.83$ | $91.24 \pm 1.52$ | $91.23 \pm 1.84$ | $91.23 \pm 1.50$ | 540 MB / 17.5 ms |
| Gemini 3.5 Flash (5-shot) | Baseline B3 (Cloud) | Proprietary | $84.50 \pm 1.02$ | $64.47 \pm 1.52$ | $100.00 \pm 0.00$ | $78.38 \pm 1.12$ | Cloud / 4,912 ms |

### 4.2 Paired McNemar Test Analysis ($\alpha=0.05$)

| Pairwise Comparison | $b$ (ViSoBERT+) | $c$ (Baseline+) | $\chi^2_{\text{cont}}$ | Exact $p$-value | Odds Ratio | Reject $H_0$? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| ViSoBERT vs. PhoBERT-base-v2 | 12 | 4 | 3.0625 | 0.0768 | 3.00 | False ($p \ge 0.05$) |
| ViSoBERT vs. FPT ViBERT-base | 14 | 5 | 3.3684 | 0.0636 | 2.80 | False ($p \ge 0.05$) |
| ViSoBERT vs. PhoBERT-large | 9 | 3 | 2.0833 | 0.1460 | 3.00 | False ($p \ge 0.05$) |
| ViSoBERT vs. Gemini 3.5 Flash | 38 | 2 | 30.625 | **0.0000** | **19.00** | **True ($p < 0.001$)** |

---

## 5. Discussion

### 5.1 Pareto-Optimality of Cost-Sensitive Social Encoders
ViSoBERT paired with cost-sensitive loss ($\mathcal{L}_{\text{WBCE}}$, $\alpha=5.0$) occupies an optimal Pareto frontier for mobile edge triage. By penalizing false negatives five times more heavily during backpropagation, the decision threshold shifts to capture borderline teencode variants and subtle impersonation patterns that conventional symmetric models disregard. In 75% of discordantly detected cases where ViSoBERT outperformed PhoBERT-base, the message contained informal Vietnamese internet slang.

### 5.2 Deconstructing Single-LLM Alarm Fatigue
While Gemini 3.5 Flash achieved 100% Scam Recall, its Precision collapsed to $64.47\%$, misclassifying $35.53\%$ of genuine communications as fraudulent. The model hyper-vigilantly flagged genuine bank OTPs and carrier promotions containing URLs. In real deployment, a 35.5% false-alarm rate causes users to disable defensive software.

### 5.3 Scientific Motivation for Amendment v1.1: 5-Agent Council
To neutralize single-LLM alarm fatigue without sacrificing sensitivity, Amendment v1.1 routes ambiguous edge samples ($P < 0.90$) to a 5-Agent Council featuring an active **Public Defender (Devil's Advocate)**. The Public Defender actively searches for legitimate banking and carrier patterns, restoring high precision.

### 5.4 Failure of Parameter Scaling Without Asymmetric Loss
Despite having nearly $3\times$ more parameters, taking $3.45\times$ longer to train, and consuming $1.48\text{ GB}$ of memory, PhoBERT-large attained a Scam Recall of only $92.33\%$, missing more scams than the 110M ViSoBERT encoder ($95.62\%$). In imbalanced safety-critical tasks, loss formulation and domain pre-training outweigh sheer model capacity.

---

## 6. Threats to Validity
* **Internal Validity:** Mitigated via 5 deterministic seeds ($[42, 100, 123, 999, 2026]$) and greedy temperature = 0 for LLMs.
* **External Validity:** Focused on Vietnamese SMS telecommunications; findings delimited from English emails.
* **Construct Validity:** Cryptographic deduplication and strict isolation of Frozen Test Set ($N=267$, IAA $\kappa = 0.88$).
* **Conclusion Validity:** High statistical power ($>0.85$ on $N=267$), paired McNemar tests with continuity correction.

---

## 7. Conclusion & Future Work
This paper demonstrated that fine-tuning ViSoBERT under a Cost-Sensitive loss ($\alpha=5.0$) achieves a dominant Scam Recall of $95.62\% \pm 2.25\%$ and Macro-F1 of $92.51\% \pm 2.39\%$ on Vietnamese SMS data, significantly outperforming few-shot Gemini 3.5 Flash ($p < 0.0001$) while operating at $15\text{ ms/msg}$ on CPU. Future work will investigate multimodal QR phishing verification and live telecommunications carrier integration.

**AI Usage Declaration:** Google Gemini was utilized for language editing and IEEE formatting verification. All experimental designs, model training pipelines, empirical benchmarks, and statistical analyses were independently conducted by the authors.
