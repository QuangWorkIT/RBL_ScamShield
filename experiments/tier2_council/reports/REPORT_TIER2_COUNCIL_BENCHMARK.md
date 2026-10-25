# BÁO CÁO THỰC NGHIỆM ĐÁNH GIÁ NĂNG LỰC HỘI ĐỒNG PHÁP Y (TIER-2 AI COUNCIL)

> **Đề tài:** ScamShield-VN — Evidence-Grounded Vietnamese Scam & Phishing Detection Platform  
> **Thời điểm xuất báo cáo:** 2026-10-18 18:40:16 (Asia/Saigon)  
> **Địa điểm lưu trữ:** `experiments/tier2_council/`  
> **Quy chuẩn khoa học:** Tuân thủ phương pháp luận RBL, Frozen Evaluation Dataset, Tuyệt đối không giả mạo số liệu.

---

## 1. Bảng Ma Trận Năng Lực Tổng Hợp (Competency Matrix)

| Model ID | Accuracy | Macro-F1 | Precision | Recall | Báo động giả (FPR) | Độ trễ (E2E) | Tổng Chi Phí | Chi phí/Thành công |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `claude-sonnet-5` | **93.16%** | **96.08%** | 92.45% | 100.0% | 42.11% | 19220.9ms | $2.8411 | $0.026065 |
| `gemini-3.5-flash-lite` | **94.87%** | **97.0%** | 95.1% | 98.98% | 26.32% | 2001.7ms | $0.0334 | $0.000301 |
| `gemini-3.8-flash` | **100.0%** | **100.0%** | 100.0% | 100.0% | 0.0% | 18904.4ms | $0.0006 | $0.000550 |
| `gpt-6.1-sol` | **99.15%** | **99.49%** | 100.0% | 98.98% | 0.0% | 5785.2ms | $0.1761 | $0.001518 |

---

## 2. Bảng Điểm Phân Hóa Theo 5 Nghiệp Vụ Pháp Y (Role Breakdown)

Mỗi cột thể hiện độ chính xác (%) của model trên từng bài toán nghiệp vụ cụ thể của Hội đồng ScamShield:

| Model ID | Ghế 1: URL & Kỹ thuật | Ghế 2: Đòn tâm lý | Ghế 3: Teencode VN | Ghế 4: Ngân hàng | Ghế 5: Public Defender (HAM) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `claude-sonnet-5` | 100.0% | 100.0% | 96.9% | 100.0% | 53.3% |
| `gemini-3.5-flash-lite` | 100.0% | 96.7% | 100.0% | 100.0% | 66.7% |
| `gemini-3.8-flash` | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `gpt-6.1-sol` | 100.0% | 96.7% | 100.0% | 100.0% | 100.0% |

---

## 3. Khuyến Nghị Phân Vai Cặp Đôi (Maker - Checker Assignment)

Dựa trên số liệu thực nghiệm khách quan ở trên, kiến trúc Hội đồng 5 Ghế được cấu hình tối ưu như sau:

1. **Ghế 1 (Giám định URL & Hạ tầng):**
   - **Maker:** Model có điểm F1 cao nhất ở `ROLE_CYBER_URL`.
   - **Checker / Standby:** Model xếp thứ 2 có tốc độ phản hồi nhanh.
2. **Ghế 2 (Hồ sơ Tâm lý & Thao túng Xã hội):**
   - **Primary:** Model bóc tách sắc thái đe dọa / giục giã chính xác nhất.
3. **Ghế 3 (Phân tích Ngôn ngữ & Teencode):**
   - **Primary:** Model giải mã biến thể teencode và từ lóng tiếng Việt tốt nhất.
4. **Ghế 4 (Pháp lý & Quy trình Ngân hàng):**
   - **Primary:** Model đối soát chuẩn xác các quy định QĐ 2345/QĐ-NHNN và OTP.
5. **Ghế 5 (Public Defender / Chống Báo động giả):**
   - **Primary:** Model có **Tỷ lệ Báo động giả (FPR) thấp nhất** và độ chính xác cao nhất ở nhóm tin nhắn hợp pháp (`ROLE_DEFENDER`).

---

## 4. Nhật Ký Sử Dụng & Đối Soát (Audit & Provenance Trail)

- Toàn bộ lượt gọi API và số liệu vi mô đã được lưu trữ vĩnh viễn tại: [`reports/usage_log.csv`](file:///C:\Users\USER\RBL_ScamShield\experiments\tier2_council\reports\competency_matrix.csv)
- Mọi kết quả đều có thể tái lập thông qua script `runner.py --suite data/master_test_suite.jsonl`.
