# GAP Analysis — Thiếu hụt Dữ liệu Tiếng Việt & Kỹ thuật Né tránh Teencode / Dấu

**Thành viên:** Nguyễn Minh Quang (`minh_quang`)  
**GAP type:** GAP-D (Dataset)  
**Ngày:** 2026-08-31  
**Evidence table nguồn:** `team-synthesis/evidence-table-merged.md`  
**N =** 6 bài báo core (`M001`, `M002`, `M003`, `M008`, `M009`, `M011`)

---

## 1. Mô tả GAP

Hiện nay, chưa có nghiên cứu nào xây dựng một bộ dữ liệu chuẩn hóa về tin nhắn lừa đảo tiếng Việt được tích hợp kỹ thuật tăng cường dữ liệu (Data Augmentation) nhằm chủ động mô phỏng các biến thể teencode, tiếng lóng và cố ý sai lỗi chính tả/mất dấu để huấn luyện mô hình chống vượt rào.

**Bằng chứng từ evidence table:**
*   **Cột Dataset & Context / Ngôn ngữ:** Các nghiên cứu về tiếng Việt hiện có (`M001`, `M002`, `M003`) bị phân mảnh mạnh: `M001` chỉ tập trung vào SMS với 2 biến thể có/không dấu đơn thuần; `M002` giải quyết lừa đảo mạng xã hội trộn lẫn Anh-Việt (code-mixed); `M003` xây dựng tập dữ liệu cho email chứ không phải tin nhắn ngắn SMS.
*   **Cột Hạn chế (Limitations & Threats to Validity):** Các bài báo về ngôn ngữ tài nguyên thấp (`M008`, `M009`, `M011`) đều chỉ ra điểm nghẽn lớn: mô hình phân loại bị suy giảm hiệu năng nghiêm trọng trước các phương ngữ phi chuẩn, từ viết tắt và tiếng lóng/teencode (`M008`), hoặc gặp nguy cơ rò rỉ dữ liệu / mất cân bằng nhãn (`M009`, `M011`).
*   **Cột Phương pháp luận (Tool / Architecture):** Trong khi `M011` đã chứng minh kỹ thuật *Easy Data Augmentation (EDA)* giúp tăng trung bình 12% F1-score cho các lớp thiểu số trên SMS tiếng Indonesia, thì ở ngữ cảnh tiếng Việt (`M001`, `M002`, `M003`), chưa có bất kỳ công trình nào áp dụng Data Augmentation (EDA hoặc LLM Few-Shot) để sinh biến thể teencode nhằm tăng cường độ bền vững cho bộ phân loại (như PhoBERT).

---

## 2. Kiểm tra phản chứng

| Paper | Đã làm GAP này không? | Chi tiết |
| :--- | :--- | :--- |
| **M001** *(Tuấn et al., 2023)* | Có (một phần) | Đã thử nghiệm trên 3 biến thể SMS tiếng Việt (có dấu, không dấu, hỗn hợp). Tuy nhiên, nghiên cứu không dùng Data Augmentation để sinh biến thể teencode/tiếng lóng mà chỉ đề xuất khôi phục dấu thủ công hoặc bằng AI trong tương lai. |
| **M002** *(Nguyen-Xuan et al., 2026)* | Không | Đề xuất kiến trúc MLTEA (PhoBERT + XLM-RoBERTa) xử lý từ ghép trộn lẫn tiếng Việt-Anh trên mạng xã hội. Tác giả thừa nhận mô hình vẫn thất bại trước tiếng lóng bị trộn lẫn nặng và không áp dụng Data Augmentation để sinh teencode. |
| **M003** *(Cam et al., 2026)* | Không | Đã xây dựng bộ dữ liệu 6.008 mẫu tiếng Việt nhưng tập trung vào Email spam, không xử lý đặc thù SMS ngắn và không giải quyết bài toán biến thể teencode. |
| **M008** *(Lihawa & Mwambe, 2025)* | Không | Thực hiện phát hiện tin nhắn lừa đảo trên ngôn ngữ Kiswahili. Nghiên cứu chỉ ra hạn chế của Swahili-BERT trước từ viết tắt và tiếng lóng địa phương, không áp dụng cho tiếng Việt. |
| **M009** *(Mambina et al., 2024)* | Không | Tập trung phân loại SMS spam tiếng Swahili, sử dụng SMOTE trên word embeddings để giải quyết mất cân bằng mẫu, không liên quan đến teencode tiếng Việt. |
| **M011** *(Latifah et al., 2024)* | Có (một phần) | Áp dụng thành công kỹ thuật Easy Data Augmentation (EDA) kết hợp IndoBERT trên tập SMS tiếng Indonesia, chứng minh tính khả thi của phương pháp nhưng chưa từng thực hiện trên tiếng Việt. |

**Kết luận:** **GAP 1 ĐƯỢC XÁC NHẬN** (Không có bài báo nào trong 6 paper giải quyết trọn vẹn việc dùng Data Augmentation sinh biến thể teencode cho tin nhắn lừa đảo tiếng Việt).

---

### Supplementary Validation (Vì N = 6 < 10)

| Lớp | Hành động | Kết quả |
| :--- | :--- | :--- |
| **L1 Targeted search** | Query: `"Data augmentation" AND "Vietnamese SMS spam"` trên Scholar + IEEE | **5 kết quả**, 0 phản chứng (không có bài báo nào sinh teencode/lỗi chính tả tiếng Việt). |
| **L2 Forward snowball** | Dùng `M002` *(Nguyen-Xuan et al., IEEE Access 2026)* làm anchor paper, kiểm tra các nghiên cứu trích dẫn | **0 GAP / 0 phản chứng** (các bài trích dẫn chỉ mở rộng mô hình đa ngôn ngữ trên social media, không làm Data Augmentation sinh teencode). |
| **L3 Survey anchor** | Đối chiếu bài SLR: *Tusher et al. (2024, IEEE Access)* | Bài tổng quan ghi nhận sự khan hiếm dữ liệu ở ngôn ngữ tài nguyên thấp và thủ thuật né tránh bằng tiếng lóng/sai chính tả, **không đề cập** cách tiếp cận sinh dữ liệu teencode cho tiếng Việt. |

→ **Kết luận:** **GAP 1 CONFIRMED** qua cả 3 lớp validation bổ sung.

---

## 3. Feasibility Check

| Tiêu chí | Mức | Ghi chú |
| :--- | :---: | :--- |
| **Dataset** | 🟢 | Có thể thu thập và kết hợp từ các nguồn công khai: NCSC, Cục An toàn thông tin, VNCERT, và bộ dữ liệu mạng xã hội công khai. Quy mô $\ge 500$ mẫu hoàn toàn khả thi trong 1 tuần. |
| **API / Tool** | 🟢 | Sử dụng Free Tier của Gemini 2.0 Flash / OpenAI API hỗ trợ sinh dữ liệu Few-shot (chi phí $\le \$5$ hoặc 0đ). |
| **Tính toán** | 🟢 | Huấn luyện và fine-tune PhoBERT-base có thể thực hiện hoàn toàn miễn phí trên GPU Google Colab T4 / Kaggle. |
| **Ground truth** | 🟢 | Gán nhãn 500-1000 mẫu theo format chuẩn (5-7 nhãn phân loại), ước tính $\le 5$ giờ cho cả nhóm thực hiện chéo. |
| **Code base** | 🟢 | Thư viện Transformers (HuggingFace), `nlpaug`, và mã nguồn EDA công khai có sẵn để tùy biến logic teencode. |
| **Kỹ năng** | 🟢 | Thành thạo Python, PyTorch, HuggingFace Transformers và xử lý văn bản NLP cơ bản. |
| **Thời gian** | 🟡 | Hoàn thành trong 1 tuần (Sprint cấp tốc). Tiến độ khá sát nút (tight), nhóm cần chia việc song song (vừa gom dữ liệu vừa viết sẵn script pipeline huấn luyện PhoBERT) để kịp nghiệm thu đúng hạn.|

**Kết quả:** 0 🔴, 1 🟡, 6 🟢, GAP 1 vẫn đạt mức An toàn, hoàn toàn khả thi để tiến hành.

**Kế hoạch xử lý (Downscope/Risk Mitigation):** Nếu việc thu thập dữ liệu thực tế gặp khó khăn về số lượng, sẽ giới hạn baseline ở 5 nhãn lừa đảo phổ biến nhất (Mạo danh ngân hàng, Việc làm online, Đe dọa tư pháp, Nhận thưởng, Vay tiền nhanh) và sử dụng EDA kết hợp dictionary teencode dựa trên tập luật (rule-based) trước khi mở rộng bằng LLM.

---

## 4. Phát biểu GAP chính thức

> *"Chưa có nghiên cứu nào xây dựng tập dữ liệu tin nhắn lừa đảo tiếng Việt đa lớp (>=500 mẫu) kết hợp kỹ thuật Tăng cường dữ liệu (Data Augmentation) sinh biến thể teencode và lỗi chính tả nhằm nâng cao độ bền vững của mô hình phân loại ngôn ngữ trước các thủ thuật né tránh bộ lọc."*

---

## 5. Đề xuất sơ bộ cho nhóm (chuẩn bị họp RBL-3)

*   **Dataset khả thi:** Xây dựng tập dữ liệu `Scam-VN-SMS` ($\ge 500$ mẫu) kết hợp từ các cảnh báo lừa đảo của Cục An toàn thông tin (NCSC), Chống Lừa Đảo (ChongLuaDaoV2) và nguồn tin nhắn phản ánh thực tế.
*   **Metric đề xuất:** Macro-F1, Precision, Recall cho từng lớp và Adversarial Robustness Score (độ sụt giảm F1 khi kiểm thử trên tập dữ liệu teencode biến thể).
*   **LLM/Tool đề xuất:** 
    *   *Data Augmentation:* Gemini-2.0-Flash / GPT-4o-mini (Few-shot Prompting) + Bộ luật biến đổi Teencode Rule-based.
    *   *Mô hình phân loại:* `PhoBERT-base` fine-tuned kết hợp kiến trúc CNN/BiLSTM.
*   **Baseline đề xuất:** So sánh trực tiếp với mô hình PhoBERT chuẩn không qua Data Augmentation và các mô hình học máy truyền thống (SVM + TF-IDF) từ bài báo M001.