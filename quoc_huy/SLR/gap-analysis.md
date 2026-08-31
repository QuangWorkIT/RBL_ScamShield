# Gap Analysis: SMS and Phishing Threat Detection

Based on the recent literature surrounding SMS, phishing email, and cross-channel threat detection, several key research gaps have been identified:

## 1. Vulnerability to Adversarial Attacks and Evasions
While deep learning and transformer-based models (such as RoBERTa and DeBERTa) show excellent performance on clean datasets, they are highly vulnerable to adversarial text perturbations. Attackers can leverage LLMs to generate semantically-lossless variations of phishing content (e.g., character swapping or synonym replacement) that evade current detectors. Frameworks like *Genshin* and *PEEK* show that without defensive mechanisms that proactively augment data via adversarial training or text recovery, existing systems suffer severe accuracy drops.

## 2. Evaluation on Multi-step, Cross-channel Fraud
Most current spam and phishing detection models are evaluated on single-modality datasets (e.g., text-only SMS or email). There is a significant gap in evaluating models on multi-step interactions, such as SMS-to-Webpage chains. When webpage features are included, current benchmarks often expose URL and domain reputation shortcuts. When these shortcuts are masked, state-of-the-art agentic LLMs struggle to make evidence-grounded decisions (as highlighted by *FraudSMSWalker*).

## 3. Benign Recall and False Positive Control
Current large language models often achieve high fraud recall but suffer from extremely low benign recall. This means they frequently flag legitimate service flows (which may include normal login forms, payment widgets, or verification steps) as fraudulent. The inability of models to discern contextual legitimacy and their tendency to over-claim based on superficial interface cues remain a major gap in deploying these systems securely.

## 4. Text Feature Representation Limitations
Traditional machine learning approaches paired with simple feature extractors like TF-IDF or Bag-of-Words fail to capture deep semantic and contextual relationships, leading to high false-positive rates on complex attacks. Even when incorporating advanced embeddings like BERT, there is a gap in effectively processing domain-specific slang, pidgin, or highly abbreviated text common in SMS environments. 

## 5. Data Imbalance and Over-reliance on Synthetic Data
Datasets in cybersecurity are inherently imbalanced. While LLMs (like GPT-4 or Llama 3.1) can generate synthetic data to balance datasets, naively relying on them introduces bias and sometimes results in synthetic data that lacks the subtle structural diversity of real-world attacks. Generative Adversarial Networks (GANs) combined with LLMs (e.g., *PEEK*) offer a pathway, but there is still a gap in generating sufficiently diverse, multi-topic, and robust synthetic threat datasets autonomously.

## 6. Multimodal Phishing Detection
Most existing defense frameworks and synthetic data generators focus exclusively on plain text. However, modern phishing campaigns increasingly utilize multimodal vectors, such as QR codes, image-based notifications, or audio messages. There is a glaring gap in extending text-based LLM defenses and adversarial training methodologies to multimodal phishing simulations.

## 7. Model Explainability and Trustworthiness
Transformer-based models operate as "black boxes." There is a gap in end-user trust due to the lack of transparency in how predictions are made. Although tools like LIME, SHAP, and Transformers Interpret exist, they often produce conflicting attribution scores for the same inputs. Hybrid approaches (such as LITA) and cascading frameworks are needed to provide consistent, unified, and human-understandable explanations for cybersecurity applications.
