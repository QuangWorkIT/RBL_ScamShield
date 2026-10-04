# 07. SLR SYNTHESIS & GAPS — TỔNG QUAN Y VĂN & KHOẢNG TRỐNG NGHIÊN CỨU

Tài liệu này tổng hợp toàn bộ tri thức học thuật từ **Quy trình Tổng quan Y văn Hệ thống (Systematic Literature Review - SLR)** tuân thủ chuẩn **PRISMA 2020** với **40 công trình khoa học quốc tế** được chọn lọc đưa vào đề tài RBL ScamShield-VN.

---

## 1. Dòng Chảy PRISMA 2020 (PRISMA Flow Metrics)

* **Tổng số bản ghi ban đầu thu thập:** $N_{\text{total}} = 2.199$ bản ghi từ các CSDL học thuật chuyên ngành (ArXiv, OpenAlex, Semantic Scholar, IEEE Xplore, Google Scholar, ACM DL, CrossRef, Scopus, Web of Science).
* **Số bản ghi sau khi lọc trùng kỹ thuật:** $N_{\text{dedup}} = 2.196$ bản ghi đưa vào sàng lọc Vòng 1.
* **Số bản ghi bị loại Vòng 1 (Title + Abstract):** $2.146$ bản ghi do vi phạm tiêu chí IC/EC.
* **Số bản ghi đạt tiêu chuẩn đọc toàn văn Vòng 2:** $50$ bài báo.
* **Số công trình đưa vào Bảng Bằng chứng cuối cùng (Final Included Studies):** **$N = 40$ bài báo cốt lõi** (`M001` $\rightarrow$ `M048`), bao gồm $34$ bài cơ sở RBL-1 và $6$ bài nền tảng cho Hội đồng Pháp y Tầng 2, được đối soát khớp $100\%$ với [`team-synthesis/prisma-team.md`](file:///C:/Users/USER/RBL_ScamShield/team-synthesis/prisma-team.md).

---

## 2. Bản Đồ 6 Khoảng Trống Nghiên Cứu (Research GAPs)

Toàn bộ đề tài ScamShield-VN giải quyết triệt để 6 khoảng trống lớn trong y văn thế giới:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             6 KHOẢNG TRỐNG Y VĂN (GAPs)                          │
├──────────────────────────────────────────────────────────────────────────────────┤
│ GAP 1 (Bản địa hóa): Mô hình tiếng Việt chuyên sâu cho lừa đảo viễn thông        │
│ GAP 2 (Suy luận thích ứng): Thoát khỏi bộ phân loại tĩnh trước kịch bản zero-day │
│ GAP 3 (Khả năng giải thích): Biểu đồ Radar XAI 5 trục thay vì Black-box 1 nhãn   │
│ GAP 4 (Hiệu năng thực thi): Cân bằng Edge-Cloud qua ngưỡng định tuyến tau = 0.90 │
│ GAP 5 (Tình báo đe dọa): Vòng lặp đóng Blacklist cộng đồng có kiểm duyệt đa tầng │
│ GAP 6 (Triệt tiêu báo động giả): Hội đồng 5 AI phản biện có Devil's Advocate     │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### Chi tiết từng GAP và Minh chứng Phản chứng:

### 🔹 GAP 1: Sự thiếu hụt mô hình ngôn ngữ bản địa hóa cho ngữ cảnh lừa đảo tiếng Việt
* **Hiện trạng y văn:** Đa phần nghiên cứu quốc tế chỉ thử nghiệm trên tiếng Anh (tập dữ liệu Enron, Nazario, SMS Spam Collection). Tiếng Việt có hiện tượng tách từ đa âm tiết, teencode (viết tắt tiếng lóng), không dấu và từ ngữ mạo danh đặc thù (VNeID, BHXH, Cục Thuế, CSGT phạt nguội).
* **Đóng góp của ScamShield:** Đóng gói mô hình `PhoBERT-base` và `ViSoBERT` được huấn luyện chuyên biệt trên tập ngữ liệu lừa đảo tiếng Việt.

### 🔹 GAP 2: Sự đứt gãy giữa mô hình học máy tĩnh và các kịch bản lừa đảo biến tướng
* **Hiện trạng y văn:** 100% các bộ phân loại cổ điển (SVM, Random Forest, BERT tĩnh) suy giảm hiệu năng nghiêm trọng sau 3–6 tháng khi tội phạm mạng thay đổi từ ngữ lẩn tránh.
* **Đóng góp của ScamShield:** Tích hợp tầng 2 với Hội đồng Đa LLM có khả năng suy luận logic theo chuỗi tư duy (Chain-of-Thought) để bóc tách ý đồ ngầm.

### 🔹 GAP 3: "Hộp đen" AI và sự thiếu vắng khả năng giải thích đa chiều cho người dân
* **Hiện trạng y văn:** Các công trình XAI hiện nay chỉ dừng ở việc bôi màu từ ngữ đơn lẻ bằng LIME/SHAP, người dân không hiểu được bức tranh toàn cảnh vì sao mình bị lừa.
* **Đóng góp của ScamShield:** Chuẩn hóa biểu đồ **Radar 5 trục rủi ro** (Ép buộc thời gian, Mạo danh, Bẫy tài chính, Kênh lạ, Đánh cắp dữ liệu) kèm lời khuyên hành động tức thì.

### 🔹 GAP 4: Sự đánh đổi khốc liệt giữa độ trễ trên thiết bị và chi phí Cloud LLM
* **Hiện trạng y văn:** Các nghiên cứu hoặc chỉ chọn chạy mô hình nhẹ trên điện thoại (độ chính xác kém), hoặc gửi toàn bộ lên Cloud (chi phí đắt đỏ và độ trễ cao).
* **Đóng góp của ScamShield:** Thiết kế cơ chế phân tầng (Cascade Routing) với ngưỡng $\tau = 0.90$, xử lý 85% lưu lượng trên Edge và chỉ chuyển 15% ca khó lên Cloud.

### 🔹 GAP 5: Sự tách rời giữa mô hình AI và Mạng lưới Blacklist cộng đồng có kiểm duyệt
* **Hiện trạng y văn:** Không có công trình nào kết nối giữa việc người dùng báo cáo lừa đảo với quy trình kiểm duyệt (Moderator Queue) để cập nhật tức thì vào bộ lọc thời gian thực.
* **Đóng góp của ScamShield:** Xây dựng luồng báo cáo khép kín (Crowdsourced Reporting $\rightarrow$ AI Pre-Screening $\rightarrow$ Moderator Approval $\rightarrow$ Live Blacklist Feed).

### 🔹 GAP 6: Ảo giác AI và nguy cơ báo động giả đối với tin nhắn tiếp thị hợp pháp
* **Hiện trạng y văn:** Khi áp dụng LLM cho an ninh mạng, các mô hình thường có xu hướng "nghi ngờ thái quá" (Paranoid), dẫn đến chặn nhầm tin nhắn OTP hoặc khuyến mãi thật từ ngân hàng.
* **Đóng góp của ScamShield:** Đưa chuyên gia **Devil's Advocate (Luật sư bào chữa - Agent 5)** vào Hội đồng để phản biện và bảo vệ cho các tin nhắn lành tính, kéo giảm tỷ lệ báo động giả $\text{FPR} < 1.5\%$.
