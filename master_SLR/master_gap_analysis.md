# Master Systematic Gap Analysis & Research Opportunities
## ScamShield: AI-Powered Scam Message and Call Detection and Community Alert Platform

---

### 1. Executive Summary of the Master Corpus
Based on the systematic synthesis of **38 unique included peer-reviewed papers** across 5 independent researcher streams (Minh Quang, Hải Phúc, Hoàng Trần, Quốc Huy, Trung Hiếu), we identify **5 fundamental Research Gaps** in the current state-of-the-art that directly justify the architectural and methodological design of the **ScamShield (SCS)** Capstone Project and its **RBL Component**.

```
  STATE-OF-THE-ART (38 PAPERS)                       SCAMSHIELD (SCS) NOVELTY
┌──────────────────────────────────────────────┐    ┌────────────────────────────────────────────────────────┐
│ • Monolingual / English-centric datasets     │───►│ 1. First Public Vietnamese Scam Corpus (>=500 samples) │
│ • Heavy LLMs (>40ms latency, high API cost)  │───►│ 2. 2-Tier Cascaded AI (Fast-Path PhoBERT + LLM Cloud)  │
│ • Plain-text evaluation only (blind to QR)   │───►│ 3. Multimodal & OCR Evasion Hardening (Quishing/Image) │
│ • Static isolated message scoring            │───►│ 4. Full Multi-turn Conversational Progression Analysis │
│ • Theoretical models without moderation      │───►│ 5. Community-Reported Blacklist with Moderator Review  │
└──────────────────────────────────────────────┘    └────────────────────────────────────────────────────────┘
```

---

### 2. Deep Dive: 5 Core Research Gaps & ScamShield Solutions

#### 🔴 Gap 1: Severe Scarcity of Vietnamese Scam Datasets & Language Nuance (Teencode / Tone Variations)
* **Evidence from Master Table:**
  * *Cam et al. (2026)* (VNSED) and *Nguyen-Xuan et al. (2026)* confirm that while English SMS benchmarks (UCI SMS Spam, LSDST-2022) have thousands of samples, high-quality, annotated Vietnamese scam datasets are practically non-existent in public academic repositories.
  * Scammers targeting Vietnamese users heavily exploit teencode (e.g. `c0ng an`, `v4y t1en`), zero-width Unicode characters, and dialectal variations to bypass standard keyword filters.
* **ScamShield Resolution:**
  * Construct the first publicly shared **Vietnamese Scam Dataset (>=500 labeled messages across 5-7 taxonomy categories)** collected from Cục An toàn thông tin (NCSC) alerts, news reports, and crowdsourced submissions.
  * Implement Adversarial Data Augmentation (using LLMs to generate teencode/spelling variants) to ensure robustness against bypass attempts (inspired by *P192*).

---

#### 🔴 Gap 2: The Accuracy-Latency-Cost Trilemma in Real-Time Mobile Deployment
* **Evidence from Master Table:**
  * *Sbei et al. (2025)* and *P471 (Edge-AI Smishing)* demonstrate that massive LLMs achieve superior semantic understanding but suffer from high latency (>2-4s) and recurring API costs ($0.002-$0.01/call), making them impractical for scanning thousands of incoming messages in real-time.
  * Conversely, ultra-lightweight models (BiGRU, Naive Bayes) have sub-millisecond latency (0.25ms) but degrade significantly on complex, unseen scam scenarios (*P446*).
* **ScamShield Resolution (2-Tier Cascaded Architecture):**
  * **Tier 1 (Fast-Path Local Inference):** Fine-tuned `PhoBERT-base` running on FastAPI CPU with **Weighted Binary Cross-Entropy (WBCE)** loss to penalize False Negatives. Classifies 80% of common scam/ham messages in `< 250ms`.
  * **Tier 2 (Cloud LLM Reasoning):** `Gemini-2.0-Flash` / `GPT-4o-mini` with *Few-shot + Scam Taxonomy prompting*. Triggered only when Tier 1 confidence is `< 90%` or when analyzing long multi-turn conversations, achieving `< 3s` latency while reducing API costs by 80%.

---

#### 🔴 Gap 3: Multimodal Threat Blindness (QR Codes / Screenshot Phishing / Evasion Attacks)
* **Evidence from Master Table:**
  * *Hoàng Trần (QuishingShield 2026)* and *Hải Phúc (GRPO-MMS 2026)* emphasize that modern scams have rapidly pivoted to **Quishing (QR Code Phishing)** and sending fraudulent notices as **Images/Screenshots** (fake banking app transfer receipts, fake police arrest warrants) to completely bypass text-based NLP filters.
  * Standard text classifiers (*P472*) acknowledge a major limitation: zero capability to parse visual cues.
* **ScamShield Resolution:**
  * Equip the platform with an **Integrated OCR Engine (Tesseract/PaddleOCR)** to extract textual content from user-uploaded screenshots (Zalo, Messenger, SMS).
  * Embed QR code decoding to extract underlying landing URLs and inspect their domain reputation against Google Safe Browsing and the ScamShield Community Blacklist.

---

#### 🔴 Gap 4: Single-Message Evaluation vs. Multi-Turn Conversational Scam Progression
* **Evidence from Master Table:**
  * Traditional NLP classifiers evaluate isolated messages (e.g. "Hello, is this Mr. Nam?"). In isolation, the message appears legitimate (Ham).
  * However, fraud schemes (pig butchering, job scams) evolve over **5-10 turns of dialogue**, escalating from casual greetings to deposit requests.
* **ScamShield Resolution:**
  * Support **Full Conversation Thread Analysis** (uploading chat transcripts or multi-message screenshots), allowing the AI Engine to detect conversational scam progression and psychological manipulation cues (urgency, authority, financial temptation).

---

#### 🔴 Gap 5: Disconnect Between Academic Classifiers and Community Threat Intelligence
* **Evidence from Master Table:**
  * Almost all 38 academic papers focus purely on static offline model training without operational feedback loops.
  * Once a new scam campaign emerges (e.g. fake VNeID app updates), static models fail until retrained months later.
* **ScamShield Resolution:**
  * Combine AI classification with a **Community Blacklist Platform**:
    * Users report suspicious phone numbers, bank accounts, and URLs.
    * Multi-tier anti-abuse moderation workflow (Moderator review, reputation scoring, duplicate clustering).
    * Real-time Threat Heatmap and Education Hub to protect vulnerable groups (students, elderly).

---

### 3. Conclusion for Capstone Defense & RBL Publication
The unified 38-paper master corpus rigorously validates that **ScamShield's hybrid technological stack (PhoBERT + Gemini Few-Shot + Community Blacklist + OCR)** is directly targeted at resolving the most critical unaddressed gaps in modern cybersecurity literature.
