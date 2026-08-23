# Paper Evidence Card: P089 (2026)

## Metadata
- **Paper ID:** P089
- **Title:** TARA: Task-Adaptive Rank Allocation for Efficient Large Language Model Fine-Tuning in Geo-Information Text Classification
- **Year:** 2026
- **Venue:** ISPRS International Journal of Geo-Information
- **Verified Link:** https://doi.org/10.3390/ijgi15080372
- **Authors:** Canhui Wang, Juntao Shen, Yicong Feng, Jin Huang, Yanwu Jing, Weiwei Chen, Wanqiang Zhang, Min Wang
- **Source:** OpenAlex

## Abstract
Geo-information texts, including geospatial data-use regulations and Earth observation metadata, are central to data governance and compliance auditing in remote sensing ecosystems. Full fine-tuning of large pre-trained language models is often computationally impractical, while standard LoRA reduces cost but assigns a fixed rank to all adapted modules, ignoring differences across layers and projection types. This paper proposes TARA, a task-adaptive rank allocation method for LoRA-based fine-tuning. TARA assigns learnable importance scores to rank dimensions and uses Gumbel–Sigmoid sampling with the Straight-Through Estimator to learn discrete rank masks under a global sparsity constraint. We further construct RSRegulation, a geospatial regulatory compliance benchmark containing 4032 English-language samples derived from 168 clauses across seven regulatory and policy sources with clause-level data isolation. Across five random seeds, TARA achieves 95.30 ± 0.10% accuracy and 95.44 ± 0.10% F1 with a maximum trainable adapter budget of 1.57 M parameters. The learned soft allocation corresponds to approximately 0.38 M effective adapter parameters and 75.8% soft rank compression. Physical hard pruning reduces the deployed adapter to 0.086 M parameters while retaining 95.12 ± 0.11% accuracy and 95.21 ± 0.10% F1. Layer-wise analysis shows that value projections retain higher ranks than query projections under the current task and backbone, revealing a task-dependent non-uniform allocation pattern.

## PRISMA Audit Checklist
- [x] IC-L: Written in English
- [x] IC-T: Published in academic venue
- [x] IC-E: Quantitative results in Table/Figure
- [x] IC-Y: Published >= 2020
- [x] IC-P: Mobile/SMS/Phishing/Scam text classification task
- [x] IC-I: AI / ML / DL / NLP / LLM / PhoBERT technique
- [x] Verified Live Working URL/DOI
