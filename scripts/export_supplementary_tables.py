import os
import json
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
SUPP_DIR = os.path.join(ROOT_DIR, "supplementary_repo")

TABLES_DIR = os.path.join(SUPP_DIR, "tables")
PROMPTS_DIR = os.path.join(SUPP_DIR, "prompts")
LATEX_DIR = os.path.join(SUPP_DIR, "latex")
SCRIPTS_DIR = os.path.join(SUPP_DIR, "scripts")

for d in [TABLES_DIR, PROMPTS_DIR, LATEX_DIR, SCRIPTS_DIR]:
    os.makedirs(d, exist_ok=True)

# -------------------------------------------------------------
# TABLE S1: Comparative Threat Detection Studies vs ScamShield-VN
# -------------------------------------------------------------
s1_data = [
    ["Study", "Language", "Model / Architecture", "Evaluation Dataset", "Key Metric", "Primary Limitation / Research GAP"],
    ["Tuan et al. (2023)", "Vietnamese", "PhoBERT, CNN, LSTM", "Multi-accent SMS (N~3,000)", "Acc: 95.56%", "Evaluated under symmetric loss; vulnerable to noisy word-segmentation failures."],
    ["Nguyen-Xuan et al. (2026)", "Viet-Eng", "MLTEA Dual-Encoder", "Code-mixed Phishing", "F1: 0.940", "Cloud-scale dual-encoder; prohibitive inference latency for edge mobile integration."],
    ["Cam & Binh (2026)", "Vietnamese", "PhoBERT, BiLSTM", "VNSED Email Corpus", "Acc: 86.47%", "Limited coverage of colloquial teencode; elevated false negative rate on subtle spam."],
    ["Zhou et al. (2026)", "Multilingual", "GPT-4o, Claude, Gemini", "FraudSMSWalker (N~4,000)", "Recall: 64.16--90.13%", "Severe alarm fatigue on legitimate traffic (benign recall collapsed to 12.81--30.25%)."],
    ["Banda et al. (2026)", "English", "Distilled SLM (Llama-3.2-3B)", "QR/Text Lures (N=4,200)", "Latency: 25.3--45 ms", "Focused on multi-modal English lures; non-trivial mobile memory footprint."],
    ["Phap et al. (2026)", "English", "BiGRU + MaskedPool + WBCE", "UCI & LSDST (N=5,574)", "Latency: 0.25 ms", "Recurrent architecture evaluated on English; lacks self-attention context for low-resource slang."],
    ["This Work (ScamShield-VN)", "Vietnamese", "Two-Tier: ViSoBERT + 3-Agent Council", "Unified SMS (N=2,664 / 384)", "Recall: 97.11%, FPR: 2.37%", "Exploratory trade-off: 267.5 ms, 0.00% bank FPR (N=19), $0.0153/1k SMS, edge privacy preservation."]
]

def write_csv(filepath, rows):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def write_md_table(filepath, title, headers, rows, note=""):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for r in rows:
            f.write("| " + " | ".join(str(c) for c in r) + " |\n")
        if note:
            f.write(f"\n> **Note:** {note}\n")

def write_tex_table(filepath, label, caption, headers, rows, col_align=None, note=""):
    if not col_align:
        col_align = "l" * len(headers)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\\begin{table*}[t]\n\\centering\n")
        f.write(f"\\caption{{{caption}}}\n")
        f.write(f"\\label{{{label}}}\n")
        f.write("\\resizebox{\\textwidth}{!}{%\n")
        f.write(f"\\begin{{tabular}}{{{col_align}}}\n\\toprule\n")
        f.write(" & ".join(f"\\textbf{{{h}}}" for h in headers) + " \\\\\n\\midrule\n")
        for r in rows:
            clean_row = [str(c).replace("%", "\\%").replace("$", "\\$").replace("_", "\\_") for c in r]
            f.write(" & ".join(clean_row) + " \\\\\n")
        f.write("\\bottomrule\n\\end{tabular}%\n}\n")
        if note:
            clean_note = note.replace("%", "\\%").replace("$", "\\$").replace("_", "\\_")
            f.write(f"\\par\\vspace{{6pt}}\n\\parbox{{\\textwidth}}{{\\footnotesize \\textit{{Note:}} {clean_note}}}\n")
        f.write("\\end{table*}\n")

# Write Table S1
write_csv(os.path.join(TABLES_DIR, "Table_S1_literature_overview.csv"), s1_data)
write_md_table(os.path.join(TABLES_DIR, "Table_S1_literature_overview.md"),
               "Supplementary Table S1: Comparative Overview of Representative Threat Detection Studies vs. Proposed ScamShield-VN",
               s1_data[0], s1_data[1:],
               "Reported metrics are extracted from corresponding publications evaluated on heterogeneous datasets, hardware environments, and task formulations; they illustrate comparative architectural paradigms rather than direct benchmark parity.")
write_tex_table(os.path.join(TABLES_DIR, "Table_S1_literature_overview.tex"),
                "tab:supp_related_work",
                "Supplementary Table S1: Comparative Overview of Representative Threat Detection Studies vs. Proposed ScamShield-VN",
                s1_data[0], s1_data[1:], "lllllp{5.0cm}",
                "Reported metrics are extracted from corresponding publications evaluated on heterogeneous datasets, hardware environments, and task formulations; they illustrate comparative architectural paradigms rather than direct benchmark parity.")

# -------------------------------------------------------------
# TABLE S2: Model Specifications Across Tiers and Arms
# -------------------------------------------------------------
s2_data = [
    ["Role / Arm", "Model Identifier", "Provider / Runtime", "Temp.", "Execution / Fallback"],
    ["Tier 1 Edge Screener", "uitnlp/visobert", "ONNX Runtime (CPU)", "N/A", "INT8 Quantized (70.7 ms)"],
    ["Tier 1 Baseline B2.1", "vinai/phobert-base-v2", "HuggingFace (PyTorch)", "N/A", "FP16 Fine-tuned"],
    ["Tier 1 Baseline B2.2", "FPTAI/vibert-base-cased", "HuggingFace (PyTorch)", "N/A", "FP16 Fine-tuned"],
    ["Tier 1 Baseline B2.3", "vinai/phobert-large", "HuggingFace (PyTorch)", "N/A", "FP16 Fine-tuned"],
    ["Tier 1 Baseline B3", "gemini-3.5-flash", "Google AI Studio API", "0.0", "5-shot ICL (4--60 s backoff)"],
    ["Tier 2 Maker (Seat A/B)", "gpt-6.1-sol", "OpenAI (via proxy)", "0.1", "Circuit breaker -> standby"],
    ["Tier 2 Fast (Arm 2)", "gemini-3.5-flash-lite", "Google AI Studio API", "0.1", "Circuit breaker -> standby"],
    ["Tier 2 Defender (Seat C)", "gemini-3.8-flash", "Google AI Studio API", "0.1", "Circuit breaker -> standby"],
    ["Tier 2 Baseline P-single", "gpt-6.1-sol", "OpenAI (via proxy)", "0.1", "Regex repair -> fallback"],
    ["Tier 2 Baseline PoLL", "claude-sonnet-5", "Anthropic (via proxy)", "0.1", "Zero-shot unweighted vote"]
]

write_csv(os.path.join(TABLES_DIR, "Table_S2_model_specifications.csv"), s2_data)
write_md_table(os.path.join(TABLES_DIR, "Table_S2_model_specifications.md"),
               "Supplementary Table S2: Complete Model Specifications Across Experimental Tiers and Baseline Arms",
               s2_data[0], s2_data[1:],
               "Evaluation conducted Oct 18--20, 2026. Complete API contracts and schemas archived in config/.")
write_tex_table(os.path.join(TABLES_DIR, "Table_S2_model_specifications.tex"),
                "tab:supp_model_specs",
                "Supplementary Table S2: Complete Model Specifications Across Experimental Tiers and Baseline Arms",
                s2_data[0], s2_data[1:], "lllcl",
                "Evaluation conducted Oct 18--20, 2026. Complete API contracts and schemas archived in config/.")

# -------------------------------------------------------------
# TABLE S3: Comprehensive 2 x 3 Confusion Matrices Across Council Configurations (N=117)
# -------------------------------------------------------------
s3_headers = ["Configuration / Arm", "Scam Pred SCAM-RISK", "Scam Pred LOW-RISK", "Scam Pred UNKNOWN", "Benign Pred SCAM-RISK", "Benign Pred LOW-RISK", "Benign Pred UNKNOWN", "Benign FPR (%)", "95% Clopper-Pearson CI", "Total Abstentions"]
s3_rows = [
    ["Arm 1: Full 5-Agent Council", 92, 2, 4, 0, 19, 0, "0.00%", "[0.00%, 17.65%]", 4],
    ["Arm 2: Proposed 3-Agent (With Defender)", 87, 1, 10, 0, 19, 0, "0.00%", "[0.00%, 17.65%]", 10],
    ["Arm 3: 3-Agent (No Defender, 2 seats)", 89, 2, 7, 2, 17, 0, "10.53%", "[1.30%, 33.14%]", 7],
    ["Arm 4: 3-Agent (Defender No Veto)", 88, 1, 9, 1, 18, 0, "5.26%", "[0.13%, 26.03%]", 9],
    ["Baseline P-single (Wang et al.)", 94, 2, 2, 0, 19, 0, "0.00%", "[0.00%, 17.65%]", 2]
]

write_csv(os.path.join(TABLES_DIR, "Table_S3_confusion_matrices_2x3.csv"), [s3_headers] + s3_rows)
write_md_table(os.path.join(TABLES_DIR, "Table_S3_confusion_matrices_2x3.md"),
               "Supplementary Table S3: Comprehensive 2 x 3 Confusion Matrices and Verdict Accounting Across Council Configurations (N=117 Hard Challenge Suite)",
               s3_headers, s3_rows,
               "Ground-truth counts: N_scam = 98, N_benign = 19, Total N = 117. FPR 95% CIs are exact two-sided Clopper-Pearson intervals.")
write_tex_table(os.path.join(TABLES_DIR, "Table_S3_confusion_matrices_2x3.tex"),
                "tab:supp_matrix_2x3",
                "Supplementary Table S3: Comprehensive 2 x 3 Confusion Matrices and Verdict Accounting Across Council Configurations (N=117 Hard Challenge Suite)",
                s3_headers, s3_rows, "lccccccccc",
                "Ground-truth counts: N_scam = 98, N_benign = 19, Total N = 117. FPR 95% CIs are exact two-sided Clopper-Pearson intervals.")

# -------------------------------------------------------------
# TABLE S4: Threshold Sensitivity Profiling across tau in [0.70, 0.95]
# -------------------------------------------------------------
s4_headers = ["Threshold tau", "Accuracy (%)", "Scam Recall (%)", "FPR (%)", "Mean Latency (ms)", "Cost / 1k SMS", "Escalation Rate (%)"]
s4_rows = [
    ["tau = 0.70", "96.35%", "95.38%", "2.84%", "99.5 ms", "$0.0023", "0.5%"],
    ["tau = 0.80", "96.61%", "95.38%", "2.37%", "162.7 ms", "$0.0072", "1.6%"],
    ["tau = 0.85", "97.14%", "96.53%", "2.37%", "220.2 ms", "$0.0117", "2.6%"],
    ["tau = 0.90", "97.40%", "97.11%", "2.37%", "267.5 ms", "$0.0153", "3.4%"],
    ["tau = 0.95", "97.92%", "97.11%", "1.42%", "668.2 ms", "$0.0410", "9.1%"]
]

write_csv(os.path.join(TABLES_DIR, "Table_S4_threshold_sensitivity_sweeps.csv"), [s4_headers] + s4_rows)
write_md_table(os.path.join(TABLES_DIR, "Table_S4_threshold_sensitivity_sweeps.md"),
               "Supplementary Table S4: Exploratory Routing Threshold Sensitivity Profiling Across tau in [0.70, 0.95]",
               s4_headers, s4_rows,
               "Evaluated across N=384 exploratory development messages (211 Ham, 173 Scam). Operating threshold tau = 0.90 was adopted as the production baseline.")
write_tex_table(os.path.join(TABLES_DIR, "Table_S4_threshold_sensitivity_sweeps.tex"),
                "tab:tau_ablation",
                "Supplementary Table S4: Exploratory Routing Threshold Sensitivity Profiling Across tau in [0.70, 0.95]",
                s4_headers, s4_rows, "ccccccc",
                "Evaluated across N=384 exploratory development messages (211 Ham, 173 Scam). Operating threshold tau = 0.90 was adopted as the production baseline.")

# -------------------------------------------------------------
# TABLE S5: Source Breakdown and Class Balance Across Partitions
# -------------------------------------------------------------
s5_headers = ["Corpus Partition", "Corpus Origin", "External Feeds", "Ham (y=0)", "Scam (y=1)"]
s5_rows = [
    ["Training / Internal Val (N=2,397)", "2,397 (2,363 uitnlp, 34 phishing)", "0", "1,726 (72.0%)", "671 (28.0%)"],
    ["Frozen Test Partition (N=267)", "267 (266 uitnlp, 1 phishing)", "0", "192 (71.9%)", "75 (28.1%)"],
    ["Hard Forensic Suite (N=117)", "109 (99 train, 10 frozen test)", "8", "19 (16.2%)", "98 (83.8%)"],
    ["Combined Exploratory (N=384)", "376 (with 10 duplicate strings)", "8", "211 (54.9%)", "173 (45.1%)"],
    ["Total Unified Corpus (N=2,664)", "2,664 (2,629 uitnlp, 35 phishing)", "0", "1,918 (72.0%)", "746 (28.0%)"]
]

write_csv(os.path.join(TABLES_DIR, "Table_S5_dataset_partitions_breakdown.csv"), [s5_headers] + s5_rows)
write_md_table(os.path.join(TABLES_DIR, "Table_S5_dataset_partitions_breakdown.md"),
               "Supplementary Table S5: Source Breakdown and Class Balance Across Corpus Partitions",
               s5_headers, s5_rows,
               "Ground truth verification disclosure: upstream kappa=0.88 cited during corpus collection cannot be independently verified from contingency logs, labels treated as unverified externally.")
write_tex_table(os.path.join(TABLES_DIR, "Table_S5_dataset_partitions_breakdown.tex"),
                "tab:dataset_sources",
                "Supplementary Table S5: Source Breakdown and Class Balance Across Corpus Partitions",
                s5_headers, s5_rows, "lcccc",
                "Ground truth verification disclosure: upstream kappa=0.88 cited during corpus collection cannot be independently verified from contingency logs, labels treated as unverified externally.")

# -------------------------------------------------------------
# TABLE S6: Paired McNemar Test Analysis across Model Configurations (alpha=0.05)
# -------------------------------------------------------------
s6_headers = ["Pairwise Comparison", "b", "c", "chi2_cont", "Exact p-value", "Odds Ratio", "Reject H0?"]
s6_rows = [
    ["Panel A: Tier 1 Edge vs Baselines (Frozen Holdout N=267)", "", "", "", "", "", ""],
    ["ViSoBERT vs. PhoBERT-base-v2", 10, 6, "0.5625", "0.4545", "1.67", "False (p >= 0.05)"],
    ["ViSoBERT vs. FPT ViBERT-base", 11, 7, "0.5000", "0.4807", "1.57", "False (p >= 0.05)"],
    ["ViSoBERT vs. PhoBERT-large", 7, 7, "0.0714", "1.0000", "1.00", "False (p >= 0.05)"],
    ["ViSoBERT vs. Gemini 3.5 Flash", 33, 3, "23.3611", "p < 0.0001", "11.00", "True (p < 0.0001)"],
    ["Panel B: Tier 2 Council Ablation (Hard Forensic N=117)", "", "", "", "", "", ""],
    ["3-Agent (Arm 2) vs. 5-Agent (Arm 1)", 5, 0, "3.2000", "0.0625", "inf", "False (p >= 0.05)"]
]

write_csv(os.path.join(TABLES_DIR, "Table_S6_mcnemar_statistical_tests.csv"), [s6_headers] + s6_rows)
write_md_table(os.path.join(TABLES_DIR, "Table_S6_mcnemar_statistical_tests.md"),
               "Supplementary Table S6: Paired McNemar Test Analysis across Model Configurations (alpha=0.05)",
               s6_headers, s6_rows,
               "Panel A evaluates released ONNX INT8 model vs baseline transformers (N=267). Panel B compares 3-Agent vs 5-Agent consensus decisions on sanitized payloads (N=117).")
write_tex_table(os.path.join(TABLES_DIR, "Table_S6_mcnemar_statistical_tests.tex"),
                "tab:mcnemar",
                "Supplementary Table S6: Paired McNemar Test Analysis across Model Configurations (alpha=0.05)",
                s6_headers, s6_rows, "lcccccc",
                "Panel A evaluates released ONNX INT8 model vs baseline transformers (N=267). Panel B compares 3-Agent vs 5-Agent consensus decisions on sanitized payloads (N=117).")

# -------------------------------------------------------------
# TABLE S7: Multi-Seed Benchmark across 5 Runs and INT8 Frozen Holdout
# -------------------------------------------------------------
s7_headers = ["Model Configuration", "Role / Category", "Parameters", "Accuracy (%)", "Precision (%)", "Scam Recall (%)", "Scam-F1 (%)", "Model Size"]
s7_rows = [
    ["ViSoBERT + WBCE (alpha=5.0)", "Proposed (Tier 1 Edge)", "97.57M", "95.65 +/- 1.54", "89.79 +/- 5.15", "95.64 +/- 2.04", "92.51 +/- 2.39", "98.42 MB (INT8)"],
    ["PhoBERT-large", "Baseline B2.3 (370M)", "370M", "95.95 +/- 1.57", "93.13 +/- 3.17", "92.33 +/- 3.44", "92.70 +/- 2.87", "1,480 MB"],
    ["FPT ViBERT-base", "Baseline B2.2", "124M", "95.04 +/- 1.11", "90.10 +/- 4.12", "92.60 +/- 2.84", "91.25 +/- 1.81", "480 MB"],
    ["PhoBERT-base-v2", "Baseline B2.1", "135M", "95.11 +/- 0.83", "91.24 +/- 1.52", "91.23 +/- 1.84", "91.23 +/- 1.50", "540 MB"],
    ["Gemini 3.5 Flash (5-shot ICL)", "Baseline B3 (Cloud API)", "Proprietary", "84.50 +/- 1.02", "64.47 +/- 1.52", "100.00 +/- 0.00", "78.38 +/- 1.12", "Cloud API"]
]

write_csv(os.path.join(TABLES_DIR, "Table_S7_multiseed_benchmark_5runs.csv"), [s7_headers] + s7_rows)
write_md_table(os.path.join(TABLES_DIR, "Table_S7_multiseed_benchmark_5runs.md"),
               "Supplementary Table S7: Multi-Seed Validation Performance across 5 Independent Training Runs (K=5) and Released INT8 Model Benchmark on Locked Frozen Holdout (N=267)",
               s7_headers, s7_rows,
               "Reported F1 denotes class-specific Scam-F1. Macro-F1 across both classes for ViSoBERT is 94.51% +/- 0.96%. Holdout scam recall at theta=0.90 is exactly 72/75 = 96.00% (exact 95% Clopper-Pearson CI: [88.75%, 99.17%], 8/192 = 4.17% FPR).")
write_tex_table(os.path.join(TABLES_DIR, "Table_S7_multiseed_benchmark_5runs.tex"),
                "tab:benchmark_summary",
                "Supplementary Table S7: Multi-Seed Validation Performance across 5 Independent Training Runs (K=5) and Released INT8 Model Benchmark on Locked Frozen Holdout (N=267)",
                s7_headers, s7_rows, "llcccccc",
                "Reported F1 denotes class-specific Scam-F1. Macro-F1 across both classes for ViSoBERT is 94.51% +/- 0.96%. Holdout scam recall at theta=0.90 is exactly 72/75 = 96.00% (exact 95% Clopper-Pearson CI: [88.75%, 99.17%], 8/192 = 4.17% FPR).")

print("All 7 supplementary tables successfully exported in CSV, Markdown, and LaTeX formats.")
