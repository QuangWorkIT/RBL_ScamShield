# 03. COUNCIL REGISTRY & CONSENSUS — HỘI ĐỒNG 5 AI & CƠ CHẾ ĐỒNG THUẬN

Tài liệu này đặc tả chi tiết cơ chế hoạt động của **Hội Đồng Giám Định Pháp Y Đa Mô Hình (5-Agent Multi-LLM Forensic Council)** ở Tầng 2, danh mục mô hình dự phòng (Failover Registry), và thuật toán trọng tài đồng thuận (Consensus Engine).

---

## 1. Danh Mục Hội Đồng & Cơ Chế Dự Phòng (Stand-by Failover)

Để đảm bảo hệ thống không bao giờ bị tê liệt khi một nhà cung cấp AI gặp sự cố (Rate Limit HTTP 429, Timeout, sập server), mỗi vai trò trong Hội đồng được cấu hình với **1 mô hình Mặc định (Default)** và **danh sách mô hình Dự phòng (Standby)**:

```yaml
council_registry:
  # Vai trò 1: Điều tra viên pháp y chính
  forensic_investigator:
    default_model: "deepseek-chat" # DeepSeek-V3
    standby_models:
      - "gemini-1.5-pro"
      - "gpt-4o"
      - "claude-3-5-sonnet-20241022"
    weight: 0.25

  # Vai trò 2: Chuyên gia phân tích tâm lý ngôn ngữ
  psycholinguistic_analyst:
    default_model: "claude-3-5-sonnet-20241022"
    standby_models:
      - "gpt-4o"
      - "gemini-1.5-pro"
      - "qwen-2.5-72b-instruct"
    weight: 0.15

  # Vai trò 3: Chuyên gia tình báo đe dọa không gian mạng
  threat_intelligence_analyst:
    default_model: "llama-3.3-70b-versatile" # Groq / Local vLLM
    standby_models:
      - "qwen-2.5-72b-instruct"
      - "deepseek-chat"
      - "gpt-4o-mini"
    weight: 0.20

  # Vai trò 4: Chuyên gia gian lận tài chính & ngân hàng
  financial_fraud_analyst:
    default_model: "gemini-1.5-pro"
    standby_models:
      - "gpt-4o"
      - "claude-3-5-sonnet-20241022"
      - "deepseek-chat"
    weight: 0.20

  # Vai trò 5: Người phản biện / Luật sư bào chữa (Devil's Advocate)
  defense_validator:
    default_model: "claude-3-5-sonnet-20241022"
    standby_models:
      - "gpt-4o-mini"
      - "gemini-1.5-flash"
      - "llama-3.3-70b-versatile"
    weight: 0.20
```

### Nguyên tắc Chuyển Đổi Kịp Thời (Failover Protocol):
* Khi gửi yêu cầu tới mô hình mặc định:
  * Nếu gặp lỗi mã `429 Too Many Requests` hoặc `504 Gateway Timeout` (> 3.5 giây):
  * Tự động chuyển đổi tức thì sang mô hình `standby_models[0]` trong danh sách.
  * Ghi nhận cảnh báo vào audit log để hệ thống giám sát tải API.

---

## 2. Đặc Tả 5 Vai Trò Giám Định

| Vai trò | Trọng tâm phân tích | Câu hỏi then chốt (Core Question) |
| :--- | :--- | :--- |
| **1. Forensic Investigator** | Bối cảnh tổng thể, thủ thuật kỹ thuật, vector tấn công | *Kịch bản này có trùng khớp với phương thức hoạt động (Modus Operandi) của các tổ chức tội phạm mạng đã biết không?* |
| **2. Psycholinguistic Analyst** | Thao túng tâm lý: Nỗi sợ (FOMO/FUD), cưỡng ép thời gian, kích thích lòng tham | *Văn bản có cố tình tạo áp lực hoảng loạn để nạn nhân không kịp suy nghĩ lý trí không?* |
| **3. Threat Intelligence** | Đối soát số điện thoại, tên miền, đầu số viễn thông, URL rút gọn | *Tên miền có giả mạo cơ quan nhà nước / thương hiệu không? Đầu số có nằm trong danh sách đen không?* |
| **4. Financial Fraud Analyst** | Dòng tiền: Khóa tài khoản, nợ thuế, VNeID cấp 2, trúng thưởng, hoàn tiền | *Yêu cầu chuyển tiền hoặc thông tin tài khoản này có tuân thủ đúng quy trình ngân hàng chính thống không?* |
| **5. Defense Validator** | Tìm lý do bảo vệ: Khuyến mãi thật, thông báo cước viễn thông hợp pháp | *Có căn cứ hợp pháp nào cho thấy đây là tin nhắn CSKH/quảng cáo bình thường bị nghi oan không?* |

---

## 3. Thuật Toán Trọng Tài Đồng Thuận (Consensus Engine)

### 3.1. Phán quyết phân loại danh mục (Categorical Verdict)
Mỗi mô hình trong 5 Agent bỏ 1 phiếu bầu $v_i \in \{\text{SAFE}, \text{SUSPICIOUS}, \text{DANGEROUS}\}$.
* **Quy tắc An Toàn Tối Cao (Safety-First Rule):** 
  * Nếu có $\ge 3$ phiếu chọn `DANGEROUS` $\rightarrow$ Kết luận: **`DANGEROUS`**.
  * Nếu $\ge 1$ phiếu `DANGEROUS` và $\ge 2$ phiếu `SUSPICIOUS` $\rightarrow$ Kết luận: **`SUSPICIOUS`**.
  * Chỉ khi $\ge 4$ phiếu chọn `SAFE` và Agent 5 (Defense Validator) xác nhận không có yếu tố rủi ro $\rightarrow$ Kết luận: **`SAFE`**.

### 3.2. Công thức Điểm Rủi Ro Tổng Hợp (Weighted Risk Score)
Điểm số rủi ro $S_{\text{final}} \in [0, 100]$ được tính theo trọng số đóng góp của từng chuyên gia:
$$S_{\text{final}} = \sum_{i=1}^5 w_i \cdot s_i$$
Trong đó:
* $w_i$: Trọng số chuyên gia ($\sum w_i = 1.0$).
* $s_i \in [0, 100]$: Điểm rủi ro do từng chuyên gia chấm.

### 3.3. Radar 5 Trục Rủi Ro (5-Axis Risk Radar)
Mỗi phán quyết của Hội đồng xuất ra 5 chỉ số trực quan để vẽ biểu đồ Radar trên ứng dụng di động / web:
1. **Urgency (0 - 100):** Mức độ ép buộc thực hiện gấp (ví dụ: "trong 24h", "khóa sim sau 2 tiếng").
2. **Authority Impersonation (0 - 100):** Mức độ mạo danh cơ quan công an, tòa án, thuế, điện lực.
3. **Financial Lure / Extortion (0 - 100):** Yếu tố tiền bạc, đe dọa tài sản, hứa hẹn trúng thưởng.
4. **Suspicious Channel (0 - 100):** Kênh liên lạc bất thường, đầu số lạ, link không chính chủ.
5. **Data Harvesting (0 - 100):** Yêu cầu cung cấp mã OTP, căn cước công dân, mật khẩu, sinh trắc học.
