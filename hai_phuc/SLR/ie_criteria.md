# Inclusion and Exclusion Criteria (ie_criteria.md)

This document defines the criteria for selecting and rejecting papers during the screening phases for the ScamShield Systematic Literature Review (SLR).

## Inclusion Criteria (IC)
Papers MUST meet ALL of the following criteria to be included:

### Fixed Criteria
* **IC-L:** Written in English.
* **IC-T:** Published in a conference or journal (excluding blogs, whitepapers, theses).
* **IC-E:** Contains at least one quantitative result (number) in a Table or Figure.

### Project-Specific Criteria
* **IC-Y (Year):** Published from 2020 onwards (rationale: GPT-3 and the rise of prompt-based LLMs began in 2020, making it a suitable baseline for comparing PLMs and LLMs).
* **IC-P (Problem/Task):** Focuses on text classification for spam, phishing, scam, or fraud detection in textual communications (e.g., SMS, chat messages, emails).
* **IC-I (Intervention):** Utilizes or evaluates Pre-trained Language Models (PLMs, e.g., BERT, RoBERTa, PhoBERT) or Large Language Models (LLMs, e.g., GPT, LLaMA) using fine-tuning or prompt-based techniques (zero-shot, few-shot).

## Exclusion Criteria (EC)
Papers meeting ANY of the following criteria will be excluded:

### Fixed Criteria
* **EC-D:** Duplicated with an already included paper.
* **EC-A:** Full-text is unavailable or inaccessible.
* **EC-S:** Less than 4 pages (e.g., abstract-only, short poster).
* **EC-N:** No empirical experiment or evaluation (e.g., vision paper, tutorial, pure survey without novel experiments).

### Project-Specific Criteria
* **EC-O (Out of Scope):** Focuses solely on voice/audio spam detection, image-based phishing detection (e.g., analyzing website layouts/screenshots), network traffic analysis, or malware binary analysis without a primary focus on natural language text processing.
