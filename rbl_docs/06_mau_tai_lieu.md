# 📎 MẪU TÀI LIỆU DÙNG LẠI (TEMPLATES & BIỂU MẪU RBL)

> Bộ biểu mẫu chuẩn hóa dùng xuyên suốt từ **RBL-1 đến RBL-5b**, đảm bảo tính đồng bộ, nhất quán và minh bạch khoa học trong toàn bộ dự án.

---

## 1. Mẫu Evidence Table (7 Cột Bắt Buộc — RBL-1)

| Cột | Ghi gì | Lưu ý kiểm tra |
| :--- | :--- | :--- |
| **Paper** | Tên tác giả + Năm + Venue + DOI (kèm link để kiểm tra) | Không cite Wikipedia, blog, GitHub README. |
| **Tool / LLM** | Tên cụ thể (vd: ViSoBERT, PhoBERT-large, GPT-4o-mini, LLM-based agent) | Tuyệt đối không ghi "AI model" chung chung. |
| **Dataset** | Tên dataset + Số lượng mẫu $N$ + Domain dữ liệu thực nghiệm | Là dữ liệu kiểm thử, không phải dữ liệu tiền huấn luyện. |
| **Metric** | Tên thước đo cụ thể (Scam Recall, F1-score, Precision, AUC, Latency) | Không ghi "accuracy" chung chung. |
| **Kết quả** | Con số thực chứng trích từ Table/Figure của bài báo | Không có thì ghi `N/A`. |
| **Code** | Link GitHub repo hoặc replication package (nếu có) | Ghi `N/A` nếu không công khai. |
| **Hạn chế** | Trích từ phần Threats to Validity / Limitations của bài báo | Không nêu thì ghi `N/A`. |

> [!NOTE]
> Có ô `N/A` là bình thường trong nghiên cứu thực tế.  
> **4 Loại GAP nghiên cứu:**
> * **GAP-T (Technology):** Kỹ thuật/công cụ/mô hình chưa từng được thử nghiệm cho tác vụ này.
> * **GAP-M (Measurement):** Khía cạnh/chỉ số chưa từng được đo đạc (ví dụ: cost-sensitive recall trong lừa đảo).
> * **GAP-D (Domain/Data):** Miền dữ liệu hoặc ngôn ngữ còn thiếu (ví dụ: SMS lừa đảo tiếng Việt mạng xã hội).
> * **GAP-S (Shared Limitation):** Hạn chế chung mà $\ge 40\%$ số bài báo cùng thừa nhận.

---

## 2. Khung Proposal Chuẩn 8 Mục (RBL-3)

```markdown
# Research Proposal: [Tên đề tài ngắn gọn]
**Nhóm:** [Tên nhóm]
**Thành viên:** [Họ tên (MSSV) - Vai trò]
**Topic code:** RT-[Mã đề tài]
**Ngày nộp:** YYYY-MM-DD
**Version:** 1.0
**Xung đột lợi ích và hỗ trợ:** Không có / [Ghi rõ nếu có tài trợ API, tài nguyên tính toán]

---

## §1 Tiêu đề và Thông tin
[Tóm tắt ngắn gọn bối cảnh và định danh nghiên cứu]

## §2 Problem Statement (~1 trang)
[Bối cảnh thực tế -> Hiện tại nghiên cứu đã làm gì -> GAP còn lại -> Vì sao GAP quan trọng. Phải nêu >= 3 paper cụ thể]

## §3 Related Work (Bảng tóm tắt)
[Tổng hợp theo pattern: cùng LLM, cùng metric, cùng dataset; pattern nào thiếu thì trỏ thẳng vào GAP]

## §4 Research Questions (Chốt tại đây)
"Với [Dataset P], [Can thiệp I] khác [Đối chứng C] thế nào về [Metric O]?"
- **H0:** [Metric] của [I] KHÔNG khác [C]
- **H1:** [Metric] của [I] KHÁC [C]
- **Ngưỡng chấp nhận thực tiễn:** [Threshold θ] (Nguồn: Case 1/2/3)

## §5 Experiment Protocol
- **5.1 LLM / Tool:** Tên version chính xác, temperature, top_p, max_tokens
- **5.2 Prompt:** Copy nguyên văn vào Appendix
- **5.3 Dataset & Pipeline:** Tên, kích thước N, cách tải, license, pipeline từ input -> output
- **5.4 Gán nhãn & IAA:** Quy trình gán nhãn, số người gán, ngưỡng Cohen's κ >= 0.7
- **5.5 Tính không tất định & Độ lặp:** Số lần lặp K >= 3, quy tắc gộp trung vị
- **5.6 Thứ tự chạy:** Batching ngẫu nhiên, lưu lịch chạy item_id
- **5.7 Đạo đức:** Khẳng định "Không có người tham gia" hoặc bản đồng ý ẩn danh

## §6 Evaluation Plan
- Tiêu chí bác bỏ H0: p-value < 0.05
- Tiêu chí chấp nhận thực tiễn: Vượt ngưỡng θ
- Cỡ mẫu tối thiểu N đảm bảo Statistical Power >= 0.8 (G*Power)

## §7 Threats to Validity
- **Internal:** Tính không tất định của model -> Mitigation: Cố định seed, K=3
- **External:** Phạm vi ngôn ngữ/tập dữ liệu -> Mitigation: Nêu rõ ranh giới
- **Construct:** Độ tin cậy của thước đo -> Mitigation: Chống data leakage
- **Conclusion:** Kiểm định thống kê phù hợp -> Mitigation: Báo cả effect size và 95% CI

## §8 Timeline, Phân công & Chi phí
- Phân công chi tiết theo từng Section (§1-§7)
- Bảng dự toán chi phí API: [N x (Token_in x Giá_in + Token_out x Giá_out) x K + Pilot] x 1.2 (Buffer 20%)
```

---

## 3. Bảng Chọn Kiểm Định Thống Kê & Thước Đo Effect Size

| Kiểu dữ liệu | Tình huống so sánh | Kiểm định thống kê | Thước đo Effect Size & Thang đánh giá |
| :--- | :--- | :--- | :--- |
| **Điểm số liên tục** | So sánh với ngưỡng cố định $\theta$ | **Wilcoxon signed-rank 1 mẫu** (1 phía) | **Rank-biserial $r$ 1 mẫu** kèm Median & $95\%\text{ CI}$ |
| **Điểm số liên tục** | 2 điều kiện trên **cùng các mục (ghép cặp)** | **Wilcoxon signed-rank ghép cặp** | **Rank-biserial $r$ ghép cặp** hoặc **Cohen's $d_z$**<br>($\|r\| \approx 0.1$: nhỏ, $0.3$: TB, $0.5$: lớn) |
| **Điểm số liên tục** | 2 nhóm mục **khác nhau (độc lập)** | **Mann-Whitney U** | **Cliff's $\delta$** ($0.147$: nhỏ, $0.33$: TB, $0.474$: lớn) hoặc **Cohen's $d$** ($0.2$: nhỏ, $0.5$: TB, $0.8$: lớn) |
| **Đúng / Sai (Nhị phân)** | So với ngưỡng tỷ lệ cố định | **Binomial exact** (1 phía) | Tỷ lệ chênh lệch kèm $95\%\text{ CI}$ |
| **Đúng / Sai (Nhị phân)** | 2 điều kiện trên **cùng các mục (ghép cặp)** | **McNemar test** (Bảng chéo $2\times 2$) | **Odds Ratio (OR)** hoặc Risk Difference |

> **Độ đồng thuận gán nhãn (IAA):**
> * **Cohen's $\kappa \ge 0.8$:** Rất tốt.
> * **$0.7 \le \kappa < 0.8$:** Chấp nhận được.
> * **$\kappa < 0.7$:** Dừng lại, làm rõ guideline gán nhãn rồi gán lại.

---

## 4. Mẫu Proposal Amendment (Điều Chỉnh Thiết Kế Nghiên Cứu)

```markdown
# Proposal Amendment — v[X]
**Nhóm:** [Tên nhóm]  
**Ngày yêu cầu:** YYYY-MM-DD  
**Proposal gốc:** v1.0 (được GVHD duyệt ngày YYYY-MM-DD)

## 1. Thay đổi đề xuất
| Mục | Nội dung cũ | Nội dung mới | Lý do bắt buộc phải đổi |
| :--- | :--- | :--- | :--- |
| §4 Metric | Accuracy | Scam Recall | Tối ưu hóa việc phát hiện lừa đảo trong tập mất cân bằng |
| §5 Dataset | N = 3000 | N = 2665 | Loại bỏ các mẫu nhiễu và trùng lặp sau khi tiền xử lý |

## 2. Trạng thái dữ liệu khi xin amendment
- [ ] Chưa chạy experiment nào
- [x] Đã chạy pilot: kết quả pilot cho thấy cần điều chỉnh
- [ ] Đã chạy full: chỉ áp dụng trường hợp bất khả kháng

## 3. Cam kết
Nhóm cam kết không tự ý thay đổi mã nguồn hoặc tiến hành chạy full cho đến khi nhận được phê duyệt chính thức từ GVHD.

**PL xác nhận:** [Ký tên, Ngày]  
**GVHD phê duyệt:** [Xác nhận, Ngày]
```

---

## 5. Mẫu Báo Cáo Kiểm Tra Văn Phong AI (`ai_check_log.md`)

```markdown
# AI Writing Check Log
**Paper:** ScamShield-VN Empirical Evaluation  
**Ngày check cuối:** YYYY-MM-DD  
**Công cụ sử dụng:** SciSpace AI Detector + Copyleaks (Phiên bản YYYY-MM)

| Section | Công cụ 1 (%) | Công cụ 2 (%) | Đoạn cần viết lại | Đã sửa |
| :--- | :---: | :---: | :--- | :---: |
| §1 Introduction | 12% | 15% | Không có | [x] |
| §2 Related Work | 18% | 22% | Đoạn 2 câu 3 (liệt kê máy móc) | [x] |
| §3 Methodology | 5% | 8% | Không có | [x] |
| §4 Results | 0% | 2% | Không có (chỉ có số và test) | [x] |
| §5 Discussion | 25% | 28% | Đoạn 1 câu mở đầu | [x] |
| §6 Threats | 10% | 14% | Không có | [x] |
| §7 Conclusion | 8% | 10% | Không có | [x] |

**Giải trình:** Các đoạn có tỷ lệ trên 20% đã được viết lại bằng tay theo quy trình 4 bước, loại bỏ hoàn toàn các cấu trúc câu bị động và mở đầu sáo rỗng.  
**Khai báo sử dụng AI:** AI được dùng để hỗ trợ kiểm tra lỗi chính tả tiếng Anh và gợi ý từ khóa tìm kiếm; toàn bộ số liệu và phân tích do nhóm tự thực hiện.  
**Kết luận:** ĐÃ ĐẠT TIÊU CHUẨN LIÊM CHÍNH HỌC THUẬT.
```

---

## 6. Mẫu Tuyên Bố Khai Báo Sử Dụng AI (Cuối Bài Báo)

```markdown
### AI Usage Declaration
During the preparation of this manuscript, the authors used [Tên công cụ, vd: Google Gemini / Grammarly] for [Mục đích, vd: language editing and grammar polishing]. The authors reviewed and edited the output and take full responsibility for the content of the publication. The authors confirm that AI was NOT used to generate experimental data, manipulate statistical metrics, or fabricate evaluation results.
```
