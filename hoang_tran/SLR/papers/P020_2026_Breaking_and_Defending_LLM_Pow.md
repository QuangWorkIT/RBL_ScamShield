# Paper Evidence Card: P020 (2026)

## Metadata
- **Paper ID:** P020
- **Title:** Breaking and Defending LLM-Powered Social Media Bot Detection Systems †
- **Year:** 2026
- **Venue:** Pragmatic Cybersecurity
- **Verified Link:** https://doi.org/10.53941/pc.2026.100010
- **Authors:** Yoni Birman, Nof Orenstein
- **Source:** OpenAlex

## Abstract
The rise of social media bots poses a persistent threat, enabling misinformation, public opinion manipulation, and erosion of trust in online platforms. To combat this, machine learning systems have been developed to detect and limit bot activity. However, attackers continuously adapt through adversarial optimization, behavior imitation, and semantic manipulation strategies, creating an escalating arms race with detection tools. Recent advances in LLMs have significantly improved bot detection by enabling deeper semantic and contextual analysis. However, this shift also introduces new attack surfaces, allowing adversaries to craft exploits that directly target LLM reasoning and generation mechanisms. Industry tools like Anthropic’s Claude Code Security similarly leverage LLMs for security, motivating our study of their attack surfaces. In this work, we explore both offensive and defensive aspects of LLM-powered, threat-specific cybersecurity applications. While centered on the challenge of social media bot detection, our methodology and insights generalize to a broad class of LLM-powered cybersecurity systems, including phishing detection, email classification, fraud analysis, and more. We introduce two novel adversarial attack strategies that systematically exploit semantic and contextual weaknesses of LLM-based classifiers, degrading LLM performance in bot detection by up to 48%, and propose a robust multi-LLM defense architecture designed to preserve detection reliability under adaptive adversarial conditions. Our solution, LSABRE, is a multi-LLM framework that improves robustness across various attacks, maintaining 86% detection accuracy even under strong adaptive adversarial attacks.

## PRISMA Audit Checklist
- [x] IC-L: Written in English
- [x] IC-T: Published in academic venue
- [x] IC-E: Quantitative results in Table/Figure
- [x] IC-Y: Published >= 2020
- [x] IC-P: Mobile/SMS/Phishing/Scam text classification task
- [x] IC-I: AI / ML / DL / NLP / LLM / PhoBERT technique
- [x] Verified Live Working URL/DOI
