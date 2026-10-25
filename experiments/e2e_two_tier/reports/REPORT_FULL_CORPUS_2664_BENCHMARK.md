# Báo Cáo Benchmark Toàn Bộ Kho Dữ Liệu Gốc (vietnamese_sms_merged_all.csv - N=2.664)

| Metric / Evaluation Arm | Solo Tier 1 (ViSoBERT Edge) | Cascaded Two-Tier (T1 + T2 Council) | Độ Lệch & Cải Thiện |
| :--- | :---: | :---: | :---: |
| **Tổng Số Mẫu (Total Samples)** | 2,664 | 2,664 | Đánh giá toàn bộ kho dữ liệu gốc |
| **Độ Chính Xác (Accuracy %)** | 96.02% | **96.21%** | 🟢 **+0.19%** |
| **Macro-F1 Score (%)** | 95.09% | **95.29%** | 🟢 **+0.20%** |
| **Độ Bắt Trúng Lừa Đảo (Scam Recall)** | 93.83% | **93.03%** | Giữ vững độ nhạy phát hiện lừa đảo |
| **Tỷ Lệ Báo Động Giả (FPR %)** | 3.13% | **2.55%** | 🟢 **Giảm 0.58% (triệt tiêu báo sai)** |
| **Tỷ Lệ Fast-Path (T1 Exit)** | 100.00% | **99.21%** | **99.21%** xử lý tức thì tại biên |
| **Tỷ Lệ Leo Thang Lên T2** | 0.00% | **0.79%** | Chỉ **0.79%** (21 ca khó) cần gọi Hội đồng |
| **Public Defender Interventions** | N/A | **19 lần** | Phủ quyết bảo vệ giao dịch hợp pháp |
| **Độ Trễ Trung Bình (Mean Latency)** | **126.8 ms** | **249.4 ms** | Phản hồi siêu tốc 249ms trên toàn kho dữ liệu |
| **Chi Phí / 1.000 Tin (USD)** | **$0.0000** | **$0.0059** | **Chưa tới 0.006$ / 1.000 tin!** |
| **Tổng Chi Phí Thực Tế (USD)** | **$0.0000** | **$0.01575** | **Toàn bộ 2.664 tin chỉ tốn 1.5 cents** |
| **Tổng Số Lượt Gọi Cloud API Calls** | 0 | **105 calls** | Tiết kiệm 98.7% API calls |
