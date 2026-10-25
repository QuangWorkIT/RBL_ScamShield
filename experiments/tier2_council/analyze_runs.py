# -*- coding: utf-8 -*-
"""
==============================================================================
ScamShield Tier-2 Forensic Council: Comprehensive Analysis & Report Generator
==============================================================================
Location: experiments/tier2_council/analyze_runs.py
Description:
    Processes results in `benchmark.db`, calculates comprehensive metrics
    (F1, Precision, Recall, FPR, TTFT, Cost/Success), and exports a visual
    scientific report `reports/REPORT_TIER2_COUNCIL_BENCHMARK.md`.
==============================================================================
"""

import os
import sys
import csv
import time
import json
import sqlite3
from typing import Dict, List, Any

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "benchmark.db")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
OUTPUT_MD = os.path.join(REPORTS_DIR, "REPORT_TIER2_COUNCIL_BENCHMARK.md")
OUTPUT_CSV = os.path.join(REPORTS_DIR, "competency_matrix.csv")
OUTPUT_JSON = os.path.join(REPORTS_DIR, "competency_matrix.json")


def generate_report():
    if not os.path.exists(DB_PATH):
        sys.exit(f"Database not found at: {DB_PATH}")

    os.makedirs(REPORTS_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT model_id FROM pilot_runs WHERE error_code IS NULL")
    models = [r[0] for r in cursor.fetchall()]

    if not models:
        print("No successful runs found in benchmark.db to analyze.")
        conn.close()
        return

    cursor.execute("SELECT DISTINCT task_role FROM pilot_runs WHERE task_role IS NOT NULL")
    roles = sorted([r[0] for r in cursor.fetchall()])

    matrix = []

    for m_id in models:
        # Overall
        cursor.execute("SELECT count(*), sum(is_correct), avg(ttft_ms), avg(total_duration_ms), sum(cost_usd) FROM pilot_runs WHERE model_id = ? AND error_code IS NULL", (m_id,))
        total, correct, avg_ttft, avg_dur, total_cost = cursor.fetchone()
        acc = (correct / total * 100.0) if total else 0.0
        cost_per_succ = (total_cost / correct) if correct else 0.0

        # Confusion Matrix for Scam
        cursor.execute("SELECT count(*) FROM pilot_runs WHERE model_id = ? AND gold_label = 'SCAM' AND predicted_label = 'SCAM' AND error_code IS NULL", (m_id,))
        tp = cursor.fetchone()[0]
        cursor.execute("SELECT count(*) FROM pilot_runs WHERE model_id = ? AND gold_label = 'HAM' AND predicted_label = 'SCAM' AND error_code IS NULL", (m_id,))
        fp = cursor.fetchone()[0]
        cursor.execute("SELECT count(*) FROM pilot_runs WHERE model_id = ? AND gold_label = 'SCAM' AND predicted_label = 'HAM' AND error_code IS NULL", (m_id,))
        fn = cursor.fetchone()[0]
        cursor.execute("SELECT count(*) FROM pilot_runs WHERE model_id = ? AND gold_label = 'HAM' AND predicted_label = 'HAM' AND error_code IS NULL", (m_id,))
        tn = cursor.fetchone()[0]

        prec = (tp / (tp + fp) * 100.0) if (tp + fp) else 0.0
        rec = (tp / (tp + fn) * 100.0) if (tp + fn) else 0.0
        f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
        fpr = (fp / (fp + tn) * 100.0) if (fp + tn) else 0.0

        # Role Breakdown
        role_scores = {}
        for r_name in roles:
            cursor.execute("SELECT count(*), sum(is_correct) FROM pilot_runs WHERE model_id = ? AND task_role = ? AND error_code IS NULL", (m_id, r_name))
            r_tot, r_cor = cursor.fetchone()
            role_scores[r_name] = (r_cor / r_tot * 100.0) if r_tot else 0.0

        matrix.append({
            "model_id": m_id,
            "total_runs": total,
            "accuracy": round(acc, 2),
            "precision": round(prec, 2),
            "recall": round(rec, 2),
            "f1_score": round(f1, 2),
            "fpr": round(fpr, 2),
            "avg_ttft_ms": round(avg_ttft or 0.0, 1),
            "avg_duration_ms": round(avg_dur or 0.0, 1),
            "total_cost_usd": round(total_cost or 0.0, 5),
            "cost_per_success": round(cost_per_succ, 6),
            "roles": role_scores
        })

    conn.close()

    # Save JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=2, ensure_ascii=False)

    # Save CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["model_id", "accuracy", "f1_score", "precision", "recall", "fpr", "avg_duration_ms", "cost_usd", "cost_per_success"] + roles)
        for row in matrix:
            writer.writerow([
                row["model_id"], row["accuracy"], row["f1_score"], row["precision"], row["recall"],
                row["fpr"], row["avg_duration_ms"], row["total_cost_usd"], row["cost_per_success"]
            ] + [row["roles"].get(r, 0.0) for r in roles])

    # Generate Markdown Report
    lines = [
        "# BÁO CÁO THỰC NGHIỆM ĐÁNH GIÁ NĂNG LỰC HỘI ĐỒNG PHÁP Y (TIER-2 AI COUNCIL)",
        "",
        "> **Đề tài:** ScamShield-VN — Evidence-Grounded Vietnamese Scam & Phishing Detection Platform  ",
        f"> **Thời điểm xuất báo cáo:** {time.strftime('%Y-%m-%d %H:%M:%S')} (Asia/Saigon)  ",
        f"> **Địa điểm lưu trữ:** `experiments/tier2_council/`  ",
        "> **Quy chuẩn khoa học:** Tuân thủ phương pháp luận RBL, Frozen Evaluation Dataset, Tuyệt đối không giả mạo số liệu.",
        "",
        "---",
        "",
        "## 1. Bảng Ma Trận Năng Lực Tổng Hợp (Competency Matrix)",
        "",
        "| Model ID | Accuracy | Macro-F1 | Precision | Recall | Báo động giả (FPR) | Độ trễ (E2E) | Tổng Chi Phí | Chi phí/Thành công |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]

    for m in matrix:
        lines.append(f"| `{m['model_id']}` | **{m['accuracy']}%** | **{m['f1_score']}%** | {m['precision']}% | {m['recall']}% | {m['fpr']}% | {m['avg_duration_ms']}ms | ${m['total_cost_usd']:.4f} | ${m['cost_per_success']:.6f} |")

    lines.extend([
        "",
        "---",
        "",
        "## 2. Bảng Điểm Phân Hóa Theo 5 Nghiệp Vụ Pháp Y (Role Breakdown)",
        "",
        "Mỗi cột thể hiện độ chính xác (%) của model trên từng bài toán nghiệp vụ cụ thể của Hội đồng ScamShield:",
        "",
        "| Model ID | Ghế 1: URL & Kỹ thuật | Ghế 2: Đòn tâm lý | Ghế 3: Teencode VN | Ghế 4: Ngân hàng | Ghế 5: Public Defender (HAM) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: |"
    ])

    for m in matrix:
        r_scores = m["roles"]
        lines.append(f"| `{m['model_id']}` | {r_scores.get('ROLE_CYBER_URL', 0.0):.1f}% | {r_scores.get('ROLE_SOC_ENG', 0.0):.1f}% | {r_scores.get('ROLE_VN_TEENCODE', 0.0):.1f}% | {r_scores.get('ROLE_BANK_VERIFY', 0.0):.1f}% | {r_scores.get('ROLE_DEFENDER', 0.0):.1f}% |")

    lines.extend([
        "",
        "---",
        "",
        "## 3. Khuyến Nghị Phân Vai Cặp Đôi (Maker - Checker Assignment)",
        "",
        "Dựa trên số liệu thực nghiệm khách quan ở trên, kiến trúc Hội đồng 5 Ghế được cấu hình tối ưu như sau:",
        "",
        "1. **Ghế 1 (Giám định URL & Hạ tầng):**",
        "   - **Maker:** Model có điểm F1 cao nhất ở `ROLE_CYBER_URL`.",
        "   - **Checker / Standby:** Model xếp thứ 2 có tốc độ phản hồi nhanh.",
        "2. **Ghế 2 (Hồ sơ Tâm lý & Thao túng Xã hội):**",
        "   - **Primary:** Model bóc tách sắc thái đe dọa / giục giã chính xác nhất.",
        "3. **Ghế 3 (Phân tích Ngôn ngữ & Teencode):**",
        "   - **Primary:** Model giải mã biến thể teencode và từ lóng tiếng Việt tốt nhất.",
        "4. **Ghế 4 (Pháp lý & Quy trình Ngân hàng):**",
        "   - **Primary:** Model đối soát chuẩn xác các quy định QĐ 2345/QĐ-NHNN và OTP.",
        "5. **Ghế 5 (Public Defender / Chống Báo động giả):**",
        "   - **Primary:** Model có **Tỷ lệ Báo động giả (FPR) thấp nhất** và độ chính xác cao nhất ở nhóm tin nhắn hợp pháp (`ROLE_DEFENDER`).",
        "",
        "---",
        "",
        "## 4. Nhật Ký Sử Dụng & Đối Soát (Audit & Provenance Trail)",
        "",
        f"- Toàn bộ lượt gọi API và số liệu vi mô đã được lưu trữ vĩnh viễn tại: [`reports/usage_log.csv`](file:///{OUTPUT_CSV})",
        "- Mọi kết quả đều có thể tái lập thông qua script `runner.py --suite data/master_test_suite.jsonl`."
    ])

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\n✅ Analysis report successfully generated at:\n   -> {OUTPUT_MD}")
    print(f"   -> {OUTPUT_CSV}\n   -> {OUTPUT_JSON}\n")


if __name__ == "__main__":
    generate_report()
