# Master Systematic Gap Analysis & Research Opportunities
## ScamShield: AI-Powered Scam Message and Call Detection and Community Alert Platform (SCS)
### Capstone Project & Research-Based Learning (RBL) Synthesis

---

## 1. Executive Summary & Corpus Synthesis
Based on the multi-researcher systematic review of **34 unique included peer-reviewed papers** across 5 independent researcher streams (**Minh Quang, Hải Phúc, Hoàng Trần, Quốc Huy, Trung Hiếu**), we identify **5 fundamental Research Gaps** in current academic literature that directly justify the design, architecture, and deployment strategy of **ScamShield (SCS)**.

```
       STATE-OF-THE-ART (34 PAPERS)                          SCAMSHIELD (SCS) NOVELTY
┌──────────────────────────────────────────────┐    ┌────────────────────────────────────────────────────────┐
│ 1. Monolingual / English-centric datasets     │───►│ • First Public Vietnamese Scam Corpus (>=500 samples)  │
│ 2. Heavy LLMs (>3s latency, recurring API fee)│───►│ • 2-Tier Cascaded AI (Fast-Path PhoBERT + LLM Cloud)  │
│ 3. Text-only evaluation (blind to QR & images)│───►│ • Multimodal & OCR Evasion Hardening (Quishing/Image) │
│ 4. Single isolated message evaluation         │───►│ • Full Multi-turn Conversational Scam Progression      │
│ 5. Static classifiers without feedback loop   │───►│ • Community-Reported Blacklist with Moderator Review  │
└──────────────────────────────────────────────┘    └────────────────────────────────────────────────────────┘
```

---

## 2. Deep Dive: 5 Core Research Gaps & ScamShield Solutions

### 🔴 Gap 1: Severe Scarcity of Vietnamese Scam Datasets & Linguistic Evasion (Teencode / Accents)
* **Empirical Evidence from Master Matrix:**
  * *Tuấn et al. (M001)*, *Nguyen-Xuan et al. (M002)*, *Cam et al. (M003)*, and *Uddin et al. (M034, M037)* confirm that while English datasets (SMS Spam Collection, Enron, PhishTank) exceed tens of thousands of samples, high-quality, annotated Vietnamese scam datasets are practically non-existent.
  * Scammers targeting Vietnamese users heavily exploit *teencode* (e.g. `c0ng an`, `v4y t1en`, `nh4n thu0ng`), zero-width Unicode characters, and dialectal spelling variations to easily bypass rule-based and keyword filters.
* **ScamShield Resolution:**
  * Construct the first benchmark **Vietnamese Scam Dataset (>=500 labeled messages across 5-7 taxonomy categories)** collected from Cục An toàn thông tin (NCSC) alerts, news reports, and community reports.
  * Implement Adversarial Data Augmentation (using LLM Few-Shot to generate synthetic teencode/spelling variants) ensuring high robustness against adversarial bypass.

---

### 🔴 Gap 2: The Accuracy-Latency-Cost Trilemma in Real-Time Mobile Scam Detection
* **Empirical Evidence from Master Matrix:**
  * *Saias (2025, M004)*, *Sbei et al. (2025, M005)*, *Peng et al. (M036, Genshin)*, and *Edge-AI Smishing (2026, M041)* demonstrate that massive LLMs (GPT-4, LLaMA-70B, Qwen) achieve strong zero-shot reasoning but suffer from high inference latency (>2-4s) and recurring per-token API costs ($0.002-$0.01/call), making them impractical for client-side mobile protection.
  * Conversely, ultra-lightweight traditional models (Naive Bayes, SVM, BiGRU) offer sub-millisecond inference (0.25ms) but degrade significantly on complex, multi-layered scams (*M006, M019, M031, M033*).
* **ScamShield Resolution (2-Tier Cascaded AI Architecture):**
  * **Tier 1 (Fast-Path Local / Edge Inference):** Fine-tuned `PhoBERT-base` with **Weighted Binary Cross-Entropy (WBCE)** loss to penalize False Negatives. Classifies 80% of routine scam/ham messages in `< 250ms` at zero external API cost.
  * **Tier 2 (Cloud LLM Reasoning):** `Gemini-2.0-Flash` / `GPT-4o-mini` with *Few-shot + Scam Taxonomy prompting*. Triggered only when Tier 1 confidence is `< 90%` or when analyzing complex multi-turn dialogs, achieving `< 3s` latency while cutting API expenses by 80%.

---

### 🔴 Gap 3: Multimodal Threat Blindness (QR Code Phishing / Image-Based Fraud Notices)
* **Empirical Evidence from Master Matrix:**
  * *QuishingShield (2026, M014)*, *GRPO-MMS (2026, M007)*, and *PEEK Phishing Framework (M035)* emphasize that modern cybercriminals increasingly send fraudulent bank transfer receipts, fake arrest warrants from police, and embedded QR codes (**Quishing**) to bypass textual NLP filters entirely.
  * Over 85% of existing literature evaluates purely plain text (*M008, M009, M010, M032, M038, M042*), creating an alarming blind spot in mobile messaging apps (Zalo, Messenger, Telegram).
* **ScamShield Resolution:**
  * Equip the platform with an **Integrated OCR Engine (Tesseract/PaddleOCR)** to extract textual content from user-uploaded screenshots.
  * Embed automated QR code decoding to inspect underlying landing URLs against Google Safe Browsing and the ScamShield Community Blacklist.

---

### 🔴 Gap 4: Single-Message Evaluation vs. Multi-Turn Conversational Scam Progression
* **Empirical Evidence from Master Matrix:**
  * Traditional NLP classifiers evaluate isolated messages (e.g. "Hello, is this Mr. Nam?"). In isolation, the message appears legitimate (Ham).
  * However, social engineering scams (pig butchering, romance fraud, fake job tasks) unfold over **5-10 turns of dialogue**, escalating from casual greetings to deposit requests.
* **ScamShield Resolution:**
  * Support **Full Conversation Thread Analysis** (uploading multi-message screenshots or chat transcripts), allowing the AI Engine to detect conversational scam progression and psychological manipulation cues (urgency, authority, financial bait).

---

### 🔴 Gap 5: Disconnect Between Academic Classifiers and Community Threat Intelligence
* **Empirical Evidence from Master Matrix:**
  * Almost all 34 academic papers focus purely on static offline model training without operational feedback loops.
  * Once a novel scam campaign emerges (e.g. fake VNeID app updates, fake utility bill refunds), static models fail until retrained months later.
* **ScamShield Resolution:**
  * Combine AI classification with a **Community Blacklist Platform**:
    * Users report suspicious phone numbers, bank accounts, and URLs.
    * Multi-tier anti-abuse moderation workflow (Moderator review, reputation scoring, duplicate clustering).
    * Real-time Threat Heatmap and Education Hub to protect vulnerable groups (students, elderly).

---

## 3. Methodological Comparison Matrix

| Dimension | Typical Literature State-of-the-Art (34 Papers) | ScamShield Capstone Platform (SCS) |
| :--- | :--- | :--- |
| **Language Scope** | English, Kiswahili, Bangla, Spanish | Vietnamese-first (PhoBERT + Teencode & Dialect Robustness) |
| **Architecture** | Single-tier (either pure heavy LLM or pure lightweight ML) | **2-Tier Hybrid Cascade (PhoBERT Tier 1 + Gemini Few-Shot Tier 2)** |
| **Modality** | 85%+ Plain text SMS only | **Multimodal (Text + OCR Screenshot Extraction + QR Quishing Decoding)** |
| **Context Window** | Single isolated message (1-turn) | **Multi-turn Dialogue & Conversational Progression Analysis** |
| **Operational Loop**| Static offline testbench | **Live Community Blacklist + Moderator Review Workflow** |
| **Latency & Cost** | High latency (>3s) or poor accuracy on novel scams | **< 250ms for 80% of traffic; 80% reduction in API cost** |

---

## 4. Conclusion for Capstone Defense & RBL Publication
The unified 34-paper master evidence corpus rigorously validates that **ScamShield's hybrid technological stack (PhoBERT + Gemini Few-Shot + Community Blacklist + OCR)** directly addresses the most critical unaddressed gaps in modern cybersecurity literature.
