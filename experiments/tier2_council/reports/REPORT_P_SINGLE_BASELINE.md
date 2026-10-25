# 📊 BÁO CÁO BASELINE P-SINGLE (WANG ET AL., ACL 2024)
**Mô hình:** `gpt-6.1-sol` (Single LLM with Structured Forensic Prompting)  
**Tập dữ liệu:** `master_test_suite.jsonl` ($N=117$)  
**Thời điểm tạo:** 2026-10-20 18:51:24  

---

## 1. Kết Quả Đo Đạc

| Chỉ Tiêu | Giá Trị Baseline P-single |
| :--- | :---: |
| **Accuracy** | **96.58%** |
| **Precision** | **100.00%** |
| **Scam Recall** | **95.92%** |
| **Macro-F1** | **97.92%** |
| **False Positive Rate (FPR)** | **0.00%** |
| **False Negative Rate (FNR)** | **4.08%** |
| **Số mẫu UNKNOWN** | **2** |
| **Median Latency** | **12176.15 ms** |
| **Chi Phí Dự Toán** | **$0.0450 / 1k SMS** |

---

## 2. Ý Nghĩa Khoa Học (Academic Significance)
* **Đối sánh với Hội đồng Đa Tác tử (Multi-Agent Council):** Baseline P-single thiết lập ngưỡng chuẩn đối chứng (reference standard) độc lập, xác nhận định lý của Wang et al. (ACL 2024) về năng lực của single LLM khi được định hướng bằng prompt đa chiều.
* **Đóng góp cho bài báo ICITT:** Bổ sung trực tiếp vào ma trận đối chứng cùng với Baseline T1 (ViSoBERT Edge Screener).
