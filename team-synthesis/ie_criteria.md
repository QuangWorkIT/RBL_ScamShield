# 📋 TIÊU CHÍ LỰA CHỌN VÀ LOẠI TRỪ TÀI LIỆU DÙNG CHUNG CẢ NHÓM (IE CRITERIA)
### Đề tài: ScamShield-VN — Evidence-Grounded Vietnamese Scam & Phishing Detection Platform
> **File:** `team-synthesis/ie_criteria.md`  
> **Phiên bản:** 1.0 (PRISMA 2020 Compliant)  
> **Áp dụng:** Toàn bộ 5 thành viên trong nhóm (Trung Hiếu, Quốc Huy, Hải Phúc, Hoàng Trân, Minh Quang)

---

## 1. Khung PICO Cốt Lõi Của Đề Tài

| Thành phần | Định nghĩa trong Đề tài ScamShield-VN | Từ khóa đại diện |
| :--- | :--- | :--- |
| **P (Population / Task)** | Tin nhắn rác, tin nhắn lừa đảo tài chính, mạo danh ngân hàng/thương hiệu tiếng Việt (SMS, mạng xã hội, tin nhắn OTT). | `Vietnamese text`, `SMS phishing`, `smishing`, `scam messages`, `fraudulent messages`, `social media scam` |
| **I (Intervention)** | Mô hình ngôn ngữ tiền huấn luyện tối ưu cho tiếng Việt mạng xã hội (ViSoBERT) kết hợp hàm mất mát có trọng số nhạy cảm chi phí ($\mathcal{L}_{\text{WBCE}}$ với $\alpha=5.0$) và suy luận tối ưu trên Edge (ONNX INT8). | `ViSoBERT`, `cost-sensitive learning`, `weighted binary cross-entropy`, `ONNX quantization`, `edge deployment`, `few-shot LLM` |
| **C (Comparison / Baseline)** | Các mô hình nền tảng đối chứng: Pre-trained Language Models tiếng Việt tiêu chuẩn (PhoBERT-base-v2, FPT ViBERT-base, PhoBERT-large) và LLM thương mại (Gemini 3.5 Flash / GPT-4o-mini). | `PhoBERT`, `ViBERT`, `BERT-base`, `GPT-4o-mini`, `Gemini Flash`, `traditional ML` |
| **O (Outcome / Metrics)** | Khả năng bắt trọn tin nhắn lừa đảo và độ trễ thực tế: Scam Recall (bắt buộc $\ge 95\%$), Macro-F1, Precision, và CPU Latency ($\le 30\text{ ms/msg}$). | `Recall`, `Scam Recall`, `F1-score`, `Precision`, `Accuracy`, `Inference latency`, `Model size` |

---

## 2. Tiêu Chí Lựa Chọn (Inclusion Criteria - IC)

Mỗi bài báo được giữ lại (**INCLUDE**) phải thỏa mãn đồng thời các tiêu chí sau:

* **`IC1` (Chủ đề nghiên cứu - Relevance to PICO):**
  * Bài báo tập trung vào phát hiện tin nhắn lừa đảo, phishing, spam, fraud detection trên văn bản (đặc biệt ưu tiên tiếng Việt hoặc các ngôn ngữ ít tài nguyên / mạng xã hội).
  * Nghiên cứu so sánh hoặc áp dụng các mô hình Transformer, PLM (BERT, RoBERTa, PhoBERT, ViSoBERT) hoặc LLM (Prompt-based / Few-shot).
* **`IC2` (Báo cáo thực nghiệm định lượng - Empirical Evidence):**
  * Bắt buộc phải có số liệu thực nghiệm đo đạc rõ ràng trong Bảng (Table) hoặc Hình (Figure) về ít nhất một trong các chỉ số: Recall, F1-score, Precision, Accuracy, Latency, hoặc Model Size.
* **`IC3` (Thời gian xuất bản - Publication Window):**
  * Xuất bản từ năm **2020 đến nay (2026)** để đảm bảo tính cập nhật với kỷ nguyên Transformer và Large Language Models.
* **`IC4` (Ngôn ngữ & Loại hình ấn phẩm - Language & Venue):**
  * Văn bản toàn văn (Full-text) bằng tiếng Anh hoặc tiếng Việt.
  * Xuất bản trên các tạp chí quốc tế uy tín (Scopus/Web of Science), kỷ yếu hội nghị chuyên ngành (IEEE, ACM, Springer LNCS) hoặc bản thảo khoa học có thể kiểm chứng độc lập trên arXiv/Zenodo.

---

## 3. Tiêu Chí Loại Trừ (Exclusion Criteria - EC)

Loại bỏ ngay lập tức (**EXCLUDE**) nếu bài báo rơi vào bất kỳ trường hợp nào sau đây:

* **`EC1` (Lệch miền nghiên cứu - Out of Scope / Wrong Population):**
  * Phát hiện lừa đảo chỉ dựa trên metadata mạng viễn thông, traffic logs, địa chỉ IP, tín hiệu phần cứng di động mà hoàn toàn không phân tích nội dung văn bản (*Text-agnostic*).
  * Lừa đảo hình ảnh, video deepfake thuần túy không có thành phần phân tích ngữ nghĩa văn bản.
* **`EC2` (Thiếu báo cáo định lượng - No Quantitative Results):**
  * Các bài báo dạng quan điểm, khảo sát định tính thuần túy, bài báo cáo tổng quan mà không có số liệu thực nghiệm đo đạc cụ thể để trích xuất vào Evidence Table.
* **`EC3` (Không có toàn văn - No Full-Text Access):**
  * Không thể truy cập bài báo toàn văn qua các cổng thư viện học thuật hoặc repository mở.
* **`EC4` (Trùng lặp - Duplicate Record):**
  * Cùng một nghiên cứu xuất bản ở nhiều cơ sở dữ liệu khác nhau (giữ lại bản chính thức có DOI).
* **`EC5` (Bài báo AI sinh chưa qua bình duyệt - AI-Generated Unverified Papers):**
  * Các bài báo do hệ thống tự động sinh (như ScientistTwo) chưa qua bình duyệt, không được công nhận là bằng chứng khoa học nền tảng.

---

## 4. Chuỗi Truy Vấn Mẫu (Standard Search Strings)

### Chuỗi A (Cơ sở dữ liệu IEEE Xplore / ACM Digital Library):
```sql
("phishing" OR "scam" OR "fraud" OR "smishing" OR "spam") 
AND ("SMS" OR "message" OR "text" OR "Vietnamese" OR "social media") 
AND ("BERT" OR "PhoBERT" OR "ViSoBERT" OR "Transformer" OR "LLM" OR "few-shot") 
AND ("recall" OR "F1" OR "detection" OR "cost-sensitive")
```

### Chuỗi B (Semantic Scholar / OpenAlex / Google Scholar):
```sql
("Vietnamese scam detection" OR "Vietnamese spam SMS") AND ("PhoBERT" OR "ViSoBERT" OR "language model")
```

---

## 5. Quy Trình Sàng Lọc 2 Vòng & Kiểm Định Độc Lập

1. **Vòng 1 (Title & Abstract Screening):**
   * Đọc tiêu đề, từ khóa và phần tóm tắt của tất cả các bản ghi thu thập được.
   * Gán nhãn `INCLUDE`, `EXCLUDE` (kèm mã lý do: `EC1`, `EC2`, `EC4`...), hoặc `UNSURE`.
   * Xuất kết quả sang file `02_after_screening_v1.csv`.
2. **Vòng 2 (Full-Text Screening):**
   * Tải toàn văn các bài báo vượt qua Vòng 1 hoặc đang ở trạng thái `UNSURE`.
   * Đọc kỹ Section 3 (Methodology), Table/Figure kết quả (Section 4), và Threats to Validity.
   * Quyết định danh sách bài báo chính thức đưa vào `03_final_included.csv` và `evidence-table.md`.
3. **Double Screening (Kiểm tra chéo 20%):**
   * Mỗi thành viên kiểm tra ngẫu nhiên $20\%$ số bài báo bị loại của một thành viên khác để đo lường độ khách quan và tính đồng thuận.
