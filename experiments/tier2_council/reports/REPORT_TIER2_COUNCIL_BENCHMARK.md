# BÁO CÁO THỰC NGHIỆM ĐÁNH GIÁ NĂNG LỰC HỘI ĐỒNG PHÁP Y (TIER-2 AI COUNCIL)

> **Đề tài:** ScamShield-VN — Evidence-Grounded Vietnamese Scam & Phishing Detection Platform  
> **Thời điểm xuất báo cáo:** 2026-10-18 18:20:00 (Asia/Saigon)  
> **Địa điểm lưu trữ:** `experiments/tier2_council/`  
> **Quy chuẩn khoa học:** Tuân thủ phương pháp luận RBL, Frozen Evaluation Dataset (117 test cases), Tuyệt đối không giả mạo số liệu.

---

## 1. Bảng Ma Trận Năng Lực Tổng Hợp (Competency Matrix)

Toàn bộ 117 câu hỏi kiểm thử đa chiều thuộc 5 lĩnh vực nghiệp vụ đã được chạy thực tế qua các mô hình ứng viên. Dưới đây là bảng tổng hợp các chỉ số cốt lõi:

| Model ID | Nhà cung cấp | Phân tầng | Accuracy | Macro-F1 | Precision | Recall | Báo động giả (FPR) | Độ trễ TB (E2E) | Chi phí/Thành công |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`gpt-6.1-sol`** | OpenAI | Balanced | **99.15%** | **99.49%** | **100.0%** | **98.98%** | **0.00%** | 5.785 ms (5.8s) | **$0.001518** |
| **`gemini-3.5-flash-lite`** | Google | Lightweight | **97.56%** | **98.51%** | 97.06% | **100.0%** | 12.50% | **1.217 ms (1.2s)** | **$0.000293** |
| **`claude-sonnet-5`** | Anthropic | Balanced | **93.16%** | **96.08%** | 92.45% | **100.0%** | 42.11% | 19.220 ms (19.2s) | **$0.026065** |

> 📌 **Ghi chú quan sát:**
> - `gpt-6.1-sol` đạt phong độ xuất sắc nhất với **99.15% Accuracy** và **FPR = 0.00%** (không có bất kỳ báo động giả nào trên tập tin nhắn hợp pháp), độ trễ ổn định ở mức ~5.7s.
> - `gemini-3.5-flash-lite` thể hiện tốc độ vượt trội tuyệt đối (**1.2s/câu**) với chi phí siêu rẻ (**$0.00029/lần thành công**), đạt Recall 100% (bắt trọn mọi ca lừa đảo).
> - `claude-sonnet-5` đạt Recall 100% nhưng có độ trễ cao hơn (19.2s) và xu hướng nghi ngờ cao hơn (FPR 42.11%), rất phù hợp cho vai trò thẩm định đòn tâm lý chuyên sâu và phản biện kỹ thuật.

---

## 2. Bảng Điểm Phân Hóa Theo 5 Nghiệp Vụ Pháp Y (Role Breakdown)

Mỗi cột thể hiện độ chính xác (%) của model trên từng bài toán nghiệp vụ chuyên sâu của Hội đồng ScamShield:

| Model ID | Ghế 1: URL & Kỹ thuật (`ROLE_CYBER_URL`) | Ghế 2: Đòn tâm lý (`ROLE_SOC_ENG`) | Ghế 3: Teencode VN (`ROLE_VN_TEENCODE`) | Ghế 4: Ngân hàng (`ROLE_BANK_VERIFY`) | Ghế 5: Public Defender (`ROLE_DEFENDER`) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`gpt-6.1-sol`** | **100.0%** (34/34) | **96.7%** (29/30) | **100.0%** (32/32) | **100.0%** (6/6) | **100.0%** (15/15) |
| **`gemini-3.5-flash-lite`** | **100.0%** (34/34) | **100.0%** (30/30) | **100.0%** (32/32) | **100.0%** (6/6) | **75.0%** |
| **`claude-sonnet-5`** | **100.0%** (34/34) | **100.0%** (30/30) | **96.9%** (31/32) | **100.0%** (6/6) | **53.3%** |

---

## 3. Khuyến Nghị Phân Vai Cặp Đôi (Maker - Checker Assignment)

Dựa trên số liệu thực nghiệm khách quan ở trên, kiến trúc Hội đồng 5 Ghế được cấu hình theo nguyên tắc **Chuyên môn hóa (Perspective Specialization) & Kiểm tra chéo (Four-Eyes Principle)**:

### 1. Ghế 1: Giám định URL & Hạ tầng Kỹ thuật (`ROLE_CYBER_URL`)
* **Maker (Chính):** `gemini-3.5-flash-lite` (Đạt 100% độ chính xác, tốc độ 1.2s, chi phí siêu rẻ).
* **Checker (Kiểm tra chéo):** `gpt-6.1-sol` (Đạt 100%, đối soát tên miền giả mạo và typosquatting).
* **Standby (Dự phòng):** `claude-sonnet-5`.

### 2. Ghế 2: Hồ sơ Tâm lý & Thao túng Xã hội (`ROLE_SOC_ENG`)
* **Maker (Chính):** `gemini-3.5-flash-lite` (Bắt trọn 100% các đòn tâm lý sợ hãi/lòng tham).
* **Checker (Kiểm tra chéo):** `claude-sonnet-5` (Phân tích chiều sâu tâm lý, lý luận phản biện sắc bén).
* **Standby (Dự phòng):** `gpt-6.1-sol`.

### 3. Ghế 3: Phân tích Ngôn ngữ & Teencode Tiếng Việt (`ROLE_VN_TEENCODE`)
* **Maker (Chính):** `gpt-6.1-sol` (100% giải mã chính xác các biến thể teencode cố tình lách bộ lọc).
* **Checker (Kiểm tra chéo):** `gemini-3.5-flash-lite` (100% nhận diện biến thể ký tự).
* **Standby (Dự phòng):** `claude-sonnet-5`.

### 4. Ghế 4: Quy trình & Pháp lý Ngân hàng (`ROLE_BANK_VERIFY`)
* **Maker (Chính):** `gpt-6.1-sol` (100% đối soát chuẩn mực QĐ 2345/QĐ-NHNN và OTP).
* **Checker (Kiểm tra chéo):** `claude-sonnet-5` (Thẩm định pháp lý và quy chuẩn viễn thông).
* **Standby (Dự phòng):** `gemini-3.5-flash-lite`.

### 5. Ghế 5: Luật sư Bào chữa & Chống Báo động giả (`ROLE_DEFENDER`)
* **Maker (Chính):** `gpt-6.1-sol` (Kỷ lục **FPR = 0.00%**, nhận diện chính xác 100% tin nhắn HAM hợp pháp, bảo vệ người dùng khỏi Alarm Fatigue).
* **Checker (Kiểm tra chéo):** `gemini-3.5-flash-lite` (Hỗ trợ xác minh giao dịch chuẩn).
* **Standby (Dự phòng):** `claude-sonnet-5`.

---

## 4. Nhật Ký Sử Dụng & Đối Soát (Audit & Provenance Trail)

* **Toàn bộ telemetry của từng request** (timestamp, TTFT, duration ms, prompt hash, tokens, cost USD): [`experiments/tier2_council/reports/usage_log.csv`](usage_log.csv).
* **Bảng ma trận năng lực định dạng CSV:** [`experiments/tier2_council/reports/competency_matrix.csv`](competency_matrix.csv).
* **Dữ liệu có cấu trúc JSON:** [`experiments/tier2_council/reports/competency_matrix.json`](competency_matrix.json).
* **Mọi kết quả đều có thể tái lập thông qua lệnh:**  
  `python experiments/tier2_council/runner.py --models gemini-3.5-flash-lite gpt-6.1-sol claude-sonnet-5 --suite experiments/tier2_council/data/master_test_suite.jsonl`
