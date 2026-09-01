# GAP Analysis — Lỗ Hổng Dữ Liệu và Năng Lực Phòng Thủ Đối Kháng Của Các Mô Hình Ngôn Ngữ Trước SMS Lừa Đảo Tiếng Việt

**Thành viên:** Nguyễn Quốc Huy
**GAP type:** GAP-M
**Ngày:** 2026-09-01
**Evidence table nguồn:** `team-synthesis/evidence-table-merged.md`
**N =** 10 bài báo core (`M029`, `M030`, `M031`, `M032`, `M033`, `M034`, `M035`, `M036`, `M037`, `M038`)

---

## 1. Mô tả GAP

Hiện nay, chưa có nghiên cứu nào xây dựng một bộ dữ liệu chuẩn hóa về tin nhắn lừa đảo tiếng Việt được tích hợp kỹ thuật tăng cường dữ liệu (Data Augmentation) nhằm chủ động mô phỏng các biến thể teencode, tiếng lóng và cố ý sai lỗi chính tả/mất dấu để huấn luyện mô hình chống vượt rào.

**Bằng chứng từ evidence table:**
- Cột Dataset / Hạn chế: Toàn bộ 10/10 bài báo core đều tập trung vào dữ liệu tiếng Anh (như SMS Spam Collection, Enron) hoặc tiếng Trung (`M029`, `M036`), hoàn toàn không có bộ dữ liệu nào hỗ trợ tiếng Việt. Đồng thời, bài `M033` chỉ ra hạn chế khi đối mặt với từ địa phương (Pidgin English) nhưng chưa có phương pháp giải quyết triệt để.
- Cột Tool/LLM / Hạn chế: Các nghiên cứu sử dụng LLM để sinh dữ liệu đối kháng (như PEEK - `M035`, Genshin - `M036`) phát hiện ra pattern rằng mô hình dễ bị đánh lừa bởi các thay đổi ký tự hoặc từ đồng nghĩa. Tuy nhiên, chưa có công trình nào áp dụng pattern này để xử lý đặc thù ngôn ngữ phi chuẩn của Việt Nam (mất dấu, teencode).
- Cột Tool/LLM / Dataset: Mặc dù các nghiên cứu (`M030`, `M032`) đã ứng dụng LLM (GPT-4, Gemini) để sinh dữ liệu tổng hợp (synthetic data), việc sinh dữ liệu chỉ thực hiện trên văn bản chuẩn mực, không mô phỏng các biến thể đánh lừa thực tế của spammer.

---

## 2. Kiểm tra phản chứng

| Paper | Đã làm GAP này không? | Chi tiết |
|---|---|---|
| `M029` (FraudSMSWalker) | Không | Benchmarking lừa đảo đa kênh SMS-to-Webpage, sử dụng tiếng Anh và tiếng Trung. Không giải quyết tiếng Việt hay teencode. |
| `M030`, `M032` | Không | Dùng LLM (Claude, GPT-4, Gemini) để sinh dữ liệu tổng hợp huấn luyện mô hình SLM/DeBERTa, nhưng chỉ tập trung vào tiếng Anh chuẩn. |
| `M031`, `M033`, `M038` | Không | Đánh giá các mô hình ML truyền thống và Transformer trên dữ liệu tĩnh mất cân bằng. Có ghi nhận khó khăn với phương ngữ nhưng không dùng Data Augmentation. |
| `M034`, `M037` | Không | Tập trung vào Explainable AI (LIME, SHAP, LITA) để giải thích mô hình (RoBERTa, DistilBERT). Hoàn toàn không liên quan đến sinh dữ liệu teencode. |
| `M035` (PEEK), `M036` (Genshin) | Có (một phần) | Sinh mẫu đối kháng bằng LLM/GAN (thay đổi ký tự, từ vựng) để vượt mặt bộ phân loại. Tuy nhiên, chỉ áp dụng cho tiếng Anh/Trung, chưa có quy tắc xử lý mất dấu hay teencode tiếng Việt. |

**Kết luận:** GAP xác nhận ✅ Các nghiên cứu hiện tại đã chứng minh hiệu quả của việc sinh dữ liệu đối kháng bằng LLM để tăng tính bền vững, nhưng chưa có công trình nào áp dụng Data Augmentation cho tiếng Việt với các đặc thù như teencode và mất dấu.

---

## 3. Đánh giá khả thi (Feasibility)

| Tiêu chí | Mức | Ghi chú |
|---|---|---|
| Dataset | ✅ | Có thể thu thập SMS lừa đảo từ ChongLuaDao, NCSC và phản ánh thực tế (>= 500 mẫu) trong < 1 tuần. |
| API/Tool | ✅ | Dùng Free Tier Gemini 1.5 Flash / GPT-4o-mini kết hợp tập luật (rule-based) để sinh teencode. |
| Tính toán | ✅ | Dùng Kaggle/Colab free (GPU T4/P100) đủ để fine-tune PhoBERT. |
| Ground truth | ✅ | Gán nhãn thủ công hoặc dùng automated proxy (<= 5 giờ cho cả nhóm). |
| Code base | ✅ | Có thư viện Transformers (HuggingFace) và các rule thay thế ký tự tiếng Việt có thể dễ dàng code từ đầu. |
| Kỹ năng | ✅ | Nhóm có thể implement data augmentation pipeline và train model NLP cơ bản. |
| Thời gian | ⚠️ | Xong nhưng tight. Cần chia việc song song (gom dữ liệu + viết script). |

**Kết quả:** 0 ❌ / 1 ⚠️ -> An toàn, tiến hành

---

## 4. Phát biểu GAP chính thức

Chưa có nghiên cứu nào xây dựng tập dữ liệu tin nhắn lừa đảo tiếng Việt đa lớp kết hợp kỹ thuật tăng cường dữ liệu chủ động sinh các biến thể teencode và mất dấu, nhằm nâng cao độ bền vững (adversarial robustness) của mô hình ngôn ngữ (như PhoBERT) trước các thủ thuật né tránh bộ lọc.

---

## 5. Đề xuất sơ bộ cho nhóm (chuẩn bị họp RBL-3)

**Dataset khả thi:** Tự xây dựng `Scam-VN-SMS` từ NCSC/ChongLuaDao và áp dụng Data Augmentation để tạo thêm phiên bản chứa teencode/mất dấu.
**Metric đề xuất:** Macro-F1, Precision, Recall và Adversarial Robustness Score (đánh giá mức độ sụt giảm F1 khi test trên tập teencode).
**LLM/Tool đề xuất:** PhoBERT-base (cho phân loại) + LLM Prompting (Gemini/GPT-4o-mini) kết hợp Rule-based script để tạo các augmentation teencode.
**Baseline đề xuất:** So sánh PhoBERT (được train trên tập có augmentation) với PhoBERT chuẩn (chỉ train trên text sạch) và các mô hình ML truyền thống (SVM + TF-IDF) từ bài `M031`/`M033` khi test trên tập teencode.
