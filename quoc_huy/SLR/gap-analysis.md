# GAP Analysis — Sự Đứt Gãy Giữa Mô Hình Học Máy Tĩnh và Trí Tuệ Đe Dọa Cộng Đồng Trong Nhận Diện Lừa Đảo

**Thành viên:** Nguyễn Quốc Huy
**GAP type:** GAP-S
**Ngày:** 2026-09-10
**Evidence table nguồn:** `team-synthesis/evidence-table-merged.md`
**N =** 10 bài báo core (`M029`, `M030`, `M031`, `M032`, `M033`, `M034`, `M035`, `M036`, `M037`, `M038`)

---

## 1. Mô tả GAP & Căn cứ Bằng chứng (GAP Description & Evidence Grounding)

Hiện nay, các nghiên cứu học thuật về phát hiện tin nhắn lừa đảo/spam chủ yếu tập trung vào việc huấn luyện các mô hình tĩnh trên những bộ dữ liệu đóng, thiếu vắng sự kết nối với tri thức từ cộng đồng theo thời gian thực. Khi các chiến dịch lừa đảo mới xuất hiện (ví dụ: mạo danh VNeID, nộp phạt giao thông online), các mô hình tĩnh này hoàn toàn bất lực và thường có độ trễ lớn trước khi được cập nhật dữ liệu và huấn luyện lại. Sự đứt gãy giữa mô hình học máy tĩnh và trí tuệ đe dọa cộng đồng (Community Threat Intelligence) khiến hệ thống thiếu tính thích ứng liên tục với thực tiễn.

**Bằng chứng từ evidence table:**
- Xuyên suốt 10/10 bài báo phân tích (từ các họ mô hình truyền thống như Naive Bayes, SVM trong `M031` đến các mô hình Transformer như RoBERTa, DeBERTa, LLM trong `M032`, `M033`, `M037`), tất cả đều chỉ dừng lại ở việc huấn luyện và đánh giá mô hình phân loại trên các bộ dữ liệu tĩnh, hoàn toàn không có cơ chế thu thập dữ liệu tự động hoặc tiếp nhận phản hồi từ người dùng cuối.
- Các framework tiên tiến như FraudSMSWalker (`M029`), PEEK (`M035`), hay Genshin (`M036`) cố gắng sinh dữ liệu tấn công đối kháng để cải thiện độ bền vững của mô hình, nhưng vẫn đóng khung trong giới hạn phòng thí nghiệm, bỏ qua nguồn cập nhật dữ liệu khổng lồ và nhanh nhạy nhất là báo cáo từ cộng đồng.

---

## 2. Kiểm tra phản chứng (Counter-Evidence Matrix)

| Paper | Đã làm GAP này không? | Chi tiết |
|---|---|---|
| `M029` (FraudSMSWalker) | Không | Tập trung benchmark khả năng phân loại của LLM agent trên chuỗi SMS-to-Webpage, hoàn toàn không có module tiếp nhận phản ánh cộng đồng. |
| `M032` (Agentic KD), `M033` (SecureNet) | Không | Dùng LLM lớn (Teacher) để chưng cất tri thức sang SLM (Student) hoặc so sánh với DeBERTa. Đều huấn luyện offline trên tập dữ liệu đóng. |
| `M031`, `M038` | Không | Đánh giá các mô hình ML và Transformer trên dữ liệu tĩnh (Kaggle SMS, SpamAssassian). Không có cơ chế thu thập dữ liệu mới. |
| `M034`, `M037` | Không | Sử dụng Explainable AI (LIME, Transformers Interpret) để giải thích mô hình, không liên quan đến hệ thống cộng đồng. |
| `M035` (PEEK), `M036` (Genshin) | Không | Framework sinh dữ liệu đối kháng bằng LLM/GAN để vượt rào bộ lọc, nhưng tự động sinh dữ liệu chứ không lấy từ cộng đồng người dùng thực. |

**Kết luận:** GAP xác nhận ✅ Tất cả các nghiên cứu hiện tại đều có một lỗ hổng chung (GAP-S): thiếu sự kết hợp giữa mô hình nhận diện tĩnh và hệ thống thông minh từ cộng đồng (cơ chế báo cáo, blacklist động, quy trình kiểm duyệt).

---

## 3. Đánh giá khả thi 7 yếu tố (7-Factor Feasibility Evaluation Matrix)

| Tiêu chí | Mức | Ghi chú |
|---|---|---|
| **1. Dataset** | ✅ | Có thể sử dụng các nguồn dữ liệu từ ChongLuaDao và tạo giả lập các báo cáo cộng đồng để thử nghiệm. |
| **2. API / Tooling** | ✅ | Stack web/app cơ bản (Node.js/Python, React) có thể dễ dàng thiết kế hệ thống workflow kiểm duyệt và API thu thập. |
| **3. Compute** | ✅ | Hệ thống workflow và heatmap không đòi hỏi GPU cấu hình cao, chủ yếu thao tác trên cơ sở dữ liệu. Phân tích AI đính kèm có thể chạy trên Colab. |
| **4. Ground Truth** | ⚠️ | Cần xây dựng quy trình kiểm duyệt đa tầng (Moderator review) để tránh báo cáo giả mạo từ cộng đồng. |
| **5. Codebase** | ✅ | Có sẵn các thư viện/framework phát triển web và xử lý luồng dữ liệu (workflow). |
| **6. Skill Set** | ✅ | Nhóm có kỹ năng phát triển Web/Backend và xây dựng luồng Moderation Workflow. |
| **7. Time Budget** | ✅ | Hoàn toàn khả thi để tích hợp tính năng Blacklist và Heatmap trong thời gian môn học. |

**Kết quả:** 0 ❌ / 1 ⚠️ -> Đã có phương án giảm thiểu rủi ro (Moderation Workflow) cho tiêu chí Ground Truth. An toàn, tiến hành.

---

## 4. Phát biểu GAP chính thức (Formal GAP Statement)

Mặc dù các mô hình ngôn ngữ và học máy hiện đại đạt độ chính xác cao trong việc phát hiện lừa đảo trên các tập dữ liệu đóng, nhưng chưa có nghiên cứu nào tích hợp các mô hình tĩnh này với nền tảng trí tuệ đe dọa cộng đồng (Community Threat Intelligence) — bao gồm cơ chế tiếp nhận báo cáo thời gian thực, quy trình kiểm duyệt đa tầng chống báo cáo giả, và bản đồ nhiệt (Threat Heatmap) — để giải quyết triệt để sự đứt gãy trong việc thích ứng với các chiến dịch lừa đảo mới.

---

## 5. Đề xuất sơ bộ phương pháp thuật toán & Hệ thống (Preliminary Technical Proposal)

- **Hệ thống mục tiêu:** Nền tảng ScamShield với sự kết hợp giữa AI Classifier (từ các thành viên khác) và **Hệ thống Blacklist Cộng đồng**.
- **Luồng hoạt động (Workflow):**
  1. Người dùng báo cáo số điện thoại, tài khoản ngân hàng, hoặc link lừa đảo thông qua Nền tảng.
  2. Hệ thống thu thập và gom cụm các báo cáo trùng lặp (dùng thuật toán clustering đơn giản hoặc match string).
  3. **Quy trình kiểm duyệt đa tầng (Moderation Workflow):** AI chấm điểm độ tin cậy sơ bộ -> Moderator duyệt thủ công chống phá hoại/spam.
  4. Cập nhật Blacklist và **Bản đồ nhiệt rủi ro (Threat Heatmap)** theo thời gian thực.
- **Tiêu chí đánh giá (Metrics):** Tốc độ cập nhật blacklist, độ chính xác của bộ lọc báo cáo rác/giả mạo (Moderation Accuracy), và khả năng visualize dữ liệu trên Heatmap.
