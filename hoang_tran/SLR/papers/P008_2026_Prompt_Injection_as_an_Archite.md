# Paper Evidence Card: P008 (2026)

## Metadata
- **Paper ID:** P008
- **Title:** Prompt Injection as an Architecture-Specific Attack Surface: Comparing LLM-Based and Traditional ML Spam Classifiers Under Adversarial Conditions
- **Year:** 2026
- **Venue:** Zenodo (CERN European Organization for Nuclear Research)
- **Verified Link:** https://doi.org/10.5281/zenodo.21939849
- **Authors:** Ammar Asif
- **Source:** OpenAlex

## Abstract
Large language models are increasingly deployed for text classification tasks that were previously handled by supervised machine learning. How the two approaches compare under adversarial conditions has received limited systematic attention, particularly in side-by-side evaluations that subject both model families to a single experimental framework. This paper reports a comparative study of three traditional ML classifiers (Naive Bayes, SVM, Logistic Regression) and three LLM-based classifiers (GPT-4, Llama 3 8B, Mistral 7B) on the SMS Spam Collection dataset, evaluated against text perturbation attacks and prompt injection attacks. The principal finding concerns prompt injection. Because TF-IDF classifiers have no mechanism for interpreting natural language instructions, they are structurally immune to instruction-following injection. The open-source LLMs were not. In a sample of ten spam messages, Llama 3 failed to detect all ten under direct instruction override (95% Wilson CI 72.2 to 100 per cent), and Mistral failed to detect nine of ten under role-play injection (95% CI 59.6 to 98.2 per cent). The two models were most vulnerable to different injection strategies, which suggests that a defence tuned to one injection pattern will not generalise across models. GPT-4 failed to detect one of ten spam messages under direct override and none under the other three strategies; at this sample size, however, that result remains consistent with an evasion rate as high as 27.8 per cent, and therefore cannot be read as evidence of robustness. Perturbation results are reported separately for each model family and are not directly comparable, because the attack procedures differ in strength. The traditional ML models faced iterative, importance-ranked attacks and showed attack success rates of 13.5 to 29.4 per cent. The LLMs faced single-pass attacks only, for reasons of computational and API cost. Among the traditional models, the classifier with the best clean accuracy (SVM) degraded the most under attack. These findings should be read as preliminary. The prompt injection sample is small, the dataset is single-domain, and the perturbation attacks use custom implementations rather than reference ones. All interval estimates reported here are Wilson score intervals. Keywords: prompt injection, adversarial robustness, large language models, spam detection, text classification, adversarial machine learning

## PRISMA Audit Checklist
- [x] IC-L: Written in English
- [x] IC-T: Published in academic venue
- [x] IC-E: Quantitative results in Table/Figure
- [x] IC-Y: Published >= 2020
- [x] IC-P: Mobile/SMS/Phishing/Scam text classification task
- [x] IC-I: AI / ML / DL / NLP / LLM / PhoBERT technique
- [x] Verified Live Working URL/DOI
