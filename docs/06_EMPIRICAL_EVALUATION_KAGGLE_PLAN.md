# 06. EMPIRICAL EVALUATION KAGGLE PLAN — KẾ HOẠCH KIỂM THỬ THỰC NGHIỆM

Tài liệu này lưu trữ **Kế hoạch Thực nghiệm Khoa học (Empirical Evaluation Protocol)** trên nền tảng Kaggle cho đề tài RBL ScamShield-VN. Kế hoạch này sẽ được thực hiện sau khi hoàn thành Sprint UI để lấy số liệu thực chứng đưa vào báo cáo nghiệm thu và bài báo khoa học.

---

## 1. Môi Trường & Hạ Tầng Thực Nghiệm (Kaggle Environment)

* **Nền tảng:** Kaggle Notebooks (Môi trường tái lập 100% mã nguồn mở).
* **Phần cứng:** 
  * GPU: NVIDIA Tesla T4 $\times 2$ (16GB VRAM) hoặc P100.
  * CPU: 4 vCPU, 30GB RAM.
* **Thư viện chính:**
  * `transformers` (Hugging Face), `torch` (PyTorch 2.x), `onnxruntime-gpu`.
  * `vllm` / `litellm` (để gọi các mô hình LLM API và mô hình mã nguồn mở nội bộ).
  * `scikit-learn`, `evaluate`, `matplotlib`, `seaborn` (vẽ ROC curve, Confusion Matrix, Radar plots).

---

## 2. Tập Dữ Liệu Thực Nghiệm (Benchmark Datasets)

Hệ thống được đánh giá trên tập dữ liệu tiếng Việt thực tế được chuẩn hóa và niêm phong:
1. **Tập Dữ Liệu Lừa Đảo Tiếng Việt Đã Đóng Băng (Frozen Benchmark Corpus - Đã Hoàn Tất):**
   * Nguồn: Hợp nhất từ Cổng cảnh báo Cục An toàn thông tin (NCSC), Dự án Chống Lừa Đảo (ChongLuaDaoV2) và bộ dữ liệu viễn thông mở (`data/raw/vietnamese_sms_merged_all.csv`).
   * Quy mô: **$2.665$ tin nhắn** ($1.918$ tin Ham lành tính - $72.0\%$, $747$ tin Scam độc hại - $28.0\%$).
   * Tập kiểm thử niêm phong (**Frozen Test Set**): Đúng **$N = 267$ mẫu** ($192$ Ham, $75$ Scam) được giữ nguyên vẹn 100% qua tất cả các đợt đánh giá.
2. **Kế hoạch Mở Rộng Quy Mô Lớn (Kaggle Phase 2 Scaling):**
   * Dự kiến mở rộng lên $5.000\text{--}10.000$ mẫu đa kênh (SMS + OTT Zalo/Telegram) để kiểm thử sức chịu tải quy mô mạng viễn thông.

---

## 3. Kết Quả Thực Nghiệm Đối Chứng 5 Runs Đã Đạt Được (Completed Benchmark)

Đề tài đã hoàn thành đánh giá thực nghiệm đa seed (`SEEDS = [42, 100, 123, 999, 2026]`) cho 5 cấu hình mô hình (Trích từ [`results/summary.csv`](file:///C:/Users/USER/RBL_ScamShield/results/summary.csv)):

| Mã Cấu Hình | Tên mô hình | Phụ trách | Accuracy | Precision | **Scam Recall (Cốt lõi)** | Macro-F1 | Kích thước / Độ trễ |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Proposed** | 👑 **ViSoBERT + WBCE ($\alpha=5.0$)** | **Hiếu (Tier 1 Edge)** | **$95.65\% \pm 1.54\%$** | **$89.79\% \pm 5.15\%$** | **$95.62\% \pm 2.25\%$** | **$92.51\% \pm 2.39\%$** | **390 MB / 15.8 ms** |
| **B2.3** | PhoBERT-large (370M) | Huy (Baseline) | $95.95\% \pm 1.57\%$ | $93.13\% \pm 3.17\%$ | $92.33\% \pm 3.44\%$ | $92.70\% \pm 2.87\%$ | 1,480 MB / 54.2 ms |
| **B2.2** | FPT ViBERT-base | Phúc (Baseline) | $95.04\% \pm 1.11\%$ | $90.10\% \pm 4.12\%$ | $92.60\% \pm 2.84\%$ | $91.25\% \pm 1.81\%$ | 480 MB / 18.2 ms |
| **B2.1** | PhoBERT-base-v2 | Trân (Baseline) | $95.11\% \pm 0.83\%$ | $91.24\% \pm 1.52\%$ | $91.23\% \pm 1.84\%$ | $91.23\% \pm 1.50\%$ | 540 MB / 17.5 ms |
| **B3** | Gemini 3.5 Flash (5-shot) | Quang (Cloud API) | $84.50\% \pm 1.02\%$ | $64.47\% \pm 1.52\%$ | **$100.00\% \pm 0.00\%$** | $78.38\% \pm 1.12\%$ | Cloud / 4,912 ms |

---

## 4. Hệ Tiêu Chí Đánh Giá (Evaluation Metrics)

1. **Hiệu năng Phân loại (Classification Performance):**
   * **Accuracy, Precision, Recall, Macro F1-Score:** Đảm bảo mô hình bắt trọn vẹn lừa đảo (High Recall).
   * **False Positive Rate (FPR - Tỷ lệ báo động giả):** Mục tiêu giữ $\text{FPR} < 1.5\%$ để không làm phiền người dùng trước các tin nhắn quảng cáo ngân hàng hợp pháp.
2. **Hiệu năng Vận hành & Kinh tế (Operational & Cost Efficiency):**
   * **Inference Latency:** Độ trễ trung bình (Mean Latency) và độ trễ phân vị 95 ($P95$ Latency tính bằng mili-giây).
   * **Cost per 1,000 Requests:** Chi phí API tính bằng USD trên 1.000 yêu cầu quét.
3. **Thực Nghiệm Bóc Tách (Ablation Study):**
   * *Ablation 1:* Thử nghiệm biến thiên ngưỡng $\tau \in \{0.70, 0.80, 0.85, 0.90, 0.95\}$ để tìm đường biên Pareto tối ưu giữa Độ chính xác và Chi phí.
   * *Ablation 2:* Loại bỏ vai trò **Devil's Advocate (Agent 5)** để chứng minh tầm quan trọng của phản biện trong việc kéo giảm tỷ lệ báo động nhầm (FPR).
