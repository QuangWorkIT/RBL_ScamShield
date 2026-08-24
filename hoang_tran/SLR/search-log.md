# SLR Search & Deduplication Log

> **Project:** ScamShield Research Intelligence (RBL)  
> **Researcher:** Phan Tran Hoang Tran  
> **Execution Date:** `2026-08-22`  
> **Topic:** SMS / Message Scam Classification & Threat Detection via LLMs (Few-Shot) vs Fine-Tuned PhoBERT  

---

## 1. Search Query Strings & Database Harvest Audit

| Query ID | Database | Search Query Executed | Date | Raw Yield |
| :--- | :--- | :--- | :---: | :---: |
| **Query-A** | OpenAlex | `("scam message" OR "smishing" OR "phishing detection" OR "SMS spam") AND ("LLM" OR "PhoBERT" OR "few-shot" OR "fine-tuning")` | 2026-08-22 | 80 |
| **Query-B** | ArXiv | `("Vietnamese" OR "SMS spam" OR "text classification") AND ("PhoBERT" OR "BERT" OR "language model")` | 2026-08-22 | 80 |
| **Query-C** | CrossRef | `("phishing email" OR "vishing" OR "scam classification") AND ("prompt tuning" OR "small language model" OR "transformers")` | 2026-08-22 | 74 |

---

## 2. Deduplication & Verification Audit Table

- **Total Raw Harvested Across Databases:** `284`
- **Duplicates Identified & Removed (DOI + Title similarity):** `29`
- **Total Unique Deduplicated Corpus (`01_all_records.csv`):** `255`
- **100% URL Accessibility Audit:** All included paper URLs/DOIs verified live.

---

## 3. PRISMA Screening Summary

- **Total Records Screened (Title + Abstract - V1):** `255`
- **Excluded at Round 1 (V1):** `123`
- **Retained for Full-Text Evaluation (V2):** `132`
- **Excluded at Round 2 (V2):** `117`
- **Final Included Verified Papers (`03_final_included.csv`):** `15`
