# RBL_SPECS.md — Đặc Tả Kiến Trúc & Hợp Đồng Dữ Liệu (Kế Thừa RBL ScamShield)

Tài liệu này tổng hợp toàn bộ các kết quả kỹ thuật, kiến trúc trí tuệ nhân tạo 2 tầng (Two-Tier AI Architecture) và hợp đồng giao tiếp API (API Contracts) được xây dựng từ đề tài nghiên cứu RBL ScamShield-VN.

---

## 1. Kiến Trúc Phát Hiện Lừa Đảo 2 Tầng (Two-Tier Pipeline)

```
                            [ Người Dùng Gửi Mẫu Kiểm Tra ]
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │   TIER 1: On-Device / Edge Screener   │
                      │  (PhoBERT-base / ViSoBERT ONNX)       │
                      │  Latency < 50ms, Phân loại siêu nhanh │
                      └───────────────────┬───────────────────┘
                                          │
                        Độ tự tin P >= 0.90 ?
                                 ┌────────┴────────┐
                             CÓ │                 │ KHÔNG (P < 0.90)
                                ▼                 ▼
                      ┌────────────────┐   ┌─────────────────────────────────────────┐
                      │ TRẢ KẾT QUẢ    │   │ TIER 2: Cloud Multi-LLM Forensic Council│
                      │ TỨC THÌ        │   │ (Hội Đồng 5 Chuyên Gia AI Độc Lập)      │
                      │ (Safe / Spam)  │   │  Gemini, DeepSeek, Claude, Llama, GPT   │
                      └────────────────┘   └────────────────────┬────────────────────┘
                                                                │
                                                                ▼
                                                   ┌─────────────────────────┐
                                                   │ Trọng Tài Đồng Thuận    │
                                                   │ Consensus Engine        │
                                                   │ Phán quyết & Radar XAI  │
                                                   └─────────────────────────┘
```

### Chi tiết 5 Chuyên Gia Hội Đồng Tier 2:
1. **Agent 1 (Forensic Lead):** Đánh giá kịch bản lừa đảo tổng thể, đối chiếu dấu vết tội phạm mạng.
2. **Agent 2 (Psycholinguistic Manipulations):** Phân tích ngôn ngữ thao túng tâm lý (sợ hãi, ép buộc thời gian, lòng tham).
3. **Agent 3 (Cyber Threat Intelligence):** Tra cứu dữ liệu Blacklist cộng đồng, domain giả mạo, đầu số viễn thông rác.
4. **Agent 4 (Financial Fraud Analyst):** Nhận diện các bẫy tài chính, chuyển tiền nhầm, khóa tài khoản, bẫy thuế/VNeID.
5. **Agent 5 (Devil's Advocate / Defense Validator):** Tìm kiếm bằng chứng phản biện để loại trừ việc báo động giả (False Positive) cho tin nhắn quảng cáo thông thường từ nhà mạng/ngân hàng thật.

---

## 2. Chuẩn API Contracts (Dành Cho Frontend & Backend)

### 2.1. API Kiểm Tra Lừa Đảo (SCRUM-12: Register User Check Scam)
* **Endpoint:** `POST /api/v1/scan`
* **Headers:** `Authorization: Bearer <jwt_token>` (nếu là user đã đăng nhập)

**Request Body:**
```json
{
  "content": "Cuc Thue TP.HCM thong bao: Quy khach con no thue 3.200.000d. Vui long truy cap https://vneid-thuetphcm.com de nop phat truoc 24h neu khong se bi phong toa tai khoan.",
  "sender": "0981234567",
  "check_type": "TEXT", // Hoặc "URL", "PHONE", "BANK_ACCOUNT"
  "target_bank": null,
  "target_account_number": null
}
```

**Response Body (200 OK):**
```json
{
  "status": "success",
  "scan_id": "SCAN-20261004-9812",
  "created_at": "2026-10-04T18:30:00Z",
  "tier_executed": 2, // 1 hoặc 2
  "verdict": {
    "risk_level": "DANGEROUS", // "SAFE" | "SUSPICIOUS" | "DANGEROUS"
    "risk_score": 96.5, // Thang điểm 0 - 100
    "scam_type": "Mạo danh cơ quan Thuế / Nhà nước (Phishing & Extortion)",
    "confidence": 0.98,
    "summary": "Tin nhắn mạo danh Cục Thuế nhằm ép buộc nạn nhân bấm vào đường link giả mạo đánh cắp thông tin tài khoản."
  },
  "radar_metrics": {
    "urgency": 95,              // Mức độ ép buộc thời gian (trước 24h)
    "authority_impersonation": 98,// Mạo danh cơ quan nhà nước
    "financial_lure": 80,       // Đe dọa nợ tiền, phong tỏa tài sản
    "suspicious_channel": 92,   // Tên miền giả mạo .com thay vì .gov.vn
    "data_harvesting": 90       // Ý đồ thu thập thông tin đăng nhập
  },
  "council_audit": {
    "consensus_ratio": "5/5",
    "lead_evaluator": "DeepSeek-V3",
    "defense_notes": "Tên miền không thuộc hệ thống gov.vn, số điện thoại lạ không có Brandname chính thức."
  },
  "recommendations": [
    "Tuyệt đối không truy cập đường link trong tin nhắn.",
    "Không cung cấp mã OTP, thông tin thẻ ngân hàng hoặc tài khoản VNeID.",
    "Báo cáo ngay số điện thoại và đường link này lên cơ sở dữ liệu ScamShield."
  ]
}
```

---

### 2.2. API Lịch Sử Kiểm Tra (SCRUM-13: Scam Check History)
* **Endpoint:** `GET /api/v1/history?page=1&limit=10&risk_level=ALL`
* **Response Body (200 OK):**
```json
{
  "status": "success",
  "total_records": 48,
  "current_page": 1,
  "total_pages": 5,
  "data": [
    {
      "scan_id": "SCAN-20261004-9812",
      "checked_at": "2026-10-04T18:30:00Z",
      "check_type": "TEXT",
      "snippet": "Cuc Thue TP.HCM thong bao: Quy khach con no thue 3.200.000d...",
      "risk_level": "DANGEROUS",
      "risk_score": 96.5,
      "scam_type": "Mạo danh Cục Thuế"
    },
    {
      "scan_id": "SCAN-20261003-4412",
      "checked_at": "2026-10-03T09:15:00Z",
      "check_type": "URL",
      "snippet": "https://vietcombank-login-security.net",
      "risk_level": "DANGEROUS",
      "risk_score": 99.0,
      "scam_type": "Phishing Ngân hàng Vietcombank"
    },
    {
      "scan_id": "SCAN-20261002-1102",
      "checked_at": "2026-10-02T14:20:00Z",
      "check_type": "TEXT",
      "snippet": "Chuc mung ban da trung thuong voucher 500k tu Shopee...",
      "risk_level": "SUSPICIOUS",
      "risk_score": 62.0,
      "scam_type": "Tin nhắn tiếp thị nghi vấn"
    },
    {
      "scan_id": "SCAN-20261001-0810",
      "checked_at": "2026-10-01T08:10:00Z",
      "check_type": "PHONE",
      "snippet": "02838295115",
      "risk_level": "SAFE",
      "risk_score": 5.0,
      "scam_type": "Tổng đài chính thức"
    }
  ]
}
```

---

### 2.3. API Báo Cáo Lừa Đảo (SCRUM-14: Submit Scam Report)
* **Endpoint:** `POST /api/v1/reports`
* **Request:**
```json
{
  "target_type": "URL", // "PHONE" | "URL" | "BANK_ACCOUNT" | "SMS"
  "target_value": "https://vneid-thuetphcm.com",
  "category": "Mạo danh cơ quan nhà nước",
  "description": "Nhận được tin nhắn dọa phong tỏa tài khoản nếu không nộp phạt thuế.",
  "loss_amount": 0,
  "evidence_urls": [
    "https://storage.scamshield.vn/evidence/screenshot_01.png"
  ]
}
```

---

### 2.4. API Theo Dõi Báo Cáo (SCRUM-15: Report Tracking)
* **Endpoint:** `GET /api/v1/reports/tracking`
* **Trạng thái:**
  * `PENDING`: Đang chờ tiếp nhận.
  * `AI_ANALYZING`: Hội đồng AI đang rà soát dữ liệu.
  * `VERIFIED_SCAM`: Đã xác thực lừa đảo & đưa vào Blacklist cộng đồng.
  * `REJECTED`: Báo cáo không đủ bằng chứng hoặc không phải lừa đảo.
