# Paper Evidence Card: P001 (2026)

## Metadata
- **Paper ID:** P001
- **Title:** QuishingShield: on-device multi-modal detection of quick response phishing
- **Year:** 2026
- **Venue:** Computer Science and Information Technologies
- **Verified Link:** https://doi.org/10.11591/csit.v7i3.p271-290
- **Authors:** Shabour Banda, Maronge Musara, Mainford Mutandavari
- **Source:** OpenAlex

## Abstract
Quick response (QR) code phishing (quishing) attacks take advantage of user trust in QR physical and digital media, while currently available protection mechanisms only detect a single dimension signal and are unable to detect cross-modal deception. This paper introduces QuishingShield, an on-device quishing detection system based on multi-modal deep learning which preserves privacy on mobile platforms. Cross-modal attention fusion is used to combine visual poster features, optical character recognition (OCR) recognized surrounding text and recognized uniform resource locator (URL) structure, as well as network reputation signals in a system. A teacher model is trained on 205,488 real-world QR code poster samples from 45 countries and 23 languages, and the knowledge is distilled into a compact model for the student model, in order to be deployed in mobile applications. The student has an accuracy of 95.55% and a recall of 98.18% for a held-out test set, with an inference latency of 25.34 ms on mobile devices, all of which are at or below the deployment targets. Robustness of 95.00% when tested adversarially on four sets of attacks. The multi-modal fusion approach enhances performance by 5.17-11.07 percentage points over the unimodal baseline approaches (p0.001). QuishingShield, to our best knowledge, is the first validated multi-modal quishing detection system satisfying accuracy, speed, size and privacy requirement for mobile deployment.

## PRISMA Audit Checklist
- [x] IC-L: Written in English
- [x] IC-T: Published in academic venue
- [x] IC-E: Quantitative results in Table/Figure
- [x] IC-Y: Published >= 2020
- [x] IC-P: Mobile/SMS/Phishing/Scam text classification task
- [x] IC-I: AI / ML / DL / NLP / LLM / PhoBERT technique
- [x] Verified Live Working URL/DOI
