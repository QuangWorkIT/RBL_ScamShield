# 🎯 KIỂM CHỨNG CÂU HỎI NGHIÊN CỨU TỔNG HỢP CẢ NHÓM (RQ VALIDATION)
### Đề tài: ScamShield-VN — Evidence-Grounded Vietnamese Scam & Phishing Detection Platform
> **File:** `team-synthesis/rq-validation.md`  
> **Tổng hợp bởi:** Project Lead (Nguyễn Trung Hiếu)  
> **Căn cứ:** 5 bản kiểm chứng cá nhân (`SLR/rq-check.md`), Bản đồ bằng chứng (`rq-evidence-map.md`), và Bảng bằng chứng gộp 34 bài báo (`evidence-table-merged.md`)

---

## 1. Câu Hỏi Nghiên Cứu Nguyên Văn (RQ) & Khung PICO

> **Phát biểu RQ:**  
> *"Với bộ dữ liệu SMS tiếng Việt ($N=2,665$), mô hình ViSoBERT kết hợp hàm mất mát Weighted Binary Cross-Entropy (WBCE, $\alpha=5.0$) khác các mô hình đối chứng (PhoBERT-base, FPT ViBERT, PhoBERT-large, Gemini 3.5 Flash) thế nào về Scam Recall và CPU Latency?"*

### Bốn Mảnh PICO:
* **P (Population / Task):** $2.665$ tin nhắn SMS và tin nhắn mạng xã hội tiếng Việt; tập Frozen Test Set niêm phong $N=267$ mẫu (192 Ham, 75 Scam).
* **I (Intervention):** Mô hình ViSoBERT tiền huấn luyện trên dữ liệu mạng xã hội tiếng Việt, tích hợp hàm mất mát Cost-Sensitive WBCE ($\alpha=5.0$) và tối ưu suy luận On-device CPU qua định dạng ONNX INT8.
* **C (Comparison / Baselines):** PhoBERT-base-v2, FPT ViBERT-base, PhoBERT-large (370M tham số), và Gemini 3.5 Flash (5-shot In-Context Learning).
* **O (Outcome / Metrics):** Scam Recall ($\ge 95.0\%$), Macro-F1, Precision, và CPU Latency ($\le 30\text{ ms/tin nhắn}$).

---

## 2. Bằng Chứng Làm Nền (Evidence Baseline Summary)
* **Tổng số bài báo gộp:** $N = 34$ bài báo khoa học đã xuất bản từ năm 2020 đến 2026.
* **Độ bao phủ của Evidence Table:**
  * Cổng P1 ($\ge 12$ paper): **ĐẠT (34/12 bài)**.
  * Cổng P2 (Cột Tool/LLM $\ge 90\%$ có dữ liệu): **ĐẠT (100% có tên mô hình cụ thể)**.
  * Cổng P3 (Cột Kết quả $\ge 50\%$ có con số): **ĐẠT (100% có số liệu đo đạc cụ thể)**.
  * Cổng P4 (Cột Hạn chế $\ge 50\%$ có dữ liệu): **ĐẠT (100% trích xuất từ Threats to Validity)**.
  * Cổng P5 (Tên Metric cụ thể): **ĐẠT (Ghi rõ Recall, F1, Accuracy, Latency, RAM)**.

---

## 3. Tổng Hợp Phản Chứng & Nhãn Tính Mới (Novelty Assessment)
Sau khi tổng hợp báo cáo kiểm chứng từ cả 5 nguồn dữ liệu độc lập của 5 thành viên:
* **Số bài báo giống đủ 4/4 yếu tố PICO:** **0 bài** $\rightarrow$ Khẳng định **KHÔNG CÓ PHẢN CHỨNG**.
* **Số bài báo giống 3/4 yếu tố:** **2 bài** (`M029` - FraudSMSWalker 2026; `M030` - Agentic Distillation SLM 2026).
* **Nhãn tính mới của đề tài:** **MỞ RỘNG NGHIÊN CỨU (Research Extension)**.
* **Lý do:** Các nghiên cứu quốc tế gần đây (`M029`, `M030`) đã bắt đầu khảo sát hiệu năng phân loại lừa đảo bằng mô hình ngôn ngữ nhưng chỉ tập trung trên ngữ liệu tiếng Anh tiêu chuẩn. Đề tài của nhóm **mở rộng phạm vi khoa học sang ngôn ngữ bản địa tiếng Việt giàu teencode, từ lóng mạng xã hội và giải quyết triệt để sự mất cân bằng chi phí phân loại (Asymmetric Cost of Misclassification)** thông qua hàm mất mát $\mathcal{L}_{\text{WBCE}}$ ($\alpha=5.0$).

---

## 4. Đánh Giá Khả Thi Lần Cuối (7 Tiêu Chí Feasibility)

| Tiêu chí | Trạng thái | Đánh giá chi tiết | Đối sách & Phương án dự phòng |
| :--- | :---: | :--- | :--- |
| **1. Dataset** | 🟢 **An toàn** | Đã thu thập và làm sạch $2.665$ mẫu SMS từ 2 nguồn Hugging Face công khai (`data/raw/`). | Tập Frozen Test Set $N=267$ đã được niêm phong cố định. |
| **2. API / Tool** | 🟢 **An toàn** | Mô hình đề xuất (ViSoBERT) chạy hoàn toàn cục bộ (0 USD chi phí API). Baseline Gemini dùng Google AI Studio API free tier. | Nếu API vượt hạn mức, chuyển sang chạy Gemini theo batch có giãn cách. |
| **3. Tính toán** | 🟢 **An toàn** | Huấn luyện trên GPU Kaggle/Colab T4 miễn phí (~7 phút cho 5 runs ViSoBERT). Suy luận CPU laptop thông thường. | Checkpoint lưu định kỳ sau mỗi epoch; mô hình ONNX INT8 siêu nhẹ ($390\text{MB}$). |
| **4. Ground truth**| 🟢 **An toàn** | Dữ liệu đã có sẵn nhãn nhị phân chuẩn (0: Ham, 1: Scam) được kiểm định bởi chuyên gia. | Không cần tốn thêm thời gian gán nhãn thủ công diện rộng. |
| **5. Code base** | 🟢 **An toàn** | ViSoBERT có sẵn trên Hugging Face Hub (`uitnlp/visobert`). Pipeline ONNX Runtime đã test hoàn chỉnh. | Scripts huấn luyện và benchmark 5 runs đã được kiểm thử thành công. |
| **6. Kỹ năng** | 🟢 **An toàn** | Nhóm nắm vững thư viện PyTorch, Transformers, ONNX Runtime và Scikit-learn. | Đã hoàn thành các script đo đạc độ trễ và tối ưu threshold. |
| **7. Thời gian** | 🟢 **An toàn** | Thời gian chạy thực nghiệm mỗi mô hình chỉ mất $7–25$ phút. Hoàn toàn chủ động tiến độ. | Đạt với $\ge 1$ tuần dự phòng trước hạn chót bảo vệ đề tài. |

> **Tổng kết Khả thi:** **0 mục 🔴 (Không làm được)**, **0 mục 🟡 (Rủi ro)** $\rightarrow$ **DỰ ÁN AN TOÀN TUYỆT ĐỐI ĐỂ TRIỂN KHAI**.

---

## 5. Phát Biểu Khoảng Trống Nghiên Cứu (Research Gap Statement)
*(Sử dụng trực tiếp cho Section 2 của bài báo và Proposal)*:

> *"Trong các nghiên cứu đã xem xét, chưa có công trình nào đánh giá mô hình chuyên biệt ngữ cảnh tiếng Việt mạng xã hội (ViSoBERT) kết hợp hàm tổn thất nhạy cảm chi phí Weighted BCE ($\alpha=5.0$) cho bài toán phát hiện tin nhắn lừa đảo viễn thông tiếng Việt với mục tiêu tối đa hóa Scam Recall ($\ge 95\%$) trên thiết bị Edge thời gian thực."*

### Phân Loại 4 Khoảng Trống:
* **`GAP-T` (Technology):** Kỹ thuật phạt lỗi bất cân xứng Cost-Sensitive Loss ($\alpha=5.0$) chưa từng được tích hợp vào kiến trúc ViSoBERT để giải quyết bài toán lừa đảo tài chính.
* **`GAP-M` (Measurement):** Các nghiên cứu trước chỉ tập trung đo lường Accuracy tổng thể hoặc Macro-F1 mà bỏ qua chỉ số then chốt quyết định an toàn người dùng là **Scam Recall (khả năng bắt trọn mọi tin nhắn độc hại)**.
* **`GAP-D` (Domain/Data):** Ngữ liệu tin nhắn lừa đảo ngân hàng tiếng Việt chứa nhiều teencode, viết tắt, ký tự thay thế để lách bộ lọc viễn thông chưa được đưa vào các benchmark quốc tế.
* **`GAP-S` (Shared Limitation):** Các mô hình LLM lớn thương mại (GPT-4, Gemini) tuy thông minh nhưng có độ trễ lớn ($> 1.000\text{ ms}$) và chi phí vận hành cao, không khả thi để nhúng vào ứng dụng bảo vệ SMS On-device thời gian thực.

---

## 6. Thiết Kế Sơ Bộ Thực Nghiệm & Cặp Giả Thuyết Thống Kê

* **Bộ dữ liệu:** $2.665$ tin nhắn tiếng Việt ($1.918$ Ham, $747$ Scam). Tập kiểm thử niêm phong Frozen Test Set: $N=267$ mẫu (192 Ham, 75 Scam).
* **Kiểm định thống kê:** **McNemar test ghép cặp** (dữ liệu phân loại nhị phân Đúng/Sai trên cùng 267 mẫu kiểm thử giữa mô hình đề xuất và từng baseline).
* **Mức ý nghĩa:** $\alpha = 0.05$.
* **Cặp Giả Thuyết:**
  * **$H_0$ (Giả thuyết không):** Không có sự khác biệt có ý nghĩa thống kê về tỷ lệ phân loại đúng giữa mô hình đề xuất ViSoBERT + WBCE ($\alpha=5.0$) và các mô hình đối chứng baseline ($p \ge 0.05$).
  * **$H_1$ (Giả thuyết đối):** Có sự khác biệt có ý nghĩa thống kê về tỷ lệ phân loại đúng giữa mô hình đề xuất ViSoBERT + WBCE ($\alpha=5.0$) và các mô hình đối chứng baseline ($p < 0.05$).
* **Tiêu chí chấp nhận thực tiễn (Threshold có nguồn - Case 2 & Case 3):**
  * Scam Recall đạt $\ge 95.0\%$.
  * CPU Inference Latency $\le 30.0\text{ ms/tin nhắn}$.

---

## 7. Quyết Định Của Nhóm
* **GIỮ NGUYÊN CÂU HỎI NGHIÊN CỨU (RQ) ĐÃ THỐNG NHẤT VỚI GVHD.**
* Tiến hành đóng băng thiết kế nghiên cứu và kết xuất hồ sơ sang `team-synthesis/proposal.md` để hoàn tất Giai đoạn 2.
