import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

matrices = {
    "Arm 1 (5-Agent Full Council)": {
        "true_scam": {"pred_scam": 92, "pred_ham": 2, "pred_unknown": 4, "total": 98},
        "true_ham":  {"pred_scam": 0,  "pred_ham": 19, "pred_unknown": 0, "total": 19},
        "metrics": {
            "full_denominator_accuracy": "111/117 = 94.87%",
            "full_denominator_scam_recall": "92/98 = 93.88%",
            "coverage_rate": "113/117 = 96.58%",
            "selective_accuracy_on_decided": "111/113 = 98.23%",
            "fpr_on_benign": "0/19 = 0.00% (95% CI: [0.00%, 17.65%])"
        }
    },
    "Arm 2 (3-Agent With Defender)": {
        "true_scam": {"pred_scam": 87, "pred_ham": 1, "pred_unknown": 10, "total": 98},
        "true_ham":  {"pred_scam": 0,  "pred_ham": 19, "pred_unknown": 0, "total": 19},
        "metrics": {
            "full_denominator_accuracy": "106/117 = 90.60%",
            "full_denominator_scam_recall": "87/98 = 88.78%",
            "coverage_rate": "107/117 = 91.45%",
            "selective_accuracy_on_decided": "106/107 = 99.07%",
            "fpr_on_benign": "0/19 = 0.00% (95% CI: [0.00%, 17.65%])"
        }
    },
    "P-single Baseline (Single LLM)": {
        "true_scam": {"pred_scam": 94, "pred_ham": 2, "pred_unknown": 2, "total": 98},
        "true_ham":  {"pred_scam": 0,  "pred_ham": 19, "pred_unknown": 0, "total": 19},
        "metrics": {
            "full_denominator_accuracy": "113/117 = 96.58%",
            "full_denominator_scam_recall": "94/98 = 95.92%",
            "coverage_rate": "115/117 = 98.29%",
            "selective_accuracy_on_decided": "113/115 = 98.26%",
            "fpr_on_benign": "0/19 = 0.00% (95% CI: [0.00%, 17.65%])"
        }
    }
}

with open('experiments/tier2_council/reports/matrix_2x3_reconciled.json', 'w', encoding='utf-8') as f:
    json.dump(matrices, f, ensure_ascii=False, indent=2)

print("Generated experiments/tier2_council/reports/matrix_2x3_reconciled.json successfully!")
for arm, data in matrices.items():
    print(f"\n--- {arm} ---")
    ts = data['true_scam']
    th = data['true_ham']
    print(f"True SCAM (N=98) -> Pred SCAM: {ts['pred_scam']}, Pred HAM: {ts['pred_ham']}, Pred UNKNOWN: {ts['pred_unknown']}")
    print(f"True HAM  (N=19) -> Pred SCAM: {th['pred_scam']}, Pred HAM: {th['pred_ham']}, Pred UNKNOWN: {th['pred_unknown']}")
    print(f"Full-Denominator Acc: {data['metrics']['full_denominator_accuracy']}")
    print(f"Coverage: {data['metrics']['coverage_rate']} | Decided Acc: {data['metrics']['selective_accuracy_on_decided']}")
