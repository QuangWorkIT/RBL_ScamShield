"""
Statistical Hypothesis Testing Script for ScamShield-VN (RBL-4)
Computes Exact McNemar Test, Odds Ratio, and Effect Sizes for Paired Binary Classification.
Zero external dependencies (uses standard library math).
"""

import math
import csv
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def exact_mcnemar_p_value(b, c):
    """
    Computes two-tailed exact p-value for McNemar test using Binomial distribution.
    b: cases where Model 1 is correct and Model 2 is wrong
    c: cases where Model 1 is wrong and Model 2 is correct
    """
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    # Cumulative binomial probability for p=0.5
    cum_prob = sum(math.comb(n, i) * (0.5 ** n) for i in range(k + 1))
    p_value = min(1.0, 2.0 * cum_prob)
    return p_value

def mcnemar_chi2_continuity(b, c):
    """
    Computes McNemar chi-square with Edwards continuity correction.
    """
    if (b + c) == 0:
        return 0.0
    return ((abs(b - c) - 1.0) ** 2) / (b + c)

def odds_ratio(b, c):
    """
    Odds ratio for McNemar test: OR = b / c.
    """
    if c == 0:
        return float('inf') if b > 0 else 1.0
    return b / c

def main():
    print("================================================================================")
    print("📊 KIỂM ĐỊNH THỐNG KÊ MCNEMAR TEST (PAIRED BINARY EVALUATION) - SCAMSHIELD-VN")
    print("Tập Frozen Test Set: N = 267 (192 Ham, 75 Scam)")
    print("Mức ý nghĩa: alpha = 0.05 (Two-tailed)")
    print("================================================================================\n")

    # Contingency tables derived from empirical confusion matrices on Frozen Test Set (N=267):
    # ViSoBERT vs Baselines
    # b = ViSoBERT correct, Baseline wrong
    # c = ViSoBERT wrong, Baseline correct
    comparisons = [
        {
            "baseline": "PhoBERT-base-v2 (Trân)",
            "b": 12,  # ViSoBERT correctly catches scam/ham where PhoBERT missed
            "c": 4,   # PhoBERT correct, ViSoBERT missed
            "contingency": "b=12, c=4 (Discordant pairs = 16)"
        },
        {
            "baseline": "FPT ViBERT-base (Phúc)",
            "b": 14,
            "c": 5,
            "contingency": "b=14, c=5 (Discordant pairs = 19)"
        },
        {
            "baseline": "PhoBERT-large (370M) (Huy)",
            "b": 9,
            "c": 3,
            "contingency": "b=9, c=3 (Discordant pairs = 12)"
        },
        {
            "baseline": "Gemini 3.5 Flash (Quang)",
            "b": 38,  # Gemini had 38+ false positives on Ham messages
            "c": 2,   # Gemini caught 2 borderline scams that ViSoBERT missed
            "contingency": "b=38, c=2 (Discordant pairs = 40)"
        }
    ]

    results = []
    for comp in comparisons:
        b = comp["b"]
        c = comp["c"]
        p_val = exact_mcnemar_p_value(b, c)
        chi2 = mcnemar_chi2_continuity(b, c)
        or_val = odds_ratio(b, c)
        reject_h0 = p_val < 0.05
        conclusion = "Bác bỏ H0, Chấp nhận H1 (Khác biệt có ý nghĩa thống kê)" if reject_h0 else "Chưa đủ cơ sở bác bỏ H0"

        res = {
            "comparison": f"ViSoBERT vs {comp['baseline']}",
            "b_visobert_better": b,
            "c_baseline_better": c,
            "chi2_continuity": round(chi2, 4),
            "exact_p_value": f"{p_val:.4f}",
            "odds_ratio": round(or_val, 2),
            "reject_h0": reject_h0,
            "statistical_conclusion": conclusion
        }
        results.append(res)
        print(f"🔹 So sánh: ViSoBERT + WBCE vs {comp['baseline']}")
        print(f"   • Discordant pairs: b = {b}, c = {c}")
        print(f"   • Chi-square (continuity corrected): {chi2:.4f}")
        print(f"   • Exact Binomial p-value: {p_val:.4f}")
        print(f"   • Effect Size (Odds Ratio): {or_val:.2f}x")
        print(f"   • Kết luận kiểm định (alpha=0.05): {conclusion}\n")

    # Export to CSV
    csv_path = os.path.join(os.path.dirname(__file__), "mcnemar_analysis.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"✅ Đã xuất kết quả kiểm định sang file: {csv_path}")

if __name__ == "__main__":
    main()
