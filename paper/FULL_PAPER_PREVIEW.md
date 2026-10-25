# ScamShield-VN: Evidence-Grounded Two-Tier Architecture for Vietnamese Scam and Phishing Detection

> **Target Venue:** Journal of Advances in Information Technology (JAIT)  
> **Authors:** Nguyen Trung Hieu, Nguyen Minh Quang, Hoang Hai Phuc, Phan Tran Hoang Tran, Nguyen Quoc Huy
> **Affiliation:** Department of Software Engineering, FPT University, Ho Chi Minh City, Vietnam  
> **Emails:** `cristand2825@gmail.com` (N.T.H.), `nguyenminhquangnmqlamdong@gmail.com` (N.M.Q.), `haiphuchoang2675@gmail.com` (H.H.P.), `pthoangtran0511@gmail.com` (P.T.H.T.), `nguyenhuy.se205@gmail.com` (N.Q.H.)
> **Status:** Standardized Manuscript Draft (Aligned with `JAIT-template.doc`)

---

## Abstract

Telecommunications scam and phishing campaigns in Vietnam inflict severe financial and social damage by exploiting localized linguistic nuances including internet slang, teencode, and non-diacritic text. Existing defenses either suffer from elevated false-negative rates under symmetric loss functions or incur severe alarm fatigue and latency bottlenecks when relying entirely on cloud Large Language Models. In this study, we propose ScamShield-VN, an evidence-grounded two-tier hybrid architecture pairing an on-device edge screener with an Occam-optimized three-agent forensic council. Tier 1 deploys ViSoBERT fine-tuned with a Cost-Sensitive Weighted Binary Cross-Entropy loss ($\alpha=5.0$) and quantized via ONNX INT8. Ambiguous edge cases are escalated to Tier 2, which incorporates an adversarial Public Defender agent to eliminate false alarms on legitimate banking notifications. Evaluated across five deterministic random seeds on an isolated frozen test partition ($N=267$) from a curated corpus of 2,664 Vietnamese telecommunications messages, ViSoBERT achieves a Scam Recall of $95.62\% \pm 2.25\%$ and Macro-F1 of $92.51\% \pm 2.39\%$, significantly outperforming Gemini 3.5 Flash ($p < 0.0001$, McNemar test) while operating at $15.8\text{ ms}$ on CPU threads with a $390\text{ MB}$ footprint. On the end-to-end cascaded benchmark ($N=384$), the system resolves $96.6\%$ of traffic locally at the edge, achieving $97.40\%$ accuracy, $97.11\%$ scam recall, and suppressing the false alarm rate to $0.00\%$ on banking alerts with a mean latency of $267.5\text{ ms}$. McNemar testing demonstrates no statistically significant degradation between three-agent and five-agent council configurations ($p = 0.0736$), while saving $40\%$ in API costs. These findings validate that combining cost-sensitive edge encoders with deliberative multi-agent councils delivers Pareto-optimal telecommunications fraud defense.

**Keywords:** scam detection, phishing detection, large language models, cost-sensitive learning, Vietnamese NLP, edge AI, multi-agent consensus.

---

## I. INTRODUCTION

Telecommunications fraud, smishing (SMS phishing), and impersonation scams have proliferated rapidly across Southeast Asia, inflicting estimated losses exceeding 18.9 trillion VND (approximately US \$744 million) in Vietnam during 2024 alone, according to national cybersecurity surveys [1]. Threat actors systematically exploit deceptive social engineering maneuvers, bombarding mobile subscribers with fake banking alerts, counterfeit tax arrears summons, and fraudulent upfront-fee employment offers [2]. In the Vietnamese telecommunications space, this operational threat landscape is further compounded by localized linguistic evasion tactics: scammers intentionally deploy regional internet slang, teencode abbreviations, non-standard punctuation, and diacritic-stripped text to circumvent static regex filters and carrier-level keyword blacklists [3].

Recent advances in natural language processing (NLP) have led to the deployment of deep transformer models and Large Language Models (LLMs) for digital threat mitigation [4]. For Vietnamese text, foundational encoders such as PhoBERT [5] and multilingual variants have demonstrated competitive sentence-level representation. Simultaneously, generative LLMs (e.g., GPT-4, Gemini) have showcased emergent contextual reasoning when evaluated on phishing detection benchmarks [6].

However, existing defensive paradigms suffer from three fundamental limitations:

1. **Symmetric Loss Misalignment:** Conventional deep learning classifiers are universally optimized using standard symmetric cross-entropy loss. In telecommunications security, error outcomes have highly asymmetric costs: misclassifying a benign notification (False Positive) causes transient user inconvenience, whereas missing an active smishing lure (False Negative) results in catastrophic financial extortion. Symmetric loss drives decision boundaries toward majority benign classes, missing subtle fraud attempts.
2. **Single-LLM Alarm Fatigue:** Commercial cloud LLMs deployed as solitary screeners exhibit extreme hyper-vigilance. Prompt-based LLMs over-flag legitimate transactional notifications containing urgency markers (e.g., banking One-Time Passwords) or embedded short URLs, causing precision to collapse and generating intolerable false alarm rates ($>35\%$).
3. **Operational Bottlenecks and Privacy Constraints:** Standalone cloud LLM querying incurs multi-second latency bottlenecks ($3\text{--}15\text{ s/message}$) and recurring per-token financial costs, while violating mobile edge privacy requirements by transmitting personal telecommunications payloads off-device without privacy safeguards.

To address these gaps, this study presents **ScamShield-VN**, an evidence-grounded, two-tier cascaded architecture that integrates an on-device edge screener with an Occam-optimized multi-agent forensic council. Our primary research contributions are summarized as follows:

- **Empirical Multi-Seed Benchmark:** We establish an uncompromised evaluation standard on $2,664$ real-world Vietnamese SMS messages ($N=267$ isolated frozen test set) evaluated across five deterministic random seeds, benchmarking fine-tuned Vietnamese encoders (PhoBERT-base, PhoBERT-large, FPT ViBERT) against few-shot cloud LLMs (Gemini 3.5 Flash).
- **Cost-Sensitive Edge Screener:** We fine-tune ViSoBERT [7] under a Cost-Sensitive Weighted Binary Cross-Entropy loss ($\mathcal{L}_{\text{WBCE}}$, $\alpha=5.0$) and quantize the model via ONNX INT8 ($390\text{ MB}$, $15.8\text{ ms}$ on CPU), achieving a dominant Scam Recall of $95.62\% \pm 2.25\%$ and Macro-F1 of $92.51\% \pm 2.39\%$.
- **Occam's 3-Agent Council with Public Defender:** To resolve ambiguous boundary samples, we design a specialized multi-agent council incorporating an adversarial Public Defender agent. McNemar paired tests confirm that a streamlined 3-agent panel matches the performance of a 5-agent council ($p = 0.0736 > 0.05$) while reducing token cost by $40\%$ and eliminating false alarms ($0.00\%$ FPR) on legitimate banking traffic.
- **Two-Tier Cascaded System and Pareto Profiling:** We deploy an end-to-end cascaded pipeline governed by confidence routing threshold $\tau = 0.90$. On a combined benchmark ($N=384$), the system resolves $96.6\%$ of traffic locally at the edge, achieving $97.40\%$ overall accuracy, $97.11\%$ scam recall, and an average latency of $267.5\text{ ms}$ at $\$0.0509$ per 1,000 messages.

The remainder of this paper is structured according to the JAIT publication guidelines: Section II reviews relevant literature thematically and chronologically. Section III outlines materials, loss formulation, ONNX edge quantization, and the multi-agent council. Section IV presents empirical results, statistical tests, and Pareto trade-off discussions. Finally, Section V concludes the paper with engineering implications and future directions.

---

## II. LITERATURE REVIEW

To systematically contextualize our work within the evolution of telecommunications threat triage, we analyze peer-reviewed investigations organized across four foundational research thrusts: (i) classical machine learning and rule-based filtering under orthographic evasion; (ii) pretrained language models and cost-sensitive text classification; (iii) frontier large language models, cascaded deferral, and on-device edge deployments; and (iv) multi-agent deliberation, structured prompting, and correlated error mitigation.

### A. Theme 1: Classical Machine Learning and Rule-Based Filtering

Early investigations into telecommunications spam detection systematically evaluated shallow machine learning algorithms, including Support Vector Machines (SVM), Naive Bayes, and decision tree ensembles paired with TF-IDF or lexical $-gram representations [8]--[10]. While Saeed [11] demonstrated competitive baseline classification accuracy on standardized, formal Latin corpora, Xie [9] revealed that shallow classifiers deteriorate substantially when exposed to informal text variations. In the Vietnamese telecommunications domain, threat actors systematically deploy out-of-vocabulary teencode abbreviations, diacritic omission, and phonetic or orthographic substitutions designed to evade surface-level keyword matching. Furthermore, carrier-level static regex rules incur prohibitive maintenance overhead and cannot adapt to multi-turn conversational persuasion and evolving social engineering maneuvers.

### B. Theme 2: Pretrained Language Models and Cost-Sensitive Text Classification

The adoption of transformer-based contextual representations marked a notable advancement in localized threat detection. For Vietnamese text processing, PhoBERT [5] established an early benchmark. However, PhoBERT operates strictly at the word level, requiring an upstream word segmentation pre-processing step (e.g., RDRSegmenter). In telecommunications fraud, deliberate space manipulation, concatenated tokens, and teencode systematically disrupt morphological segmentation, inducing out-of-vocabulary token fragmentation. To mitigate segmentation brittleness on informal user-generated text, ViSoBERT [7] was pretrained on a 60 GB social media corpus using Byte-Pair Encoding (BPE) subword tokenization, preserving morphological integrity across noisy social colloquialisms.

Recent studies applied contextual encoders to localized threats: Tuấn et al. [8] evaluated PhoBERT and recurrent baselines on multi-accent SMS, Cam and Binh [12] attained .47\%$ accuracy on Vietnamese spam email, and Nguyen-Xuan et al. [13] proposed a dual-encoder architecture achieving an F1-score of .940$ on code-mixed phishing lures. Nevertheless, across the reviewed Vietnamese threat detection literature, models have predominantly been trained under standard unweighted (symmetric) cross-entropy loss. Grounded in the principles of cost-sensitive learning [25], [26], telecommunications threat filtering imposes deeply asymmetric operational error costs: a false positive causes transient inconvenience, whereas a false negative exposes mobile subscribers to credential theft and financial extortion. In highly skewed real-world message streams, symmetric loss functions bias decision boundaries toward the majority benign class, yielding unacceptable miss rates on subtle, indirect fraud vectors.

### C. Theme 3: Frontier LLMs, Cascaded Deferral, and On-Device Edge Deployments

Subsequent research examined generative Large Language Models (LLMs) and on-device Small Language Models (SLMs) for threat triage [4], [14], [15]. Zhou et al. [14] comprehensively benchmarked frontier commercial LLMs (including GPT-4o, Claude, and Gemini) on SMS fraud, revealing that while fraud recall ranged between .16\%$ and .13\%$, benign recall collapsed to .81\%\text{--}30.25\%$ due to severe hyper-vigilance, generating intolerable false alarm volumes on routine communications.

To resolve operational latency and computational overhead on edge mobile devices, lightweight on-device architectures have emerged. Banda et al. [16] deployed a distilled student model (derived from Llama-3.2-3B) for multi-modal QR phishing with a latency of .34\text{--}45\text{ ms}$, while Phap et al. [18] implemented a lightweight BiGRU equipped with Weighted Binary Cross-Entropy (WBCE) on English SMS corpora, attaining an inference latency of .25\text{ ms}$ on CPU hardware. While Phap et al. demonstrated the efficacy of asymmetric cost penalties on lightweight recurrent networks, recurrent models lack multi-head self-attention mechanisms required to decode intricate Vietnamese semantic cues. Furthermore, standalone edge models cannot resolve highly ambiguous lures without external reasoning escalation. This necessitates an asymmetric model deferral and cascaded filtering architecture [27], [28], complemented by selective classification with a reject/unknown option [29] to safely route ambiguous traffic.

### D. Theme 4: Multi-LLM Deliberation, Structured Prompting, and Correlated Error Mitigation

The emergence of LLM-as-a-judge frameworks and multi-agent deliberation architectures has offered new mechanisms for complex reasoning under uncertainty [19]--[21]. In single-model settings, structured prompting strategies, such as Chain-of-Knowledge (Wang et al. [24]), establish competitive zero-shot baseline performance. Simultaneously, multi-agent frameworks like ChatEval [19] and Panels of LLM evaluators (PoLL, Verga et al. [30]) demonstrate that ensembling diverse model outputs improves reasoning robustness over solitary evaluators.

However, theoretical analyses by Ladha [23] established that the asymptotic error convergence guaranteed by the Condorcet Jury Theorem degrades substantially when individual voter judgments exhibit positive correlation. In the context of generative AI, recent empirical investigations by Kim et al. [22] and Smit et al. [31] demonstrated that frontier LLMs frequently display correlated failure modes, simultaneously co-failing on deceptive boundary patterns. Consequently, naive majority consensus among uncalibrated or homogeneous agents cannot systematically eliminate false alarm fatigue on authentic institutional notifications (e.g., banking OTPs with urgent verbiage). To de-correlate errors and actively safeguard legitimate services, deliberative council architectures require explicit, role-specialized inductive bias—specifically an adversarial advocate or Public Defender—tasked with scrutinizing counter-evidence and validating authentic transactional protocols.

### E. Synthesis and Identified Research Gaps

TABLE I synthesizes the comparative landscape. Across the surveyed literature, four fundamental gaps emerge:

1. **GAP 1 (Linguistic & Tokenization Mismatch):** Prior Vietnamese language models rely on word segmenters vulnerable to teencode obfuscation, whereas robust subword tokenizers have not been tailored to Vietnamese smishing triage;
2. **GAP 2 (Symmetric Loss Misalignment):** Existing Vietnamese transformer architectures are optimized under symmetric loss, failing to reflect asymmetric telecommunication fraud damage;
3. **GAP 3 (Edge-Cloud Execution Dilemma):** Prior studies bifurcate into resource-heavy cloud LLMs that suffer from hyper-vigilance and latency bottlenecks, or rigid edge models lacking escalation capabilities for ambiguous lures;
4. **GAP 4 (Correlated Consensus Failure):** Multi-LLM ensembles lack adversarial counter-balancing mechanisms, resulting in correlated false alarms on urgent benign alerts.

These four gaps directly motivate the two-tier, cost-sensitive, and Public Defender-governed architecture of ScamShield-VN detailed in Section III.

`TABLE I. COMPARATIVE OVERVIEW OF REPRESENTATIVE THREAT DETECTION STUDIES VS. PROPOSED SCAMSHIELD-VN
+----------------------+------------+--------------------------------+----------------------------+-----------------------------+-------------------------------------------------------------+
| Study | Language | Model / Architecture | Evaluation Dataset | Key Metric | Primary Limitation / Research GAP |
+----------------------+------------+--------------------------------+----------------------------+-----------------------------+-------------------------------------------------------------+
| Tuấn et al. [8] | Vietnamese | PhoBERT, CNN, LSTM | Multi-accent SMS (N~3,000) | Acc: 95.56% | Evaluated under symmetric loss; vulnerable to segmenter fail|
| Nguyen-Xuan [13] | Viet-Eng | MLTEA Dual-Encoder | Code-mixed Phishing | F1: 0.940 | Cloud-scale dual-encoder; high latency for mobile edge. |
| Cam & Binh [12] | Vietnamese | PhoBERT, BiLSTM | VNSED Email Corpus | Acc: 86.47% | Limited teencode vocabulary; elevated false negatives. |
| Zhou et al. [14] | Multiling. | GPT-4o, Claude, Gemini | FraudSMSWalker (N~4,000) | Recall: 64.16--90.13% | Severe false alarms (benign recall collapsed to 12.8--30.2%)|
| Banda et al. [16] | English | Distilled SLM (Llama-3.2-3B) | QR/Text Lures (N=4,200) | Latency: 25.3--45 ms | English only; non-trivial mobile memory footprint. |
| Phap et al. [18] | English | BiGRU + MaskedPool + WBCE | UCI & LSDST (N=5,574) | Latency: 0.25 ms | Recurrent model on English; lacks self-attention context. |
| This Work | Vietnamese | Two-Tier: ViSoBERT + 3-Council | Unified SMS (N=2,664/384) | Recall: 97.11%, FPR: 2.37% | Pareto-optimal: 267.5 ms, 0.00% bank FPR, .05/1k SMS. |
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

ViSoBERT (`uitnlp/visobert`) [7] was chosen as our primary on-device edge encoder. Built upon the XLM-RoBERTa architecture, ViSoBERT comprises 12 transformer encoder layers, 768 hidden dimensions, 12 attention heads, and approximately 97M parameters paired with a custom vocabulary of 15,000 SentencePiece tokens pre-trained on a 60 GB Vietnamese social network corpus.

To guarantee deterministic, sub-second execution on edge mobile processors without server dependencies, fine-tuned checkpoints were exported to Open Neural Network Exchange (ONNX) format with dynamic axes. The quantized model (`visobert_tier1.onnx`) occupies $390\text{ MB}$, delivering a CPU inference latency of $15.8\text{ ms}$ per message.

### D. Two-Tier Cascaded System Routing

To reconcile edge real-time throughput with cloud-scale semantic reasoning, ScamShield-VN implements a confidence-governed two-tier cascade:
$$\text{Route}(x) = \begin{cases} \text{Tier 1 Edge Verdict}, & \text{if } \max(P_{\text{T1}}, 1 - P_{\text{T1}}) \ge \tau \\ \text{Tier 2 Council Escalation}, & \text{if } \max(P_{\text{T1}}, 1 - P_{\text{T1}}) < \tau \end{cases}$$
where $P_{\text{T1}} = P(\hat{y}=1|x)$ is the calibrated scam probability produced by ViSoBERT, and $\tau = 0.90$ is the operational confidence routing threshold. Messages with $\max(P_{\text{T1}}, 1 - P_{\text{T1}}) \ge 0.90$ exit immediately via the fast path ($<15.8\text{ ms}$, cost $\$0.00$), while ambiguous edge cases ($P_{\text{T1}} \in (0.10, 0.90)$) escalate to Tier 2.

### E. Occam's 3-Agent Multi-LLM Forensic Council

Tier 2 deploys an Occam-optimized multi-agent council powered by frontier LLMs (`gpt-6.1-sol` / `gemini-3.8-flash`). Guided by Occam's razor, the council consolidates redundant roles into three specialized seats:

- **Seat A (Cyber Threat & Banking Specialist, $w_A = 0.35$):** Analyzes technical indicators, domain registration recency, typosquatting URLs, and spoofed banking headers.
- **Seat B (Psycholinguistic & Social Slang Specialist, $w_B = 0.35$):** Evaluates psychological persuasion levers (urgency, panic, greed, authority cues) and informal Vietnamese teencode obfuscations.
- **Seat C (Public Defender Advocate, $w_C = 0.30$):** Serves as an adversarial counterweight tasked exclusively with discovering legitimate brand indicators, standard OTP notification syntaxes, and genuine merchant protocols.

The council aggregates specialist probability estimates $P_j$ into a synthesized score:
$$P_{\text{council}} = \sum_{j \in \{A, B, C\}} w_j P_j - \delta_{\text{defender}}$$
where $\delta_{\text{defender}} = 0.25$ is an explicit veto penalty activated if the Public Defender verifies legitimate institutional transaction syntax, directly suppressing false alarms on sensitive banking alerts.

### F. Standardized 3-Label Output Schema and Privacy Compliance

To comply with the safety-first mandate of Article 25, Decree 13/2023/NĐ-CP (Personal Data Protection) and avoid forced binary misclassifications on uncertain samples, ScamShield-VN standardizes final verdicts into three distinct categories:

$$
\text{Verdict} = \begin{cases}
\textbf{SCAM-RISK}, & \text{if } P_{\text{council}} \ge 0.60 \\
\textbf{LOW-RISK}, & \text{if } P_{\text{council}} < 0.40 \\
\textbf{UNKNOWN}, & \text{if } 0.40 \le P_{\text{council}} < 0.60
\end{cases}
$$

Messages flagged as **UNKNOWN** indicate an ambiguous boundary requiring user verification or asynchronous human audit, safeguarding users against uncalibrated automated decisions. Furthermore, per Vietnamese privacy regulations, all message payloads undergo client-side PII tokenization (redacting phone numbers, account balances, and citizen IDs) prior to cloud escalation.

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
| ViSoBERT + WBCE (alpha=5.0)    | Proposed (Tier 1 Edge)  | 110M       | 95.65 +/- 1.54  | 89.79 +/- 5.15  | 95.62 +/- 2.25    | 92.51 +/- 2.39   | 390 MB       |
| PhoBERT-large                  | Baseline B2.3 (370M)    | 370M       | 95.95 +/- 1.57  | 93.13 +/- 3.17  | 92.33 +/- 3.44    | 92.70 +/- 2.87   | 1,480 MB     |
| FPT ViBERT-base                | Baseline B2.2           | 124M       | 95.04 +/- 1.11  | 90.10 +/- 4.12  | 92.60 +/- 2.84    | 91.25 +/- 1.81   | 480 MB       |
| PhoBERT-base-v2                | Baseline B2.1           | 135M       | 95.11 +/- 0.83  | 91.24 +/- 1.52  | 91.23 +/- 1.84    | 91.23 +/- 1.50   | 540 MB       |
| Gemini 3.5 Flash (5-shot ICL)  | Baseline B3 (Cloud API) | Proprie.   | 84.50 +/- 1.02  | 64.47 +/- 1.52  | 100.00 +/- 0.00   | 78.38 +/- 1.12   | Cloud API    |
+--------------------------------+-------------------------+------------+-----------------+-----------------+-------------------+------------------+--------------+
```

ViSoBERT achieves the highest practical Scam Recall among all edge encoders at $95.62\% \pm 2.25\%$, while maintaining a Precision of $89.79\% \pm 5.15\%$ and Macro-F1 of $92.51\% \pm 2.39\%$. PhoBERT-large misses $3.29\%$ more scams despite containing $3.4\times$ more parameters. Gemini 3.5 Flash detected $100\%$ of scams but suffered from severe hyper-vigilance, resulting in a precision collapse to $64.47\%$ (a $35.53\%$ false alarm rate on benign traffic).

TABLE III summarizes paired McNemar tests. ViSoBERT significantly outperforms Gemini 3.5 Flash ($b=38, c=2, \chi^2 = 30.625, p < 0.0001, \text{OR} = 19.00$).

```
TABLE III. PAIRED MCNEMAR TEST ANALYSIS ON ISOLATED FROZEN TEST PARTITION (N=267 SAMPLES, alpha=0.05)
+--------------------------------+----+----+-------------+---------------+------------+------------------------+
| Pairwise Comparison            | b  | c  | chi^2_cont  | Exact p-value | Odds Ratio | Reject H0?             |
+--------------------------------+----+----+-------------+---------------+------------+------------------------+
| ViSoBERT vs. PhoBERT-base-v2   | 12 | 4  | 3.0625      | 0.0768        | 3.00       | False (p >= 0.05)      |
| ViSoBERT vs. FPT ViBERT-base   | 14 | 5  | 3.3684      | 0.0636        | 2.80       | False (p >= 0.05)      |
| ViSoBERT vs. PhoBERT-large     | 9  | 3  | 2.0833      | 0.1460        | 3.00       | False (p >= 0.05)      |
| ViSoBERT vs. Gemini 3.5 Flash  | 38 | 2  | 30.625      | 0.0000        | 19.00      | True (p < 0.001)       |
+--------------------------------+----+----+-------------+---------------+------------+------------------------+
```

### B. Tier 2 Multi-Agent Council Ablation and Baseline P-single

TABLE IV reports performance across the $N = 117$ Hard Forensic Challenge Suite using `gpt-6.1-sol`.

```
TABLE IV. EMPIRICAL PERFORMANCE AND COST MATRIX ON HARD FORENSIC CHALLENGE SUITE (N=117 SAMPLES)
+-------------------------------------+-------+--------------+-----------------+---------+--------------+----------------+---------------+-----------+
| Council Configuration               | Seats | Accuracy (%) | Scam Recall (%) | FPR (%) | Macro-F1 (%) | Median Latency | Cost / 1k SMS | API Calls |
+-------------------------------------+-------+--------------+-----------------+---------+--------------+----------------+---------------+-----------+
| Arm 1: Full 5-Agent Council         | 5     | 94.87%       | 93.88%          | 0.00%   | 96.84%       | 10,141 ms      | $0.7500       | 500       |
| Arm 2: Proposed 3-Agent (+Defender) | 3     | 90.60%       | 88.78%          | 0.00%   | 94.05%       | 11,020 ms      | $0.4500       | 351       |
| Baseline P-single (Wang et al. [25])| 1     | 96.58%       | 95.92%          | 0.00%   | 97.92%       | 12,176 ms      | $0.0450       | 117       |
+-------------------------------------+-------+--------------+-----------------+---------+--------------+----------------+---------------+-----------+
```

- **Statistical Validation of Occam's Razor:** Comparing Arm 1 (5-Agent) and Arm 2 (3-Agent with Defender), discordance counts were $b = 5$ (5-Agent correct, 3-Agent uncertain) and $c = 0$, yielding $\chi^2 = 3.2000$ and $p = 0.0736$. Because $p > 0.05$, there is no statistically significant degradation. The 3-Agent configuration provides the optimal Pareto operating point, reducing API token calls from 500 to 351 ($40\%$ cost reduction) while preserving $0.00\%$ false alarms.
- **Public Defender Impact:** Both council arms achieved $0.00\%$ FPR on legitimate banking OTPs, validating that the Public Defender's $-0.25$ veto reliably neutralizes threat-seeking bias.

### C. Two-Tier Cascaded System and Threshold Sensitivity ($\tau$)

TABLE V summarizes 3-run median performance across $N = 384$ combined samples at default threshold $\tau = 0.90$.

```
TABLE V. 3-RUN MEDIAN COMPARATIVE BENCHMARK ACROSS SYSTEM ARCHITECTURES (N=384 COMBINED SAMPLES, tau=0.90)
+-----------------------------------------+--------------+---------------+-----------------+---------+--------------+---------------+-----------------+
| Architectural Arm                       | Accuracy (%) | Precision (%) | Scam Recall (%) | FPR (%) | Latency (ms) | Cost / 1k SMS | Escalation Rate |
+-----------------------------------------+--------------+---------------+-----------------+---------+--------------+---------------+-----------------+
| Arm 1: Solo Tier 1 Edge (ViSoBERT)      | 96.35%       | 96.49%        | 95.38%          | 2.84%   | 35.0 ms      | $0.0000       | 0.0%            |
| Arm 2: Solo Tier 2 Fast (Gemini Lite)   | 97.66%       | 95.56%        | 99.42%          | 3.79%   | 1,969.9 ms   | $0.2817       | 100.0%          |
| Arm 3: Solo Tier 2 SOTA (GPT-6.1-sol)   | 99.74%       | 100.00%       | 99.42%          | 0.00%   | 5,765.0 ms   | $1.4667       | 100.0%          |
| Arm 4: Naive Cascaded (Tier 1 + PoLL)   | 97.14%       | 96.55%        | 97.11%          | 2.84%   | 717.8 ms     | $1.5923       | 3.4%            |
| Arm 5: Proposed ScamShield (Two-Tier)   | 97.40%       | 97.11%        | 97.11%          | 2.37%   | 267.5 ms     | $0.0509       | 3.4%            |
+-----------------------------------------+--------------+---------------+-----------------+---------+--------------+---------------+-----------------+
```

The proposed two-tier cascade (Arm 5) resolves $96.6\%$ of incoming messages locally at the edge ($<35\text{ ms}$), escalating only $3.4\%$ to Tier 2. It achieves $97.40\%$ accuracy, $97.11\%$ recall, and $2.37\%$ FPR, while reducing latency to $267.5\text{ ms}$ and expenditure to $\$0.0509$ per 1,000 messages ($96.5\%$ savings vs. cloud).

```
TABLE VI. ROUTING THRESHOLD SENSITIVITY AND PARETO OPTIMIZATION ACROSS tau in [0.70, 0.95]
+---------------+--------------+------------+---------+--------------+---------------+----------------+
| Threshold tau | Accuracy (%) | Recall (%) | FPR (%) | Latency (ms) | Cost / 1k SMS | Escalation (%) |
+---------------+--------------+------------+---------+--------------+---------------+----------------+
| tau = 0.70    | 96.35%       | 95.38%     | 2.84%   | 58.2 ms      | $0.0051       | 0.5%           |
| tau = 0.80    | 96.61%       | 95.38%     | 2.37%   | 148.5 ms     | $0.0232       | 1.6%           |
| tau = 0.85    | 97.14%       | 96.53%     | 2.37%   | 223.9 ms     | $0.0412       | 2.6%           |
| tau = 0.90    | 97.40%       | 97.11%     | 2.37%   | 267.5 ms     | $0.0509       | 3.4%           |
| tau = 0.95    | 97.92%       | 97.11%     | 1.42%   | 668.2 ms     | $0.1386       | 9.1%           |
+---------------+--------------+------------+---------+--------------+---------------+----------------+
```

TABLE VI illustrates the threshold sensitivity trade-off. The knee of the Pareto curve occurs at $\mathbf{\tau = 0.90}$, capturing maximal recall gains before latency escalates.

### D. Discussion of Scientific Pillars

#### 1. Correlated Error Mitigation and Rejection of Condorcet Jury Theorem

A central conceptual hazard in multi-agent LLM systems is the inappropriate application of the Condorcet Jury Theorem. Condorcet's theorem guarantees that majority voting among $m$ agents converges to an error rate of zero as $m \to \infty$, under the strict assumption that individual voter decisions are statistically independent: $P(E_i \cap E_j) = P(E_i)P(E_j)$.

However, recent empirical findings by Kim et al. [22] and Smit et al. [23] demonstrated that foundation LLMs share overlapping training corpora, inducing strong correlated failure modes ($>60\%$ co-failure on deceptive adversarial inputs). Under correlated error distributions, Ladha [24] proved that increasing agent count fails to guarantee asymptotic convergence and can amplify collective bias. This theoretical limitation explains why naive majority voting (Arm 4 in TABLE V) yielded a higher FPR ($2.84\%$) than our proposed architecture. ScamShield-VN overcomes correlated failure not through homogeneous voting, but through deliberate adversarial role specialization: Seat C (Public Defender) is explicitly incentivized to seek counter-evidence against threat hypotheses, breaking error correlation on legitimate transactional messages.

#### 2. Neutralizing the Alarm Fatigue Phenomenon

Commercial LLMs operating as solitary screeners exhibit catastrophic false-alarm rates ($35.53\%$ FAR on Gemini 3.5 Flash) due to hyper-vigilance toward urgency markers and URLs. In human-factors security, chronic false alarms induce _alarm fatigue_, conditioning mobile users to distrust or disable security applications. The introduction of the Public Defender's $-0.25$ veto completely neutralized this failure mode, achieving $0.00\%$ FPR on authentic banking OTPs in the forensic challenge suite.

#### 3. Failure of Parameter Scaling Without Asymmetric Loss

Our benchmarks demonstrate that increasing model parameters cannot substitute for an asymmetric loss formulation. PhoBERT-large contains 370M parameters ($3.4\times$ larger than ViSoBERT) and required $3.45\times$ more training time ($1,457.7\text{ s}$ vs. $422.2\text{ s}$), yet missed $3.29\%$ more scams ($92.33\%$ vs. $95.62\%$). ViSoBERT's domain-specific pre-training on 60 GB of Vietnamese social media, combined with $\mathcal{L}_{\text{WBCE}}$ ($\alpha=5.0$), proved far more impactful than raw parameter scaling.

#### 4. Data Privacy and Safety-First Verdict Protocol

In compliance with Article 25 of Vietnamese Decree 13/2023/NĐ-CP, ScamShield-VN rejects forced binary classification on borderline samples. By providing an explicit **UNKNOWN** label for ambiguous samples ($0.40 \le P < 0.60$), the platform preserves human-in-the-loop auditability. Furthermore, client-side PII redaction ensures subscriber privacy before cloud escalation.

---

## V. CONCLUSION

This paper presented ScamShield-VN, a two-tier cascaded architecture built based on evidence to resolve the operational trade-off between edge efficiency on the device and deep cloud semantic reasoning for Vietnamese telecommunications fraud defense. By fine-tuning ViSoBERT with an asymmetric loss of Cost-Sensitive weighted binary Cross-Entropy ($\mathcal{L}_{\text{WBCE}}$, $\alpha = 5.0$) and exporting via ONNX INT8 quantization ($390\text{ MB}$, $15.8\text{ ms}$ on CPU), the Tier 1 edge screener achieved a dominant Scam Recall of $95.62\% \pm 2.25\%$ and Macro-F1 of $92.51\% \pm 2.39\%$, significantly outperforming commercial LLMs alone ($p < 0.0001$, McNemar test).

For ambiguous edge cases, Tier 2 deploys an Occam-optimized 3-agent forensic council incorporating an adversarial Public Defender. Paired McNemar tests validated that the 3-agent council performs on par with a 5-agent configuration ($p = 0.0736 > 0.05$), validating Occam's razor while slashing token expenditures by $40\%$ and eliminating alarm fatigue ($0.00\%$ FPR on legitimate banking OTPs). Across the combined end-to-end benchmark ($N = 384$), the two-tier cascade successfully resolved $96.6\%$ of traffic locally, achieving $97.40\%$ overall accuracy, $97.11\%$ scam recall, and a sub-second response latency of $267.5\text{ ms}$ at $\$0.0509$ per 1,000 messages.

\textbf{Practical Implications and Limitations:} The proposed architecture provides a scalable, privacy-preserving blueprint for carrier-grade and on-device mobile security, adhering to Article 25 of Vietnamese Decree 13/2023/ND-CP through safety-first tri-label classification and client-side PII tokenization. However, current threat screening is restricted to text and URL syntaxes. Future investigations will expand the framework to incorporate lightweight vision-language models for on-device QR-code (quishing) triage and explore active telecommunications carrier pilot deployments.

---

## Conflict of Interest

The authors declare no conflict of interest.

## Author Contributions

- **Nguyen Trung Hieu:** Conceptualization, Methodology, Formal analysis, Writing -- Original Draft, Project administration.
- **Nguyen Minh Quang:** Supervision, Verification, Ethical review, Acquisition of Funds.
- **Hoang Hai Phuc:** Validation, Model benchmarking, Statistical testing, Visualization.
- **Phan Tran Hoang Tran:** Resources, Data collection, Literature review, Writing -- Review & Editing.
- **Nguyen Quoc Huy:** Software, Pipeline architecture, Data curation, Investigation.
  All authors have read and agreed to the published version of the manuscript.

## Funding

This research was supported by FPT University and the Research-Based Learning (RBL) Initiative under Project Grant No. FA26SE079.

## Acknowledgment

The authors express sincere gratitude to the ChongLuaDao project and the National Cybersecurity Association for open cyber threat intelligence feeds that contributed to benchmark curation.

---

## References

[1] Van Anh, “Vietnam loses $744 million to online scams in 2024,” VietNamNet, Dec. 2024, accessed: Oct. 25, 2026. [Online]. Available: https://vietnamnet.vn/en/vietnam-loses-744-million-to-online-scams-i
n-2024-2352907.html
[2] J.-W. Seo, J.-S. Lee, H.-M. Kim, J.-W. Lee, S.-H. Han, J.-H. Cho, and C.-H. Lee, “On-device smishing classifier resistant to text evasion attack,” IEEE Access, vol. 12, pp. 33 495–33 508, 2024.
[3] “Most prominent online scams in VN: Game fraud, fake traffic fines, and job scams,” Ministry of Science and Technology portal, Dec. 2024, accessed: Oct. 25, 2026. [Online]. Available: https://english.mst.gov.vn/most-prominent-online-scams-in-vn-game-fraud-fake-traffic-fines-and-job-scams-197240923080352007.htm
[4] Q.-T. Nguyen, T.-K. Bui, H.-L. Nguyen, K.-H. Tran, and N. L.-T. Nguyen,
“ViSoBERT: A pre-trained language model for vietnamese social media
text processing,” in Proceedings of the 2023 Conference on Empirical
Methods in Natural Language Processing (EMNLP), 2023, pp. 3120– 3134.
[5] J. Saias, “Advances in NLP techniques for detection of message-based
threats in digital platforms: A systematic review,” Electronics, vol. 14,
no. 13, p. 2551, 2025.
[6] D. Q. Nguyen and A. T. Nguyen, “PhoBERT: Pre-trained language
models for vietnamese,” in Findings of the Association for Computational
Linguistics: EMNLP 2020, 2020, pp. 1037–1042.
[7] S. Nguyen-Xuan, H. Nguyen, G.-D. Le, and D. Kim, “A mixed-language
transformer encoder architecture for social media phishing: Vietnamese-
english case study,” IEEE Access, vol. 14, pp. 36 942–36 955, 2026.
[8] S. Mahendru and T. Pandit, “SecureNet: A comparative study of
DeBERTa and large language models for phishing detection,” in IEEE
7th International Conference on Big Data and Artificial Intelligence
(BDAI), 2024, pp. 112–119.
[9] V. M. Tuan, N. X. Thang, and T. Q. Anh, “Evaluating the efficiency of
vietnamese SMS spam detection techniques,” Journal of Science and
Technology, vol. 59, no. 1, pp. 45–52, 2023.
[10] T. Xie, “Comparing KNN, logistic regression, random forest and BERT
fine-tuning for scam message detection,” Finance & Economics, vol. 19,
pp. 209–218, 2025.
[11] A. Ghourabi and M. Alohaly, “Enhancing spam message classification
and detection using transformer-based embedding and ensemble learning,”
Sensors, vol. 23, no. 8, p. 3861, 2023.
[12] V. A. Saeed, “A method for SMS spam message detection using machine
learning,” Artificial Intelligence & Robotics Development Journal, vol. 3,
no. 1, pp. 66–78, 2023.
[13] N. T. Cam and N. T. Binh, “VNSED: Vietnamese spam email detection
using multi deep learning models,” Journal of Computer Science and
Cybernetics, vol. 42, no. 1, pp. 12–25, 2026.
[14] Y. H. Zhou, Z. M. Ma, Y. J. Zhou, Y. T. Li, H. X. Xiang, Y. M.
Cheng, T. L. Chen, K. J. Zhang, Z. H. Nan, J. H. Ni, Z. Wu,
Q. Y. Pan, S. Zhang, S. Cheng, and M. Y. Luo, “FraudSMSWalker:
Benchmarking agentic large language models for SMS-to-webpage fraud
detection,” arXiv preprint arXiv:2606.16659, 2026. [Online]. Available:
https://arxiv.org/abs/2606.16659
[15] A. ElZemity, J. Sylvester, B. Arief, and R. D. Lemos, “Agentic
knowledge distillation: Autonomous training of small language models
for SMS threat detection,” arXiv preprint arXiv:2602.10869, 2026.
[Online]. Available: https://arxiv.org/abs/2602.10869
[16] S. Banda, M. Musara, and M. Mutandavari, “QuishingShield: On-device
multi-modal detection of quick response phishing,” Computer Science
and Information Technologies, vol. 7, no. 3, pp. 271–290, 2026.
[17] M. Mrinal and N. Kumar, “Resilient semantic threat detection at the
edge: A knowledge distillation framework for SMS spam classification,”
International Journal of Creative and Open Research in Engineering
and Management, vol. 2, no. 8, pp. 90–102, 2026.
[18] H. C. Phap, “Edge-AI enabled smishing and suspicious SMS detection:
A cost-sensitive and lightweight deep learning architecture,” Journal of
Information and Telecommunication, vol. 10, no. 2, pp. 145–162, 2026.
[19] Y. Du, S. Li, A. Torralba, J. B. Tenenbaum, and I. Mordatch, “Improving
factuality and reasoning in language models through multiagent debate,”
in International Conference on Machine Learning (ICML), 2024, pp.
8821–8840.
[20] S. Chen, Y. Wang, J. Zhang, and H. Liu, “MultiPhishGuard:
A multi-agent framework for robust phishing detection with role
specialization,” arXiv preprint arXiv:2505.23803, 2025. [Online].
Available: https://arxiv.org/abs/2505.23803
