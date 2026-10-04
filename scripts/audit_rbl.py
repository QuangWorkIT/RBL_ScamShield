"""
Comprehensive RBL Audit Script
Strictly audits all files and gates against rbl_docs/01-06 guidelines.
"""
import os
import sys
import csv
import re

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"C:\Users\USER\RBL_ScamShield"

print("="*60)
print("AUDIT RBL SCAMSHIELD-VN (PHASES 1-5)")
print("="*60)

# 1. Check Members and SLR files
members = ['trung_hieu', 'quoc_huy', 'hai_phuc', 'hoang_tran', 'minh_quang']
required_slr_files = [
    'search-log.md',
    '01_all_records.csv',
    '02_after_screening_v1.csv',
    '03_final_included.csv',
    'prisma-flow.md',
    'evidence-table.md',
    'rq-check.md'
]

print("\n--- 1. AUDIT MEMBER SLR FILES & CRITERIA ---")
for m in members:
    slr_dir = os.path.join(ROOT, m, "SLR")
    files = os.listdir(slr_dir) if os.path.exists(slr_dir) else []
    missing = [f for f in required_slr_files if f not in files]
    
    # Counts
    c01, c02, c03 = 0, 0, 0
    f01 = os.path.join(slr_dir, "01_all_records.csv")
    f02 = os.path.join(slr_dir, "02_after_screening_v1.csv")
    f03 = os.path.join(slr_dir, "03_final_included.csv")
    
    if os.path.exists(f01):
        with open(f01, encoding='utf-8', errors='ignore') as f:
            c01 = max(0, sum(1 for _ in csv.reader(f)) - 1)
    if os.path.exists(f02):
        with open(f02, encoding='utf-8', errors='ignore') as f:
            c02 = max(0, sum(1 for _ in csv.reader(f)) - 1)
    if os.path.exists(f03):
        with open(f03, encoding='utf-8', errors='ignore') as f:
            c03 = max(0, sum(1 for _ in csv.reader(f)) - 1)
            
    status = "PASS" if (len(missing) == 0 and c03 >= 6) else "WARNING"
    print(f"[{status:7}] Member: {m:12} | Included papers: {c03:2d} (Req >= 6) | Missing files: {missing}")

# 2. Check team-synthesis
print("\n--- 2. AUDIT TEAM-SYNTHESIS & PRISMA-TEAM ---")
ts_dir = os.path.join(ROOT, "team-synthesis")
ts_files = os.listdir(ts_dir) if os.path.exists(ts_dir) else []
req_ts = [
    'ie_criteria.md',
    'evidence-table-merged.md',
    'prisma-team.md',
    'rq-evidence-map.md',
    'rq-validation.md',
    'proposal.md'
]
missing_ts = [f for f in req_ts if f not in ts_files]
print(f"Missing team-synthesis files: {missing_ts}")

merged_path = os.path.join(ts_dir, "evidence-table-merged.md")
merged_count = 0
if os.path.exists(merged_path):
    with open(merged_path, encoding='utf-8', errors='ignore') as f:
        for line in f:
            line_s = line.strip()
            if line_s.startswith("|") and ("`M" in line_s or "M0" in line_s) and "Master ID" not in line_s:
                merged_count += 1
print(f"Merged Evidence Table Paper Count: {merged_count} (Req >= 12)")

# 3. Check Phase 3 & 4 (Data, Scripts, Results)
print("\n--- 3. AUDIT EXPERIMENTAL ARTIFACTS (PHASES 3 & 4) ---")
checks = {
    "data/raw/README.md": os.path.exists(os.path.join(ROOT, "data", "raw", "README.md")),
    "results/summary.csv": os.path.exists(os.path.join(ROOT, "results", "summary.csv")),
    "results/summary_5runs_detailed.csv": os.path.exists(os.path.join(ROOT, "results", "summary_5runs_detailed.csv")),
    "results/mcnemar_analysis.csv": os.path.exists(os.path.join(ROOT, "results", "mcnemar_analysis.csv")),
    "notes.md": os.path.exists(os.path.join(ROOT, "notes.md")),
    "figures/fig1_model_performance_comparison.svg": os.path.exists(os.path.join(ROOT, "figures", "fig1_model_performance_comparison.svg")),
    "figures/fig2_tradeoff_latency_vs_recall.svg": os.path.exists(os.path.join(ROOT, "figures", "fig2_tradeoff_latency_vs_recall.svg")),
}
for k, v in checks.items():
    print(f"{'PASS' if v else 'MISSING':7} {k:45}")

# 4. Check Phase 5 (Paper, Presentations, AI Check Log)
print("\n--- 4. AUDIT PAPER, PRESENTATION & DELIVERABLE D5 (PHASE 5) ---")
p5_checks = {
    "paper/main.tex": os.path.exists(os.path.join(ROOT, "paper", "main.tex")),
    "paper/references.bib": os.path.exists(os.path.join(ROOT, "paper", "references.bib")),
    "paper/sections/01_intro.tex": os.path.exists(os.path.join(ROOT, "paper", "sections", "01_intro.tex")),
    "paper/sections/02_related.tex": os.path.exists(os.path.join(ROOT, "paper", "sections", "02_related.tex")),
    "paper/sections/03_method.tex": os.path.exists(os.path.join(ROOT, "paper", "sections", "03_method.tex")),
    "paper/sections/04_results.tex": os.path.exists(os.path.join(ROOT, "paper", "sections", "04_results.tex")),
    "paper/sections/05_discussion.tex": os.path.exists(os.path.join(ROOT, "paper", "sections", "05_discussion.tex")),
    "paper/sections/06_threats.tex": os.path.exists(os.path.join(ROOT, "paper", "sections", "06_threats.tex")),
    "paper/sections/07_conclusion.tex": os.path.exists(os.path.join(ROOT, "paper", "sections", "07_conclusion.tex")),
    "paper/quality/ai_check_log.md": os.path.exists(os.path.join(ROOT, "paper", "quality", "ai_check_log.md")),
    "presentation/slides_final.pptx": os.path.exists(os.path.join(ROOT, "presentation", "slides_final.pptx")),
}
for k, v in p5_checks.items():
    print(f"{'PASS' if v else 'MISSING':7} {k:45}")

# 5. Security & Git Integrity Audit
print("\n--- 5. SECURITY & GIT INTEGRITY AUDIT ---")
gitignore_path = os.path.join(ROOT, ".gitignore")
if os.path.exists(gitignore_path):
    with open(gitignore_path, encoding='utf-8') as f:
        gi = f.read()
    print(f"PASS .gitignore exists ({len(gi)} bytes)")
    print(f"     .env protected: {'.env' in gi}")
    print(f"     onnx/safetensors protected: {'onnx' in gi}")
else:
    print("FAIL .gitignore MISSING!")
