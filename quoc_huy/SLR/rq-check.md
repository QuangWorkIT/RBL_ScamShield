# Kiểm chứng RQ – phần của Lê Quốc Huy
**Nguồn phụ trách:** IEEE Xplore, Google Scholar  
**Lớp bổ sung:** L2 (Tra Semantic Scholar các bài trích dẫn paper mới nhất)  
**Ngày:** 2026-08-25

---

## 1. Bảng Phản Chứng (Ứng viên từ nguồn của tôi)

**RQ Mục Tiêu:**  
*"Với bộ dữ liệu SMS tiếng Việt (N=2,665), mô hình ViSoBERT kết hợp hàm mất mát Cost-Sensitive WBCE (α=5.0) khác các mô hình đối chứng (PhoBERT, FPT ViBERT, Gemini 3.5 Flash) thế nào về Scam Recall và CPU Latency?"*

| Paper | P giống? | I giống? | C giống? | O giống? | Chi tiết đối chiếu |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **M029 (Zhou et al., 2026)** | Có (SMS Fraud) | Không (Dùng Agentic LLMs: Qwen, GPT-5, Gemini) | Có (LLMs đối sánh) | Có (Fraud Recall, Benign Recall) | Đánh giá LLMs đa tác vụ trên tiếng Anh, đạt Fraud Recall 64–90%, nhưng benign recall chỉ đạt 12–30% (mất cân bằng nghiêm trọng). Không xử lý tiếng Việt. |
| **M030 (ElZemity et al., 2026)** | Có (SMS Threat) | Không (Dùng Agentic Distillation SLM Qwen/SmolLM) | Có (DPO Baseline) | Có (Recall, F1) | Đạt Recall 96.25% trên tiếng Anh bằng SLM chưng cất, nhưng không nghiên cứu tác động của hàm mất mát có trọng số WBCE trên dữ liệu mất cân bằng ngôn ngữ thấp tài nguyên. |
| **M032 (SecureNet, 2024)** | Có (Phishing/Spam) | Không (So sánh LSTM, CNN, BERT cơ bản) | Có (Comparative Study) | Một phần (Accuracy, F1) | Nghiên cứu tổng hợp các mô hình DL truyền thống, không có cơ chế tối ưu Edge hay xử lý teencode tiếng Việt. |
| **M036 (Genshin, 2025)** | Có (Network Shield) | Không (Hệ thống phòng thủ mạng) | Không | Một phần (Detection Rate) | Giải pháp cấp độ hạ tầng mạng, không phân tích chuyên sâu ngữ nghĩa văn bản tiếng Việt. |

**Kết luận phần của tôi:**  
* **Không có phản chứng** (Không có bài báo nào giống đủ 4/4 yếu tố P/I/C/O).
* Bài `M029` và `M030` là căn cứ quan trọng xác định tính mới theo dạng **Mở rộng (Extension)**: giải quyết bài toán trade-off giữa độ chính xác và độ nhạy trong bối cảnh ngôn ngữ tiếng Việt.

---

## 2. Lớp Tìm Kiếm Bổ Sung (L2)
* **Quy trình thực hiện:** Chọn paper `M029` (FraudSMSWalker, 2026) trên Semantic Scholar, kiểm tra 12 paper trích dẫn bài này.
* **Kết quả:** Chưa có bài báo nào áp dụng hướng tiếp cận mô hình ngôn ngữ xã hội bản địa hóa (ViSoBERT) kết hợp Cost-Sensitive Loss cho phát hiện lừa đảo tin nhắn. Không có phản chứng.

---

## 3. Ghi Chú Khả Thi Từ Các Paper Đã Đọc
* **Tài nguyên tính toán:** Paper `M030` chứng minh mô hình SLM ($< 1\text{B}$ tham số) có thể chạy mượt mà trên môi trường máy tính cá nhân hoặc thiết bị di động.
* **Chi phí:** Các nghiên cứu sử dụng API LLM thương mại (như `M029`) tốn kém ngân sách lớn nếu quét liên tục hàng ngàn tin nhắn. Do đó, phương án dùng mô hình cục bộ ViSoBERT ONNX INT8 là giải pháp tối ưu chi phí (0 USD chi phí API khi triển khai).
