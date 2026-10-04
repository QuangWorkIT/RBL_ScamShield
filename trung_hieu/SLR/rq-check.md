# Kiểm chứng RQ – phần của Nguyễn Trung Hiếu
**Nguồn phụ trách:** ArXiv, OpenAlex, Semantic Scholar  
**Lớp bổ sung:** L1 (Search thẳng vào RQ trên Scholar + IEEE)  
**Ngày:** 2026-08-25

---

## 1. Bảng Phản Chứng (Ứng viên từ nguồn của tôi)

**RQ Mục Tiêu:**  
*"Với bộ dữ liệu SMS tiếng Việt (N=2,665), mô hình ViSoBERT kết hợp hàm mất mát Cost-Sensitive WBCE (α=5.0) khác các mô hình đối chứng (PhoBERT, FPT ViBERT, Gemini 3.5 Flash) thế nào về Scam Recall và CPU Latency?"*

| Paper | P giống? | I giống? | C giống? | O giống? | Chi tiết đối chiếu |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **P001 (Tang et al., 2026)** | Không | Không | Có | Không | Nghiên cứu về Text-to-Image Diffusion models, không liên quan đến bài toán phân loại tin nhắn lừa đảo. |
| **P446 (Konstantinou et al., 2026)** | Có (Scam Detection) | Không (Dùng LLM thuần túy) | Có (Prompt-based LLMs) | Có (Recall & Accuracy) | Đánh giá Generative AI cho phát hiện lừa đảo, đạt Recall 88–92% nhưng chưa áp dụng kỹ thuật phạt chi phí mất cân bằng nhãn trên tiếng Việt. |
| **M023 (Xie, 2025)** | Có (Scam Messages) | Không (Chỉ dùng BERT chuẩn) | Có (Logistic Regression, KNN) | Một phần (Accuracy) | Thử nghiệm fine-tuning BERT trên tập tin nhắn lừa đảo nhưng không xử lý vấn đề false negative bias. |
| **M039 (Siddiq et al., 2024)** | Không | Có (Fine-tuning) | Có (Baseline so sánh) | Không | Tập trung vào kiểm thử mã nguồn, không thuộc miền an ninh thông tin văn bản. |

**Kết luận phần của tôi:**  
* **Không có phản chứng** (Không có bài báo nào giống đủ 4/4 yếu tố P/I/C/O).
* Bài `P446` đạt 3/4 yếu tố $\rightarrow$ Xác nhận đề tài thuộc nhóm **Mở rộng (Extension)**: giải quyết bài toán tối ưu độ nhạy lừa đảo (*Scam Recall*) trên ngôn ngữ bản địa tiếng Việt.

---

## 2. Lớp Tìm Kiếm Bổ Sung (L1)
* **Search Query L1:** `"ViSoBERT" AND ("scam" OR "phishing" OR "spam") AND ("recall" OR "cost-sensitive")`
* **Cơ sở dữ liệu:** Google Scholar + IEEE Xplore
* **Số kết quả thu được:** 6 kết quả.
* **Đánh giá phản chứng:** Các nghiên cứu hiện tại chủ yếu dùng ViSoBERT cho phân tích cảm xúc (Sentiment Analysis) hoặc gán nhãn thực thể tên riêng (NER) trên mạng xã hội; **chưa có bài báo nào áp dụng ViSoBERT với hàm mất mát WBCE ($\alpha=5.0$) cho bài toán phát hiện tin nhắn lừa đảo**. Không có phản chứng.

---

## 3. Ghi Chú Khả Thi Từ Các Paper Đã Đọc
* **Mã nguồn:** Hầu hết các bài báo hiện đại đều cung cấp mã nguồn dựa trên thư viện `transformers` và `PyTorch`. ViSoBERT đã có sẵn trên Hugging Face Hub (`uitnlp/visobert`).
* **Cỡ mẫu:** Các nghiên cứu thường thực nghiệm trên $2.000–5.000$ mẫu tin nhắn văn bản. Cỡ mẫu $2.665$ của nhóm hoàn toàn phù hợp và đủ độ tin cậy thống kê.
* **Khó khăn ghi nhận:** Các bài báo chỉ ra rằng mô hình LLM lớn chạy chậm và tốn chi phí API, do đó việc nén mô hình sang ONNX INT8 chạy trên CPU Edge là hướng tiếp cận rất khả thi và có tính ứng dụng cao.
