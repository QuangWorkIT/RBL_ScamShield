# Kiểm chứng RQ – phần của Phan Trần Hoàng Trân
**Nguồn phụ trách:** Scopus, Web of Science, Zenodo  
**Lớp bổ sung:** L1 (Search thẳng vào RQ trên Scholar + Scopus)  
**Ngày:** 2026-08-25

---

## 1. Bảng Phản Chứng (Ứng viên từ nguồn của tôi)

**RQ Mục Tiêu:**  
*"Với bộ dữ liệu SMS tiếng Việt (N=2,665), mô hình ViSoBERT kết hợp hàm mất mát Cost-Sensitive WBCE (α=5.0) khác các mô hình đối chứng (PhoBERT, FPT ViBERT, Gemini 3.5 Flash) thế nào về Scam Recall và CPU Latency?"*

| Paper | P giống? | I giống? | C giống? | O giống? | Chi tiết đối chiếu |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **M014 (QuishingShield, 2026)** | Một phần (QR & Text Lures) | Không (Dùng Llama-3.2-3B đa phương thức) | Không | Có (Latency 45ms, F1 96.4%) | Nghiên cứu về lừa đảo qua mã QR và tin nhắn, mô hình nặng đòi hỏi nhiều RAM di động, không áp dụng cho tin nhắn thuần túy. |
| **M017 (Asif, 2026)** | Có (SMS Spam) | Không (PhoBERT FT thông thường) | Có (GPT-4o-mini, Naive Bayes) | Một phần (F1 95.8%, không đo Recall riêng) | Thử nghiệm PhoBERT trên tấn công prompt injection, không có hàm mất mát có trọng số WBCE. |
| **M018 (Mrinal & Kumar, 2026)** | Có (SMS Lures) | Một phần (Edge MobileBERT nén INT8) | Có (RoBERTa-large teacher) | Có (RAM 8.5MB, Latency 12ms, F1 96.3%) | Đề xuất giải pháp Edge SLM nén mô hình cho SMS, nhưng áp dụng trên tiếng Anh; lượng tử hóa INT8 làm giảm ~0.6% F1. |
| **M019 (Phishing GAT, 2026)** | Có (Scam Lures) | Không (Dùng Graph Attention Networks) | Có (PhoBERT Embeddings) | Một phần (F1 97.4%, ROC-AUC) | Sử dụng PhoBERT để trích xuất đặc trưng đồ thị, kiến trúc pipeline phức tạp, không tối ưu cho suy luận thời gian thực trên di động. |
| **M025 (Saeed, 2023)** | Có (SMS Spam) | Không (SVM + TF-IDF) | Có (Naive Bayes, Random Forest) | Một phần (Accuracy 98.1%) | Thiếu khả năng học biểu diễn ngữ cảnh sâu cho tiếng Việt teencode. |

**Kết luận phần của tôi:**  
* **Không có phản chứng** (Không có bài báo nào giống đủ 4/4 yếu tố P/I/C/O).
* Paper `M018` chứng minh tính khả thi vượt trội của việc nén mô hình sang INT8 cho thiết bị di động (độ trễ đạt $12\text{ ms}$), hỗ trợ trực tiếp cho thiết kế kỹ thuật của đề tài nhóm.

---

## 2. Lớp Tìm Kiếm Bổ Sung (L1)
* **Search Query L1:** `"ViSoBERT" AND ("weighted cross entropy" OR "cost-sensitive") AND ("SMS" OR "message")`
* **Cơ sở dữ liệu:** Scopus + Google Scholar
* **Số kết quả:** 0 kết quả trùng khớp.
* **Đánh giá phản chứng:** Hoàn toàn chưa có nghiên cứu nào kết hợp ViSoBERT với hàm mất mát Weighted BCE để giải quyết bài toán mất cân bằng chi phí phân loại lừa đảo. Không có phản chứng.

---

## 3. Ghi Chú Khả Thi Từ Các Paper Đã Đọc
* **Tối ưu hóa mô hình:** Paper `M018` cho thấy việc chuyển đổi mô hình sang ONNX INT8 có thể chạy ổn định trên CPU di động thông thường với mức chiếm dụng bộ nhớ RAM rất thấp ($< 10\text{MB}$ đối với SLM hoặc $\approx 100–390\text{MB}$ với ViSoBERT).
* **Độ chính xác:** Việc nén mô hình sang 8-bit chỉ làm giảm độ chính xác không đáng kể ($< 1\%$), hoàn toàn chấp nhận được để đổi lấy tốc độ và khả năng bảo mật dữ liệu cục bộ.
