# SLR Search & Deduplication Log

> **Project:** ScamShield Research Intelligence (RBL)  
> **Researcher:** Phan Tran Hoang Tran  
> **Execution Date:** `2026-08-20`  
> **Topic:** SMS / Message Scam Classification & Threat Detection via LLMs (Few-Shot) vs Fine-Tuned PhoBERT  

---

## 1. Search Query Strings & Database Harvest Audit

| Query ID | Database | Search Query Executed | Date | Raw Yield |
| :--- | :--- | :--- | :---: | :---: |
| **Query-A** | OpenAlex | `("scam detection" OR "smishing" OR "phishing detection" OR "SMS spam") AND ("LLM" OR "PhoBERT" OR "few-shot" OR "fine-tuning")` | 2026-08-20 | 45 |
| **Query-B** | ArXiv | `("scam detection" OR "smishing" OR "phishing detection" OR "SMS spam") AND ("LLM" OR "PhoBERT" OR "few-shot" OR "fine-tuning")` | 2026-08-20 | 45 |
| **Query-C** | CrossRef | `("scam message" OR "smishing" OR "phishing" OR "SMS spam") AND ("LLM" OR "PhoBERT" OR "few-shot" OR "fine-tuning")` | 2026-08-20 | 52 |
| **Query-D** | Semantic Scholar | `("Vietnamese" OR "SMS spam" OR "scam message") AND ("BERT" OR "PhoBERT" OR "text classification")` | 2026-08-20 | 60 |

---

## 2. Deduplication Audit Table

- **Total Raw Harvested Across Databases:** `242`
- **Duplicates Identified & Removed (DOI + Title Levenshtein similarity >= 0.88):** `41`
- **Total Unique Deduplicated Corpus (`01_all_records.csv`):** `201`

---

## 3. PRISMA Screening Summary

- **Total Records Screened (Title + Abstract - V1):** `201`
- **Excluded at Round 1 (V1):** `96`
- **Retained for Full-Text Evaluation (V2):** `105`
- **Excluded at Round 2 (V2):** `90`
- **Final Included Verified Papers (`03_final_included.csv`):** `15`
