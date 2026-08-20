# GAP Analysis & Feasibility Evaluation Report

> **Researcher:** `Nguyen Trung Hieu`  
> **Date:** `2026-08-20`  
> **Target GAP ID:** `GAP-T-01` (Technological & Comparative Evaluation)  
> **Topic:** ScamShield — Efficacy, Latency, and Robustness of Few-Shot LLMs vs. Fine-Tuned PhoBERT for Vietnamese Scam Classification

---

## 1. Concrete Research GAP Description

Based on the **5 papers** systematically extracted in the Evidence Table, no prior literature provides a head-to-head empirical benchmark comparing modern lightweight LLMs (under zero-shot, few-shot, and Chain-of-Thought prompting) against fine-tuned Vietnamese Pretrained Language Models (`PhoBERT-base`, `ViDeBERTa`) on authentic Vietnamese scam lures containing dialectal teencode, character homoglyphs, and psychological urgency manipulation.

---

## 2. 7-Factor Feasibility Evaluation Matrix

| Feasibility Factor | Status | Concrete Justification & Evidence |
| :--- | :---: | :--- |
| **1. Dataset** | **Approved** | Publicly accessible Vietnamese short text and SMS spam/scam datasets available ($N \ge 2,000$). |
| **2. API / Tooling** | **Approved** | Google Gemini API & OpenAI API keys accessible within project free/academic tier. |
| **3. Compute** | **Approved** | PhoBERT fine-tuning executable on local GPU or Google Colab T4 (16GB VRAM). |
| **4. Ground Truth** | **Approved** | Binary labels (`scam` vs `ham`) objectively verifiable against known threat databases. |
| **5. Codebase** | **Approved** | Standard open-source libraries: PyTorch, HuggingFace Transformers, Scikit-learn. |
| **6. Skill Set** | **Approved** | Team proficiency in Python, PyTorch modeling, and NLP evaluation pipelines. |
| **7. Time Budget** | **Approved** | Experiments, statistical testing (Wilcoxon, McNemar), and manuscript drafting feasible within semester timeline. |

- **Evaluation Verdict:** **APPROVED (Zero Disqualifying Flags, Safe to Proceed)**
