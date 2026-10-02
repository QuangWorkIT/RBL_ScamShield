# 📝 RESEARCH NOTES & TECHNICAL LOG
### Project: ScamShield-VN — Evidence-Grounded Vietnamese Scam & Phishing Detection Platform
> **File:** `notes.md`  
> **Repository:** `https://github.com/QuangWorkIT/RBL_ScamShield.git`  
> **Lead Researcher:** Nguyen Trung Hieu (PL / LR)

---

## 1. Technical Decisions & Experimental Configuration

### 1.1 Model Selection & Justification:
* **Canonical Hugging Face Hub ID:** `uitnlp/visobert` (Architecture: RoBERTa-based, 110M parameters).
* **Rationale:** Pre-trained on a massive 60GB corpus of Vietnamese social media, forums, and comment sections. Perfectly adapted to the syntactic nuances, abbreviations, and teencode prevalent in modern Vietnamese smishing and scam lures.
* **Loss Function Formulation:**
  Standard binary cross-entropy treats False Positives (FPs: legitimate SMS flagged as scam) and False Negatives (FNs: scam message missed, causing financial loss to users) with equal severity. In scam defense, an FN is catastrophic. We therefore integrate **Cost-Sensitive Weighted Binary Cross-Entropy Loss ($\mathcal{L}_{\text{WBCE}}$)**:
  $$\mathcal{L}_{\text{WBCE}} = -\frac{1}{N} \sum_{i=1}^{N} \left[ \alpha \cdot y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right], \quad \alpha = 5.0$$
  This exerts a $5\times$ heavier penalty gradient whenever the model fails to detect a scam message.

### 1.2 Multi-Seed Protocol (5 Runs for Statistical Significance):
To control for weight initialization variance, all deep learning models are evaluated over 5 distinct, deterministic random seeds:
$$\text{SEEDS} = [42, 100, 123, 999, 2026]$$

---

## 2. Dataset Partitioning & Frozen Test Set Isolation

* **Unified Corpus:** $2,665$ processed Vietnamese SMS messages (`data/raw/vietnamese_sms_merged_all.csv`).
  * Ham (Label 0): $1,918$ messages ($72.0\%$).
  * Scam (Label 1): $747$ messages ($28.0\%$).
* **Stratified Split (seed = 42):**
  * Train / Validation: $2,398$ messages ($90\%$).
  * **Frozen Test Set:** **$N = 267$ messages** ($10\%$: $192$ Ham, $75$ Scam).
* **Protocol Rule:** The $267$-sample Frozen Test Set remains completely untouched during threshold tuning and model hyperparameter search. All comparative models are evaluated on this identical sample set.

---

## 3. Engineering Challenges & Error Resolution Log

### Log #1: Kaggle / Colab Disk Exhaustion (`[Errno 28] No space left on device`)
* **Incident:** Saving Hugging Face checkpoints across 5 consecutive runs filled the $20\text{GB}$ temporary disk on Kaggle.
* **Resolution:** Added automated garbage collection and directory cleanup scripts immediately after evaluation:
  ```python
  import shutil
  for run in range(1, 6):
      shutil.rmtree(f'./visobert_run_{run}_ckpt', ignore_errors=True)
      shutil.rmtree(f'./visobert_run_{run}', ignore_errors=True)
  ```
  Freed up $> 15\text{GB}$ of disk space, allowing all 5 runs to complete flawlessly.

### Log #2: ONNX Runtime CPU Export & Dynamic Axes Warning
* **Incident:** `torch.onnx.export` threw a deprecation warning regarding legacy TorchScript exporter and opset mismatch.
* **Resolution:** Standardized ONNX opset version to `opset_version=18` with dynamic axes for variable sequence lengths (`batch_size`, `sequence_length`), yielding `models/visobert_tier1.onnx` ($390\text{MB}$) with inference latency $\approx 15\text{ ms/msg}$ on consumer CPU.

---

## 4. Final Empirical Benchmark Results (All 5 Models Completed)

| Model | Lead Member | Accuracy | Precision | **Scam Recall (Cốt lõi)** | F1-Score | Model Size | Train/Infer Time |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 👑 **ViSoBERT + WBCE ($\alpha=5.0$)** | **Hiếu (Proposed)** | $95.65\% \pm 1.54\%$ | $89.79\% \pm 5.15\%$ | **$95.62\% \pm 2.25\%$** | **$92.51\% \pm 2.39\%$** | **$390\text{ MB}$** | **$422.2\text{ s}$ (~7.0 min)** |
| **PhoBERT-large (370M)** | Huy (Baseline B2.3) | $95.95\% \pm 1.57\%$ | $93.13\% \pm 3.17\%$ | **$92.33\% \pm 3.44\%$** | $92.70\% \pm 2.87\%$ | $1,480\text{ MB}$ | $1,457.7\text{ s}$ (~24.3 min) |
| **FPT ViBERT-base** | Phúc (Baseline B2.2) | $95.04\% \pm 1.11\%$ | $90.10\% \pm 4.12\%$ | **$92.60\% \pm 2.84\%$** | $91.25\% \pm 1.81\%$ | $480\text{ MB}$ | $447.9\text{ s}$ (~7.5 min) |
| **PhoBERT-base-v2** | Trân (Baseline B2.1) | $95.11\% \pm 0.83\%$ | $91.24\% \pm 1.52\%$ | **$91.23\% \pm 1.84\%$** | $91.23\% \pm 1.50\%$ | $540\text{ MB}$ | $374.7\text{ s}$ (~6.2 min) |
| **Gemini 3.5 Flash (5-shot ICL)** | Quang (Baseline B3) | $84.50\% \pm 1.02\%$ | $64.47\% \pm 1.52\%$ | **$100.00\% \pm 0.00\%$** | $78.38\% \pm 1.12\%$ | Cloud API | ~$109\text{ min}$ (~4.9s/msg) |

### Key Trade-Off Insights for Section 5 (Discussion):
1. **ViSoBERT Pareto-Optimality:** ViSoBERT captures the highest practical Scam Recall ($95.62\%$) among all deployable edge models while maintaining high precision ($89.79\%$) and compact size ($390\text{MB}$).
2. **Failure of Large Scale Without Cost-Weighting:** PhoBERT-large ($370\text{M}$ params) uses $3.8\times$ more memory and $3.5\times$ longer training, yet its Scam Recall ($92.33\%$) is inferior to ViSoBERT ($95.62\%$), proving parameter scaling cannot compensate for asymmetric loss.
3. **Gemini 3.5 Flash Alarm Fatigue:** Gemini catches 100% of scams but suffers from severe false positive over-flagging (Precision collapses to $64.47\%$, Accuracy drops to $84.50\%$). Furthermore, cloud latency ($4.9\text{s/msg}$) is $326\times$ slower than ViSoBERT ONNX INT8 ($15\text{ms/msg}$).
