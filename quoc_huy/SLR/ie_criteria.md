## Research Protocol Manager (PICO • IC • EC)

> The PICO Framework governs systematic eligibility across Population, Intervention, Comparison, and Outcome benchmarks. These parameters are directly injected into the Gemini AI Batch Screening Prompt.

---

## 1. PICO Framework

| Component                        | Definition                                                                                                                                                                                             |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **P – Population / Problem**     | Suspected scam messages/SMS/emails (scam, phishing, spam, fraud) — prioritizing Vietnamese, but accepting English or other low-resource languages as supplements due to the lack of Vietnamese papers. |
| **I – Intervention / Technique** | LLM prompting (zero-shot/few-shot) or fine-tuned PLMs.                                                                                                                                                 |
| **C – Comparison / Baselines**   | Comparison between the 2 approaches (LLM vs. fine-tuned model), or comparison between different prompting configurations.                                                                              |
| **O – Outcome / Target Metrics** | Accuracy, Precision/Recall, macro-F1, latency, cost per request.                                                                                                                                       |

---

## 2. Inclusion Criteria (IC)

> Papers must satisfy **all or applicable** Inclusion Criteria (IC) to advance from Title/Abstract screening into the full 7-Column Evidence Extraction Matrix.

| Code     | Description                                                    |
| -------- | -------------------------------------------------------------- |
| **IC-L** | Paper written in English                                       |
| **IC-T** | Published in a conference or journal (excluding blogs, theses) |
| **IC-E** | Contains at least 1 quantitative result in a Table or Figure   |

---

## 3. Exclusion Criteria (EC)

> Meeting any **single** Exclusion Criterion (EC) immediately disqualifies a record. These ECs directly populate both the AI Judge decision matrix and the manual exclusion dropdown modal.

| Code     | Description                                      |
| -------- | ------------------------------------------------ |
| **EC-D** | Duplicate of an already included paper           |
| **EC-A** | Full-text unavailable for download               |
| **EC-S** | Fewer than 4 pages (abstract, poster)            |
| **EC-N** | No empirical evaluation (vision paper, tutorial) |
