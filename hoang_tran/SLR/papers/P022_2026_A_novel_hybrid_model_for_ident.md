# Paper Evidence Card: P022 (2026)

## Metadata
- **Paper ID:** P022
- **Title:** A novel hybrid model for identifying the most informative instances for improving text data classification
- **Year:** 2026
- **Venue:** PLoS ONE
- **Verified Link:** https://doi.org/10.1371/journal.pone.0355603
- **Authors:** Amira Abdelwahab, Mohamed Salama
- **Source:** OpenAlex

## Abstract
The rapid growth of user-generated textual content on the internet has intensified the need for accurate and scalable text classification methods. However, supervised learning approaches remain heavily constrained by the high cost and effort required for manual data annotation, particularly in large and heterogeneous datasets. To address this challenge, this paper proposes a novel hybrid active learning framework for efficient classification of unlabeled text data. The proposed approach integrates multiple classical machine learning classifiers-Support Vector Machines, Logistic Regression, Naive Bayes, and Random Forest-within a hybrid ensemble architecture, combined with a pool-based active learning strategy to iteratively select the most informative unlabeled instances for annotation. Textual data are transformed into numerical representations using several feature extraction techniques, including Bag-of-Words, TF-IDF, Word2Vec, and BERT-based embeddings, allowing for a comprehensive evaluation of representation effectiveness. Extensive experiments are conducted on four diverse benchmark datasets from healthcare, finance, spam detection, and e-commerce domains. The results consistently demonstrate that the proposed hybrid active learning model outperforms traditional ensemble classifiers across all datasets and evaluation metrics. In particular, TF-IDF-based hybrid ensembles achieve the highest gains in accuracy, precision, recall, and F1 score, while requiring substantially fewer labeled instances. Furthermore, the proposed framework exhibits strong robustness in imbalanced classification scenarios, significantly improving minority class detection. Overall, the findings confirm that combining hybrid ensemble learning with active learning offers an effective, lightweight, and cost-efficient alternative to purely transformer-based approaches, making it well-suited for real-world text classification tasks where labeled data are scarce or expensive.

## PRISMA Audit Checklist
- [x] IC-L: Written in English
- [x] IC-T: Published in academic venue
- [x] IC-E: Quantitative results in Table/Figure
- [x] IC-Y: Published >= 2020
- [x] IC-P: Mobile/SMS/Phishing/Scam text classification task
- [x] IC-I: AI / ML / DL / NLP / LLM / PhoBERT technique
- [x] Verified Live Working URL/DOI
