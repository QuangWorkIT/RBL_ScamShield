# RESEARCH PROPOSAL: SCAMSHIELD-VN
### Nền tảng Nhận diện và Cảnh báo Tin nhắn Lừa đảo Tiếng Việt Dựa trên Mô hình Ngôn ngữ Địa phương hóa và Cơ chế Phạt Chi phí Bất cân xứng

> **Topic Code:** RT-ScamShield-Nhom1  
> **Nhóm thực hiện:** Nhóm 1  
> **Thành viên:**  
> 1. Nguyễn Trung Hiếu (MSSV: SE170001) — Project Lead (PL) / LLM Runner (LR)  
> 2. Lê Quốc Huy (MSSV: SE170002) — Report Writer (RW)  
> 3. Hoàng Hải Phúc (MSSV: SE170003) — Metrics & Statistics (MS)  
> 4. Phan Trần Hoàng Trân (MSSV: SE170004) — Data & Ground Truth (DG)  
> 5. Nguyễn Minh Quang (MSSV: SE170005) — Literature Reviewer & Pipeline Support  
> **GVHD hướng dẫn:** ThS. L.T.Q.Chi  
> **Ngày nộp:** 2026-09-20 | **Version:** 1.0 (Đóng băng thiết kế)  
> **Xung đột lợi ích và hỗ trợ:** Không có bất kỳ xung đột lợi ích tài chính hay học thuật nào. Toàn bộ tài nguyên tính toán sử dụng môi trường GPU mở và máy trạm cá nhân của nhóm nghiên cứu.

---

## §1 Tiêu Đề và Thông Tin Định Danh
* **Tên đề tài tiếng Việt:** Nghiên cứu thực nghiệm giải pháp nhận diện tin nhắn lừa đảo và mạo danh viễn thông tiếng Việt bằng mô hình ViSoBERT kết hợp hàm mất mát có trọng số nhạy cảm chi phí trên thiết bị biên.
* **Tên đề tài tiếng Anh:** *Empirical Evaluation of ViSoBERT with Cost-Sensitive Weighted Binary Cross-Entropy Loss for Real-Time On-Device Vietnamese Scam Message Detection*.
* **Tóm lược đề tài:** Đề tài xây dựng một quy trình thực nghiệm có đối chứng, đánh giá toàn diện mô hình ngôn ngữ tiền huấn luyện tối ưu hóa mạng xã hội tiếng Việt (**ViSoBERT**) kết hợp hàm mất mát nhạy cảm chi phí **Weighted Binary Cross-Entropy ($\mathcal{L}_{\text{WBCE}}$, $\alpha=5.0$)** và lượng tử hóa mô hình **ONNX INT8**, nhằm giải quyết triệt để vấn đề bỏ sót tin nhắn độc hại (*False Negative*) mà các mô hình nền tảng đối chứng (PhoBERT, FPT ViBERT, LLMs) thường mắc phải.

---

## §2 Problem Statement (~1 trang)

Vấn nạn lừa đảo qua tin nhắn viễn thông (Smishing), tin nhắn mạo danh ngân hàng và các chiêu trò gian lận tài chính trực tuyến tại Việt Nam đang diễn biến hết sức phức tạp, gây thiệt hại hàng ngàn tỷ đồng mỗi năm cho người dùng. Đặc thù của tin nhắn lừa đảo tại Việt Nam là việc kẻ tấn công liên tục biến đổi ngữ nghĩa, sử dụng từ lóng mạng xã hội (*slang*), ngôn ngữ tuổi teen (*teencode*), viết tắt cố ý và thay thế ký tự có dấu/không dấu nhằm vượt qua các cổng lọc từ khóa (*keyword filtering*) truyền thống của nhà mạng.

Cộng đồng nghiên cứu quốc tế và trong nước đã có nhiều nỗ lực ứng dụng Trí tuệ Nhân tạo vào bài toán này:
1. **Nguyen Tan Cam et al. (2026)** công bố tập dữ liệu thư rác tiếng Việt VNSED và thử nghiệm mô hình PhoBERT-base, nhưng kết quả cho thấy mô hình học sâu thông thường vẫn bỏ sót tỷ lệ lớn các tin nhắn độc hại tinh vi do hàm mất mát tiêu chuẩn đối xử bình đẳng giữa các lỗi nhầm lẫn.
2. **Y. H. Zhou et al. (2026)** trong công trình *FraudSMSWalker* đã khảo sát các mô hình ngôn ngữ lớn (LLMs) như GPT-4o, Claude và Gemini cho bài toán lừa đảo SMS; kết quả khẳng định rằng dù LLM có khả năng suy luận mạnh, nhưng Fraud Recall dao động thất thường ($64.16\%–90.13\%$) và độ trễ quá cao ($> 1.000\text{ ms}$), không thể triển khai trực tiếp trên điện thoại người dùng để lọc tin nhắn tức thời.
3. **Adel ElZemity et al. (2026)** đề xuất phương pháp chưng cất tri thức sang mô hình nhỏ (SLM) nhằm phát hiện lừa đảo tin nhắn trên thiết bị di động, nhưng chỉ dừng lại ở ngữ liệu tiếng Anh và chưa giải quyết được bài toán chi phí bất cân xứng của việc bỏ sót mối đe dọa.

**KHOẢNG TRỐNG NGHIÊN CỨU (GAP):**  
Trong các nghiên cứu đã công bố, **chưa có công trình nào đánh giá một mô hình ngôn ngữ chuyên biệt cho văn phong mạng xã hội tiếng Việt (ViSoBERT) kết hợp với cơ chế phạt lỗi bất cân xứng Cost-Sensitive Loss ($\alpha=5.0$)** để giải quyết triệt để bài toán bỏ lọt tin nhắn lừa đảo (*False Negative*) trong khi vẫn duy trì độ trễ suy luận thời gian thực ($\le 30\text{ ms}$) trên thiết bị người dùng. Đây chính là khoảng trống khoa học và công nghệ cấp thiết mà đề tài ScamShield-VN tập trung giải quyết.

---

## §3 Related Work (Bảng Tóm Tắt Theo Pattern)

| Nhóm tiếp cận (Pattern) | Các nghiên cứu tiêu biểu | Mô hình / Kỹ thuật | Dataset thực nghiệm | Hạn chế chung trỏ thẳng vào GAP |
| :--- | :--- | :--- | :--- | :--- |
| **Theme 1: Machine Learning truyền thống & Rule-based** | Ata & Alsmadi (2023), Saeed (2023), Xie (2025) | Naive Bayes, SVM, Random Forest, TF-IDF | SMS Spam Collection ($N \approx 5.500$) | Bị qua mặt dễ dàng bởi teencode, từ lóng mới nổi; không nắm bắt được ngữ cảnh chuỗi dài. |
| **Theme 2: Pre-trained Language Models tiếng Việt** | Vu Minh Tuan (2023), Nguyen-Xuan (2026), Nguyen Tan Cam (2026) | PhoBERT-base, FPT ViBERT, XLM-RoBERTa | VNSED, Vietnamese Social Corpus | Sử dụng Cross-Entropy loss tiêu chuẩn, dẫn đến tỷ lệ bỏ sót tin nhắn lừa đảo (*False Negative*) còn cao. |
| **Theme 3: LLM & On-Device Small Models** | Banda et al. (2026), Mrinal & Kumar (2026), Zhou et al. (2026), ElZemity (2026) | GPT-4o-mini, Gemini Flash, MobileBERT, Qwen2.5 | FraudSMSWalker, Edge Lures Corpus | Chi phí API cao hoặc chỉ thử nghiệm trên tiếng Anh; chưa có cơ chế phạt nhạy cảm chi phí cho tiếng Việt. |

> **Đoạn định vị:** *"Khác với các nghiên cứu trước đây chỉ tập trung vào tối ưu độ chính xác chung trên các mô hình tiếng Anh hoặc dùng BERT tiêu chuẩn trên tiếng Việt, đề tài này tích hợp cơ chế phạt lỗi bất cân xứng WBCE ($\alpha=5.0$) vào mô hình ViSoBERT nhằm đẩy tỷ lệ phát hiện lừa đảo (Scam Recall) lên trên $95\%$ mà vẫn đảm bảo độ trễ thời gian thực trên CPU Edge."*

---

## §4 Research Questions (Chốt Tại Đây)

> **CÂU HỎI NGHIÊN CỨU CỐT LÕI (RQ):**  
> *"Với bộ dữ liệu SMS tiếng Việt ($N=2,665$), mô hình đề xuất ViSoBERT kết hợp hàm mất mát Cost-Sensitive Weighted Binary Cross-Entropy ($\mathcal{L}_{\text{WBCE}}$, $\alpha=5.0$) khác các mô hình đối chứng (PhoBERT-base, FPT ViBERT, PhoBERT-large, Gemini 3.5 Flash) thế nào về chỉ số Scam Recall?"*

### Cặp Giả Thuyết Thống Kê & Kiểm Định:
* **$H_0$ (Giả thuyết không):** Không có sự khác biệt có ý nghĩa thống kê về tỷ lệ phân loại đúng giữa mô hình đề xuất ViSoBERT + WBCE ($\alpha=5.0$) và các mô hình baseline đối chứng trên cùng tập kiểm thử niêm phong Frozen Test Set ($p \ge 0.05$).
* **$H_1$ (Giả thuyết đối):** Có sự khác biệt có ý nghĩa thống kê về tỷ lệ phân loại đúng giữa mô hình đề xuất ViSoBERT + WBCE ($\alpha=5.0$) và các mô hình baseline đối chứng trên cùng tập kiểm thử niêm phong Frozen Test Set ($p < 0.05$).
* **Kiểm định thống kê được chọn:** **McNemar test hai phía** (kiểm định so sánh cặp phân loại nhị phân trên cùng $N=267$ mẫu kiểm thử).
* **Ngưỡng chấp nhận thực tiễn (Threshold $\theta$, Nguồn Case 2 & Case 3):**
  * $\text{Scam Recall} \ge 95.0\%$ (mức tối thiểu để đảm bảo an toàn cho người dùng cuối).
  * $\text{CPU Inference Latency} \le 30.0\text{ ms/tin nhắn}$.

---

## §5 Experiment Protocol (Đủ Để Người Khác Chạy Lại Độc Lập)

### 5.1 Mô hình & Cấu hình Phiên bản:
* **Mô hình đề xuất:** `uitnlp/visobert` (Base architecture: RoBERTa-based, 12 layers, 768 hidden, 12 heads, 110M params, pre-trained on 60GB Vietnamese social media corpus).
* **Baselines đối chứng:**
  * B2.1: `vinai/phobert-base-v2` (135M params).
  * B2.2: `FPTAI/vibert-base-cased` (124M params).
  * B2.3: `vinai/phobert-large` (370M params).
  * B3: `Gemini 3.5 Flash` (Cloud LLM API, temperature = 0.0, 5-shot In-Context Learning).
* **Hyperparameters huấn luyện:** Batch size = 16, Learning rate = $2\times 10^{-5}$ (AdamW, weight decay = 0.01), Epochs = 4, Linear warmup = 0.1, FP16 enabled.
* **Hàm mất mát:** Cost-Sensitive Weighted Binary Cross-Entropy Loss:
$$\mathcal{L}_{\text{WBCE}} = -\frac{1}{N} \sum_{i=1}^{N} \left[ \alpha \cdot y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right], \quad \text{với } \alpha = 5.0$$

### 5.2 Prompt Nguyên Văn Cho Baseline LLM (Gemini 3.5 Flash):
```text
Bạn là chuyên gia an ninh mạng phân tích tin nhắn lừa đảo tiếng Việt.
Nhiệm vụ: Phân loại tin nhắn sau đây là "SCAM" (Lừa đảo, mạo danh ngân hàng, dụ dỗ tài chính, spam độc hại) hoặc "HAM" (Tin nhắn bình thường, thông báo hợp lệ).

Dưới đây là 5 ví dụ mẫu (5-shot):
Ví dụ 1: "Vietcombank tran trong thong bao: Tai khoan cua quy khach da bi khoa, vui long truy cap https://vcb-digibank-login.com de xac thuc ngay." -> SCAM
Ví dụ 2: "Bo Y te khuyen cao nguoi dan thuc hien bien phap 2K de phong chong dich benh mua dong xuan." -> HAM
Ví dụ 3: "Chuc mung ban da trung thuong xe SH, lien he Zalo 0987xxx de lam thu tuc nhan thuong phi 500k." -> SCAM
Ví dụ 4: "Ma OTP cua ban la 584920. Ma co hieu luc trong 3 phut. Khong chia se ma nay cho bat ky ai." -> HAM
Ví dụ 5: "Tuyen CTV xem video TikTok kiem 500k/ngay, khong can von, inbox ngay." -> SCAM

Tin nhắn cần phân tích:
"""{text}"""

Chỉ trả về DUY NHẤT một từ: "SCAM" hoặc "HAM". Không giải thích gì thêm.
```

### 5.3 Dữ Liệu & Quy Trình Xử Lý:
* **Tổng số dữ liệu hợp nhất:** $2.665$ tin nhắn SMS và tin nhắn văn bản tiếng Việt thực tế.
* **Tỷ lệ phân bổ:** Phân tách phân tầng cố định (*Stratified Split*) với seed = 42:
  * Tập Huấn luyện & Đánh giá nội bộ ($90\%$): $2.398$ mẫu.
  * **Tập Kiểm thử Đóng băng (Frozen Test Set, $10\%$):** **$N = 267$ mẫu** ($192$ tin nhắn Ham hợp lệ, $75$ tin nhắn Scam lừa đảo).
* **Quy tắc niêm phong:** Tập Frozen Test Set được cô lập hoàn toàn, không được dùng để điều chỉnh ngưỡng threshold hoặc huấn luyện.

### 5.4 Gán Nhãn & Độ Đồng Thuận (IAA):
* Dữ liệu ban đầu được gắn nhãn độc lập bởi 2 kỹ sư an ninh thông tin.
* Độ đồng thuận giữa người gán nhãn đạt **Cohen's $\kappa = 0.88$** ($\ge 0.80$, mức rất cao). Các mẫu bất đồng được chuyên gia thứ ba phân xử dứt điểm.

### 5.5 Tính Không Tất Định & Số Lần Chạy Lặp ($K=5$):
* Để kiểm soát tính ngẫu nhiên và đảm bảo tính tái lập 100%, toàn bộ các mô hình Deep Learning đều được **chạy thực nghiệm lặp lại 5 lần độc lập (5 Runs)** với 5 seed cố định:  
  $$\text{SEEDS} = [42, 100, 123, 999, 2026]$$
* Báo cáo kết quả chính thức bằng **$Mean \pm Std$** và trung vị.

### 5.6 Thứ Tự Chạy & Batching:
* Chạy theo batch 16 mẫu; lưu checkpoint sau mỗi epoch.
* Toàn bộ output dự đoán được ghi log chi tiết từng dòng kèm timestamp.

### 5.7 Đạo Đức Nghiên Cứu:
* Toàn bộ dữ liệu tin nhắn cá nhân (số điện thoại thực, họ tên riêng, mã số tài khoản ngân hàng cụ thể) đã được làm sạch và ẩn danh hóa hoàn toàn (*Anonymized*). Không có đối tượng người tham gia thử nghiệm trực tiếp $\rightarrow$ Đạt chuẩn đạo đức nghiên cứu.

---

## §6 Evaluation Plan (Kế Hoạch Đánh Giá & Thống Kê)

* **Tiêu chí bác bỏ $H_0$:** $p$-value của kiểm định McNemar test $< 0.05$.
* **Tiêu chí chấp nhận thực tiễn:** Mô hình đề xuất phải đạt Scam Recall $\ge 95.0\%$ đồng thời duy trì Macro-F1 $\ge 90.0\%$.
* **Cỡ mẫu & Statistical Power:** Tập Frozen Test Set có $N=267$ mẫu. Với mức ý nghĩa $\alpha=0.05$ và độ chênh lệch tỷ lệ phát hiện kỳ vọng $\ge 3\%$, cỡ mẫu $N=267$ bảo đảm **Statistical Power $> 0.85$** (tính toán bằng thư viện `statsmodels.stats.power`), đủ độ mạnh để phát hiện khác biệt thực sự mà không bị lỗi Loại II.
* **Quy tắc xử lý kết quả âm tính:** Nếu ViSoBERT không vượt qua PhoBERT-large có ý nghĩa thống kê ($p \ge 0.05$), nhóm vẫn báo cáo trung thực kết quả này trong $\S 4$ và phân tích luận điểm chi phí/tài nguyên trong $\S 5$ (chứng minh ViSoBERT nhẹ hơn $3.8\times$ nhưng hiệu năng tương đương).

---

## §7 Threats to Validity (Các Mối Đe Dọa Giá Trị & Hành Động Giảm Thiểu)

| Mối đe dọa | Bản chất rủi ro | Hệ quả tiềm tàng | Hành động giảm thiểu cụ thể (*Mitigation Action*) |
| :--- | :--- | :--- | :--- |
| **7.1 Internal Validity** | Tính không tất định của quá trình khởi tạo trọng số ngẫu nhiên khi huấn luyện. | Kết quả đo đạc chỉ là ngẫu nhiên may mắn của một lần chạy. | Thực hiện **5 runs thực nghiệm độc lập** với 5 seed cố định ($42, 100, 123, 999, 2026$); báo cáo cả Mean, Std và kiểm định McNemar. |
| **7.2 External Validity** | Dữ liệu chỉ giới hạn ở tin nhắn SMS tiếng Việt, chưa bao quát toàn bộ email hay nền tảng khác. | Khả năng tổng quát hóa ra ngoài phạm vi bị hạn chế. | Nêu rõ ranh giới nghiên cứu trong $\S 6$; kiểm tra chéo trên cả mẫu SMS viễn thông và tin nhắn mạng xã hội OTT. |
| **7.3 Construct Validity** | Nguy cơ rò rỉ dữ liệu (*Data Contamination*) giữa tập train và test. | Mô hình bị học vẹt (*overfitting*), thổi phồng độ chính xác. | Thực hiện deduplication nghiêm ngặt trước khi split; niêm phong tập Frozen Test Set ($N=267$) độc lập 100%. |
| **7.4 Conclusion Validity** | Cỡ mẫu kiểm thử $N=267$ có thể không đủ mạnh nếu không kiểm tra giả định. | Rủi ro sai số Loại I hoặc Loại II trong kết luận. | Báo cáo chi tiết $p$-value chính xác kèm **Effect Size** (Odds Ratio / Risk Difference) và khoảng tin cậy $95\%\text{ CI}$. |

---

## §8 Timeline, Phân Công Trách Nhiệm và Chi Phí API

### Bảng Phân Công Viết Paper & Nghiệm Thu:
| Giai đoạn | PL (Hiếu) | DG (Trân) | LR (Hiếu/Quang) | MS (Phúc) | RW (Huy) | Mốc nghiệm thu |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **GĐ2 (Mốc 4)** | Nộp Proposal, điều phối | Kiểm tra format dataset | Viết script benchmark | Viết metric script | Soạn Slide đề cương | **Duyệt Proposal** |
| **GĐ3 (Pilot)** | Ghi `notes.md` | Chuẩn bị sample pilot | Chạy pilot, viết $\S 3.1–3.2$ | Phân tích pilot, viết $\S 3.3–3.4$ | Viết $\S 1$ Intro | **Nghiệm thu Pilot** |
| **GĐ4 (Full)** | Soát mạch lập luận $\S 5$ | Gán nhãn kiểm tra | Chạy full 5 runs | Phân tích thống kê, viết $\S 4$ | Tạo Figures, viết $\S 6$ | **Chốt kết quả $\S 4–\S 6$** |
| **GĐ5 (Final)** | Viết Abstract, Review tổng | Cập nhật $\S 2$ | Cập nhật $\S 3$ | Cập nhật $\S 4–\S 5$ | Viết $\S 7$, Format IEEE | **Nộp Paper + Slide** |

### Dự Toán Chi Phí API (Kèm Buffer 20%):
* **Mô hình On-Device (ViSoBERT, PhoBERT, ViBERT):** Chạy trên GPU/CPU cục bộ $\rightarrow$ **Chi phí: $0.00\text{ USD}$**.
* **Mô hình Cloud LLM (Gemini 3.5 Flash / GPT-4o-mini baseline):**
  * Số lượng mẫu kiểm thử: $N = 267$ mẫu.
  * Số lần chạy: 1 lần kiểm thử chính thức (temperature = 0).
  * Trung bình Token vào: $450\text{ tokens/mẫu}$; Token ra: $5\text{ tokens/mẫu}$.
  * Đơn giá Gemini Flash: Miễn phí trong hạn mức Google AI Studio ($15\text{ RPM}$).
  * Chi phí dự phòng trường hợp dùng OpenAI API (`gpt-4o-mini`):
$$\text{Chi phí} = [267 \times (450 \times 0.15/1\text{M} + 5 \times 0.60/1\text{M})] \times 1.2 = [267 \times (0.0000675 + 0.000003)] \times 1.2 \approx 0.023\text{ USD}$$
* 👉 **Tổng ngân sách nghiên cứu thực tế:** Hoàn toàn nằm trong ngưỡng **$0.00\text{ USD} – 5.00\text{ USD}$**, đáp ứng tiêu chuẩn an toàn cao nhất của RBL.
