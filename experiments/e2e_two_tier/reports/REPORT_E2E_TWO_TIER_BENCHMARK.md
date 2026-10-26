# 🔬 ScamShield-VN: EXP-03 Two-Tier Cascaded System Empirical Benchmark Report

> **Suite:** Combined Benchmark ($N=384$ samples: $267$ Frozen Test Set + $117$ Hard Forensic Challenges)
> **Evaluation Protocol:** 3 Independent Iterations (Median aggregation with stability jitter analysis)
> **Date:** 2026-10-18 21:08:44

---

## 1. 3-Run Median Comparative Matrix (Default Routing Threshold $\tau = 0.90$)

| Experimental Arm | Accuracy | Precision | **Scam Recall** | Macro-F1 | **FPR** | Latency (ms) | Cost / 1k SMS | Escalation Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Arm 1: Solo Tier 1 Edge (ViSoBERT) | 96.35% | 96.49% | 95.38% | 95.93% | 2.84% | 35.0 ms | $0.0000 | 0.0% |
| Arm 2: Solo Tier 2 Fast (Gemini Flash-Lite) | 97.66% | 95.56% | 99.42% | 97.45% | 3.79% | 1969.9 ms | $0.2817 | 100.0% |
| Arm 3: Solo Tier 2 SOTA (GPT-6.1-sol) | 99.74% | 100.00% | 99.42% | 99.71% | 0.00% | 5765.0 ms | $1.4667 | 100.0% |
| Arm 4: Naive Cascaded (Tier 1 + PoLL 3/5) | 97.14% | 96.55% | 97.11% | 96.83% | 2.84% | 717.8 ms | $1.5923 | 3.4% |
| **Arm 5: Proposed ScamShield Cascaded (Tier 1 + Council)** | 97.40% | 97.11% | **97.11%** | 97.11% | **2.37%** | 267.7 ms | $0.0509 | 3.4% |

---

## 2. Ablation Study: Sensitivity & Pareto Optimization Across Thresholds $\tau$

| Routing Threshold ($\tau$) | Accuracy | Precision | Scam Recall | FPR | Latency (ms) | Cost / 1k SMS | Escalation Rate (\% Tier 2) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| \tau = 0.70 | 96.35% | 96.49% | 95.38% | 2.84% | 58.2 ms | $0.0051 | 0.5% |
| \tau = 0.80 | 96.61% | 97.06% | 95.38% | 2.37% | 148.5 ms | $0.0232 | 1.6% |
| \tau = 0.85 | 97.14% | 97.09% | 96.53% | 2.37% | 223.9 ms | $0.0412 | 2.6% |
| **\tau = 0.90** | 97.40% | 97.11% | 97.11% | 2.37% | 267.5 ms | $0.0509 | **3.4%** |
| \tau = 0.95 | 97.92% | 98.25% | 97.11% | 1.42% | 668.2 ms | $0.1386 | 9.1% |

---

## 3. Key Scientific Findings & Discussion for Paper Section 5

1. **Pareto Optimality of Proposed Cascade (Arm 5):** Reaches **97.40% Accuracy, 97.11% Scam Recall, and 2.37% FPR** while resolving **96.6% of traffic locally at the edge** (Tier 1 latency 35.0 ms). Median system latency is 267.7 ms and cost is $0.0509 / 1k messages (96.5% saving vs. cloud-only Arm 3 at $1.4667; Arm 3 reaches 99.74% accuracy and 0.00% FPR but at 28.8x the cost and 21.5x the latency).
2. **Alarm Fatigue Mitigation (partial):** On the combined N=384 suite, solo Tier 1 yields FPR 2.84%, solo Tier 2 Fast (Gemini Flash-Lite) 3.79%, and the Naive Cascade 2.84%, whereas the proposed cascade lowers FPR to **2.37%**. Only the solo GPT-6.1-sol arm reaches 0.00% FPR. The 0.00% FPR reported for the Public Defender councils applies to the N=117 challenge suite only (see REPORT_ABLATION_3V5.md), not to the cascade.
3. **Recall Rescue via Escalation:** Tier 1 alone reaches 95.38% Scam Recall; escalating 3.39% of messages lifts it to 97.11% (derived counts on 173 scams: 165 -> 168 detected, i.e., 3 of the 8 Tier 1 misses rescued). Residual misses remain, so the claim of rescuing 100% of zero-day lures is not supported by the CSV results.
