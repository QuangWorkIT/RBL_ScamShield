# Inclusion and Exclusion Criteria (SLR Protocol v1.0)


## 1. PICO Framework

| Component | Definition |
|---|---|
| **P – Population** | Scam messages (SMS, Zalo, Messenger, Email) and fraudulent call scripts targeting users, particularly within the context of the Vietnamese language and community alert platforms. |
| **I – Intervention** | Text classification based on Large Language Models (LLMs) utilizing In-context Learning techniques (Zero-shot, Few-shot, Few-shot + taxonomy) integrated into software systems. |
| **C – Comparison** | Fine-tuned Pre-trained Language Models (such as PhoBERT) and traditional filtering mechanisms based on blacklists or keyword matching. |
| **O – Outcome** | Classification performance (Accuracy, Precision, Recall, Macro-F1 per scam category), system inference latency (< 3 seconds), and API token cost (Cost per request). |

---

## 2. Inclusion Criteria (IC)

Papers **MUST** satisfy all of the following inclusion criteria to be considered for final synthesis:

| Code | Criteria / Description |
|---|---|
| **IC1** | Studies focusing on the detection and classification of spam messages, scam messages (phishing/smishing), or fraud via conversational scripts. |
| **IC2** | Papers that apply or evaluate Large Language Models (LLMs via prompting) or Pre-trained Language Models (PLMs like BERT, PhoBERT). |
| **IC3** | Studies providing clear empirical results with metrics such as Accuracy, Precision, Recall, F1-score, inference latency, or computational cost. |
| **IC4** | Papers discussing system architecture, integrating AI into real-world platforms (web/mobile apps), or community alert mechanisms (crowdsourcing/blacklist). |
| **IC5** | Studies published from 2020 onwards. |

---

## 3. Exclusion Criteria (EC)

Papers meeting **ANY** of the following criteria will be excluded from the review:

| Code | Criteria / Description |
|---|---|
| **EC1** | Studies focusing solely on malware analysis, or pure URL identification via hash algorithms without semantic text analysis. |
| **EC2** | Papers dealing with acoustic voice/audio processing to detect fraudulent calls rather than processing text/scripts. |
| **EC3** | Studies that do not utilize Machine Learning, LLMs, or PLMs (e.g., relying entirely on classical rule-based methods). |
| **EC4** | Purely theoretical or vision papers lacking experimental datasets, practical implementations, or empirical evaluation. |
| **EC5** | Papers not written in English, or where the full-text is inaccessible. |

---

## 4. Decision Rule

A paper is designated as **Included** if and only if it satisfies all of the following conditions:

1. Meets **IC1** (focuses on spam/scam/phishing text or fraud scripts).
2. Meets **IC2** (utilizes/evaluates LLMs or PLMs like PhoBERT/BERT).
3. Meets **IC3** (provides quantitative/empirical evaluation metrics).
4. Meets **IC4** (covers system architecture, platform integration, or community alert/blacklist mechanisms).
5. Meets **IC5** (published in or after 2020).
6. Does **NOT** violate any Exclusion Criteria (**EC1 – EC5**).

> **Decision Summary:** `Include` = (IC1 ∧ IC2 ∧ IC3 ∧ IC4 ∧ IC5) ∧ ¬(EC1 ∨ EC2 ∨ EC3 ∨ EC4 ∨ EC5)

---

## 5. Screening Examples

### Example 1 — Include
**Title:** *Few-Shot Prompting with LLMs for Vietnamese Phishing & Scam SMS Detection*
- **IC Evaluation:** IC1 (Pass), IC2 (Pass - LLM prompting), IC3 (Pass - F1 & Latency), IC4 (Pass - Web architecture), IC5 (Pass - 2024)
- **EC Evaluation:** None triggered
- **Decision:** **Include**

### Example 2 — Include
**Title:** *Fine-Tuning PhoBERT for Scam Message Classification and Blacklist Integration*
- **IC Evaluation:** IC1 (Pass), IC2 (Pass - PhoBERT baseline), IC3 (Pass - Accuracy/Precision/Recall), IC4 (Pass - Blacklist mechanism), IC5 (Pass - 2023)
- **EC Evaluation:** None triggered
- **Decision:** **Include**

### Example 3 — Exclude (EC1)
**Title:** *Malware Identification via Hash Signatures and Suspicious URL Filtering*
- **IC Evaluation:** IC1 (Fail - no semantic text analysis)
- **EC Evaluation:** **EC1 triggered** (Malware/Hash URL without text analysis)
- **Decision:** **Exclude**

### Example 4 — Exclude (EC2)
**Title:** *Acoustic Feature Extraction for Voice Phishing Detection in Phone Calls*
- **IC Evaluation:** IC1 (Fail - raw audio acoustics rather than text/scripts)
- **EC Evaluation:** **EC2 triggered** (Acoustic audio processing)
- **Decision:** **Exclude**

### Example 5 — Exclude (EC3)
**Title:** *A Classical Rule-Based Blacklist Approach for SMS Spam Filtering*
- **IC Evaluation:** IC2 (Fail - no ML/LLM/PLM)
- **EC Evaluation:** **EC3 triggered** (Pure classical rule-based method without ML/LLM/PLM)
- **Decision:** **Exclude**

### Example 6 — Exclude (EC4)
**Title:** *Future Vision: Architecting Next-Gen AI for Anti-Scam Systems*
- **IC Evaluation:** IC3 (Fail - no empirical dataset or quantitative evaluation)
- **EC Evaluation:** **EC4 triggered** (Pure vision paper without empirical results)
- **Decision:** **Exclude**

### Example 7 — Exclude (EC5)
**Title:** *Nghiên cứu phân loại tin nhắn rác bằng thuật toán học máy* (Full text only in Vietnamese / Abstract only available)
- **EC Evaluation:** **EC5 triggered** (Full-text not written in English or inaccessible)
- **Decision:** **Exclude**

---

## 6. Notes for Reviewers

- **Multi-modality & Script Focus:** Fraudulent calls are eligible *only* if the paper analyzes textual transcripts or conversational scripts (text analysis). Acoustic/signal audio processing papers are excluded under **EC2**.
- **System & Alert Mechanisms:** System architecture papers including platform deployment (web/mobile app) or community crowdsourcing/blacklist controls satisfy **IC4**.
- **Metrics Requirement:** Evaluation must include at least one concrete quantitative metric (Accuracy, F1-score, Latency, Token Cost, etc.) per **IC3**.
- **Publication Window:** Ensure the publication date is **2020 or later** (**IC5**).
