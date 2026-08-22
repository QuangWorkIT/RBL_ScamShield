# Paper Evidence Card: P077 (2026)

## Metadata
- **Paper ID:** P077
- **Title:** RefusalGuard-M: a scalable human–machine framework for multi-turn LLM jailbreak evaluation via semantic refusal manifold modeling
- **Year:** 2026
- **Venue:** Cybersecurity
- **Verified Link:** https://doi.org/10.1186/s42400-026-00633-z
- **Authors:** Michael Tchuindjang, Nathan Duran, Phil Legg, Faiza Medjek
- **Source:** OpenAlex

## Abstract
Abstract Existing multi-turn jailbreak evaluation methods increasingly rely on large language models (LLMs) as automated judges to reduce the cost and scalability limitations of human assessment. However, recent studies show that LLM-based evaluators can diverge from human judgments under adversarial strategies involving subtle linguistic and semantic variations, raising reliability concerns in safety-critical domains such as cybersecurity. To address this challenge, we propose Refusal Manifold Guard (RefusalGuard-M), an open-source semantic evaluation framework that constructs a semantic refusal manifold from human-validated refusal responses for assessing LLM jailbreak interactions, including multi-turn scenarios. RefusalGuard-M uses embedding-based geometric representations to measure deviations from refusal behavior, providing a lightweight, interpretable, and reproducible alternative to LLM-based judging. We evaluate the framework across AdvBench, HarmBench, and CyMulTenSet, covering diverse jailbreak strategies, linguistic transformations, and multi-turn scenarios. Results show that RefusalGuard-M achieves strong agreement with human annotations and comparable recall performance to GPT-based evaluators while adopting a conservative evaluation strategy that prioritizes the detection of harmful outputs. On CyMulTenSet, which evaluates past-tense reformulated multi-turn jailbreaks, RefusalGuard-M achieves up to 0.87 recall, compared with 0.86 for GPT-5 and 0.81 for GPT-4, and reduces inference overhead by up to 3.7 $$\times$$ × relative to embedding-based baselines. These findings demonstrate that semantic refusal representations provide an efficient and scalable approach for jailbreak evaluation, particularly in cybersecurity settings where minimizing missed harmful outputs is critical.

## PRISMA Audit Checklist
- [x] IC-L: Written in English
- [x] IC-T: Published in academic venue
- [x] IC-E: Quantitative results in Table/Figure
- [x] IC-Y: Published >= 2020
- [x] IC-P: Mobile/SMS/Phishing/Scam text classification task
- [x] IC-I: AI / ML / DL / NLP / LLM / PhoBERT technique
- [x] Verified Live Working URL/DOI
