# RBL_SPECS.md — Đặc Tả Kiến Trúc & Hợp Đồng Dữ Liệu (Kế Thừa RBL ScamShield-VN)

> **Tài liệu tham chiếu:** Kế thừa từ chuẩn nghiên cứu khoa học [`RBL_FRAMEWORK.md`](file:///c:/Users/USER/RBL_ScamShield/RBL_FRAMEWORK.md) (v3.0).  
> **Mục đích:** Đặc tả kiến trúc kỹ thuật triển khai 2 tầng (Two-Tier Cascaded Architecture) và hợp đồng giao tiếp API (API Data Contracts) giữa Core AI Engine và các phân hệ Web/App Frontend & Backend.

---

## 1. Kiến Trúc Phát Hiện Lừa Đảo 2 Tầng (Two-Tier Cascaded Pipeline)

Hệ thống vận hành theo cơ chế phân luồng tầng bậc (Cascade) nhằm giải quyết triệt để bài toán đánh đổi Độ chính xác – Độ trễ – Chi phí (Accuracy–Latency–Cost Trilemma):

```
                             [ Người Dùng Gửi Mẫu Kiểm Tra (SMS/Chat/URL) ]
                                                   │
                                                   ▼
                               ┌───────────────────────────────────────┐
                               │   TIER 1: On-Device / Edge Screener   │
                               │   ViSoBERT-v2 Fine-Tuned (INT8 ONNX)  │
                               │   Độ trễ < 15.8ms, Chi phí: $0.00     │
                               │   Hiệu chỉnh nhiệt độ: T* = 1.0       │
                               └───────────────────┬───────────────────┘
                                                   │
                                  Độ tự tin P >= 0.90 (Ngưỡng an toàn τ)?
                                           ┌───────┴───────┐
                     CÓ (Chiếm ~85% lưu lượng)     │       │ KHÔNG (Vùng phân vân 0.10 <= P < 0.90)
                                                   ▼       ▼
                               ┌────────────────────────┐  ┌──────────────────────────────────────────┐
                               │ PHẢN HỒI TRỰC TIẾP     │  │ TIER 2: Cloud Multi-LLM Forensic Council │
                               │ TẠI THIẾT BỊ / EDGE    │  │ (Hội Đồng Pháp Y 3 Chuyên Gia AI)        │
                               │ (SCAM-RISK / LOW-RISK) │  │ Maker: gpt-6.1-sol                       │
                               └────────────────────────┘  │ Checker: gemini-3.5-flash-lite/3.8-flash │
                                                           └────────────────────┬─────────────────────┘
                                                                                │
                                                                                ▼
                                                           ┌──────────────────────────────────────────┐
                                                           │ Trọng Tài Borda & Phản Biện Defender     │
                                                           │ • Veto Boost: -0.25 (Chống Alarm Fatigue)│
                                                           │ • Cơ chế Early-Exit Fast-Path            │
                                                           │ • Chuẩn hóa 3 nhãn theo NĐ 13/2023       │
                                                           └──────────────────────────────────────────┘
```

---

## 2. Chi Tiết Các Tầng Xử Lý (Tier Specification)

### 2.1. Tier 1: Local Edge Screener (ViSoBERT-v2 Fast-Path)
* **Backbone:** Fine-tuned `ViSoBERT` trên ngữ liệu mạng xã hội Việt Nam (`visobert_5runs_release`).
* **Kỹ thuật tối ưu:**
  - Lượng tử hóa INT8 ONNX Runtime chạy trên CPU/thiết bị đầu cuối.
  - Hàm mất mát Cost-Sensitive Weighted BCE ($\mathcal{L}_{\text{WBCE}}$, $\alpha = 5.0$), phạt nặng gấp 5 lần lỗi bỏ sót lừa đảo (False Negative).
  - Post-hoc Temperature Scaling ($T^* = 1.0$) loại bỏ hiện tượng tự tin thái quá của Transformer.
* **Hiệu năng thực nghiệm:** Độ trễ trung bình **$15.8\text{ ms}$**, chi phí **$\$0.00$**, Scam Recall **$95.62\% \pm 2.25\%$**.
* **Ngưỡng định tuyến ($\tau = 0.90$):**
  - $P(\text{Scam}) \ge 0.90 \implies$ Kết luận ngay `SCAM-RISK` (Fast-Path).
  - $P(\text{Scam}) \le 0.10 \implies$ Kết luận ngay `LOW-RISK` (Fast-Path).
  - $0.10 < P(\text{Scam}) < 0.90 \implies$ Leo thang lên Tier 2 (~$15\%$ lưu lượng tin nhắn phức tạp).

---

### 2.2. Tier 2: Consolidated 3-Agent Forensic Council (Cloud Panel)
Dựa trên kết quả thực nghiệm Ablation và kiểm định McNemar ($\chi^2 = 3.2000, p = 0.0736 \ge 0.05$), hội đồng được tinh giản thành **3 ghế chuyên môn hóa theo nguyên lý Occam's Razor**, tiết kiệm $29.8\%$ số cuộc gọi API và $40\%$ chi phí token so với cấu hình 5 tác tử cũ:

| Ghế Chuyên Môn | Trách Nhiệm Giám Định Pháp Y | Mô Hình Chuẩn Hóa | Trọng Số |
| :--- | :--- | :--- | :---: |
| **Seat 1: `cyber_financial_analyst`**<br>*(An ninh Mạng & Tài chính)* | Bóc tách tên miền giả mạo (homoglyph/typosquatting), link rút gọn, mã độc APK ngoài kho ứng dụng; đối chiếu quy chuẩn ngân hàng và Quyết định 2345/QĐ-NHNN (sinh trắc học). | **Maker:** `gpt-6.1-sol`<br>**Checker:** `gemini-3.5-flash-lite` | **1.3** |
| **Seat 2: `psycholinguistic_slang_profiler`**<br>*(Tâm lý Học & Ngôn ngữ Biến thể)* | Nhận diện đòn bẩy tâm lý (tạo áp lực thời gian "trong 24h", đe dọa tố tụng công an/VKS, bẫy trúng thưởng/CTV); giải mã teencode, tiếng lóng, ký tự số thay thế (`t4i kh04n`, `n9an h4n9`). | **Maker:** `gpt-6.1-sol`<br>**Checker:** `gemini-3.5-flash-lite` | **1.2** |
| **Seat 3: `public_defender_advocate`**<br>*(Luật sư Bào chữa Công cộng)* | **Sứ mệnh chống báo động giả (Anti-Alarm Fatigue):** Tìm mọi căn cứ chứng minh tin nhắn là giao dịch hợp pháp (OTP chuẩn, thông báo tiền điện nước định kỳ). Kích hoạt cơ chế **Veto Boost ($-0.25$)** để bảo vệ 100% tin nhắn an toàn ($0.00\%$ FPR). | **Maker:** `gpt-6.1-sol`<br>**Checker:** `gemini-3.8-flash` | **1.3** |

---

### 2.3. Chuẩn Hóa 3 Nhãn Phán Quyết (Điều 25 Nghị Định 13/2023/NĐ-CP)
Hệ thống tuân thủ nguyên tắc an toàn dữ liệu cá nhân, loại bỏ việc ép buộc nhị phân:
1. **`SCAM-RISK`** ($P \ge 0.60$): Phát hiện chứng cứ lừa đảo rõ ràng. Mức độ rủi ro: `HIGH` hoặc `CRITICAL` (khi $P \ge 0.85$).
2. **`LOW-RISK`** ($P < 0.40$): Tin nhắn an toàn / giao dịch thường nhật. Mức độ rủi ro: `LOW`.
3. **`UNKNOWN`** ($0.40 \le P < 0.60$ hoặc mâu thuẫn biểu quyết $|\text{Scam} - \text{Ham}| \le 1$): Vùng ranh giới mơ hồ. Không gán nhãn tùy tiện, trả về khuyến nghị xác minh thủ công hoặc chuyển kiểm toán viên con người (Human-in-the-loop).

---

## 3. Chuẩn Hợp Đồng API (API Contracts for Backend & Frontend)

### 3.1. API Kiểm Tra An Toàn Tin Nhắn / URL
* **Endpoint:** `POST /api/v1/scan`
* **Headers:** `Authorization: Bearer <jwt_token>` (tùy chọn đối với khách vãng lai)

**Request Body:**
```json
{
  "content": "Vietcombank tran trong thong bao: Tai khoan quy khach bi khoa do chua cap nhat sinh trac hoc theo QĐ 2345. Vui long truy cap https://vcb-digibank-login.com de xac thuc ngay.",
  "sender": "0981234567",
  "check_type": "TEXT",
  "metadata": {
    "channel": "SMS",
    "received_at": "2026-10-21T08:30:00Z"
  }
}
```

**Response Body (200 OK — Kịch bản Leo thang Tier 2 Hội đồng):**
```json
{
  "status": "success",
  "scan_id": "SCAN-20261021-9812",
  "created_at": "2026-10-21T08:30:02Z",
  "routing": {
    "routing_path": "TIER_2_FORENSIC_COUNCIL",
    "tier_used": "Tier 2 (AI Forensic Council)",
    "escalated": true,
    "routing_reason": "Độ tự tin Tầng 1 nằm trong vùng rủi ro, kích hoạt Hội đồng Pháp y 3 Chuyên gia phản biện."
  },
  "verdict": {
    "final_label": "SCAM-RISK",
    "is_scam": true,
    "is_unknown": false,
    "risk_level": "CRITICAL",
    "consensus_confidence": 0.945,
    "scam_type": "Mạo danh Ngân hàng & Vi phạm Quyết định 2345/QĐ-NHNN",
    "explanation": "Phát hiện tên miền giả mạo Vietcombank không thuộc vietcombank.com.vn và vi phạm quy định: Ngân hàng không bao giờ gửi SMS yêu cầu click link cập nhật sinh trắc học."
  },
  "telemetry": {
    "total_latency_ms": 1102.5,
    "total_cost_usd": 0.00045,
    "tier1": {
      "model": "ViSoBERT-5runs-release",
      "calibrated_scam_prob": 0.785,
      "latency_ms": 15.8,
      "status": "UNSURE"
    },
    "tier2": {
      "architecture": "3-Agent Heterogeneous Council",
      "early_exit_triggered": false,
      "defender_intervened": false,
      "api_calls_count": 3,
      "specialist_votes": {
        "cyber_financial_analyst": {
          "vote": "SCAM-RISK",
          "confidence": 0.95,
          "model": "gpt-6.1-sol",
          "analysis": "Tên miền 'vcb-digibank-login.com' là tên miền lừa đảo giả mạo cổng giao dịch VCB."
        },
        "psycholinguistic_slang_profiler": {
          "vote": "SCAM-RISK",
          "confidence": 0.90,
          "model": "gpt-6.1-sol",
          "analysis": "Tạo áp lực khẩn cấp 'bị khóa ngay' nhằm thao túng tâm lý nạn nhân."
        },
        "public_defender_advocate": {
          "vote": "SCAM-RISK",
          "confidence": 0.92,
          "model": "gpt-6.1-sol",
          "analysis": "Nội dung vi phạm trực tiếp khuyến cáo an toàn của NHNN, không có dấu hiệu tin nhắn giao dịch thông thường."
        }
      }
    }
  },
  "recommendations": [
    "Tuyệt đối KHÔNG click vào đường link trong tin nhắn.",
    "Ngân hàng không bao giờ yêu cầu cập nhật sinh trắc học qua đường link SMS.",
    "Đổi mật khẩu ứng dụng ngân hàng ngay lập tức nếu đã lỡ bấm vào liên kết."
  ]
}
```

**Response Body (200 OK — Kịch bản Xử lý nhanh Tier 1 Fast-Path):**
```json
{
  "status": "success",
  "scan_id": "SCAN-20261021-1102",
  "created_at": "2026-10-21T08:35:00Z",
  "routing": {
    "routing_path": "TIER_1_DIRECT_FASTPATH",
    "tier_used": "Tier 1 (Local CPU ViSoBERT)",
    "escalated": false,
    "routing_reason": "Độ tự tin Tầng 1 đạt 99.2% >= 90.0% (Ngưỡng an toàn). Xử lý trực tiếp tại thiết bị, tiết kiệm 100% chi phí API."
  },
  "verdict": {
    "final_label": "LOW-RISK",
    "is_scam": false,
    "is_unknown": false,
    "risk_level": "LOW",
    "consensus_confidence": 0.992,
    "scam_type": "Tin nhắn Dịch vụ Thông thường",
    "explanation": "Xử lý trực tiếp bởi Tier 1 ViSoBERT: Mã xác thực giao dịch hợp pháp tiêu chuẩn."
  },
  "telemetry": {
    "total_latency_ms": 15.8,
    "total_cost_usd": 0.0,
    "tier1": {
      "model": "ViSoBERT-5runs-release",
      "calibrated_scam_prob": 0.008,
      "latency_ms": 15.8,
      "status": "CONFIDENT"
    },
    "tier2": {
      "status": "SKIPPED",
      "reason": "FastPath satisfied; no cloud escalation needed."
    }
  },
  "recommendations": [
    "Tin nhắn an toàn. Hãy giữ bảo mật mã OTP của bạn và không chia sẻ cho bất kỳ ai."
  ]
}
```

---

### 3.2. API Lịch Sử Kiểm Tra (Audit & History)
* **Endpoint:** `GET /api/v1/history?page=1&limit=10&label=ALL`
* **Response Body (200 OK):**
```json
{
  "status": "success",
  "total_records": 128,
  "current_page": 1,
  "total_pages": 13,
  "data": [
    {
      "scan_id": "SCAN-20261021-9812",
      "checked_at": "2026-10-21T08:30:02Z",
      "snippet": "Vietcombank tran trong thong bao: Tai khoan quy khach bi khoa do chua cap nhat sinh trac hoc...",
      "final_label": "SCAM-RISK",
      "risk_level": "CRITICAL",
      "tier_used": "Tier 2 (AI Forensic Council)",
      "latency_ms": 1102.5
    },
    {
      "scan_id": "SCAN-20261021-1102",
      "checked_at": "2026-10-21T08:35:00Z",
      "snippet": "Ma OTP xac thuc giao dich thanh toan hoa don dien EVN cua ban la 481920...",
      "final_label": "LOW-RISK",
      "risk_level": "LOW",
      "tier_used": "Tier 1 (Local CPU ViSoBERT)",
      "latency_ms": 15.8
    },
    {
      "scan_id": "SCAN-20261020-4412",
      "checked_at": "2026-10-20T19:15:00Z",
      "snippet": "Thong bao nghi le 30/4 tu ban quan ly toa nha...",
      "final_label": "UNKNOWN",
      "risk_level": "MEDIUM",
      "tier_used": "Tier 2 (AI Forensic Council)",
      "latency_ms": 980.2
    }
  ]
}
```

---

### 3.3. API Báo Cáo Khiếu Nại & Cảnh Báo Cộng Đồng (Article 25 Compliance)
Theo Điều 25 Nghị định 13/2023/NĐ-CP, người dùng có quyền khiếu nại kết quả phân loại tự động nếu nghi ngờ phán quyết sai (đặc biệt đối với các mẫu có nhãn `UNKNOWN` hoặc tranh chấp):
* **Endpoint:** `POST /api/v1/reports/dispute`
* **Request Body:**
```json
{
  "scan_id": "SCAN-20261021-9812",
  "dispute_type": "FALSE_ALARM",
  "user_note": "Đây là tin nhắn nội bộ từ ngân hàng đối tác của công ty chúng tôi.",
  "contact_email": "citizen@example.com"
}
```
* **Response Body (200 OK):**
```json
{
  "status": "success",
  "ticket_id": "TICKET-20261021-0042",
  "message": "Đã tiếp nhận yêu cầu thẩm định thủ công. Kiểm toán viên an ninh mạng sẽ rà soát lại kết quả của Hội đồng AI."
}
```
