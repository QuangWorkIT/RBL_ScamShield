# Search Log

- **Project:** ScamShield – AI-Powered Scam Message and Call Detection Platform
- **Reviewer:** Hoang Hai Phuc
- **Assigned Database / Source:** IEEE Xplore
- **Search Date:** 20/08/2026
- **Time Window / Filter:** 2020 – 2026 | Focus: English & Vietnamese

---

## 1. Search Query Design & Strategy

The search strategy combines concepts representing the problem domain (scam/fraud), message modalities, and AI/NLP techniques (PhoBERT, LLMs):

- **Concept Group 1 (Problem):** `"scam message"` | `"phishing message"` | `"fraud message"` | `"classification"` | `"detection"` | `"machine learning"` | `"deep learning"` | `"transformer"`
- **Concept Group 2 (Vietnamese):** `"Vietnamese"` | `"Vietnamese language"` | `"text classification"` | `"message classification"` | `"BERT"` | `"PhoBERT"` | `"transformer"` | `"large language model"`
- **Concept Group 3 (LLM comparison):** `"large language model"` | `"LLM"` | `"zero-shot"` | `"few-shot"` | `"prompting"` | `"text classification"` | `"message classification"`

---

## 2. Search Execution Log

| Query ID | Date | Source | Search Query | Applied Filters | Total Hits | Screened / Retrieved | Target Output | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Q01** | 20/08/2026 | IEEE Xplore | `("scam message" OR "phishing message" OR "fraud message") AND ("classification" OR "detection") AND ("machine learning" OR "deep learning" OR transformer)` | Custom range: 2020–2026 | 15 | Top relevant | `01_all_records.csv` | General ML/DL and Transformer models for scam/phishing message detection |
| **Q02** | 20/08/2026 | IEEE Xplore | `("PhoBERT") AND ("scam" OR "fraud" OR "spam") AND ("sms" OR "message" OR "text classification")` | Custom range: 2020–2026 | 25 | Top relevant | `01_all_records.csv` | Focus on applying PhoBERT for Vietnamese scam/spam message classification |
| **Q03** | 20/08/2026 | IEEE Xplore | `("large language model" OR LLM) AND ("zero-shot" OR "few-shot" OR prompting) AND ("text classification" OR "message classification")` | Custom range: 2020–2026 | 182 | Top relevant | `01_all_records.csv` | Focus on LLM prompting capabilities (zero-shot, few-shot) for message classification |
| **Q04** | 20/08/2026 | IEEE Xplore | `("Vietnamese" OR "Vietnamese language") AND ("scam" OR phishing OR fraud) AND ("classification" OR detection)` | Custom range: 2020–2026 | 4 | Top relevant | `01_all_records.csv` | Focus specifically on scam/fraud detection in the Vietnamese language |
| **Q05** | 20/08/2026 | IEEE Xplore | `("few-shot" OR "zero-shot" OR prompting) AND ("fine-tuning" OR "fine-tuned") AND ("text classification")` | Custom range: 2020–2026 | 209 | Top relevant | `01_all_records.csv` | Investigating techniques involving fine-tuning and prompting (zero-shot/few-shot) for text classification |

---
