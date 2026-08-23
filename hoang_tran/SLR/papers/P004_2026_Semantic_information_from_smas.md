# Paper Evidence Card: P004 (2026)

## Metadata
- **Paper ID:** P004
- **Title:** Semantic information from smashed data: text reconstruction attack on phishing detection models in split learning
- **Year:** 2026
- **Venue:** International Journal of Information Security
- **Verified Link:** https://doi.org/10.1007/s10207-026-01311-4
- **Authors:** Yushin Kim, Jungin Kim, Yongseok Kwon, Seyoung Ahn, Sunghyun Cho
- **Source:** OpenAlex

## Abstract
Phishing attacks via desktops, smartphones and internet of things devices are becoming increasingly sophisticated, posing critical security challenges for digital infrastructures. Defending against these attacks requires AI-based detection models that maintain high accuracy, since false positives or negatives can lead to severe breaches, while remaining lightweight enough to run on resource-constrained client devices. Split Learning (SL) meets these requirements by having clients compute only initial model layers locally and transmit intermediate activations (“smashed data”) to a server for the remaining inference, avoiding direct sharing of raw inputs. However, prior work in the image domain has shown that smashed data can leak original content, suggesting that SL may not be safe for user privacy. Therefore, it is essential to investigate whether these privacy risks also extend to language-model–based SL systems, which have fundamentally different neural network architectures, including attention mechanism. This paper introduces the Semantic Information Reconstruction Attack (SIRA), a novel framework designed to infer sensitive semantic elements directly from smashed data by leveraging the generative capabilities of large language models. In experiments on real-world phishing datasets, SIRA outperforms conventional reconstruction attacks in accurately inferring private webpage information. These findings reveal a potential privacy vulnerability in SL-based language models for security applications and motivate the development of targeted defense strategies.

## PRISMA Audit Checklist
- [x] IC-L: Written in English
- [x] IC-T: Published in academic venue
- [x] IC-E: Quantitative results in Table/Figure
- [x] IC-Y: Published >= 2020
- [x] IC-P: Mobile/SMS/Phishing/Scam text classification task
- [x] IC-I: AI / ML / DL / NLP / LLM / PhoBERT technique
- [x] Verified Live Working URL/DOI
