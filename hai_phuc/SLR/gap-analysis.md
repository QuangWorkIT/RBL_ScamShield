# GAP Analysis — Đánh giá tin nhắn đơn lẻ vs Tiến trình hội thoại lừa đảo nhiều lượt

**Thành viên:** Hoàng Hải Phúc (hai_phuc)  
**GAP type:** GAP-T (Technological)  
**Ngày:** 2026-08-31  
**Evidence table nguồn:** `team-synthesis/evidence-table-merged.md`  
**N =:** 8 bài báo (`M006` - `M013`)

---

## 1. Mô tả GAP

Hiện tại, 100% các nghiên cứu trong danh sách khảo sát chỉ tập trung vào việc phân loại các tin nhắn đơn lẻ (single-turn message evaluation), hoàn toàn thiếu vắng các nghiên cứu về đánh giá ngữ cảnh của một cuộc hội thoại lừa đảo đa lượt (multi-turn conversational progression), nơi tội phạm mạng thực hiện các chiến thuật thao túng tâm lý leo thang qua nhiều tin nhắn.

**Bằng chứng từ evidence table:**
- **Cột Dataset:** Toàn bộ 8/8 bài báo (M006-M013) sử dụng các tập dữ liệu tin nhắn đơn lẻ truyền thống (ví dụ: Bangla-English financial scams, KISA SMS, SMS Spam Collection). Không có dataset nào là hội thoại đa lượt.
- **Cột Limitation:** Các bài báo thừa nhận mô hình không xử lý được các chiêu trò tinh vi mới hoặc thiếu context (ví dụ: M008, M010, M013).
- **Ví dụ:** 8/8 paper chỉ đọc 1 tin nhắn văn bản (hoặc 1 cặp image-text như M007) để ra quyết định, không paper nào lưu trữ và phân tích context của các tin nhắn trước đó.

---

## 2. Kiểm tra phản chứng

| Paper | Đã làm GAP này không? | Chi tiết |
|---|---|---|
| `M006` | Không | Chỉ đánh giá tin nhắn tài chính đơn lẻ bằng Transformer. |
| `M007` | Không | Mặc dù là đa phương thức (image-text), nhưng vẫn xử lý trên 1 tin nhắn/lượt duy nhất. |
| `M008` | Không | Phân loại tin nhắn SMS Kiswahili đơn lẻ bằng Swahili-BERT. |
| `M009` | Không | Phân loại tin nhắn SMS Swahili đơn lẻ. |
| `M010` | Không | Phân loại tin nhắn Smishing (SMS) đơn lẻ trên thiết bị. |
| `M011` | Không | Phân loại multiclass cho tin nhắn SMS Indonesia. |
| `M012` | Không | Sử dụng GPT-3 embedding cho bộ dữ liệu SMS Spam Collection 2011 (tin nhắn đơn lẻ). |
| `M013` | Không | Phân loại Spam.csv (tin nhắn đơn lẻ). |

**Kết luận:** GAP xác nhận ✅ (0 phản chứng)

### Supplementary Validation (Vì N = 8 < 10)

| Lớp | Hành động | Kết quả |
|---|---|---|
| L1 Targeted search | Query: `"multi-turn conversation" AND ("scam detection" OR "phishing detection")` — Scholar + IEEE — 2026-08-31 | 15 kết quả, 0 relevant / phản chứng (hầu hết nói về multi-turn chatbot chung chung, không áp dụng cho scam detection). |
| L2 Forward snowball | Cite [M006 (2026)] — 5 citing papers checked | 0 GAP / phản chứng: Các bài trích dẫn vẫn tập trung vào multilingual NLP single-turn. |
| L3 Survey anchor | [Saias 2025 - `M004`] SLR N=30 | Không đề cập: Đánh giá các đe dọa trên tin nhắn đơn lẻ, không đề cập đến multi-turn conversational analysis. |

→ Kết luận: **GAP CONFIRMED**

---

## 3. Feasibility Check

| Tiêu chí | Mức | Ghi chú |
|---|---|---|
| Dataset | 🟡 | Phải tự xây dựng quy trình thu thập. **Kế hoạch xử lý:** Thu thập Real/public data → LLM-based augmentation → synthetic data có kiểm soát → human validation → held-out real/public evaluation. Sẽ downscope GAP nếu không thu thập được *bất kỳ* real data nào. |
| API/Tool | ✅ | Dùng Gemini / GPT-4o-mini qua API (chi phí < $5 hoặc có free tier đủ dùng). |
| Tính toán | ✅ | Dạy inference qua Cloud API, không cần GPU mạnh để fine-tune. |
| Ground truth | 🟡 | Gán nhãn cho một luồng hội thoại mất thời gian hơn nhiều so với 1 tin nhắn lẻ (dự kiến ~10 giờ). |
| Code base | ✅ | Có thể sử dụng các framework quản lý context có sẵn (LangChain) để gửi multi-turn prompt. |
| Kỹ năng | ✅ | Yêu cầu kỹ năng API, Prompt Engineering và quản lý context state. |
| Thời gian | 🟡 | Việc thu thập và validate dataset phức tạp có thể gây trễ tiến độ, cần quản lý chặt chẽ. |

**Kết quả:** 3 🟡 → **Rủi ro cao**. 
**Kế hoạch xử lý (Downscope/Risk Mitigation):** Rủi ro cao nhất nằm ở Dataset. Tuyệt đối không dùng "500 conversations được ChatGPT tự sinh + tự label" làm toàn bộ bằng chứng. Bắt buộc phải có tập dữ liệu test là Real/Public data. Nếu thất bại trong việc kiếm data thật để test, bắt buộc phải downscope phạm vi của GAP thay vì ép toàn bộ thử nghiệm trên dữ liệu 100% synthetic.

---

## 4. Phát biểu GAP chính thức

"Không có nghiên cứu nào phát triển và đánh giá khả năng phát hiện lừa đảo dựa trên ngữ cảnh của một tiến trình hội thoại nhiều lượt (multi-turn conversational progression) — nơi các chiến thuật thao túng tâm lý xã hội được tội phạm mạng leo thang qua từng câu thoại, thay vì chỉ đánh giá một tin nhắn đơn lẻ (single-message evaluation)."

---

## 5. Đề xuất sơ bộ cho nhóm (chuẩn bị họp RBL-3)

**Dataset khả thi:** Bộ dữ liệu Hội thoại lừa đảo (Multi-turn Scam Conversation) tự xây dựng theo pipeline: Real/public data → LLM-based augmentation → controlled synthetic data → human validation → held-out real/public evaluation.

**Metric đề xuất:** Thread-level F1-score (Độ chính xác phân loại trên toàn bộ ngữ cảnh luồng hội thoại thay vì độ chính xác của từng câu đơn lẻ).

**LLM/Tool đề xuất:** Gemini-2.0-Flash (hoặc GPT-4o-mini) do có khả năng long-context reasoning và giá thành API hợp lý. Công nghệ này chưa được khảo sát trong 8 bài báo lõi (phần lớn dùng BERT/PhoBERT).

**Baseline đề xuất:** So sánh với mô hình PhoBERT-base (hoặc SVM) truyền thống chỉ đánh giá dựa trên tin nhắn đơn lẻ (single-message evaluation).
