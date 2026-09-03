# GAP Analysis — Điểm mù đa phương thức (Quishing mã QR & Ảnh chụp màn hình mạo danh)

**Thành viên:** Phan Trần Hoàng Trân (`hoang_tran`)  
**GAP type:** GAP-T (Technological)  
**Ngày:** 2026-09-01  
**Evidence table nguồn:** `team-synthesis/evidence-table-merged.md`  
**N =:** 6 bài báo (`M014`, `M017`, `M018`, `M019`, `M021`, `M025`)

---

## 1. Mô tả GAP

Hiện tại, hơn 85% các nghiên cứu trong tập khảo sát chỉ tập trung xử lý tin nhắn lừa đảo dạng văn bản thuần túy (text-only SMS/Email), tạo ra một "điểm mù đa phương thức" (multimodal threat blindness) trước xu hướng tội phạm mạng chuyển sang gửi ảnh chụp màn hình thông báo giả mạo (biên lai chuyển tiền, lệnh bắt, ứng dụng VNeID giả) và mã QR độc hại (Quishing) trên các nền tảng tin nhắn như Zalo, Messenger, Telegram.

**Bằng chứng từ evidence table:**
- **Cột Tool/LLM:** 5/6 bài báo lõi (`M017`, `M018`, `M019`, `M021`, `M025`) sử dụng các mô hình xử lý văn bản thuần túy (PhoBERT, MobileBERT, Phishing-GAT, SVM + TF-IDF) hoàn toàn không có khả năng đọc ảnh hoặc giải mã QR code.
- **Cột Dataset:** Các tập dữ liệu trong khảo sát (`N=3,500` đến `N=5,574`) chỉ chứa nội dung văn bản (SMS lures, email entity graphs, forensics logs). Duy nhất `M014` sử dụng dữ liệu QR (N=4,200), nhưng chỉ tập trung vào Quishing dạng link di động mà bỏ qua các ảnh chụp màn hình tin nhắn lừa đảo tiếng Việt.
- **Cột Limitation:** Các nghiên cứu ghi nhận hạn chế lớn khi mở rộng sang dữ liệu đa phương thức. Ví dụ `M014` thừa nhận mô hình di động đa phương thức đòi hỏi bộ nhớ RAM di động rất lớn để trích xuất đặc trưng song song (dual vision-text feature extraction); trong khi `M042` ghi nhận trực tiếp *"mô hình hiện tại chỉ xử lý văn bản thuần và thiếu khả năng đa phương thức để xử lý tin nhắn lừa đảo chứa hình ảnh"*.

---

## 2. Kiểm tra phản chứng

| Paper | Đã làm GAP này không? | Chi tiết |
|---|---|---|
| `M014` | Có (một phần) | Đánh giá Quishing trên di động dùng Llama-3.2-3B, nhưng tập trung vào QR code thuần túy trên thiết bị, chưa có module OCR bóc tách văn bản tiếng Việt từ ảnh chụp màn hình Zalo/Messenger và yêu cầu phần cứng RAM di động cao. |
| `M017` | Không | Chỉ đánh giá các đòn tấn công Prompt Injection văn bản ngắn đơn lượt bằng PhoBERT và GPT-4o-mini. |
| `M018` | Không | Phân loại SMS Spam dạng văn bản bằng MobileBERT nén trên thiết bị Edge. |
| `M019` | Không | Sử dụng Phishing-GAT kết hợp PhoBERT embedding trên đồ thị ngữ nghĩa văn bản. |
| `M021` | Không | Hệ thống đa tầng PhoBERT + DistilBERT + Rule Engine chỉ phân loại log và văn bản real-time. |
| `M025` | Không | Phân loại tin nhắn SMS bằng SVM + TF-IDF truyền thống. |

**Kết luận:** GAP xác nhận ✅ (Có 1 bài `M014` làm QR phishing nhưng dừng lại ở QR lure + text lure di động, chưa giải quyết được OCR bóc tách ảnh chụp màn hình lừa đảo Tiếng Việt / thông báo mạo danh).

### Supplementary Validation (Vì N = 6 < 10)

| Lớp | Hành động | Kết quả |
|---|---|---|
| **L1 Targeted search** | Query: `"quishing detection" AND ("screenshot OCR" OR "vietnamese scam")` — Scholar + IEEE — 2026-09-01 | 18 kết quả, 0 relevant / phản chứng. Hầu hết bài báo về Quishing tập trung bóc tách URL từ file PDF/Email hoặc mã QR chuẩn, chưa bài báo nào xây dựng pipeline OCR tiếng Việt kết hợp giải mã QR thời gian thực cho tin nhắn lừa đảo trên mobile. |
| **L2 Forward snowball** | Cite [`M014` (2026)] — 6 citing papers checked | 0 GAP / phản chứng: Các bài trích dẫn tiếp tục tập trung vào việc tối ưu hóa dung lượng SLM trên thiết bị IoT/Edge, không mở rộng sang xử lý ảnh chụp màn hình giao diện chat tiếng Việt. |
| **L3 Survey anchor** | [`M004` (Saias 2025)] SLR N=30 | Không đề cập: Khảo sát 30 công trình NLP threat detection chỉ ra rằng 80%+ nghiên cứu dùng ML/NLP truyền thống trên text, hoàn toàn chưa có khảo sát về xử lý đa phương thức OCR + QR Quishing trên ứng dụng OTT. |

→ Kết luận: **GAP CONFIRMED**

---

## 3. Feasibility Check

| Tiêu chí | Mức | Ghi chú |
|---|---|---|
| Dataset | ✅ | Có thể thu thập 300+ ảnh chụp màn hình lừa đảo thực tế (Zalo/Messenger/SMS) từ NCSC, báo chí và cộng đồng; kết hợp dataset mã QR public từ `M014`. |
| API/Tool | ✅ | Tesseract OCR / PaddleOCR mã nguồn mở (miễn phí 100%), PyZbar giải mã QR, kết hợp Gemini-2.0-Flash / GPT-4o-mini API để phân tích multimodal. |
| Tính toán | ✅ | Công đoạn bóc tách OCR và QR decode chạy cực nhẹ trên CPU laptop/server, không đòi hỏi GPU đắt tiền để fine-tune vision model nặng. |
| Ground truth | ✅ | Gán nhãn cho tập ảnh chụp màn hình (Lừa đảo / Lành tính) và QR code (Độc hại / An toàn) trực quan, nhóm thực hiện nhanh chóng trong < 5 giờ. |
| Code base | ✅ | Các thư viện Python xử lý ảnh (`opencv-python`, `pytesseract`, `pyzbar`) sẵn có và vô cùng dễ tích hợp thành pipeline. |
| Kỹ năng | ✅ | Yêu cầu kỹ năng xử lý ảnh cơ bản, tích hợp thư viện OCR và gọi API LLM Multimodal context. |
| Thời gian | ✅ | Xây dựng và nghiệm thu pipeline bóc tách OCR + QR decoding hoàn thành dễ dàng trong 1–2 tuần còn lại. |

**Kết quả:** 7 ✅ / 0 🟡 / 0 ❌ → **An toàn, tiến hành**.

---

## 4. Phát biểu GAP chính thức

"Hầu hết các nghiên cứu hiện tại (hơn 85%) chỉ tập trung xử lý tin nhắn lừa đảo dạng văn bản thuần túy (text-only), tạo ra 'điểm mù đa phương thức' (multimodal threat blindness) trước các hình thức lừa đảo qua ảnh chụp màn hình (biên lai chuyển tiền giả, lệnh bắt giả, thông báo mạo danh) và mã QR độc hại (Quishing) trên các nền tảng tin nhắn phổ biến tại Việt Nam."

---

## 5. Đề xuất sơ bộ cho nhóm (chuẩn bị họp RBL-3)

> Phần này **không cần chi tiết** – chỉ để chuẩn bị ý kiến cho buổi họp chọn GAP chính. Quyết định:

**Dataset khả thi:** Bộ dữ liệu Đa phương thức ScamShield (Text + Screenshot + QR Code) kết hợp từ tập QR phishing public (`M014`) và 300+ ảnh chụp màn hình tin nhắn/biên lai lừa đảo Tiếng Việt thực tế thu thập từ NCSC & cộng đồng.

**Metric đề xuất:** Multimodal F1-score (đánh giá tổng thể), OCR Character/Word Error Rate (CER/WER), QR Decoding Rate (tỷ lệ giải mã QR thành công) và Processing Latency (ms).

**LLM/Tool đề xuất:** PaddleOCR / Tesseract OCR (bóc tách chữ tiếng Việt từ ảnh) + PyZbar (trích xuất URL từ mã QR) + Gemini-2.0-Flash / GPT-4o-mini (phân tích ngữ cảnh đa phương thức). Các công cụ này giải quyết hạn chế thiếu OCR trong 5/6 bài báo lõi.

**Baseline đề xuất:** So sánh hiệu năng phát hiện lừa đảo giữa hệ thống Đa phương thức (ScamShield) với các mô hình NLP chỉ đọc văn bản thuần túy (PhoBERT-base / SVM từ `M017`, `M025`) khi đối mặt với dữ liệu đầu vào chứa ảnh chụp và mã QR.
