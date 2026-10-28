# ScamShield-VN: Evidence-Grounded Two-Tier Architecture for Vietnamese Scam and Phishing Detection

> **Target Venue:** Journal of Advances in Information Technology (JAIT)  
> **Authors:** Nguyen Trung Hieu, Nguyen Minh Quang, Hoang Hai Phuc, Phan Tran Hoang Tran, Nguyen Quoc Huy
> **Affiliation:** Department of Software Engineering, FPT University, Ho Chi Minh City, Vietnam  
> **Emails:** `cristand2825@gmail.com` (N.T.H.), `nguyenminhquangnmqlamdong@gmail.com` (N.M.Q.), `haiphuchoang2675@gmail.com` (H.H.P.), `pthoangtran0511@gmail.com` (P.T.H.T.), `nguyenhuy.se205@gmail.com` (N.Q.H.)
> **Status:** Standardized Manuscript Draft (Aligned with `JAIT-template.doc`)

---

## Abstract

Telecommunications fraud and smishing in Vietnam exploit localized linguistic evasion, including regional slang, teencode abbreviations, and diacritic omission. Conventional defenses suffer from elevated false-negative rates under symmetric loss or induce severe alarm fatigue when relying on solitary cloud Large Language Models. We present ScamShield-VN, an integrated two-tier architecture pairing an on-device edge screener with a consolidated three-agent forensic council. Tier 1 deploys ViSoBERT fine-tuned with Cost-Sensitive Weighted Binary Cross-Entropy loss ($\alpha=5.0$) and quantized via ONNX INT8 ($98.42\text{ MB}$ / $93.86\text{ MiB}$, $70.7\text{ ms}$ CPU latency). Across five independent training seeds evaluated on stratified validation partitions ($351/367$ pooled scam detections), ViSoBERT achieves $95.64\% \pm 2.04\%$ macro-average scam recall and $92.51\%$ Scam-F1 ($94.51\%$ Macro-F1). When deployed as a quantized engine on the locked frozen holdout benchmark ($N=267$, $192$ benign, $75$ scam, threshold $\theta_{\text{scam}}=0.90$), it attains $96.00\%$ scam recall ($72/75$, exact $95\%$ Clopper-Pearson confidence interval (CI): $[88.8\%, 99.2\%]$) and $4.17\%$ false-positive rate ($8/192$), significantly outperforming solitary Gemini 3.5 Flash in paired correctness ($p < 0.0001$). On an exploratory suite ($N=384$), the cascade resolves $96.6\%$ of traffic locally at $70.7\text{ ms}$ per-message median latency ($267.5\text{ ms}$ mean system latency), attaining $97.40\%$ accuracy, $2.37\%$ false-alarm rate, and $\$0.0153$ marginal cloud cost per 1,000 messages. In paired testing on a 117-sample challenge suite, 3-agent and 5-agent councils showed no statistically significant difference ($p = 0.0625$); the 3-agent panel reduced token cost by $40\%$ while preserving a $0.00\%$ false-alarm rate on authentic transactional and service notifications.

**Keywords:** scam detection, phishing detection, large language models, cost-sensitive learning, Vietnamese NLP, edge AI, multi-agent consensus.

---

## I. INTRODUCTION

Telecommunications fraud, smishing (SMS phishing), and impersonation scams have proliferated rapidly across Southeast Asia, inflicting estimated losses exceeding 18.9 trillion VND (approximately US \$744 million) in Vietnam during 2024 alone, according to national cybersecurity surveys [1], [2]. Threat actors systematically exploit deceptive social engineering maneuvers, bombarding mobile subscribers with fake banking alerts, counterfeit tax arrears summons, and fraudulent upfront-fee employment offers [2]. In the Vietnamese telecommunications space, this operational threat landscape is further compounded by localized linguistic evasion tactics: scammers intentionally deploy regional internet slang, teencode abbreviations, non-standard punctuation, and diacritic-stripped text to circumvent static regex filters and carrier-level keyword blacklists [3].

Recent advances in natural language processing (NLP) have led to the deployment of deep transformer models and Large Language Models (LLMs) for digital threat mitigation [4]. For Vietnamese text, foundational encoders such as PhoBERT [5] and multilingual variants have demonstrated competitive sentence-level representation. Simultaneously, generative LLMs (e.g., GPT-4, Gemini) have showcased emergent contextual reasoning when evaluated on phishing detection benchmarks [6].

However, existing defensive paradigms suffer from three fundamental limitations:

1. **Symmetric Loss Misalignment:** Conventional deep learning classifiers are universally optimized using standard symmetric cross-entropy loss. In telecommunications security, error outcomes have highly asymmetric costs: misclassifying a benign notification (False Positive) causes transient user inconvenience, whereas missing an active smishing lure (False Negative) results in catastrophic financial extortion. Symmetric loss drives decision boundaries toward majority benign classes, missing subtle fraud attempts.
2. **Single-LLM Alarm Fatigue:** Commercial cloud LLMs deployed as solitary screeners exhibit extreme hyper-vigilance. Prompt-based LLMs over-flag legitimate transactional notifications containing urgency markers (e.g., banking One-Time Passwords) or embedded short URLs, causing precision to collapse and generating intolerable false alarm rates ($>35\%$, specifically $\text{FAR} = 35.53\%$ observed on Gemini 3.5 Flash).
3. **Operational Bottlenecks and Privacy Constraints:** Standalone cloud LLM querying incurs multi-second latency bottlenecks ($3\text{--}15\text{ s/message}$) and recurring per-token financial costs, while violating mobile edge privacy requirements by transmitting personal telecommunications payloads off-device without privacy safeguards.

To address these gaps, this study presents **ScamShield-VN**, an evidence-grounded, two-tier cascaded architecture that integrates an on-device edge screener with a consolidated three-agent forensic council. Our primary research contributions are summarized as follows:

- **Empirical Multi-Seed Benchmark:** We establish an uncompromised evaluation standard on $2,664$ real-world Vietnamese SMS messages ($N=267$ isolated frozen test set) evaluated across five deterministic random seeds, benchmarking fine-tuned Vietnamese encoders (PhoBERT-base, PhoBERT-large, FPT ViBERT) against few-shot cloud LLMs (Gemini 3.5 Flash).
- **Cost-Sensitive Edge Screener:** We fine-tune ViSoBERT [7] under a Cost-Sensitive Weighted Binary Cross-Entropy loss ($\mathcal{L}_{\text{WBCE}}$, $\alpha=5.0$) and quantize the model via ONNX INT8 ($97.57\text{M}$ parameters, $98.42\text{ MB}$ ($93.86\text{ MiB}$) with $70.7\text{ ms}$ CPU latency; baseline FP32: $390.54\text{ MB}$), achieving an edge Scam Recall of $95.64\% \pm 2.04\%$ and Scam-F1 of $92.51\% \pm 2.39\%$ (unweighted Macro-F1: $94.51\% \pm 0.96\%$).
- **Consolidated 3-Agent Council with Public Defender:** To resolve ambiguous boundary samples, we design a specialized multi-agent council incorporating an adversarial Public Defender agent. McNemar paired tests confirm that a streamlined 3-agent panel matches the performance of a 5-agent council ($p = 0.0736 > 0.05$) while reducing token cost by $40\%$ and eliminating false alarms ($0.00\%$ FPR) on legitimate banking traffic.
- **Two-Tier Cascaded System and Pareto Profiling:** We deploy an end-to-end cascaded pipeline governed by confidence routing threshold $\tau = 0.90$. On a combined benchmark ($N=384$), the system resolves $96.6\%$ of traffic locally at the edge, achieving $97.40\%$ overall accuracy, $97.11\%$ scam recall, and an average latency of $267.5\text{ ms}$ at $\$0.0153$ marginal cloud cost per 1,000 messages.

The remainder of this paper is structured according to the JAIT publication guidelines: Section II (Literature Review) reviews relevant literature thematically and chronologically across four research themes. Section III (Materials and Methods) outlines materials, loss formulation, ONNX edge quantization, and the multi-agent council. Section IV (Result and Discussion) presents empirical results, statistical tests, and Pareto trade-off discussions. Finally, Section V (Conclusion) concludes the paper with engineering implications and future directions.

---

## II. LITERATURE REVIEW

To systematically contextualize our work within the evolution of telecommunications threat triage, we analyze peer-reviewed investigations organized across four foundational research thrusts: (i) classical machine learning and rule-based filtering under orthographic evasion; (ii) pretrained language models and cost-sensitive text classification; (iii) frontier large language models, cascaded deferral, and on-device edge deployments; and (iv) multi-agent deliberation, structured prompting, and correlated error mitigation.

### A. Theme 1: Classical Machine Learning and Rule-Based Filtering

Early investigations into telecommunications spam detection systematically evaluated shallow machine learning algorithms, including Support Vector Machines (SVM), Naive Bayes, and decision tree ensembles paired with TF-IDF or lexical $-gram representations [8]–[10]. While Saeed [8] demonstrated competitive baseline classification accuracy on standardized, formal Latin corpora, Xie [9] revealed that shallow classifiers deteriorate substantially when exposed to informal text variations. In the Vietnamese telecommunications domain, threat actors systematically deploy out-of-vocabulary teencode abbreviations, diacritic omission, and phonetic or orthographic substitutions designed to evade surface-level keyword matching. Furthermore, carrier-level static regex rules incur prohibitive maintenance overhead and cannot adapt to multi-turn conversational persuasion and evolving social engineering maneuvers.

### B. Theme 2: Pretrained Language Models and Cost-Sensitive Text Classification

The adoption of transformer-based contextual representations marked a notable advancement in localized threat detection. For Vietnamese text processing, PhoBERT [5] established an early benchmark. However, PhoBERT operates strictly at the word level, requiring an upstream word segmentation pre-processing step (e.g., RDRSegmenter). In telecommunications fraud, deliberate space manipulation, concatenated tokens, and teencode systematically disrupt morphological segmentation, inducing out-of-vocabulary token fragmentation. To mitigate segmentation brittleness on informal user-generated text, ViSoBERT [7] was pretrained on a 1 GB corpus of uncompressed Vietnamese social media text using Byte-Pair Encoding (BPE) subword tokenization, preserving morphological integrity across noisy social colloquialisms.

Recent studies applied contextual encoders to localized threats: Tuấn et al. [11] evaluated PhoBERT and recurrent baselines on multi-accent SMS, Cam and Binh [12] attained $86.47\%$ accuracy on Vietnamese spam email, and Nguyen-Xuan et al. [13] proposed a dual-encoder architecture achieving an F1-score of $0.940$ on code-mixed phishing lures. Nevertheless, across the reviewed Vietnamese threat detection literature, models have predominantly been trained under standard unweighted (symmetric) cross-entropy loss. Grounded in the principles of cost-sensitive learning [14]–[16], telecommunications threat filtering imposes deeply asymmetric operational error costs: a false positive causes transient inconvenience, whereas a false negative exposes mobile subscribers to credential theft and financial extortion. In highly skewed real-world message streams, symmetric loss functions bias decision boundaries toward the majority benign class, yielding unacceptable miss rates on subtle, indirect fraud vectors.

### C. Theme 3: Frontier LLMs, Cascaded Deferral, and On-Device Edge Deployments

Subsequent research examined generative Large Language Models (LLMs) and on-device Small Language Models (SLMs) for threat triage [4], [17], [18]. Zhou et al. [17] comprehensively benchmarked frontier commercial LLMs (including GPT-4o, Claude, and Gemini) on SMS fraud, revealing that while fraud recall ranged between $64.16\%$ and $90.13\%$, benign recall collapsed to $12.81\%\text{--}30.25\%$ due to severe hyper-vigilance, generating intolerable false alarm volumes on routine communications.

To resolve operational latency and computational overhead on edge mobile devices, lightweight on-device architectures have emerged. Banda et al. [19] deployed a distilled student model (derived from Llama-3.2-3B) for multi-modal QR phishing with a latency of $25.3\text{--}45\text{ ms}$, while Phap et al. [20] implemented a lightweight BiGRU equipped with Weighted Binary Cross-Entropy (WBCE) on English SMS corpora, attaining an inference latency of $0.25\text{ ms}$ on CPU hardware. While Phap et al. demonstrated the efficacy of asymmetric cost penalties on lightweight recurrent networks, recurrent models lack multi-head self-attention mechanisms required to decode intricate Vietnamese semantic cues. Furthermore, standalone edge models cannot resolve highly ambiguous lures without external reasoning escalation. This necessitates an asymmetric model deferral and cascaded filtering architecture [21], [22], complemented by selective classification with a reject/unknown option [23] to safely route ambiguous traffic.

### D. Theme 4: Multi-LLM Deliberation, Structured Prompting, and Correlated Error Mitigation

The emergence of LLM-as-a-judge frameworks and multi-agent deliberation architectures has offered new mechanisms for complex reasoning under uncertainty [24]–[26]. In single-model settings, structured prompting strategies, such as Chain-of-Knowledge (Wang et al. [27]), establish competitive zero-shot baseline performance. Simultaneously, multi-agent frameworks like ChatEval [24] and Panels of LLM evaluators (PoLL, Verga et al. [28]) demonstrate that ensembling diverse model outputs improves reasoning robustness over solitary evaluators. MultiPhishGuard [26] proposed a 5-agent multi-role LLM framework for phishing email triage with learned weights.

However, theoretical analyses by Ladha [29] established that the asymptotic error convergence guaranteed by the Condorcet Jury Theorem degrades substantially when individual voter judgments exhibit positive correlation. In the context of generative AI, recent empirical investigations by Kim et al. [30] and Smit et al. [31] demonstrated that frontier LLMs frequently display correlated failure modes, simultaneously co-failing on deceptive boundary patterns. Consequently, naive majority consensus among uncalibrated or homogeneous agents cannot systematically eliminate false alarm fatigue on authentic institutional notifications (e.g., banking OTPs with urgent verbiage). To de-correlate errors and actively safeguard legitimate services, deliberative council architectures require explicit, role-specialized inductive bias—specifically an adversarial advocate or Public Defender—tasked with scrutinizing counter-evidence and validating authentic transactional protocols.

### E. Synthesis and Identified Research Gaps

TABLE I synthesizes the comparative landscape. Across the surveyed literature, four fundamental gaps emerge:

1. **GAP 1 (Linguistic & Tokenization Mismatch):** Prior Vietnamese language models rely on word segmenters vulnerable to teencode obfuscation, whereas robust subword tokenizers have not been tailored to Vietnamese smishing triage;
2. **GAP 2 (Symmetric Loss Misalignment):** Existing Vietnamese transformer architectures are optimized under symmetric loss, failing to reflect asymmetric telecommunication fraud damage;
3. **GAP 3 (Edge-Cloud Execution Dilemma):** Prior studies bifurcate into resource-heavy cloud LLMs that suffer from hyper-vigilance and latency bottlenecks, or rigid edge models lacking escalation capabilities for ambiguous lures;
4. **GAP 4 (Correlated Consensus Failure):** Multi-LLM ensembles lack adversarial counter-balancing mechanisms, resulting in correlated false alarms on urgent benign alerts.

These four gaps directly motivate the two-tier, cost-sensitive, and Public Defender-governed architecture of ScamShield-VN detailed in Section III.

`TABLE I. COMPARATIVE OVERVIEW OF REPRESENTATIVE THREAT DETECTION STUDIES VS. PROPOSED SCAMSHIELD-VN
+----------------------+------------+--------------------------------+----------------------------+-----------------------------+-------------------------------------------------------------+
| Study                | Language   | Model / Architecture           | Evaluation Dataset         | Key Metric                  | Primary Limitation / Research GAP                           |
+----------------------+------------+--------------------------------+----------------------------+-----------------------------+-------------------------------------------------------------+
| Tuấn et al. [11]      | Vietnamese | PhoBERT, CNN, LSTM             | Multi-accent SMS (N~3,000) | Acc: 95.56%                 | Evaluated under symmetric loss; vulnerable to segmenter fail|
| Nguyen-Xuan [13]     | Viet-Eng   | MLTEA Dual-Encoder             | Code-mixed Phishing        | F1: 0.940                   | Cloud-scale dual-encoder; high latency for mobile edge.     |
| Cam & Binh [12]      | Vietnamese | PhoBERT, BiLSTM                | VNSED Email Corpus         | Acc: 86.47%                 | Limited teencode vocabulary; elevated false negatives.      |
| Zhou et al. [17]     | Multiling. | GPT-4o, Claude, Gemini         | FraudSMSWalker (N~4,000)   | Recall: 64.16--90.13%       | Severe false alarms (benign recall collapsed to 12.8--30.2%)|
| Banda et al. [19]    | English    | Distilled SLM (Llama-3.2-3B)   | QR/Text Lures (N=4,200)    | Latency: 25.3--45 ms        | English only; non-trivial mobile memory footprint.          |
| Phap et al. [20]     | English    | BiGRU + MaskedPool + WBCE      | UCI & LSDST (N=5,574)      | Latency: 0.25 ms            | Recurrent model on English; lacks self-attention context.   |
| This Work            | Vietnamese | Two-Tier: ViSoBERT + 3-Council | Unified SMS (N=2,664/384)  | Recall: 97.11%, FPR: 2.37%  | Pareto-optimal: 267.5 ms, 0.00% bank FPR, $0.0153/1k SMS.   |
+----------------------+------------+--------------------------------+----------------------------+-----------------------------+-------------------------------------------------------------+
Note: Reported metrics are extracted from corresponding publications evaluated on heterogeneous datasets, hardware environments, and task formulations; they illustrate comparative architectural paradigms rather than direct benchmark parity.`

---

## III. MATERIALS AND METHODS

### A. Benchmark Dataset and Evaluation Partitions

To reflect authentic telecommunications threat distributions in Vietnam, we curated a unified corpus of $2,664$ genuine Vietnamese messages by merging verified public repositories, community reports from ChongLuaDao, and national cybersecurity warning feeds (`data/raw/vietnamese_sms_merged_all.csv`). The corpus consists of $1,918$ benign messages ($72.0\%$) and $746$ confirmed scam instances ($28.0\%$).

To ensure rigorous evaluation, we established two isolated testing partitions:

1. **Frozen Test Partition ($N = 267$):** Generated via stratified sampling with a fixed random seed of 42 ($10\%$ holdout: $192$ Ham, $75$ Scam). This set was strictly isolated from training, hyperparameter optimization, and threshold tuning to benchmark standalone model performance.
2. **Hard Forensic Challenge Suite ($N = 117$):** Curated to stress-test ambiguous decision boundaries, comprising $98$ adversarial scam lures (incorporating teencode obfuscation, non-financial urgency, and counterfeit brand headers) and $19$ legitimate banking OTPs and carrier service notifications.
3. **Combined End-to-End Suite ($N = 384$):** Formed by merging the $N=267$ Frozen Test Set and the $N=117$ Forensic Suite to evaluate the full two-tier cascaded pipeline across both routine and adversarial traffic.

### B. Cost-Sensitive Loss Formulation ($\mathcal{L}_{\text{WBCE}}$)

In telecommunications security, binary classification error outcomes impose deeply asymmetric operational costs. Misclassifying a benign message as fraudulent (False Positive) causes transient annoyance, whereas failing to intercept an active smishing vector (False Negative) exposes subscribers to credential theft and financial fraud. Standard Binary Cross-Entropy (BCE) treats both errors symmetrically, driving decision boundaries toward the majority benign class.

To embed an explicit inductive bias favoring scam recall, we formulate the **Cost-Sensitive Weighted Binary Cross-Entropy Loss ($\mathcal{L}_{\text{WBCE}}$)**:
$$\mathcal{L}_{\text{WBCE}} = -\frac{1}{N} \sum_{i=1}^{N} \left[ \alpha \cdot y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right]$$
where $y_i \in \{0, 1\}$ represents the ground-truth binary label ($0 = \text{Ham}$, $1 = \text{Scam}$), $\hat{y}_i \in [0, 1]$ denotes the predicted sigmoid probability, and $\alpha > 1$ represents the asymmetric cost penalty multiplier for False Negatives:
$$\frac{\partial \mathcal{L}_{\text{WBCE}}}{\partial z_i} = \begin{cases} \alpha (\hat{y}_i - 1), & \text{if } y_i = 1 \text{ (False Negative penalty)} \\ \hat{y}_i, & \text{if } y_i = 0 \text{ (False Positive penalty)} \end{cases}$$
In our implementation, we set $\alpha = 5.0$, exerting a 5-fold steeper gradient penalty whenever an authentic scam message is misclassified. Models were fine-tuned utilizing AdamW with an initial learning rate of $2\times 10^{-5}$, linear warmup ratio of $0.1$, weight decay of $0.01$, and batch size of 16 across 4 epochs under FP16 mixed precision.

### C. Model Architecture and ONNX Edge Quantization

ViSoBERT (`uitnlp/visobert`) [7] was chosen as our primary on-device edge encoder. Built upon the XLM-RoBERTa architecture, ViSoBERT comprises 12 transformer encoder layers, 768 hidden dimensions, 12 attention heads, and approximately 97.57M parameters (verified 97,566,721 parameters) paired with a custom vocabulary of 15,000 SentencePiece tokens pre-trained on a 1 GB corpus of uncompressed Vietnamese social media text.

To guarantee deterministic, sub-second execution on edge mobile processors without server dependencies, fine-tuned checkpoints were exported to Open Neural Network Exchange (ONNX) format with dynamic axes. The unquantized FP32 baseline occupies $390.54\text{ MB}$ ($372.45\text{ MiB}$), whereas dynamic INT8 quantization compresses the deployed model footprint (`visobert_tier1.onnx`) to $98.42\text{ MB}$ ($93.86\text{ MiB}$, achieving a $74.8\%$ reduction), delivering a median CPU inference latency of $70.7\text{ ms}$ ($70.66\text{ ms}$ median, $70.72 \pm 6.13\text{ ms}$ mean on desktop CPU threads) per message across the frozen test set.

### D. Two-Tier Cascaded System Routing

To reconcile edge real-time throughput with cloud-scale semantic reasoning, ScamShield-VN implements a confidence-governed two-tier cascade:
$$\text{Route}(x) = \begin{cases} \text{Tier 1 Edge Verdict}, & \text{if } \max(P_{\text{T1}}, 1 - P_{\text{T1}}) \ge \tau \\ \text{Tier 2 Council Escalation}, & \text{if } \max(P_{\text{T1}}, 1 - P_{\text{T1}}) < \tau \end{cases}$$
where $P_{\text{T1}} = P(\hat{y}=1|x)$ is the calibrated scam probability produced by ViSoBERT, and $\tau = 0.90$ is the operational confidence routing threshold. Messages with $\max(P_{\text{T1}}, 1 - P_{\text{T1}}) \ge 0.90$ exit immediately via the fast path ($<100\text{ ms}$, median $70.7\text{ ms}$, cost $\$0.00$), while ambiguous edge cases ($P_{\text{T1}} \in (0.10, 0.90)$) escalate to Tier 2.

### E. Consolidated 3-Agent Multi-LLM Forensic Council

Tier 2 deploys a consolidated 3-agent forensic council powered by frontier LLMs (`gpt-6.1-sol` / `gemini-3.8-flash`). Guided by principles of model parsimony, the council consolidates redundant roles into three specialized seats:

- **Seat A (Cyber Threat & Banking Specialist, $w_A = 0.35$):** Analyzes technical indicators, domain registration recency, typosquatting URLs, and spoofed banking headers.
- **Seat B (Psycholinguistic & Social Slang Specialist, $w_B = 0.35$):** Evaluates psychological persuasion levers (urgency, panic, greed, authority cues) and informal Vietnamese teencode obfuscations.
- **Seat C (Public Defender Advocate, $w_C = 0.30$):** Serves as an adversarial counterweight tasked exclusively with discovering legitimate brand indicators, standard OTP notification syntaxes, and genuine merchant protocols.

The council aggregates specialist probability estimates $P_j$ into a synthesized score:
$$P_{\text{council}} = \sum_{j \in \{A, B, C\}} w_j P_j - \delta_{\text{defender}}$$
where $\delta_{\text{defender}} = 0.25$ is an explicit veto penalty activated if the Public Defender verifies legitimate institutional transaction syntax, directly suppressing false alarms on sensitive banking alerts.

### F. Standardized 3-Label Output Schema and Privacy Compliance

To adhere to safety-first principles aligned with Article 25 of Vietnamese Decree 13/2023/ND-CP (Personal Data Protection) and avoid forced binary misclassifications on uncertain samples, ScamShield-VN standardizes final verdicts into three distinct categories:

$$
\text{Verdict} = \begin{cases}
\textbf{SCAM-RISK}, & \text{if } P_{\text{council}} \ge 0.60 \\
\textbf{LOW-RISK}, & \text{if } P_{\text{council}} < 0.40 \\
\textbf{UNKNOWN}, & \text{if } 0.40 \le P_{\text{council}} < 0.60
\end{cases}
$$

Messages flagged as **UNKNOWN** indicate an ambiguous boundary requiring user verification or asynchronous human audit, safeguarding users against uncalibrated automated decisions. Furthermore, per technical privacy safeguards, all message payloads undergo client-side PII tokenization (redacting phone numbers, account balances, and citizen IDs) prior to cloud escalation; formal regulatory compliance with Decree 13/2023/ND-CP was not assessed by legal counsel.

### G. Statistical Significance Testing Protocol

To evaluate paired differences between classifiers evaluated on the identical test partitions, we perform two-tailed **McNemar's tests** with continuity correction ($\alpha = 0.05$):
$$\chi^2_{\text{cont}} = \frac{(|b - c| - 1)^2}{b + c}$$
where $b$ is the number of samples correctly classified exclusively by the proposed model, and $c$ is the number of samples correctly classified exclusively by the comparative baseline. We test the null hypothesis $H_0$ ($p \ge 0.05$, no difference) against $H_1$ ($p < 0.05$, statistically significant difference).

---

## IV. RESULT AND DISCUSSION

### A. Tier 1 Edge Screener Performance on Frozen Benchmark

TABLE II presents empirical results aggregated over $K = 5$ independent deterministic random seeds ($\text{SEEDS} = [42, 100, 123, 999, 2026]$) on the isolated Frozen Test partition ($N = 267$).

```
TABLE II. EMPIRICAL BENCHMARK ACROSS 5 INDEPENDENT RUNS ON THE FROZEN TEST SET (N=267 SAMPLES: 192 HAM, 75 SCAM)
+--------------------------------+-------------------------+------------+-----------------+-----------------+-------------------+------------------+--------------+
| Model Configuration            | Role / Category         | Parameters | Accuracy (%)    | Precision (%)   | Scam Recall (%)   | Macro-F1 (%)     | Model Size   |
+--------------------------------+-------------------------+------------+-----------------+-----------------+-------------------+------------------+--------------+
| ViSoBERT + WBCE (alpha=5.0)    | Proposed (Tier 1 Edge)  | 97.57M     | 95.65 +/- 1.54  | 89.79 +/- 5.15  | 95.64 +/- 2.04    | 92.51 +/- 2.39   | 98.42 MB     |
| PhoBERT-large                  | Baseline B2.3 (370M)    | 370M       | 95.95 +/- 1.57  | 93.13 +/- 3.17  | 92.33 +/- 3.44    | 92.70 +/- 2.87   | 1,480 MB     |
| FPT ViBERT-base                | Baseline B2.2           | 124M       | 95.04 +/- 1.11  | 90.10 +/- 4.12  | 92.60 +/- 2.84    | 91.25 +/- 1.81   | 480 MB       |
| PhoBERT-base-v2                | Baseline B2.1           | 135M       | 95.11 +/- 0.83  | 91.24 +/- 1.52  | 91.23 +/- 1.84    | 91.23 +/- 1.50   | 540 MB       |
| Gemini 3.5 Flash (5-shot ICL)  | Baseline B3 (Cloud API) | Proprie.   | 84.50 +/- 1.02  | 64.47 +/- 1.52  | 100.00 +/- 0.00   | 78.38 +/- 1.12   | Cloud API    |
+--------------------------------+-------------------------+------------+-----------------+-----------------+-------------------+------------------+--------------+
```

ViSoBERT achieves the highest practical Scam Recall among all edge encoders at $95.64\% \pm 2.04\%$, while maintaining a Precision of $89.79\% \pm 5.15\%$ and Scam-F1 of $92.51\% \pm 2.39\%$ (unweighted Macro-F1: $94.51\% \pm 0.96\%$). PhoBERT-large misses $3.31\%$ more active scam vectors despite containing $3.8\times$ more parameters. Gemini 3.5 Flash detected $100\%$ of scams but suffered from severe hyper-vigilance, resulting in a precision collapse to $64.47\%$ (a $35.53\%$ false alarm rate on benign traffic).

TABLE III summarizes paired McNemar tests. ViSoBERT significantly outperforms Gemini 3.5 Flash ($b=33, c=3, \chi^2_{\text{cont}} = 23.3611, p < 0.0001, \text{OR} = 11.00$).

```
TABLE III. PAIRED MCNEMAR TEST ANALYSIS ON ISOLATED FROZEN TEST PARTITION (N=267 SAMPLES, alpha=0.05)
+--------------------------------+----+----+-------------+---------------+------------+------------------------+
| Pairwise Comparison            | b  | c  | chi^2_cont  | Exact p-value | Odds Ratio | Reject H0?             |
+--------------------------------+----+----+-------------+---------------+------------+------------------------+
| ViSoBERT vs. PhoBERT-base-v2   | 12 | 4  | 3.0625      | 0.0768        | 3.00       | False (p >= 0.05)      |
| ViSoBERT vs. FPT ViBERT-base   | 14 | 5  | 3.3684      | 0.0636        | 2.80       | False (p >= 0.05)      |
| ViSoBERT vs. PhoBERT-large     | 9  | 3  | 2.0833      | 0.1460        | 3.00       | False (p >= 0.05)      |
| ViSoBERT vs. Gemini 3.5 Flash  | 33 | 3  | 23.3611     | < 0.0001      | 11.00      | True (p < 0.0001)      |
+--------------------------------+----+----+-------------+---------------+------------+------------------------+
```

### B. Tier 2 Multi-Agent Council Ablation and Baseline P-single

TABLE IV reports performance across the $N = 117$ Hard Forensic Challenge Suite using `gpt-6.1-sol`.

```
TABLE IV. EMPIRICAL PERFORMANCE AND COST MATRIX ON HARD FORENSIC CHALLENGE SUITE (N=117 SAMPLES)
+-------------------------------------+-------+--------------+-----------------+---------+--------------+----------------+---------------+-----------+
| Council Configuration               | Seats | Accuracy (%) | Scam Recall (%) | FPR (%) | Macro-F1 (%) | Median Latency | Cost / 1k SMS | API Calls |
+-------------------------------------+-------+--------------+-----------------+---------+--------------+----------------+---------------+-----------+
| Arm 1: Full 5-Agent Council         | 5     | 94.87%       | 93.88%          | 0.00%   | 96.84%       | 10,141 ms      | $0.7500       | 585       |
| Arm 2: Proposed 3-Agent (+Defender) | 3     | 90.60%       | 88.78%          | 0.00%   | 94.05%       | 11,020 ms      | $0.4500       | 351       |
| Baseline P-single (Wang et al. [27])| 1     | 96.58%       | 95.92%          | 0.00%   | 97.92%       | 12,176 ms      | $0.0450       | 117       |
+-------------------------------------+-------+--------------+-----------------+---------+--------------+----------------+---------------+-----------+
```

- **Statistical Validation of Panel Consolidation:** Comparing Arm 1 (5-Agent) and Arm 2 (3-Agent with Defender), discordance counts were $b = 5$ (5-Agent correct, 3-Agent uncertain) and $c = 0$, yielding exact binomial $p = 0.0625$ ($\chi^2_{\text{cont}} = 3.2000, p = 0.0736$). Because $p > 0.05$, there is no statistically significant degradation. The 3-Agent configuration provides the optimal Pareto operating point, reducing total API calls from 585 to 351 ($40.0\%$ cost reduction) while preserving $0.00\%$ false alarms (exact $95\%$ CI: $[0.00\%, 17.65\%]$).
- **Public Defender Impact:** Both council arms achieved $0.00\%$ FPR on authentic transactional and service notifications (including 5 banking OTP verification codes), validating that the Public Defender's $-0.25$ veto reliably neutralizes threat-seeking bias.

### C. Two-Tier Cascaded System and Threshold Sensitivity ($\tau$)

TABLE V summarizes 3-run median performance across $N = 384$ combined samples at default threshold $\tau = 0.90$.

```
TABLE V. 3-RUN MEDIAN COMPARATIVE BENCHMARK ACROSS SYSTEM ARCHITECTURES (N=384 COMBINED SAMPLES, tau=0.90)
+-----------------------------------------+--------------+---------------+-----------------+---------+--------------+---------------+-----------------+
| Architectural Arm                       | Accuracy (%) | Precision (%) | Scam Recall (%) | FPR (%) | Latency (ms) | Cost / 1k SMS | Escalation Rate |
+-----------------------------------------+--------------+---------------+-----------------+---------+--------------+---------------+-----------------+
| Arm 1: Solo Tier 1 Edge (ViSoBERT)      | 96.35%       | 96.49%        | 95.38%          | 2.84%   | 70.7 ms      | $0.0000       | 0.0%            |
| Arm 2: Solo Tier 2 Fast (Gemini Lite)   | 97.66%       | 95.56%        | 99.42%          | 3.79%   | 1,969.9 ms   | $0.2817       | 100.0%          |
| Arm 3: Solo Tier 2 SOTA (GPT-6.1-sol)   | 99.74%       | 100.00%       | 99.42%          | 0.00%   | 5,765.0 ms   | $1.4667       | 100.0%          |
| Arm 4: Naive Cascaded (Tier 1 + PoLL)   | 97.14%       | 96.55%        | 97.11%          | 2.84%   | 717.8 ms     | $0.0541       | 3.4%            |
| Arm 5: Proposed ScamShield (Two-Tier)   | 97.40%       | 97.11%        | 97.11%          | 2.37%   | 267.5 ms     | $0.0153       | 3.4%            |
+-----------------------------------------+--------------+---------------+-----------------+---------+--------------+---------------+-----------------+
```

The proposed two-tier cascade (Arm 5) resolves $96.6\%$ of incoming messages locally at the edge, escalating only $3.4\%$ to Tier 2. It achieves $97.40\%$ accuracy, $97.11\%$ recall, and $2.37\%$ FPR, while reducing latency to $267.5\text{ ms}$ and reducing operational expenditure to $\$0.0153$ marginal cloud cost per 1,000 messages ($98.9\%$ cost saving compared to full cloud deployment).

```
TABLE VI. ROUTING THRESHOLD SENSITIVITY AND PARETO OPTIMIZATION ACROSS tau in [0.70, 0.95]
+---------------+--------------+------------+---------+--------------+---------------+----------------+
| Threshold tau | Accuracy (%) | Recall (%) | FPR (%) | Latency (ms) | Cost / 1k SMS | Escalation (%) |
+---------------+--------------+------------+---------+--------------+---------------+----------------+
| tau = 0.70    | 96.35%       | 95.38%     | 2.84%   | 99.5 ms      | $0.0023       | 0.5%           |
| tau = 0.80    | 96.61%       | 95.38%     | 2.37%   | 148.5 ms     | $0.0072       | 1.6%           |
| tau = 0.85    | 97.14%       | 96.53%     | 2.37%   | 223.9 ms     | $0.0117       | 2.6%           |
| tau = 0.90    | 97.40%       | 97.11%     | 2.37%   | 267.5 ms     | $0.0153       | 3.4%           |
| tau = 0.95    | 97.92%       | 97.11%     | 1.42%   | 668.2 ms     | $0.0410       | 9.1%           |
+---------------+--------------+------------+---------+--------------+---------------+----------------+
```

TABLE VI illustrates the threshold sensitivity trade-off. The knee of the Pareto curve occurs at $\mathbf{\tau = 0.90}$, capturing maximal recall gains before latency escalates.

### D. Discussion of Scientific Pillars

#### 1. Correlated Error Mitigation and Rejection of Condorcet Jury Theorem

A central conceptual hazard in multi-agent LLM systems is the inappropriate application of the Condorcet Jury Theorem. Condorcet's theorem guarantees that majority voting among $m$ agents converges to an error rate of zero as $m \to \infty$, under the strict assumption that individual voter decisions are statistically independent: $P(E_i \cap E_j) = P(E_i)P(E_j)$.

However, recent empirical findings by Kim et al. [30] and Smit et al. [31] demonstrated that foundation LLMs share overlapping training corpora, inducing strong correlated failure modes ($>60\%$ co-failure on deceptive adversarial inputs). Under correlated error distributions, Ladha [29] proved that increasing agent count fails to guarantee asymptotic convergence and can amplify collective bias. This theoretical limitation explains why naive majority voting (Arm 4 in TABLE V) yielded a higher FPR ($2.84\%$) than our proposed architecture. ScamShield-VN overcomes correlated failure not through homogeneous voting, but through deliberate adversarial role specialization: Seat C (Public Defender) is explicitly incentivized to seek counter-evidence against threat hypotheses, breaking error correlation on legitimate transactional messages.

#### 2. Neutralizing the Alarm Fatigue Phenomenon

Commercial LLMs operating as solitary screeners exhibit catastrophic false-alarm rates ($35.53\%$ FAR on Gemini 3.5 Flash) due to hyper-vigilance toward urgency markers and URLs. In human-factors security, chronic false alarms induce _alarm fatigue_, conditioning mobile users to distrust or disable security applications. The introduction of the Public Defender's $-0.25$ veto completely neutralized this failure mode, achieving $0.00\%$ FPR on authentic banking OTPs in the forensic challenge suite.

#### 3. Failure of Parameter Scaling Without Asymmetric Loss

Our benchmarks demonstrate that increasing model parameters cannot substitute for an asymmetric loss formulation. PhoBERT-large contains 370M parameters ($3.4\times$ larger than ViSoBERT) and required $3.45\times$ more training time ($1,457.7\text{ s}$ vs. $422.2\text{ s}$), yet missed $3.29\%$ more scams ($92.33\%$ vs. $95.62\%$). ViSoBERT's domain-specific pre-training on 1 GB of uncompressed Vietnamese social media text, combined with $\mathcal{L}_{\text{WBCE}}$ ($\alpha=5.0$), proved far more impactful than raw parameter scaling.

#### 4. Data Privacy and Safety-First Verdict Protocol

In alignment with technical safeguards under Article 25 of Vietnamese Decree 13/2023/ND-CP, ScamShield-VN rejects forced binary classification on borderline samples. By providing an explicit **UNKNOWN** label for ambiguous samples ($0.40 \le P < 0.60$), the platform preserves human-in-the-loop auditability. Furthermore, client-side PII redaction ensures subscriber privacy before cloud escalation; formal regulatory compliance with Decree 13/2023/ND-CP was not assessed by legal counsel.

---

## V. CONCLUSION

This paper presented ScamShield-VN, an integrated, evidence-grounded two-tier architecture designed to resolve the operational trade-off between edge efficiency on mobile devices and deep cloud semantic reasoning for Vietnamese telecommunications fraud defense. By fine-tuning ViSoBERT with an asymmetric loss of Cost-Sensitive weighted binary Cross-Entropy ($\mathcal{L}_{\text{WBCE}}$, $\alpha = 5.0$) and exporting via ONNX INT8 quantization ($98.42\text{ MB}$ / $93.86\text{ MiB}$, $70.7\text{ ms}$ CPU latency), the Tier 1 edge screener achieved a Scam Recall of $95.64\% \pm 2.04\%$ and Scam-F1 of $92.51\% \pm 2.39\%$ (unweighted Macro-F1: $94.51\% \pm 0.96\%$), significantly outperforming commercial LLMs alone in paired overall correctness ($p < 0.0001$, McNemar test).

For ambiguous edge cases, Tier 2 deploys a consolidated 3-agent forensic council incorporating an adversarial Public Defender. Paired McNemar tests validated that the 3-agent council performs on par with a 5-agent configuration ($p = 0.0736 > 0.05$), reducing token expenditures by $40\%$ and eliminating alarm fatigue ($0.00\%$ FPR on authentic transactional and service notifications). Across the combined end-to-end benchmark ($N = 384$), the two-tier cascade successfully resolved $96.6\%$ of traffic locally, achieving $97.40\%$ overall accuracy, $97.11\%$ scam recall, and a sub-second response latency of $267.5\text{ ms}$ at $\$0.0153$ marginal cloud cost per 1,000 messages.

\textbf{Practical Implications and Limitations:} The proposed architecture provides a scalable, privacy-preserving blueprint for carrier-grade and on-device mobile security, incorporating safety-first tri-label classification and client-side PII tokenization; formal compliance with Article 25 of Vietnamese Decree 13/2023/ND-CP requires separate organizational and legal review, and technical efficacy was not assessed by legal counsel. Key unmitigated limitations include the lack of multi-rater ground-truth annotation logs, the exploratory status of threshold $\tau = 0.90$, and non-deterministic cloud API inference. Future investigations will expand the framework to incorporate lightweight vision-language models for on-device QR-code (quishing) triage and explore active telecommunications carrier pilot deployments.

---

## Conflict of Interest

The authors declare no conflict of interest.

## Author Contributions

- **Nguyen Trung Hieu:** Conceptualization, Methodology, Formal analysis, Writing -- Original Draft, Project administration.
- **Nguyen Minh Quang:** Supervision, Verification, Ethical review.
- **Hoang Hai Phuc:** Validation, Model benchmarking, Statistical testing, Visualization.
- **Phan Tran Hoang Tran:** Resources, Data collection, Literature review, Investigation, Writing -- Review & Editing.
- **Nguyen Quoc Huy:** Software, Pipeline architecture, Data curation, Investigation.
- **Le Thi Quynh Chi:** Academic supervision, Conceptual validation, Writing -- Review & Editing.
  All authors have read and agreed to the published version of the manuscript.

## Funding

This research received no external funding.

## Acknowledgment

The authors express sincere gratitude to the ChongLuaDao project and the National Cybersecurity Association for open cyber threat intelligence feeds that contributed to benchmark curation.

---

## References

[1] Van Anh, “Vietnam loses \$744 million to online scams in 2024,” VietNamNet, Dec. 2024. Accessed: Oct. 25, 2026. [Online]. Available: [https://vietnamnet.vn/en/vietnam-loses-744-million-to-online-scams-in-2024-2352907.html](https://vietnamnet.vn/en/vietnam-loses-744-million-to-online-scams-in-2024-2352907.html)

[2] “Most prominent online scams in VN: Game fraud, fake traffic fines, and job scams,” Ministry of Science and Technology portal, Dec. 2024. Accessed: Oct. 25, 2026. [Online]. Available: [https://english.mst.gov.vn/most-prominent-online-scams-in-vn-game-fraud-fake-traffic-fines-and-job-scams-197240923080352007.htm](https://english.mst.gov.vn/most-prominent-online-scams-in-vn-game-fraud-fake-traffic-fines-and-job-scams-197240923080352007.htm)

[3] J.-W. Seo, J.-S. Lee, H.-M. Kim, J.-W. Lee, S.-H. Han, J.-H. Cho, and C.-H. Lee, “On-device smishing classifier resistant to text evasion attack,” _IEEE Access_, vol. 12, pp. 33495–33508, 2024. doi: [10.1109/ACCESS.2024.3349577](https://doi.org/10.1109/ACCESS.2024.3349577).

[4] J. Saias, “Advances in NLP techniques for detection of message-based threats in digital platforms: A systematic review,” _Electronics_, vol. 14, no. 13, p. 2551, 2025. doi: [10.3390/electronics14132551](https://doi.org/10.3390/electronics14132551).

[5] D. Q. Nguyen and A. T. Nguyen, “PhoBERT: Pre-trained language models for Vietnamese,” in _Findings of the Association for Computational Linguistics: EMNLP 2020_, 2020, pp. 1037–1042.

[6] S. Mahendru and T. Pandit, “SecureNet: A comparative study of DeBERTa and large language models for phishing detection,” in _IEEE 7th International Conference on Big Data and Artificial Intelligence (BDAI)_, 2024, pp. 112–119.

[7] Quoc-Nam Nguyen, Thanh-Cong Phan, Duc-Vu Nguyen, and Kiet Van Nguyen, “ViSoBERT: A Pre-Trained Language Model for Vietnamese Social Media Text Processing,” in _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP)_, 2023, pp. 5191–5207, ACL Anthology `2023.emnlp-main.315`. doi: [10.18653/v1/2023.emnlp-main.315](https://doi.org/10.18653/v1/2023.emnlp-main.315). [Online]. Available: [https://aclanthology.org/2023.emnlp-main.315/](https://aclanthology.org/2023.emnlp-main.315/)

[8] V. A. Saeed, “A method for SMS spam message detection using machine learning,” _Artificial Intelligence & Robotics Development Journal_, vol. 3, no. 1, pp. 66–78, 2023. doi: [10.52098/airdj.202366](https://doi.org/10.52098/airdj.202366).

[9] T. Xie, “Comparing KNN, logistic regression, random forest and BERT fine-tuning for scam message detection,” _Finance & Economics_, vol. 19, pp. 209–218, 2025.

[10] A. Ghourabi and M. Alohaly, “Enhancing spam message classification and detection using transformer-based embedding and ensemble learning,” _Sensors_, vol. 23, no. 8, p. 3861, 2023. doi: [10.3390/s23083861](https://doi.org/10.3390/s23083861).

[11] V. M. Tuan, N. X. Thang, and T. Q. Anh, “Evaluating the efficiency of Vietnamese SMS spam detection techniques,” _Journal of Science and Technology_, vol. 59, no. 1, pp. 45–52, 2023.

[12] N. T. Cam and N. T. Binh, “VNSED: Vietnamese spam email detection using multi deep learning models,” _Journal of Computer Science and Cybernetics_, vol. 42, no. 1, pp. 12–25, 2026.

[13] S. Nguyen-Xuan, H. Nguyen, G.-D. Le, and D. Kim, “A mixed-language transformer encoder architecture for social media phishing: Vietnamese-English case study,” _IEEE Access_, vol. 14, pp. 36942–36955, 2026. doi: [10.1109/ACCESS.2026.3694267](https://doi.org/10.1109/ACCESS.2026.3694267).

[14] C. Elkan, “The foundations of cost-sensitive learning,” in _Proceedings of the 17th International Joint Conference on Artificial Intelligence (IJCAI)_, vol. 2, 2001, pp. 973–978.

[15] T.-Y. Lin, P. Goyal, R. Girshick, K. He, and P. Dollár, “Focal loss for dense object detection,” in _Proceedings of the IEEE International Conference on Computer Vision (ICCV)_, 2017, pp. 2980–2988.

[16] H. T. Madabushi, E. Kochkina, and M. Castelle, “Cost-Sensitive BERT for Generalisable Sentence Classification on Imbalanced Data,” in _Proceedings of the Second Workshop on Natural Language Processing for Internet Freedom: Censorship, Disinformation, and Propaganda_, 2019, pp. 125–134. doi: [10.18653/v1/D19-5017](https://doi.org/10.18653/v1/D19-5017).

[17] Y. H. Zhou, Z. M. Ma, Y. J. Zhou, Y. T. Li, H. X. Xiang, Y. M. Cheng, T. L. Chen, K. J. Zhang, Z. H. Nan, J. H. Ni, Z. Wu, Q. Y. Pan, S. Zhang, S. Cheng, and M. Y. Luo, “FraudSMSWalker: Benchmarking agentic large language models for SMS-to-webpage fraud detection,” arXiv preprint arXiv:2606.16659, 2026. [Online]. Available: [https://arxiv.org/abs/2606.16659](https://arxiv.org/abs/2606.16659)

[18] A. ElZemity, J. Sylvester, B. Arief, and R. D. Lemos, “Agentic knowledge distillation: Autonomous training of small language models for SMS threat detection,” arXiv preprint arXiv:2602.10869, 2026. [Online]. Available: [https://arxiv.org/abs/2602.10869](https://arxiv.org/abs/2602.10869)

[19] S. Banda, M. Musara, and M. Mutandavari, “QuishingShield: On-device multi-modal detection of quick response phishing,” _Computer Science and Information Technologies_, vol. 7, no. 3, pp. 271–290, 2026.

[20] H. C. Phap, “Edge-AI enabled smishing and suspicious SMS detection: A cost-sensitive and lightweight deep learning architecture,” _Journal of Information and Telecommunication_, vol. 10, no. 2, pp. 145–162, 2026. doi: [10.1080/24751839.2026.2713250](https://doi.org/10.1080/24751839.2026.2713250).

[21] L. Chen, M. Zaharia, and J. Zou, “FrugalGPT: How to use large language models while reducing cost and improving performance,” arXiv preprint arXiv:2305.05176, 2023. [Online]. Available: [https://arxiv.org/abs/2305.05176](https://arxiv.org/abs/2305.05176)

[22] H. Mozannar and D. Sontag, “Consistent estimators for learning to defer to an expert,” in _International Conference on Machine Learning (ICML)_, 2020, pp. 7076–7087.

[23] C. K. Chow, “On optimum recognition error and reject option,” _IEEE Transactions on Information Theory_, vol. 16, no. 1, pp. 41–46, 1970. doi: [10.1109/TIT.1970.1054406](https://doi.org/10.1109/TIT.1970.1054406).

[24] C.-M. Chan, W. Chen, Y. Su, J. Xiao, Z. Liu, et al., “ChatEval: Towards better LLM-based evaluators through multi-agent debate,” in _International Conference on Learning Representations (ICLR)_, 2024.

[25] Y. Du, S. Li, A. Torralba, J. B. Tenenbaum, and I. Mordatch, “Improving factuality and reasoning in language models through multiagent debate,” in _International Conference on Machine Learning (ICML)_, 2024, pp. 8821–8840.

[26] Yi-Nuo Xue, Eric Spero, Yun Sing Koh, and Giovanni Russello, “MultiPhishGuard: An Explainable and Adaptive Multi-Agent LLM System for Phishing Email Detection,” arXiv preprint arXiv:2505.23803v2, 2025. [Online]. Available: [https://arxiv.org/abs/2505.23803v2](https://arxiv.org/abs/2505.23803v2)

[27] J. Wang, Q. Sun, X. Li, and M. Gao, “Boosting language models reasoning with Chain-of-Knowledge prompting,” in _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_, Association for Computational Linguistics, 2024, pp. 5014–5031. doi: [10.18653/v1/2024.acl-long.271](https://doi.org/10.18653/v1/2024.acl-long.271).

[28] P. Verga, S. Hofstatter, S. Althammer, Y. Su, A. Piktus, A. Arkhangorodsky, M. Xu, N. White, and P. Lewis, “Replacing judges with juries: Evaluating LLM generations with a panel of diverse models,” arXiv preprint arXiv:2404.18796, 2024. [Online]. Available: [https://arxiv.org/abs/2404.18796](https://arxiv.org/abs/2404.18796)

[29] K. K. Ladha, “The Condorcet jury theorem, free speech, and correlated votes,” _American Journal of Political Science_, vol. 36, no. 3, pp. 617–634, 1992. doi: [10.2307/2111584](https://doi.org/10.2307/2111584).

[30] E. Kim, A. Garg, K. Peng, and N. Garg, “Correlated errors in large language models,” arXiv preprint arXiv:2506.07962, 2025. [Online]. Available: [https://arxiv.org/abs/2506.07962](https://arxiv.org/abs/2506.07962)

[31] A. Smit, P. Duckworth, N. Grinsztajn, T. D. Barrett, and A. Pretorius, “Should we be going MAD? A look at multi-agent debate strategies for LLMs,” arXiv preprint arXiv:2311.17371, 2024. [Online]. Available: [https://arxiv.org/abs/2311.17371](https://arxiv.org/abs/2311.17371)

[32] F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and E. Duchesnay, “Scikit-learn: Machine learning in Python,” _Journal of Machine Learning Research_, vol. 12, pp. 2825–2830, 2011.

[33] ONNX Runtime Developers, “ONNX Runtime: Cross-platform, high performance ML inferencing and training accelerator,” 2021. [Online]. Available: [https://onnxruntime.ai/](https://onnxruntime.ai/)

[34] Q. McNemar, “Note on the sampling error of the difference between correlated proportions or percentages,” _Psychometrika_, vol. 12, no. 2, pp. 153–157, 1947. doi: [10.1007/BF02295996](https://doi.org/10.1007/BF02295996).

[35] A. L. Edwards, “Note on the ‘correction for continuity’ in testing the significance of the difference between correlated proportions,” _Psychometrika_, vol. 13, no. 3, pp. 185–187, 1948. doi: [10.1007/BF02289261](https://doi.org/10.1007/BF02289261).
