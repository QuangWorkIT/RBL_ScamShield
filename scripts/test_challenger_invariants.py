# -*- coding: utf-8 -*-
"""
scripts/test_challenger_invariants.py
Empirical Adversarial Verification Suite for challenger_2:
1. Small-sample Clopper-Pearson exact bounds (N=19 and N=117) & Zero-error non-overclaim audit.
2. Ablation confounder disclosure check (Arm 3 panel size reduction from 3 to 2 seats).
3. Data leakage & overlap disclosure check (N=384 text overlap: 10 strings, 99 templates).
4. Overleaf ZIP package SHA-256 bit-for-bit match audit (all 10 members).
"""
import sys, os, re, zipfile, hashlib, math

def test_clopper_pearson_bounds():
    print("=== Challenge 1: Small-Sample Clopper-Pearson Exact Bounds & Overclaim Audit ===")
    # Exact calculation
    def cp_zero_upper(n, alpha=0.05):
        return 1.0 - (alpha / 2.0)**(1.0 / n)

    cp_19 = cp_zero_upper(19) * 100.0
    cp_117 = cp_zero_upper(117) * 100.0

    print(f"  Calculated N=19  exact upper bound: {cp_19:.4f}% -> {cp_19:.2f}%")
    print(f"  Calculated N=117 exact upper bound: {cp_117:.4f}% -> {cp_117:.2f}%")
    assert abs(cp_19 - 17.6514) < 0.01, "N=19 formula mismatch"
    assert abs(cp_117 - 3.1018) < 0.01, "N=117 formula mismatch"

    with open('paper/sections/04_results.tex', 'r', encoding='utf-8') as f:
        res = f.read()
    with open('paper/main.tex', 'r', encoding='utf-8') as f:
        main = f.read()
    with open('paper/sections/05_conclusion.tex', 'r', encoding='utf-8') as f:
        conc = f.read()

    # Check N=19 in results, main, and conclusion
    assert r"[0.00\%, 17.65\%]" in res, "Results missing [0.00%, 17.65%]"
    assert r"[0.00\%, 17.65\%]" in main, "Main missing [0.00%, 17.65%]"
    assert r"[0.00\%, 17.65\%]" in conc, "Conclusion missing [0.00%, 17.65%]"
    print("  [PASS] N=19 Clopper-Pearson 95% CI strictly reported as [0.00%, 17.65%]")

    # Check N=117 PII sanitizer concordance
    assert r"[0.00\%, 3.10\%]" in res, "Results missing [0.00%, 3.10%]"
    assert r"[0.00\%, 3.10\%]" in main, "Main missing [0.00%, 3.10%]"
    print("  [PASS] N=117 PII sanitizer concordance 95% CI strictly reported as [0.00%, 3.10%]")

    # Audit for forbidden overclaims: "guaranteed zero error", "guaranteed zero"
    for text_name, content in [("main.tex", main), ("04_results.tex", res), ("05_conclusion.tex", conc)]:
        lower = content.lower()
        assert "guaranteed zero error" not in lower, f"Overclaim found in {text_name}: 'guaranteed zero error'"
        assert "guaranteed zero" not in lower, f"Overclaim found in {text_name}: 'guaranteed zero'"
        assert "zero error" not in lower, f"Unhedged claim found in {text_name}: 'zero error'"
    print("  [PASS] Zero overclaim audit: paper NEVER claims 'guaranteed zero error' or 'guaranteed zero'.")


def test_ablation_confounder_disclosure():
    print("\n=== Challenge 2: Ablation Confounder Disclosure ===")
    with open('paper/sections/04_results.tex', 'r', encoding='utf-8') as f:
        res = f.read()

    # Check that Arm 3 is clearly identified as 2 seats
    assert "Arm 3: 3-Agent (No Defender, 2 seats)" in res, "Table IX must label Arm 3 with 2 seats"

    # Check explicit disclosure of panel size confounder
    confounder_phrase = "Arm 3 reduces the council size from three agents to two seats rather than substituting a generic control agent"
    assert confounder_phrase in res, f"Results must explicitly disclose: '{confounder_phrase}'"
    print("  [PASS] Section IV explicitly discloses panel-size confounder in Arm 3.")


def test_data_leakage_overlap_transparency():
    print("\n=== Challenge 3: Data Leakage & Overlap Transparency ===")
    with open('paper/sections/03_method.tex', 'r', encoding='utf-8') as f:
        meth = f.read()
    with open('paper/sections/04_results.tex', 'r', encoding='utf-8') as f:
        res = f.read()

    # Section III.A checks
    assert r"\textbf{99 / 117 ($84.6\%$)}" in meth, "Section III.A must report 99/117 (84.6%) overlap with Training"
    assert "10 overlapping text strings and 99 training-derived templates" in meth, \
        "Section III.A must explicitly disclose 10 overlapping text strings and 99 training templates"
    assert "exploratory development benchmark rather than a fully disjoint test set" in meth, \
        "Section III.A must explicitly designate N=384 as exploratory development benchmark"
    print("  [PASS] Section III.A explicitly discloses 10 overlapping strings and 99 templates for N=384.")

    # Section IV.G (Threats to Validity) checks
    assert "shares 10 exact strings with the frozen test partition and contains 99 payloads derived from training templates" in res, \
        "Section IV.G must disclose 10 exact strings and 99 payloads from training templates"
    assert "exploratory development evaluation rather than a fully disjoint test set" in res, \
        "Section IV.G must report potential leakage as unmitigated threat to validity"
    print("  [PASS] Section IV.G (Threats to Validity) explicitly discloses data leakage as an unmitigated threat.")


def test_overleaf_zip_integrity():
    print("\n=== Challenge 4: Overleaf Zip Package Integrity ===")
    zip_path = 'paper/ScamShield_Overleaf_Ready.zip'
    assert os.path.exists(zip_path), f"Zip file missing: {zip_path}"
    
    expected_members = {
        'main.tex',
        'supplementary.tex',
        'references.bib',
        'sections/00_abstract.tex',
        'sections/01_intro.tex',
        'sections/02_related.tex',
        'sections/03_method.tex',
        'sections/04_results.tex',
        'sections/05_conclusion.tex',
        'sections/06_endmatter.tex',
        'figures/pipeline_architecture.png'
    }

    z = zipfile.ZipFile(zip_path, 'r')
    members = set(z.namelist())
    print(f"  Zip file contains {len(members)} entries.")
    assert members == expected_members, f"Zip member mismatch. Expected {expected_members}, got {members}"

    for name in members:
        zip_bytes = z.read(name)
        zip_sha = hashlib.sha256(zip_bytes).hexdigest()

        disk_path = os.path.join('paper', name)
        assert os.path.exists(disk_path), f"Disk file missing: {disk_path}"
        with open(disk_path, 'rb') as f:
            disk_bytes = f.read()
        disk_sha = hashlib.sha256(disk_bytes).hexdigest()

        assert zip_sha == disk_sha, f"Hash mismatch for {name}: zip={zip_sha} vs disk={disk_sha}"
        print(f"  [PASS] {name}: SHA-256 bit-for-bit matched ({len(zip_bytes)} bytes)")

    print("  [PASS] Overleaf ZIP package contains all 10 files matching disk files SHA-256 bit-for-bit.")


if __name__ == '__main__':
    test_clopper_pearson_bounds()
    test_ablation_confounder_disclosure()
    test_data_leakage_overlap_transparency()
    test_overleaf_zip_integrity()
    print("\n========================================================")
    print("ALL 4 CHALLENGER ADVERSARIAL VERIFICATIONS PASSED 100%!")
    print("========================================================")
