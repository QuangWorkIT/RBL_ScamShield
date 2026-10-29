# -*- coding: utf-8 -*-
"""
scripts/verify_paper_invariants.py
Rigorous verification suite asserting all mathematical, cross-table, and textual invariants across ScamShield-VN.
"""
import sys, re, os

def run_checks():
    errors = []
    warnings = []

    def check(condition, msg):
        if not condition:
            errors.append(msg)
            print(f"  [FAIL] {msg}")
        else:
            print(f"  [PASS] {msg}")

    print("=" * 80)
    print("SCAMSHIELD-VN: MASTER INVARIANT VERIFICATION SUITE")
    print("=" * 80)

    # Read all sections
    sections = {}
    sec_dir = 'paper/sections'
    for f in os.listdir(sec_dir):
        if f.endswith('.tex'):
            with open(os.path.join(sec_dir, f), 'r', encoding='utf-8') as fp:
                sections[f] = fp.read()

    full_text = "\n".join(sections.values())
    supp = ""
    if os.path.exists('paper/supplementary.tex'):
        with open('paper/supplementary.tex', 'r', encoding='utf-8') as fp:
            supp = fp.read()

    # 1. Table VIII vs Table IX Accuracy Invariant
    print("\n--- 1. Cross-Table Accuracy & Matrix Invariants (Tables VIII & IX) ---")
    res = sections['04_results.tex']
    # Arm 4 in Table VIII must be 90.60%
    check(r"Arm 4: 3-Agent (Defender No Veto) & 3 & $\mathbf{90.60\%}$" in res,
          "Table VIII Arm 4 Accuracy must be 90.60%")
    # Table IX must have 88 TP and 18 TN for Arm 4 (in main results or supplementary Table S3)
    check(r"Arm 4: 3-Agent (Defender No Veto) & 88 & 1 & 9 & 1 & 18 & 0" in res or r"Arm 4: 3-Agent (Defender No Veto) & 88 & 1 & 9 & 1 & 18 & 0" in supp,
          "Table IX Arm 4 row must be: 88 | 1 | 9 | 1 | 18 | 0 (Sum=106/117 = 90.60%)")
    # Clopper-Pearson CI for 0/19 benign
    check(r"[0.00\%, 17.65\%]" in res, "Table IX Clopper-Pearson 95% CI for 0/19 benign must be [0.00%, 17.65%]")

    # 2. Cost Invariants Across Tables I, X, and XI ---
    print("\n--- 2. Cost Invariants Across Tables I, X, and XI ---")
    rel = sections['02_related.tex']
    check(r"\$0.0153/1k SMS" in rel or r"\$0.0153/1k SMS" in supp, "Table I 'This Work' cost must be $0.0153/1k SMS")
    check(r"Arm 4: Naive Cascaded (Tier 1 + PoLL 3/5) & $97.14\%$ & $96.55\%$ & $97.11\%$ & $2.84\%$ & $717.8\text{ ms}$ & $\mathbf{\$0.0541}$ & $3.4\%$" in res,
          "Table X Arm 4 Naive Cascaded Cost must be $0.0541 (0.034 * $1.5923)")
    check(r"$\mathbf{\tau = 0.90}$ & $\mathbf{97.40\%}$ & $\mathbf{97.11\%}$ & $\mathbf{2.37\%}$ & $\mathbf{267.5\text{ ms}}$ & $\mathbf{\$0.0153}$ & $\mathbf{3.4\%}$" in res or r"$\mathbf{\tau = 0.90}$ & $\mathbf{97.40\%}$ & $\mathbf{97.11\%}$ & $\mathbf{2.37\%}$ & $\mathbf{267.5\text{ ms}}$ & $\mathbf{\$0.0153}$ & $\mathbf{3.4\%}$" in supp,
          "Table XI tau=0.90 must be $0.0153 at 3.4% escalation")

    # 3. Table IV Partition Overlap Invariants
    print("\n--- 3. Partition Overlap Invariants (Table IV) ---")
    meth = sections['03_method.tex']
    check(r"\textbf{99 / 117 ($84.6\%$)}" in meth, "Table IV Challenge vs Train overlap must be 99/117 (84.6%)")
    check("None (Cloud LLMs zero-shot)" not in meth, "Table IV must NOT claim 'None (Cloud LLMs zero-shot)'")
    check("Zero (Strict Holdout)" not in meth, "Table IV must NOT claim 'Zero (Strict Holdout)' without near-duplicate disclosure")

    # 4. Table I Dynamic References Invariant (Novelty Matrix)
    print("\n--- 4. Dynamic Cross-Reference Invariants (Table I Novelty Matrix) ---")
    check("Table II), McNemar discordance (Table III)" not in full_text,
          "Table II must NOT have hardcoded 'Table II, Table III, Table IV, Table VI'")
    check(r"Table~\ref{tab:benchmark_summary}" in full_text, "Table I must dynamically reference tab:benchmark_summary")
    check(r"Table~\ref{tab:mcnemar}" in full_text, "Table I must dynamically reference tab:mcnemar")
    check(r"Tables~\ref{tab:ablation_council}--\ref{tab:matrix_2x3}" in full_text, "Table I must dynamically reference tab:ablation_council--tab:matrix_2x3")
    check(r"Table~\ref{tab:tau_ablation}" in full_text, "Table I must dynamically reference tab:tau_ablation")

    # 5. Figure 1 Parameter and Size Invariants
    print("\n--- 5. Figure 1 Parameter and Size Invariants ---")
    with open('scripts/generate_architecture_figure.py', 'r', encoding='utf-8') as fp:
        fig_script = fp.read()
    check("110M Params" not in fig_script, "Figure script must NOT contain '110M Params'")
    check("97.57M Params" in fig_script, "Figure script must contain '97.57M Params'")
    check("98.42 MB / 93.86 MiB" in fig_script, "Figure script must contain '98.42 MB / 93.86 MiB'")
    check("Occam-Optimized" not in fig_script, "Figure script must NOT contain 'Occam-Optimized'")

    # 6. Table VI ViSoBERT Benchmark Invariants
    print("\n--- 6. Table VI ViSoBERT Benchmark Invariants ---")
    check(r"$95.64 \pm 2.04$" in res, "Table VI ViSoBERT Scam Recall must be 95.64 +- 2.04%")
    check(r"98.42 MB (INT8)" in res, "Table VI ViSoBERT model size must be 98.42 MB (INT8)")
    check(r"351/367 = 95.64\%" in res, "Table VI note must report micro-pooled recall 351/367 = 95.64%")
    check(r"72/75 = 96.00\%" in res, "Table VI note must report frozen holdout recall 72/75 = 96.00%")
    check(r"$94.51\% \pm 0.96\%$" in res, "Table VI note must report unweighted Macro-F1 = 94.51% +- 0.96%")
    check(r"\theta_{\text{scam}}" in res, "Table VI note must use theta_scam for decision threshold")

    # 7. FDR / FPR Separation & Mathematical Clarity
    print("\n--- 7. FDR and FPR Terminology Invariants ---")
    check(r"False Discovery Rate was $35.34\%$" in res,
          "Section IV.A must define 41/116 as False Discovery Rate (FDR)")
    check("on benign stress probes" not in res, "Section IV.A must NOT misname 116 as 'benign stress probes'")
    check("on benign challenge lures" not in res, "Section IV.A must NOT misname 116 as 'benign challenge lures'")

    # 8. McNemar Table VII & Differences Invariants
    print("\n--- 8. McNemar Invariants (Table VII) ---")
    check(r"ViSoBERT vs. Gemini 3.5 Flash & 33 & 3 & 23.3611" in res,
          "Table VII ViSoBERT vs Gemini row must be b=33, c=3, chi2=23.3611")
    check(r"b=33, c=3" in res, "Results text must discuss b=33, c=3")
    check(r"b - c = 30" in res, "Results text must note b - c = 30")

    # 9. Confidence Interval Invariants
    print("\n--- 9. Confidence Interval Invariants ---")
    check(r"Newcombe $95\%$ CI: $[-9.75\%, -0.45\%]" in res,
          "Section IV.B must report Newcombe paired difference CI [-9.75%, -0.45%]")
    check(r"asymptotic $95\%$ CI: $[-9.46\%, -0.75\%]" not in res,
          "Section IV.B must NOT report invalid Wald CI [-9.46%, -0.75%]")
    conc = sections['05_conclusion.tex']
    check(r"Newcombe $95\%$ CI: $[-9.75\%, -0.45\%]" in conc,
          "Conclusion RQ2 must report Newcombe CI [-9.75%, -0.45%]")

    # 10. Call Count Invariants
    print("\n--- 10. API Call Count Invariants ---")
    check("585" in meth and "40.0\\%" in meth, "Section III.F must report 585 calls and 40.0% reduction")
    check("585" in res and "40.0\\%" in res, "Section IV.B must report 585 calls and 40.0% reduction")

    # 11. Latency Invariant in Table XI
    print("\n--- 11. Latency Invariants (Table XI) ---")
    check(r"$\tau = 0.70$ & $96.35\%$ & $95.38\%$ & $2.84\%$ & $99.5\text{ ms}$" in res or r"$\tau = 0.70$ & $96.35\%$ & $95.38\%$ & $2.84\%$ & $99.5\text{ ms}$" in supp,
          "Table XI tau=0.70 latency must be 99.5 ms")

    # 12. Prompt Disclosures & Telemetry
    print("\n--- 12. Prompt Disclosures and Failure Recovery Telemetry ---")
    check("Gemini 3.5 Flash 5-Shot In-Context Learning Prompt" in meth, "Prompt Gemini 5-shot must be disclosed")
    check(r"\textbf{2. Single-LLM Baseline with Structured Forensic Prompting ($\text{P-single}$):}" in meth,
          "Prompt P-single must be disclosed")
    check("Seat A (Cyber-Financial Security Analyst)" in meth, "Seat A prompt must be disclosed")
    check(r"Seat B (Psycholinguistic \& Urgency Profiler)" in meth, "Seat B prompt must be disclosed")
    check(r"Seat C (Public Defender \& Anti-Alarm Fatigue Advocate)" in meth, "Seat C prompt must be disclosed")
    check("Reference 5-Agent Council Specification (Arm 1)" in meth, "Arm 1 5-agent specification must be disclosed")
    check("PoLL Baseline" in meth, "PoLL baseline must be disclosed")
    check(r"$0/351$ schema violations" in meth, "Section III.F must report 0/351 schema violations")

    # 13. Data Provenance & 8 External Lures Breakdown
    print("\n--- 13. Data Provenance and External Lures Breakdown ---")
    check(r"\textbf{Label Ontology and Operational Scope:}" in meth, "Section III.A must contain Label Ontology paragraph")
    check(r"deceptive lures incorporate sophisticated institutional impersonation" in meth,
          "Section III.A must describe operational stress of challenge lures")
    check(r"zero benign samples are synthetic" in meth, "Section III.A must state zero benign samples are synthetic")
    check(r"authentic customer service and promotional notifications outside the corpus" in meth,
          "Section III.A must identify authentic notices outside corpus")

    # 14. Forbidden Strings and Overclaim Checks
    print("\n--- 14. Forbidden Strings and Overclaim Checks ---")
    forbidden = [
        ("dominant Scam Recall", "Intro/Results must not claim 'dominant Scam Recall'"),
        ("Occam-optimized", "Paper must not claim 'Occam-optimized'"),
        ("prespecified acceptance threshold", "Paper must not claim 'prespecified acceptance threshold'"),
        ("pp.~5191--5207)", "Paper must not have floating 'pp. 5191--5207' in sentences"),
        ("60 GB", "Paper must not claim 60 GB pretraining corpus"),
        ("89.74%", "Table VIII must not report 89.74% Accuracy for Arm 4"),
        ("1.5923", "Table X must not report unscaled $1.5923 cost for Arm 4 at 3.4% escalation"),
        ("0.05/1k SMS", "Table I must not report $0.05/1k SMS"),
        ("500 to 351", "Paper must not state 500 to 351 API calls (must be 585 to 351)"),
        ("29.8% call reduction", "Paper must not claim 29.8% call reduction (must be 40.0%)"),
        ("58.2\\text{ ms}", "Table XI must not list 58.2 ms at tau=0.70"),
        ("93.86\\text{ MB}", "Conclusion must not use MB for 93.86 (must be MiB)"),
        ("19 authentic banking OTPs", "Paper must not use imprecise phrase '19 authentic banking OTPs'"),
        ("3 GB uncompressed", "Paper must not claim '3 GB uncompressed' for ViSoBERT pretraining corpus"),
        ("100% precision and zero false negatives", "Paper must not claim 100% precision when over-redaction occurred"),
        ("Median 267.7 ms", "Paper must not mislabel mean latency as 'Median 267.7 ms'")
    ]
    for phrase, msg in forbidden:
        check(phrase not in full_text, msg)

    # 15. Bibliography Invariants
    print("\n--- 15. Bibliography Invariants ---")
    with open('paper/references.bib', 'r', encoding='utf-8') as fp:
        bib_text = fp.read()
    check("Quoc-Nam Nguyen and Thanh-Cong Phan and Duc-Vu Nguyen and Kiet Van Nguyen" in bib_text,
          "Ref nguyen2023visobert must have formal full author names")
    check("Yi-Nuo Xue and Eric Spero and Yun Sing Koh and Giovanni Russello" in bib_text,
          "Ref chen2025multiphishguard must list Xue, Spero, Koh, Russello")

    # 16. Reproducibility Commit Pinning & SHA-256 Formatting
    print("\n--- 16. Reproducibility Commit Pinning & SHA-256 Formatting ---")
    endm = sections['06_endmatter.tex']
    check("https://github.com/QuangWorkIT/RBL_ScamShield" in endm,
          "Section 06_endmatter must point to root repository https://github.com/QuangWorkIT/RBL_ScamShield")
    check("SHA-256 checksum in the repository manifest" in endm,
          "Section 06_endmatter must refer to SHA-256 checksum in repository manifest")

    # 17. Audit Phase 3 Invariants (New Invariant Additions)
    print("\n--- 17. Audit Phase 3 Invariants (Prompts, CI, Latency, and Settings) ---")
    check("Chỉ trả về DUY NHẤT một số nguyên: 0 hoặc 1" in meth,
          "Prompt Gemini 5-shot must direct 0 or 1 integer output")
    check(r"[88.75\%, 99.17\%]" in res,
          "Results must report Clopper-Pearson CI [88.75%, 99.17%] for 72/75")
    check(r"\theta = 0.50" in res,
          "Table X note must disclose threshold theta = 0.50 for Arm 1")
    check(r"Mean Latency (ms)" in res,
          "Table X and XI headers must specify Mean Latency")

    # 18. Markdown Preview Invariants (FULL_PAPER_PREVIEW.md)
    print("\n--- 18. Markdown Preview Invariants (FULL_PAPER_PREVIEW.md) ---")
    preview_path = 'paper/FULL_PAPER_PREVIEW.md'
    if os.path.exists(preview_path):
        with open(preview_path, 'r', encoding='utf-8') as fp:
            preview_text = fp.read()
        preview_forbidden = [
            ("1.5923", "FULL_PAPER_PREVIEW.md must not contain unscaled cost '1.5923'"),
            ("58.2 ms", "FULL_PAPER_PREVIEW.md must not contain prohibited latency '58.2 ms'"),
            ("0.0509", "FULL_PAPER_PREVIEW.md must not contain conflicting cost '0.0509'"),
            ("b=38, c=2", "FULL_PAPER_PREVIEW.md must not contain legacy McNemar 'b=38, c=2'"),
        ]
        for term, msg in preview_forbidden:
            check(term not in preview_text, msg)
    else:
        errors.append(f"{preview_path} not found")

    print("\n" + "=" * 80)
    print(f"VERIFICATION SUMMARY: {len(errors)} ERRORS, {len(warnings)} WARNINGS")
    print("=" * 80)
    if errors:
        print("\nFailed checks:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("\nALL INVARIANTS PASSED PERFECTLY! ZERO CONTRADICTIONS DETECTED.")
        return True

if __name__ == '__main__':
    success = run_checks()
    sys.exit(0 if success else 1)
