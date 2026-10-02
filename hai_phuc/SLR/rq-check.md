# Kiểm chứng RQ – phần của Hoàng Hải Phúc
**Nguồn phụ trách:** ACM Digital Library, CrossRef  
**Lớp bổ sung:** L3 (Tìm 1 bài Survey/SLR về chủ đề từ 2023)  
**Ngày:** 2026-08-25

---

## 1. Bảng Phản Chứng (Ứng viên từ nguồn của tôi)

**RQ Mục Tiêu:**  
*"Với bộ dữ liệu SMS tiếng Việt (N=2,665), mô hình ViSoBERT kết hợp hàm mất mát Cost-Sensitive WBCE (α=5.0) khác các mô hình đối chứng (PhoBERT, FPT ViBERT, Gemini 3.5 Flash) thế nào về Scam Recall và CPU Latency?"*

| Paper | P giống? | I giống? | C giống? | O giống? | Chi tiết đối chiếu |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **M006 (Financial Fraud, 2026)** | Một phần (Multilingual text) | Không (Dùng mBERT, XLM-RoBERTa không tối ưu chi phí) | Có (Multilingual PLMs) | Một phần (F1, Accuracy) | Đánh giá phát hiện gian lận đa ngôn ngữ nhưng không đi sâu vào đặc thù teencode/tiếng lóng mạng xã hội Việt Nam. |
| **M008 (Smishing ML, 2025)** | Có (Smishing detection) | Không (Dùng ML truyền thống: Random Forest, SVM) | Có (ML baselines) | Một phần (Accuracy: 97%) | Bài toán phân loại tin nhắn rác truyền thống, bỏ qua ngữ cảnh sâu của Transformer. |
| **M010 (On-Device Smishing, 2026)** | Có (Mobile smishing) | Một phần (On-device quantization) | Không | Có (Latency < 20ms, Recall) | Paper đề xuất bộ phân loại trên thiết bị di động nhưng áp dụng cho tiếng Anh, không có cơ chế Weighted BCE loss. |
| **M013 (Ata & Alsmadi, 2023)** | Có (Spam SMS) | Không (Naive Bayes, RNN) | Có (Baselines) | Một phần (Accuracy 98.74%) | Dữ liệu mất cân bằng nặng (86% Ham vs 14% Spam) nhưng tác giả thừa nhận đã bỏ qua việc xử lý mất cân bằng nhãn. |

**Kết luận phần của tôi:**  
* **Không có phản chứng** (Không có bài báo nào giống đủ 4/4 yếu tố P/I/C/O).
* Paper `M013` trực tiếp xác nhận khoảng trống nghiên cứu cốt lõi mà đề tài chúng ta đang giải quyết: **nhiều nghiên cứu trước đây bỏ qua việc xử lý mất cân bằng nhãn và chi phí phạt false negative**.

---

## 2. Lớp Tìm Kiếm Bổ Sung (L3)
* **Search Query L3:** `"systematic review" AND ("smishing" OR "SMS phishing" OR "scam detection")` (Giới hạn từ 2023 đến nay).
* **Bài Survey tìm được:** *A Systematic Literature Review on Mobile Phishing and Smishing Countermeasures* (2024).
* **Đánh giá phản chứng:** Bài survey chỉ ra rằng hơn 75% các nghiên cứu về SMS scam chỉ tập trung vào tiếng Anh; các ngôn ngữ dấu thanh và teencode phức tạp như tiếng Việt hoàn toàn vắng bóng trong các giải pháp On-device tối ưu hóa độ nhạy lừa đảo. Không có phản chứng.

---

## 3. Ghi Chú Khả Thi Từ Các Paper Đã Đọc
* **Độ trễ và triển khai thực tế:** Paper `M010` khẳng định mô hình On-device cần độ trễ dưới $50\text{ ms}$ để không gây gián đoạn trải nghiệm người dùng khi nhận tin nhắn SMS.
* **Xử lý dữ liệu:** Phần lớn các nghiên cứu sử dụng tập dữ liệu công khai từ Kaggle hoặc UCI. Việc nhóm thu thập và làm sạch $2.665$ mẫu tiếng Việt thực tế là một đóng góp rất giá trị cho cộng đồng nghiên cứu trong nước.
