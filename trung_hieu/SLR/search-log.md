# Systematic Literature Review Search Log

> **Protocol Version:** 1.1 (PRISMA 2020 Compliant, Updated for Tier-2 Forensic Council)  
> **Researcher:** `Nguyen Trung Hieu` (`LR` / Literature Reviewer & LLM Runner)  
> **Date of Execution:** `2026-08-20` (Updated: `2026-10-02`)  
> **Target Research Question:** *"How effective are prompt-based LLMs (few-shot) and Multi-Agent Forensic Councils compared with fine-tuned local models for Vietnamese scam message classification?"*

---

## 1. Primary Search Strings & Database Queries

- **Search Query String (Phase 1 Baseline):** `("scam" OR "phishing" OR "fraud") AND ("SMS" OR "message") AND ("LLM" OR "BERT" OR "transformer")`
- **Search Query String (Phase 2 Tier-2 Council Update):** `("multi-agent" OR "LLM council" OR "panel of LLMs" OR "adversarial debate" OR "role specialization") AND ("phishing" OR "scam" OR "evaluator" OR "false positive")`
- **Active Academic Databases:** ArXiv, OpenAlex, Semantic Scholar, CrossRef, Google Scholar, ACL Anthology, ICLR, ICML, NAACL
- **Date Executed:** `2026-08-20` & `2026-10-02`
- **Language Scope:** English, Vietnamese
- **Temporal Window:** 2023 – 2026

---

## 2. Consolidation & Deduplication Audit

| Academic Database | Search Query Executed | Search Date | Total Records Harvested |
| :--- | :--- | :---: | :---: |
| **ArXiv** | Multi-Agent / Council / Phishing search | 2026-10-02 | Verified via API |
| **OpenAlex** | LLM-as-a-judge / Role specialization | 2026-10-02 | Verified via API |
| **Semantic Scholar** | MultiPhishGuard / PoLL citations | 2026-10-02 | Verified via API |
| **CrossRef** | NAACL / ICLR / ICML multi-agent debate | 2026-10-02 | Verified via API |
| **Google Scholar** | Karpathy llm-council reference | 2026-10-02 | Verified via API |

- **Total Deduplicated Records in Corpus (`01_all_records.csv`):** `471` (Initial) + Targeted Tier-2 Council Searches

---

## 3. PRISMA Screening Progress Breakdown

- **Total Records Screened (Title + Abstract):** `471`
- **Round 1 Excluded Records:** `460`
- **Round 1 Retained / Screened Records (`02_after_screening_v1.csv`):** `11`
- **Final Included Verified Papers (`03_final_included.csv` & `evidence-table.md`):** `11` (5 baseline PLM/Few-shot comparison papers + 6 Tier-2 Multi-Agent Forensic Council papers: MultiPhishGuard, PoLL, NAACL 2025 Council, ChatEval, ICML 2024 Debate, Karpathy's llm-council)
