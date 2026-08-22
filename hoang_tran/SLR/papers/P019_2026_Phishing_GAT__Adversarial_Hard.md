# Paper Evidence Card: P019 (2026)

## Metadata
- **Paper ID:** P019
- **Title:** Phishing GAT: Adversarial-Hardened Phishing Email Detection via Semantic-Structural Fusion and Graph Attention Networks
- **Year:** 2026
- **Venue:** International Journal of Innovative Research in Engineering
- **Verified Link:** https://doi.org/10.59256/ijire.20260704015
- **Authors:** Rohith Kodali, Siva Rama Krishna T Dr
- **Source:** OpenAlex

## Abstract
Phishing email detection has been destabilised by Large Language Models (LLMs), which allow attackers to mass-produce fluent, contextually plausible messages. Detectors tuned on legacy corpora, notably the 2008 CEAS spam collection, consequently report benchmark accuracies that do not survive deployment. We present PhishingGAT, a detector that fuses word-level semantic features with structural ones and is hardened against adversarial perturbation. Each email is represented as an undirected graph whose nodes are unique tokens carrying 100-dimensional GloVe embeddings, and whose edges record co- occurrence inside a three-token sliding window. A two-layer Graph Attention Network (GAT) then learns per-edge importance over that graph. Robustness comes from Projected Gradient Descent (PGD) adversarial training, applied to continuous node features during optimisation only. Training uses a hybrid corpus of 70,716 emails assembled from the CEAS collection, the Enron collection, and curated LLM-generated samples. Evaluation follows two protocols. The first is strictly zero-shot: 1,186 unseen LLM-generated adversarial emails, on which the model reaches 77.40 per cent accuracy and an area under the receiver operating characteristic curve (AUC) of 0.8700. The second is domain-adapted: 401 held-out hard samples, on which accuracy rises to 90.27 per cent and AUC to 0.9717. The 12.87 percentage-point difference between the two is, to our knowledge, the first such measurement reported for graph-based phishing detection, and it quantifies a degradation that same-distribution benchmarks systematically hide. An ablation separates the contribution of attention from that of adversarial defence, and repeated runs across independent random seeds confirm that the reported figures are reproducible rather than seed artefacts.

## PRISMA Audit Checklist
- [x] IC-L: Written in English
- [x] IC-T: Published in academic venue
- [x] IC-E: Quantitative results in Table/Figure
- [x] IC-Y: Published >= 2020
- [x] IC-P: Mobile/SMS/Phishing/Scam text classification task
- [x] IC-I: AI / ML / DL / NLP / LLM / PhoBERT technique
- [x] Verified Live Working URL/DOI
