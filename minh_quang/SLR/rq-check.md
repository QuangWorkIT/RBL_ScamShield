# Kiểm chứng RQ – phần của Nguyễn Minh Quang
**Nguồn phụ trách:** SpringerLink, ScienceDirect, ACL Anthology  
**Lớp bổ sung:** L2 (Tra cứu bài trích dẫn trên Semantic Scholar)  
**Ngày:** 2026-08-25

---

## 1. Bảng Phản Chứng (Ứng viên từ nguồn của tôi)

**RQ Mục Tiêu:**  
*"Với bộ dữ liệu SMS tiếng Việt (N=2,665), mô hình ViSoBERT kết hợp hàm mất mát Cost-Sensitive WBCE (α=5.0) khác các mô hình đối chứng (PhoBERT, FPT ViBERT, Gemini 3.5 Flash) thế nào về Scam Recall và CPU Latency?"*

| Paper | P giống? | I giống? | C giống? | O giống? | Chi tiết đối chiếu |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **M001 (Vu Minh Tuan, 2023)** | Có (Phishing detection) | Không (Dùng BERT, RoBERTa chuẩn) | Có (Transformer baselines) | Một phần (Accuracy, F1) | Đánh giá hiệu quả của các mô hình Transformer cho phát hiện phishing nhưng chỉ chạy trên tiếng Anh, không có cơ chế phạt chi phí nhầm lẫn. |
| **M002 (Nguyen-Xuan, 2026)** | Có (Vietnamese text) | Không (Mixed-Language Transformer tổng quát) | Có (Multilingual PLMs) | Một phần (F1-score) | Tập trung vào bài toán dịch máy và phân loại ngữ nghĩa tiếng Việt đa pha trộn, không chuyên sâu vào bài toán an ninh lừa đảo. |
| **M003 (Nguyen Tan Cam, 2026)** | Có (Vietnamese spam/scam) | Không (Dùng PhoBERT chuẩn với CE loss) | Có (PhoBERT baseline) | Một phần (Accuracy, Macro-F1) | Giới thiệu tập dữ liệu VNSED nhưng chỉ thử nghiệm PhoBERT thông thường; tác giả ghi nhận hạn chế tỷ lệ bỏ sót tin nhắn lừa đảo còn cao do không phạt nặng lỗi False Negative. |
| **M005 (Sbei, 2024)** | Có (Phishing text) | Không (Transformer chuẩn) | Có (Baselines) | Một phần (F1-score) | Khảo sát hiệu năng của Transformer trên dữ liệu phishing tiếng Anh chuẩn. |

**Kết luận phần của tôi:**  
* **Không có phản chứng** (Không có bài báo nào giống đủ 4/4 yếu tố P/I/C/O).
* Paper `M003` (VNSED, 2026) là minh chứng học thuật đắt giá nhất cho khoảng trống nghiên cứu của chúng ta: **chính tác giả của bộ dữ liệu VNSED đã chỉ ra rằng việc sử dụng Cross-Entropy thông thường khiến mô hình bị lệch và bỏ sót nhiều tin nhắn lừa đảo quan trọng**.

---

## 2. Lớp Tìm Kiếm Bổ Sung (L2)
* **Quy trình thực hiện:** Kiểm tra 15 bài báo trích dẫn paper `M003` (VNSED) trên Semantic Scholar.
* **Kết quả:** Chưa có nghiên cứu nào tiếp tục cải tiến VNSED bằng cách huấn luyện mô hình ngôn ngữ mạng xã hội chuyên biệt (ViSoBERT) kết hợp với hàm mất mát có trọng số WBCE ($\alpha=5.0$) và xuất bản mô hình ONNX thời gian thực. Không có phản chứng.

---

## 3. Ghi Chú Khả Thi Từ Các Paper Đã Đọc
* **Tài nguyên tiếng Việt:** Paper `M002` và `M003` xác nhận việc sử dụng bộ tokenizer tiền huấn luyện trên tiếng Việt (như PhoBERT hay ViSoBERT) mang lại hiệu quả biểu diễn ngữ nghĩa vượt trội so với các mô hình đa ngôn ngữ tổng quát như mBERT hay XLM-RoBERTa.
* **Tính khả thi của đề tài:** Khung thực nghiệm của nhóm giải quyết đúng điểm nghẽn mà `M003` để ngỏ, đảm bảo tính đóng góp khoa học rõ ràng và thuyết phục khi bảo vệ trước Hội đồng.
