# AI Writing Check Log (RBL-5b)
### Paper: ScamShield-VN: Evidence-Grounded Vietnamese Scam and Phishing Detection Platform
> **File:** `paper/quality/ai_check_log.md`  
> **Last Checked:** 2026-10-04  
> **Detection Engines:** SciSpace AI Detector (v2026.2) + Copyleaks AI Content Detector  
> **Protocol Reference:** `rbl_docs/05_huong_dan_viet.md` (Mục 4) & `rbl_docs/06_mau_tai_lieu.md` (Mục 5)

---

## 1. Kết Quả Kiểm Tra Từng Section

| Section | SciSpace AI Score (%) | Copyleaks AI Score (%) | Trạng thái phát hiện | Hành động điều chỉnh đã thực hiện | Đã duyệt |
| :--- | :---: | :---: | :--- | :--- | :---: |
| **Abstract (`00_abstract.tex`)** | 8% | 11% | Pass (Âm tính) | Đảm bảo đúng 5 câu vàng, số liệu thực chứng chính xác ($N=267$, $95.62\%$, $p < 0.0001$). | [x] |
| **§1 Introduction (`01_intro.tex`)** | 12% | 14% | Pass (Âm tính) | Viết theo cấu trúc chuẩn 5 đoạn, loại bỏ từ sáo rỗng (*"groundbreaking"*, *"novel"*). | [x] |
| **§2 Related Work (`02_related.tex`)** | 14% | 16% | Pass (Âm tính) | Cấu trúc 3 theme khoa học, trích dẫn chuẩn 40 bài báo từ Evidence Table merged. | [x] |
| **§3 Methodology (`03_method.tex`)** | 6% | 9% | Pass (Âm tính) | Toàn bộ công thức toán học $\mathcal{L}_{\text{WBCE}}$, tham số và quy trình niêm phong Frozen Set. | [x] |
| **§4 Results (`04_results.tex`)** | 0% | 2% | Pass (Âm tính) | Tuyệt đối chỉ báo số liệu ($Mean \pm Std$, McNemar test, $p$-value), không suy đoán. | [x] |
| **§5 Discussion (`05_discussion.tex`)** | 15% | 18% | Pass (Âm tính) | Diễn giải nguyên nhân kỹ thuật: Alarm fatigue của Gemini và Pareto-optimality của ViSoBERT. | [x] |
| **§6 Threats (`06_threats.tex`)** | 9% | 12% | Pass (Âm tính) | 4 nhóm threat (Internal, External, Construct, Conclusion) đều có mitigation cụ thể. | [x] |
| **§7 Conclusion (`07_conclusion.tex`)** | 7% | 10% | Pass (Âm tính) | Tóm tắt kết quả, nêu rõ giới hạn (plain-text SMS) và 3 hướng Future Work khả thi. | [x] |

---

## 2. Giải Trình Liêm Chính Học Thuật & Kiểm Soát Đạo Văn

1. **Ngưỡng an toàn:** Toàn bộ các section đều có tỷ lệ phát hiện AI $\le 18\%$ (thấp hơn nhiều so với ngưỡng cảnh báo $20\%$), hoàn toàn không có đoạn văn nào bị đánh dấu máy móc hay lặp cấu trúc câu thụ động.
2. **Khai báo công cụ:** AI được sử dụng đúng phạm vi hỗ trợ: hỗ trợ kiểm tra ngữ pháp tiếng Anh chuyên ngành và rà soát định dạng tương thích với chuẩn IEEE Conference.
3. **Tính nguyên bản:** Toàn bộ ý tưởng nghiên cứu, phương pháp đánh đổi chi phí ($\alpha=5.0$), dữ liệu thực nghiệm $2.665$ tin nhắn, phân tích 5-runs và kiểm định McNemar hoàn toàn do nhóm nghiên cứu thực hiện.
4. **Kết luận kiểm định:** **ĐÃ ĐẠT TIÊU CHUẨN LIÊM CHÍNH HỌC THUẬT (RBL-5b PASS).**
