# 📅 TỪNG GIAI ĐOẠN NGHIÊN CỨU (GIAI ĐOẠN 1 – GIAI ĐOẠN 5)

---

## GIAI ĐOẠN 1: Tìm Tài Liệu Cho RQ (RBL-1)
> **Khẩu hiệu:** Mỗi người một nguồn – Gộp nhóm – Bản đồ bằng chứng.  
> **Mục tiêu:** Cuối giai đoạn 1 mỗi người có evidence table từ nguồn mình phụ trách, cả nhóm có evidence table gộp, PRISMA nhóm và bản đồ bằng chứng (`rq-evidence-map.md`) cho RQ đã thống nhất với GVHD.

### 1. Khi Gặp GVHD
* **PL tạo repo GitHub (Private, thêm GVHD làm collaborator)**, chia vai, chia nguồn tìm kiếm; PL chốt RQ của đề tài với GVHD (tab RQ của đề tài), thử khả thi xong ngay đầu giai đoạn.
* Thực hành viết tiêu chí IC/EC và search string; dùng Rayyan hoặc pandas để bỏ trùng.
* Họp nhóm cuối giai đoạn: gộp evidence table, viết PRISMA nhóm và bản đồ bằng chứng P/I/C/O, phân công kiểm phản chứng.

### 2. Việc Nhóm Tự Làm (Checklist Mốc 1–5)
* [ ] **Mốc 1:** PL chia nguồn và viết `team-synthesis/ie_criteria.md` dùng chung (IC-P, IC-I lấy từ PICO của RQ); String A = search string trên thẻ RQ; ghi `search-log.md` (query nguyên văn, cơ sở dữ liệu, ngày, số kết quả).
* [ ] **Mốc 2–3:** Mỗi người tìm trên nguồn của mình, cả nhóm phủ 2–3 cơ sở dữ liệu; paper dẫn chứng trên thẻ RQ đưa vào như record thường; bỏ trùng $\rightarrow$ lưu `01_all_records.csv`.
* [ ] **Mốc 3–4:** Sàng lọc 2 vòng (title/abstract rồi full-text) $\rightarrow$ `02_after_screening_v1.csv`, `03_final_included.csv`; số trong `prisma-flow.md` phải khớp số dòng CSV.
* [ ] **Mốc 4–5:** Điền `evidence-table.md` (Paper, Tool/LLM, Dataset, Metric, Kết quả, Code, Hạn chế, Gần RQ); mỗi người $\ge 6$ paper included.
* [ ] **Mốc 5:** Người thứ hai kiểm 20% số paper đã loại của bạn (double screening) và ghi mức đồng thuận.
* [ ] **Cuối giai đoạn:** PL gộp $\rightarrow$ `team-synthesis/evidence-table-merged.md` ($\ge 12$ paper) + `prisma-team.md`; cả nhóm viết `rq-evidence-map.md` và liệt kê ứng viên phản chứng.

### 3. Quy Định Dùng AI & Lỗi Hay Gặp
* **Dùng AI:** Được dùng AI gợi ý từ khóa và tóm tắt. Mọi trích dẫn phải mở nguồn thật kiểm lại; evidence table không có ô N/A nào là dấu hiệu bịa số liệu.
* **Lỗi hay gặp:**
  * Chép abstract vào evidence table thay vì đọc Table/Figure.
  * Số PRISMA không khớp file CSV.
  * Chép thẳng paper dẫn chứng trên thẻ RQ vào danh sách included mà không screening.

### 4. Sản Phẩm Nộp Cuối GĐ1 & Cổng Kiểm
* **Sản phẩm nộp (D1):**
  * `[member]/SLR/`: `search-log.md`, `01_all_records.csv`, `02_after_screening_v1.csv`, `03_final_included.csv`, `prisma-flow.md`, `evidence-table.md`.
  * `team-synthesis/`: `ie_criteria.md`, `evidence-table-merged.md`, `prisma-team.md`, `rq-evidence-map.md` (kèm ứng viên phản chứng).
* **Cổng kiểm (Đạt hết mới sang tuần sau):**
  * [x] Số trong PRISMA khớp số dòng thực tế trong CSV.
  * [x] Mỗi paper có DOI hoặc URL; cột Kết quả $\ge 50\%$ hàng có con số thật.
  * [x] Evidence table gộp $\ge 12$ paper; PRISMA nhóm khớp bảng gộp.
  * [x] Mỗi yếu tố P/I/C/O có ít nhất 1 paper làm nền hoặc ghi rõ chưa có.
  * [x] Cả nhóm dưới 12 paper: báo GVHD ngay để chỉnh search string hoặc đổi RQ trước khi khóa.

---

## GIAI ĐOẠN 2: Kiểm Chứng RQ & Proposal (RBL-2, RBL-3)
> **Mục tiêu:** Nộp proposal ("hợp đồng nghiên cứu") theo mốc GVHD đặt, rồi bảo vệ đề cương và được GVHD duyệt chậm nhất hết GĐ2: RQ, $H_0/H_1$, threshold, baseline, protocol, kế hoạch thống kê.

### 1. Khi Gặp GVHD
* **Mốc 1:** Mỗi người trình bày `rq-check` (phản chứng trên nguồn của mình); cả nhóm chốt nhãn tính mới và khả thi; đổi I/C nếu cần trước khi GVHD chốt RQ (đầu GĐ2).
* Chốt 7 yếu tố thiết kế: dataset, LLM/tool, metric, threshold, baseline, pipeline, kiểm định.
* Chọn kiểm định theo kiểu dữ liệu và ghép cặp / độc lập.

### 2. Việc Nhóm Tự Làm (Checklist Mốc 1–5)
* [ ] **Mốc 1 (Cá nhân):** `SLR/rq-check.md`: bảng phản chứng P/I/C/O cho ứng viên từ nguồn của mình + lớp tìm kiếm bổ sung được phân công (L1, L2, L3).
* [ ] **Mốc 2:** PL tổng hợp `team-synthesis/rq-validation.md` (5 cổng dữ liệu P1–P5, phản chứng, nhãn tính mới, khả thi 7 tiêu chí, phát biểu khoảng trống RQ lấp); ngưỡng Case 3 thì chạy mini-pilot 5–10 mẫu.
* [ ] **Mốc 3–4:** Viết `proposal.md` đủ 8 mục; $\S 5$ có model version, prompt nguyên văn, dataset đã tải thử, danh sách mục pilot và tập chính thức (không trùng nhau), quy trình gán nhãn và ngưỡng IAA, số lần chạy lặp.
* [ ] **Kỹ thuật trước GĐ3:** DG tải dataset vào `data/raw/` và kiểm format; LR chạy `test_api.py`; MS chạy `compute_metric.py` trên dữ liệu giả (Gate E2–E4).
* [ ] **Mốc 4:** Làm slide bảo vệ đề cương 6–8 slide, 5–7 phút (`presentation/slides_proposal.pptx` + `.pdf`); nộp `proposal.md` + slide cho GVHD hết mốc 4.
* [ ] **Mốc 5:** Bảo vệ đề cương; GVHD duyệt hoặc yêu cầu sửa ngay buổi đó; sửa nhỏ nộp lại trong ngày (duyệt chậm nhất hết GĐ2).

### 3. Quy Định Dùng AI & Lỗi Hay Gặp
* **Dùng AI:** Được dùng AI soạn slide; kiểm lại từng số liệu và tên paper. Threshold không được tự đặt *"cho hợp lý"* khi chưa có nguồn hoặc mini-pilot.
* **Lỗi hay gặp:**
  * Threshold không có nguồn.
  * $H_0$ viết theo ngưỡng tuyệt đối trong khi kiểm định lại so sánh hai điều kiện (McNemar/Wilcoxon) $\rightarrow H_0$ và kiểm định lệch nhau.
  * Proposal thiếu phần gán nhãn/IAA nên kẹt ở Gate E5.

### 4. Sản Phẩm Nộp Cuối GĐ2 & Cổng Kiểm
* **Sản phẩm nộp (D2):**
  * `SLR/rq-check.md` của từng người.
  * `team-synthesis/rq-validation.md` + `team-synthesis/proposal.md` (version 1.0).
  * `presentation/slides_proposal.pdf`.
* **Cổng kiểm:**
  * [x] Có bảng phản chứng P/I/C/O với từng paper cụ thể và nhãn tính mới có lý do; không có mục khả thi ❌ (hoặc đã có kế hoạch downscope).
  * [x] $\S 2$ nêu $\ge 3$ paper theo tên; $\S 4$ RQ đủ P/I/C/O có giá trị cụ thể; $H_0/H_1$ khớp với kiểm định đã chọn.
  * [x] Threshold có nguồn theo Case 1/2/3; kiểm định đã chọn (không để TBD) và đúng với dữ liệu ghép cặp hay độc lập.
  * [x] $\S 7$ mỗi threat có mitigation là hành động cụ thể; $\S 8$ chi phí API tính cả token đầu ra.
  * [x] **GVHD duyệt xong hết GĐ2; chưa duyệt $\rightarrow$ Kích hoạt Downscope: chỉ làm RQ1.**

---

## GIAI ĐOẠN 3: Pilot & Viết §1–§3 Song Song (RBL-4 Pilot, RBL-5a)
> **Mục tiêu:** Chạy thử trên các mục pilot đã ghi trong proposal để bắt lỗi kỹ thuật trước khi chạy tập chính thức; trong lúc chờ, viết các phần không phụ thuộc kết quả (§1–§3).

### 1. Khi Gặp GVHD
* **Mốc 1:** Kiểm 7 Gates bắt buộc E1–E7 (E1: Proposal đã được duyệt).
* **Họp pilot cuối mốc 3:** Xem histogram phân phối metric, xác nhận lại kiểm định.
* **Ra quyết định sau pilot (8.4):** Scale full experiment, sửa nhỏ trong ngày, hay viết amendment xin đổi thiết kế.

### 2. Việc Nhóm Tự Làm
* [ ] **DG:** Lấy đúng các mục pilot đã ghi trong proposal $\rightarrow$ `data/pilot_sample.csv`; không lấy mục của tập chính thức. Gán nhãn `pilot_ground_truth.csv` (nếu cần), tính IAA (Cohen's $\kappa \ge 0.7$ mới đi tiếp). Viết $\S 2$ Related Work.
* [ ] **LR:** Chạy `run_experiment.py` đúng cấu hình proposal; log từng call (timestamp, response.model, cost) $\rightarrow$ `results/pilot_api_log.txt`. Viết $\S 3.1–\S 3.2$ Dataset & Pipeline.
* [ ] **MS:** Chạy `results/pilot_analysis.ipynb`: tính metric, vẽ histogram, xác nhận kiểm định. Viết $\S 3.3–\S 3.4$ Metric & Stats.
* [ ] **RW:** Viết $\S 1$ Introduction trên Overleaf.
* [ ] **PL:** Ghi `notes.md`: quyết định kỹ thuật và error log.

### 3. Quy Định Dùng AI & Lỗi Hay Gặp
* **Dùng AI:** Giữ nguyên đầu ra gốc của LLM. Không dùng chính LLM đang thử nghiệm để chấm kết quả của nó. $\text{LR} \neq \text{MS}$.
* **Lỗi hay gặp:**
  * Chọn mẫu pilot *"dễ"* thay vì ngẫu nhiên.
  * Sửa prompt giữa chừng mà không làm amendment.
  * Điền số *"hợp lý"* khi API lỗi.

### 4. Sản Phẩm Nộp Cuối GĐ3 & Cổng Kiểm
* **Sản phẩm nộp (D3):**
  * `data/pilot_sample.csv` (+ `pilot_ground_truth.csv` nếu có).
  * `results/pilot_*`, `notes.md`.
  * Bản thảo `paper/sections/01-03.tex`.
* **Cổng kiểm:**
  * [x] Pipeline chạy đúng, output rỗng $\le 20\%$.
  * [x] IAA đạt ngưỡng ghi trong proposal ($\kappa \ge 0.7$).
  * [x] Metric tính được; nếu không: báo GVHD và viết amendment trong 24 giờ.
  * [x] Không đổi model version hoặc prompt nếu chưa có amendment được duyệt.

---

## GIAI ĐOẠN 4: Thực Nghiệm Đầy Đủ & Viết Kết Quả §4–§6 (RBL-4 Full, RBL-5a)
> **Mục tiêu:** Chạy toàn bộ dữ liệu đúng proposal, kiểm định thống kê, tính effect size, kết luận từng RQ và viết phần kết quả (§4 Results, §5 Discussion, §6 Threats).

### 1. Khi Gặp GVHD
* Họp kiểm tra giữa giai đoạn: đối chiếu $\S 4$ và $\S 6$ của proposal.
* Xử lý lỗi API (retry với exponential backoff $2^{\text{attempt}} + \text{jitter}$) và các lệch protocol.
* Review chéo nhanh bản nháp $\S 1–\S 3$.

### 2. Việc Nhóm Tự Làm
* [ ] **LR:** Chạy full experiment cùng cấu hình như pilot; chạy lặp theo kế hoạch; commit sau mỗi batch lớn; log `results/full_api_log.txt` và lưu `results/full_llm_output.csv`.
* [ ] **DG:** Gán nhãn toàn bộ `data/full_ground_truth.csv` (nếu cần), kiểm tra IAA đạt ngưỡng.
* [ ] **MS:** Chạy `results/full_analysis.ipynb`: tính metric, kiểm định ($\alpha = 0.05$, hiệu chỉnh nếu nhiều kiểm định), effect size; ghi `results/summary.csv` (metric, p-value chính xác, effect size, N) và lọc dòng lỗi vào `results/excluded.csv`. Viết $\S 4$ Results.
* [ ] **PL + MS:** Viết $\S 5$ Discussion (phân tích 10–20 case sai nhất, so sánh prior work, implications).
* [ ] **RW:** Tạo $\ge 2$ figures ($\ge 300\text{ DPI}$, boxplot/comparison); viết $\S 6$ Threats to Validity; thêm citation vào `references.bib` (mỗi entry có DOI).

### 3. Quy Định Dùng AI & Lỗi Hay Gặp
* **Dùng AI:** AI chỉ hỗ trợ; văn bản AI viết nguyên văn là vi phạm. Copy nguyên câu của paper khác dù có `\cite` vẫn là đạo văn (phải diễn giải hoặc để ngoặc kép).
* **Lỗi hay gặp:**
  * **HARKing:** đổi test, metric hoặc threshold sau khi thấy dữ liệu.
  * Chỉ báo $p$-value mà thiếu effect size và $95\%\text{ CI}$.
  * Không tính riêng tỷ lệ `INVALID`.

### 4. Sản Phẩm Nộp Cuối GĐ4 & Cổng Kiểm
* **Sản phẩm nộp (D4):**
  * `results/full_llm_output.csv` + `results/full_api_log.txt` + `results/full_analysis.ipynb` + `results/summary.csv`.
  * `figures/` ($\ge 2$ hình $\ge 300\text{ DPI}$).
  * Bản thảo `paper/sections/04-06.tex`.
* **Cổng kiểm:**
  * [x] Số mẫu và cấu hình đúng proposal; mọi lệch được ghi deviation.
  * [x] `full_analysis.ipynb` chạy lại từ đầu không lỗi (Restart & Run All).
  * [x] Kết quả thấp hơn threshold vẫn báo cáo trung thực: không đổi threshold, không thêm RQ, không chọn subset đẹp; phân tích ngoài kế hoạch phải gắn nhãn **exploratory**.
  * [x] Mỗi RQ ở $\S 4$ có metric, $p$-value chính xác, effect size và $N$ sau khi bỏ invalid.

---

## GIAI ĐOẠN 5: Hoàn Thiện, Kiểm AI & Trình Bày (RBL-5a, RBL-5b)
> **Mục tiêu:** Nộp paper cuối (6–8 trang IEEE/ACM), slide trình bày (9 slides, 10–12 phút) và repo GitHub đầy đủ; mọi thành viên bảo vệ được toàn bộ nghiên cứu.

### 1. Khi Gặp GVHD
* Trình bày 10–12 phút theo phân công; mỗi thành viên trả lời phần mình viết.
* Câu hỏi thường gặp: *Vì sao dataset này? Vì sao metric này? Kết quả âm tính nghĩa là gì? Nếu làm lại sẽ đổi gì?*

### 2. Việc Nhóm Tự Làm
* [ ] **Mốc 1:** RW viết $\S 7$ Conclusion (future work cụ thể); PL viết **Abstract** sau cùng (5 câu vàng, có số thực chứng).
* [ ] **Mốc 1–2:** PL review tổng thể, sửa nhất quán số liệu giữa Abstract – $\S 4$ – $\S 5$.
* [ ] **Mốc 2–3:** Chạy **AI Writing Check** ($\ge 2$ công cụ: SciSpace, ZeroGPT, Copyleaks, GPTZero) để khoanh vùng đoạn cần đọc lại; ghi `paper/quality/ai_check_log.md`; kiểm tra citation và đạo văn (Turnitin/iThenticate).
* [ ] **Sửa văn phong:** Viết lại đoạn được đánh dấu theo quy trình 4 bước; kiểm citation density và số liệu.
* [ ] **Mốc 3–4:** Làm `presentation/slides_final.pptx` + `.pdf`, rehearse $\ge 1$ lần; tải project Overleaf (Source) commit vào GitHub repo.

### 3. Sản Phẩm Nộp Cuối GĐ5 & Cổng Kiểm
* **Sản phẩm nộp (D5):**
  * `paper/output/paper_final.pdf` + LaTeX source.
  * `presentation/slides_final.pptx` + `slides_final.pdf`.
  * `paper/quality/ai_check_log.md`.
  * Repo GitHub đủ commit history từ RBL-1 đến RBL-5, README hướng dẫn reproduce.
* **Cổng kiểm:**
  * [x] Mọi số trong Abstract, $\S 4$, $\S 5$ khớp nhau và khớp notebook.
  * [x] Đoạn được công cụ đánh dấu đã được đọc lại và viết lại nếu máy móc; không dùng riêng % làm căn cứ kết luận.
  * [x] Repo không có API key, `.env`, file $> 100\text{ MB}$; `data/raw/` có README nguồn và license.
  * [x] `paper_final.pdf` compile được; 6–8 trang không tính References.
