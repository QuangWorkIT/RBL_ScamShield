## Screening Criteria

> **IC (Inclusion Criteria)** = criteria the paper MUST satisfy. **EC (Exclusion Criteria)** = reasons for exclusion.

| Code | Description |
|---|---|
| IC-L | Paper written in English |
| IC-T | Published in a conference or journal (excluding blogs, theses) |
| IC-E | Contains at least one quantitative evaluation result in a Table or Figure |
| EC-D | Duplicate of an already included paper |
| EC-A | Full-text unavailable for download |
| EC-S | Fewer than 4 pages (abstracts, posters) |
| EC-N | No empirical evaluation (vision papers, tutorials) |

## Domain-Specific Criteria

### Research Question

> **RQ:** How effective are prompt-based LLMs (few-shot) compared with a fine-tuned PhoBERT model for Vietnamese scam message classification?

### PICO Framework

| Component | Definition for this RQ |
|---|---|
| **P – Population** | Vietnamese text messages / short messages that are classified for scam or non-scam detection, preferably with clearly defined scam categories |
| **I – Intervention** | Prompt-based Large Language Models (LLMs), especially few-shot or in-context learning approaches |
| **C – Comparison** | Fine-tuned PhoBERT or a comparable Vietnamese pre-trained language model used as a supervised classification baseline |
| **O – Outcome** | Classification effectiveness measured using quantitative metrics such as Accuracy, Precision, Recall, F1-score, Macro-F1, ROC-AUC, or confusion matrix results |

## RQ-Specific Criteria

| Code | What to Check | Criteria / Description |
|---|---|---|
| **IC-Y** | Publication year | Study published between **2022 and 2026** |
| **IC-P** | Population / Task | Study conducts **text/message classification** related to scam, phishing, fraud, spam scam, or malicious messages; priority given to Vietnamese data or data directly applicable to Vietnamese |
| **IC-I** | Intervention | Uses **LLMs for text classification**, specifically **prompt-based / few-shot / in-context learning** |
| **IC-C** | Comparison | Includes a **baseline or comparative method** based on a supervised/fine-tuned transformer; priority given to **PhoBERT** or comparable Vietnamese language models |
| **IC-O** | Outcome | Provides at least one **quantitative outcome** evaluating classification performance (e.g., Accuracy, Precision, Recall, F1-score, Macro-F1, or ROC-AUC) |
| **IC-V** | Vietnamese relevance | Study involves data, models, language, or results that are **clearly relevant to Vietnamese language tasks** |
| **EC-P** | Wrong task | Exclude if the study primarily focuses on **debugging, code completion, sentiment analysis, machine translation**, or NLP tasks unrelated to scam/message classification |
| **EC-I** | Wrong intervention | Exclude if the paper does not study **LLM/prompt-based/few-shot classification** when evaluated as evidence for the LLM branch of the RQ |
| **EC-C** | No meaningful comparison | Exclude if the paper lacks a suitable baseline/comparison when evaluated to answer the **LLM vs. fine-tuned model** comparison of the RQ |
| **EC-O** | No measurable outcome | Exclude if there are no empirical results or quantitative metrics to evaluate classification performance |
| **EC-V** | No Vietnamese relevance | Exclude if the study has no relevance to **Vietnamese language/data/model applicability** and provides no transferable evidence for the Vietnamese problem context |

## Decision Rule

A paper is **Included** when it satisfies the following:

1. Meets **IC-Y**.
2. Meets **IC-P**.
3. Meets **IC-I** or provides direct evidence for the **comparison/baseline** branch of the RQ.
4. Meets **IC-O**.
5. Has direct **Vietnamese relevance** or provides foundational methodological evidence for the studied approach.
6. Does not violate any **EC**.

> **Note:** Papers do not need to evaluate both prompt-based LLMs **and** PhoBERT simultaneously. In an SLR, individual papers focusing on a single component are valid as long as they build necessary evidence for the RQ comparison.

## Screening Examples

### Example 1 — Include

**Paper:** Few-shot prompting with LLMs for phishing/scam message classification

- IC-Y: Pass
- IC-P: Pass
- IC-I: Pass
- IC-O: Pass
- IC-V: Pass or clearly applicable to Vietnamese
- Decision: **Include**

### Example 2 — Include as baseline evidence

**Paper:** Fine-tuning PhoBERT for Vietnamese spam/scam text classification

- IC-Y: Pass
- IC-P: Pass
- IC-C: Pass
- IC-O: Pass
- IC-V: Pass
- Decision: **Include**

### Example 3 — Exclude

**Paper:** Using GPT-4 for automated code completion

- IC-Y: Pass
- IC-I: LLM used
- IC-P: **Fail**
- EC-P: **Apply**
- Decision: **Exclude**

### Example 4 — Exclude

**Paper:** LLM-based scam detection without any classification experiment or quantitative evaluation

- IC-P: Pass
- IC-I: Pass
- IC-O: **Fail**
- EC-O: **Apply**
- Decision: **Exclude**

## Notes for Reviewers

- **IC-P, IC-I, IC-C, and IC-O** are the primary criteria for determining direct relevance to the RQ.
- Do not treat **scam detection**, **spam detection**, and **phishing detection** as completely identical, though overlap exists.
- Non-Vietnamese papers may still be included if they provide direct **methodological evidence** for prompt-based LLMs or fine-tuned transformer classification transferable to experimental design.
- When a paper addresses only one side of the RQ, explicitly annotate whether it provides **LLM evidence**, **PhoBERT/baseline evidence**, or **comparison evidence**.



