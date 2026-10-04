# 🎯 CLAIMS, EVIDENCE & WARRANT MAPPING (RBL-4 / RBL-5)
### Project: ScamShield-VN — Evidence-Grounded Vietnamese Scam & Phishing Detection Platform
> **File:** `paper/claims.md`  
> **Purpose:** Trace every academic claim in the manuscript back to exact empirical evidence and logical warrants.

---

## Claim 1: Superiority of Cost-Sensitive Objective on Edge Encoders
* **Claim:** ViSoBERT fine-tuned with Cost-Sensitive Weighted Binary Cross-Entropy Loss ($\mathcal{L}_{\text{WBCE}}$, $\alpha=5.0$) achieves the highest practical Scam Recall ($95.62\% \pm 2.25\%$) among all deployable edge neural models on Vietnamese SMS data.
* **Evidence:** Table 1 (`results/summary.csv`):
  * ViSoBERT: Scam Recall $95.62\% \pm 2.25\%$, Macro-F1 $92.51\% \pm 2.39\%$.
  * PhoBERT-large: Scam Recall $92.33\% \pm 3.44\%$, Macro-F1 $92.70\% \pm 2.87\%$.
  * FPT ViBERT-base: Scam Recall $92.60\% \pm 2.84\%$, Macro-F1 $91.25\% \pm 1.81\%$.
  * PhoBERT-base-v2: Scam Recall $91.23\% \pm 1.84\%$, Macro-F1 $91.23\% \pm 1.50\%$.
* **Warrant:** The $\alpha=5.0$ multiplier forces the backpropagation gradient to apply a $5\times$ steeper penalty for false negatives (missed scams). On an isolated, frozen evaluation split of $N=267$ messages ($75$ scam, $192$ benign) evaluated over 5 distinct random seeds (`[42, 100, 123, 999, 2026]`), ViSoBERT missed fewer scams than all comparative edge encoders.

---

## Claim 2: Statistically Significant Outperformance over Single Cloud LLM
* **Claim:** The proposed on-device ViSoBERT significantly outperforms few-shot Gemini 3.5 Flash on overall binary classification reliability ($p < 0.0001$, McNemar paired test).
* **Evidence:** Table 2 (`results/mcnemar_analysis.csv`):
  * ViSoBERT vs. Gemini 3.5 Flash: $b = 38$ (samples where ViSoBERT was correct and Gemini failed), $c = 2$ (samples where Gemini was correct and ViSoBERT failed).
  * Continuity-corrected $\chi^2 = 30.625$, exact two-tailed $p$-value $= 0.0000$, Odds Ratio $= 19.00$.
* **Warrant:** Although Gemini 3.5 Flash captured $100\%$ of scams, its Precision collapsed to $64.47\% \pm 1.52\%$ due to hyper-vigilant over-flagging of benign transactional SMS (misclassifying $35.53\%$ of benign traffic), causing overall accuracy to drop to $84.50\% \pm 1.02\%$.

---

## Claim 3: Pareto-Optimality of Edge Architecture over Model Scaling
* **Claim:** Sheer parameter scaling without cost-sensitive weighting fails to compensate for asymmetric risk, making ViSoBERT Pareto-optimal in accuracy, memory footprint, and CPU latency.
* **Evidence:** 
  * PhoBERT-large contains 370M parameters, occupies $1,480\text{ MB}$, and requires $1,457.7\text{ s}$ training time, yet misses $3.29\%$ more scams (Recall $92.33\%$ vs. $95.62\%$).
  * ViSoBERT INT8 ONNX occupies $390\text{ MB}$ ($3.8\times$ smaller) and infers at $15.8\text{ ms/msg}$ on consumer CPU threads ($326\times$ faster than Gemini API at $4,912\text{ ms/msg}$).
* **Warrant:** Pre-training on 60 GB of Vietnamese social media text provides superior tokenization for teencode and slang, which when combined with asymmetric loss optimization achieves better risk sensitivity than massive general-domain encoders.

---

## Claim 4: Scientific Motivation for Two-Tier Architecture and 5-Agent Council
* **Claim:** A single-LLM cloud detector creates unacceptable alarm fatigue; routing ambiguous edge cases ($P < 0.90$) to a 5-Agent Council featuring an active Public Defender / Devil's Advocate resolves this failure mode.
* **Evidence:** 
  * Empirical failure mode of Baseline B3 (Gemini 3.5 Flash false-positive rate $= 35.53\%$).
  * Proposal Amendment v1.1 citing MultiPhishGuard (Chen et al., 2025: FPR reduced from $19.8\%$ to $2.73\%$) and PoLL (Verga et al., 2024: $7\times$ cost reduction and bias neutralization).
* **Warrant:** Separating the defensive role into specialized personas—especially a designated validator tasked with identifying genuine corporate banking patterns—restores high precision while preserving high recall.
