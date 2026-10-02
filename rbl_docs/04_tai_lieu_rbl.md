# 📘 BỘ TÀI LIỆU HƯỚNG DẪN CHI TIẾT RBL (RBL-1 ĐẾN RBL-5B)

---

## 1. Thiết Lập GitHub Repo & Quy Chuẩn Bảo Mật

* **Tên repo:** `RT-[mã đề tài CP]-[ten-nhom]` (Ví dụ: `RT-ScamShield-nhom1`). **Visibility: Private**.
* **Collaborators:** Thêm toàn bộ thành viên nhóm và **email của GVHD** để theo dõi tiến độ.
* **Quy tắc `.gitignore` bắt buộc (Tuyệt đối không commit API keys, secrets, dữ liệu > 100MB):**

```gitignore
# API keys & secrets: TUYỆT ĐỐI không commit
.env
*.env
secrets.json
api_key.txt
config.py

# Python cache & virtual environments
__pycache__/
*.pyc
.venv/
venv/
.ipynb_checkpoints/

# OS files
.DS_Store
desktop.ini
Thumbs.db

# File lớn (thêm nếu data > 100MB)
data/raw/*.csv
data/raw/*.bin
models/*.onnx
models/*.safetensors
```

### Template `README.md` Ban Đầu:
```markdown
# [Tên đề tài ngắn gọn]
**Topic:** RT-[mã đề tài CP]
**Môn:** Research-Based Learning (RBL) / Capstone Project
**Nhóm:** [Tên nhóm] — [Học kỳ, năm]
**Thành viên:** Nguyễn Văn A (PL), Trần Thị B (DG), Lê Văn C (LR), Phạm Văn D (MS), Hoàng Văn E (RW)
**GVHD hướng dẫn:** [Tên GVHD]

## Tiến độ
- [ ] RBL-1: Tìm paper (Giai đoạn 1)
- [ ] RBL-2 + RBL-3: Kiểm chứng RQ, Proposal (Giai đoạn 2)
- [ ] RBL-4: Pilot (Giai đoạn 3), Thực nghiệm đầy đủ (Giai đoạn 4)
- [ ] RBL-5: Báo cáo và trình bày (Giai đoạn 3–5)
```

### Quy Tắc Commit Message Chuẩn:
| Khi nào | Format commit |
| :--- | :--- |
| Xong một bước trong RBL | `[RBL-1A] add evidence-table - nguyen-van-a` |
| Cuối mỗi giai đoạn | `[Phase 1] merge evidence tables + evidence map` |
| Sau pilot | `[RBL-4] pilot done - N=50, kappa=0.82` |
| Sau full experiment | `[RBL-4] full experiment - N=500, p=0.003` |
| Sửa lỗi nhỏ | `[fix] correct typo in proposal §4` |

---

## 2. Cấu Trúc Thư Mục Chuẩn Toàn Dự Án

```
[ten-nhom]/                                 <- Root = GitHub repo (Private)
├── [member-A]/SLR/                         <- [RBL-1] papers/, search-log.md, 01_all_records.csv,
│                                              02_after_screening_v1.csv, 03_final_included.csv,
│                                              prisma-flow.md, evidence-table.md
│                                              [RBL-2] rq-check.md
├── [member-B]/SLR/                         <- Mỗi thành viên một thư mục, tên thật không dấu
├── team-synthesis/                         <- ie_criteria.md, evidence-table-merged.md, prisma-team.md,
│                                              rq-evidence-map.md [RBL-1]; rq-validation.md [RBL-2]; proposal.md [RBL-3]
├── data/                                   <- raw/ (KHÔNG sửa, kèm README nguồn+license), pilot_sample.csv,
│                                              pilot_ground_truth.csv, full_ground_truth.csv [RBL-4]
├── scripts/                                <- test_api.py, run_experiment.py, compute_metric.py [RBL-4]
├── results/                                <- pilot_llm_output.csv, pilot_api_log.txt, pilot_analysis.ipynb,
│                                              full_llm_output.csv, full_api_log.txt, full_analysis.ipynb,
│                                              summary.csv, excluded.csv
├── figures/                                <- fig1_distribution.png, fig2_comparison.png (>= 300 DPI)
├── paper/                                  <- main.tex, references.bib, sections/00-07*.tex, figures/,
│                                              output/paper_final.pdf, quality/ai_check_log.md [RBL-5]
├── presentation/                           <- slides_proposal.pptx/.pdf [RBL-3], slides_final.pptx/.pdf [RBL-5]
└── notes.md                                <- Mọi quyết định kỹ thuật + error log [RBL-4]
```

---

## 3. RBL-1 · Tìm Paper Cho RQ, Gộp Nhóm, Bản Đồ Bằng Chứng

### Khái Niệm 4 Lần Chạy Thực Nghiệm:
1. **① Thử khả thi (Lúc chốt RQ, GĐ1):** Chạy trên 1 mục bất kỳ để biết RQ làm được (tải được dữ liệu, chạy được 1 prompt/model). Không đo số liệu.
2. **② Mini-pilot (GĐ2, chỉ khi Threshold thuộc Case 3):** Chạy 5–10 mẫu pilot để tìm ngưỡng $\theta$ ghi vào proposal. Có đo để đặt $\theta$.
3. **③ Pilot (GĐ3, sau khi Proposal được duyệt):** Chạy toàn bộ mẫu pilot theo cấu hình proposal để bắt lỗi kỹ thuật. Có đo nhưng không đưa vào paper.
4. **④ Chạy thật (GĐ4):** Chạy toàn bộ tập chính thức đã niêm phong. Cho ra kết quả chính thức và kiểm định $H_0/H_1$.

> [!IMPORTANT]
> **Tập chính thức = Đề thi niêm phong.** Nhóm chia dữ liệu thành 2 phần không trùng nhau: mục pilot (5–10 mục) và tập chính thức. Chỉ chạy tập chính thức khi đã chốt xong prompt, model, ngưỡng, cách tính metric.  
> **Cách chọn mẫu:** Bốc ngẫu nhiên với seed cố định (`random.seed(42)`).

---

## 4. RBL-2 · Kiểm Chứng RQ (5 Cổng, Phản Chứng, Khả Thi)

### Bước 1: Kiểm Tra Evidence Table (5 Cổng P1–P5)
* **P1:** $\ge 12$ paper included (mức tối thiểu của bảng gộp).
* **P2:** Cột `Tool/LLM` $\ge 90\%$ hàng có dữ liệu.
* **P3:** Cột `Kết quả` $\ge 50\%$ hàng có con số cụ thể.
* **P4:** Cột `Hạn chế` $\ge 50\%$ hàng có dữ liệu.
* **P5:** Cột `Metric` ghi tên cụ thể (không ghi "accuracy" chung chung).

### Bước 2: Kiểm Tra Phản Chứng Bắt Buộc (So 4 Yếu Tố P/I/C/O)
* **0/4 yếu tố giống:** Không phản chứng $\rightarrow$ Dùng làm nền cho RQ.
* **3/4 yếu tố giống:** **Mở rộng (Extension)** $\rightarrow$ Giữ RQ, ghi rõ khác ở yếu tố nào (đóng góp của nhóm).
* **4/4 yếu tố giống:** **Tái hiện (Replication)** $\rightarrow$ Báo PL & GVHD để đổi $I$ hoặc $C$ trước khi khóa RQ.

### 3 Lớp Tìm Kiếm Bổ Sung (Nếu $N_{\text{included}} < 10$):
* **L1:** Search thẳng vào RQ: `"[can thiệp I]" AND "[task P]" AND "[metric O]"` trên Google Scholar & IEEE.
* **L2:** Vào Semantic Scholar, lấy paper mới nhất trong tập included, xem 10–15 paper cite nó.
* **L3:** Tìm 1 bài Survey/SLR về chủ đề (`"systematic review" AND [topic]`, từ 2023).

### Bước 3: Rà Khả Thi (7 Tiêu Chí) & Downscope Protocol
| Tiêu chí | 🟢 An toàn | 🟡 Cần xử lý | 🔴 Không làm được |
| :--- | :--- | :--- | :--- |
| **Dataset** | Public, tải được ngay | Cần crawl $< 1$ tuần | Phải thu thập $> 1$ tháng |
| **API/Tool** | Free tier đủ cho $N$ | Cần trả $\le \$5$ tổng | Cần license đặc biệt |
| **Tính toán** | CPU laptop hoặc Colab T4 | GPU: Kaggle/Colab free | Cần cluster riêng |
| **Ground truth** | Có sẵn hoặc không cần | Gán nhãn tay $\le 5$ giờ cả nhóm | Cần domain expert / $> 20$ giờ |
| **Code base** | Paper liên quan có repo GitHub | Có nhưng framework cũ | Không có, phải code từ đầu |
| **Kỹ năng** | Thư viện sẵn có | Cần học thêm $< 1$ tuần | Cần kiến thức research-level |
| **Thời gian** | Xong với $\ge 3$ ngày dự phòng | Xong nhưng tight | Không đủ thời gian |

> **Quyết định:** Có bất kỳ 🔴 $\rightarrow$ **Downscope ngay** hoặc đổi RQ; có $\ge 3$ 🟡 $\rightarrow$ Viết kế hoạch xử lý; $\le 2$ 🟡 và 0 🔴 $\rightarrow$ **An toàn**.

---

## 5. RBL-3 · Research Proposal ("Hợp Đồng Nghiên Cứu")

### 7 Yếu Tố Thiết Kế Cốt Lõi:
$$\text{Baseline} \neq \text{Threshold} \neq \text{Metric}$$
* **Metric:** Cách đo (trục đo, ví dụ: F1, Scam Recall, Cosine similarity).
* **Threshold ($\theta$):** Con số cần đạt, có nguồn (Case 1/2/3), chốt trước khi chạy.
* **Baseline:** Đối tượng so sánh ($C$: công cụ cũ, GPT-3.5, chuyên gia, rule-based).

### Cây Quyết Định Chọn Threshold (3 Cases):
* **Case 1:** Paper trong SLR đề xuất ngưỡng cụ thể $\rightarrow$ Dùng ngưỡng đó, trích dẫn paper.
* **Case 2:** Có kết quả số nhưng không có ngưỡng $\rightarrow$ Dùng **trung vị (median)** các kết quả trong bảng.
* **Case 3:** Không có kết quả số $\rightarrow$ Chạy **mini-pilot 5–10 mẫu**, lấy kết quả làm căn cứ.

### Ước Tính Chi Phí API (Kèm Buffer 20%):
$$\text{Chi phí} = (N_{\text{items}} \times (\text{Token}_{\text{in}} \times \text{Giá}_{\text{in}} + \text{Token}_{\text{out}} \times \text{Giá}_{\text{out}}) \times \text{Số lần lặp} + \text{Chi phí Pilot}) \times 1.2$$

### Quy Trình Amendment:
* **Bắt buộc có Amendment duyệt trước:** Đổi RQ, metric chính, threshold, dataset, đổi model (OpenAI $\rightarrow$ Gemini), giảm $N < 80\%$, đổi prompt.
* **Ghi vào `notes.md` (Không cần amendment):** Sửa lỗi script không đổi thiết kế, sửa format output.

---

## 6. RBL-4 · Thực Nghiệm (Pilot & Full Experiment)

### 7 Gate Bắt Buộc Trước Pilot (E1–E7):
* **E1:** Proposal đã được GVHD duyệt.
* **E2:** File dataset thật đã có trong `data/raw/`, đúng format.
* **E3:** `test_api.py` chạy được, có 1 output mẫu.
* **E4:** `compute_metric.py` chạy trên dữ liệu giả không lỗi.
* **E5:** Có quy trình gán nhãn và ngưỡng IAA ($\kappa \ge 0.7$).
* **E6:** Chi phí ước tính $\le$ Ngân sách sẵn có.
* **E7:** GitHub repo Private đã thêm GVHD, `.gitignore` chuẩn.

### Giải Thuật Gọi LLM Xử Lý Lỗi & Retry:
```python
import time, random

def call_llm_with_retry(prompt, max_retries=5):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(...)
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                # Exponential backoff + jitter: 1s, 2s, 4s, 8s, 16s
                wait = (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limit. Retry {attempt+1}/{max_retries} sau {wait:.1f}s")
                time.sleep(wait)
            else:
                raise  # Lỗi khác: không retry để biết nguyên nhân
    return None  # Hết 5 lần retry: đánh dấu INVALID (tính riêng tỷ lệ INVALID)
```

---

## 7. RBL-5a & RBL-5b · Báo Cáo, Trình Bày, Văn Phong AI & Đạo Văn

### Bảng Phân Bổ Slide Thuyết Trình (9 Slides, 10–12 Phút):
| Slide | Nội dung chính | Phụ trách | Thời gian |
| :-: | :--- | :---: | :---: |
| 1 | Tiêu đề + Nhóm + Thành viên | PL | 30s |
| 2 | Vấn đề thực tế (Pain point thực tiễn, không mở bằng "AI is...") | RW | 1.0 min |
| 3 | GAP + RQ + $H_0/H_1$ | RW | 1.5 min |
| 4 | Dataset + Pipeline (Sơ đồ luồng) | LR | 1.5 min |
| 5 | Metric + Kiểm định thống kê | MS | 1.0 min |
| 6–7 | Results (Bảng số liệu + Figures $\ge 300\text{ DPI}$) | MS | 3.0 min |
| 8 | Discussion + Limitations (Phân tích case sai lệch) | PL + MS | 1.5 min |
| 9 | Conclusion + Future Work | RW | 1.0 min |

### RBL-5b: Kiểm Tra Văn Phong AI & Liêm Chính:
* Chạy từng section qua $\ge 2$ công cụ: **SciSpace, ZeroGPT, Copyleaks, GPTZero** $\rightarrow$ Ghi log `paper/quality/ai_check_log.md`.
* **Ngưỡng xử lý:**
  * $< 20\%$: Ít dấu hiệu $\rightarrow$ Giữ nguyên, rà văn phong tự nhiên.
  * $20–50\%$: Cần đọc lại $\rightarrow$ Viết lại các câu máy móc.
  * $> 50\%$: Cần xem xét kỹ $\rightarrow$ Đọc toàn bộ section, đối chiếu bản nháp, viết lại từ đầu.

---

## 8. Đọc Thêm: Hệ Thống Tự Động Hóa Nghiên Cứu (*ScientistTwo*)

> **ScientistTwo** (Google Cloud AI Research, arXiv 2609.19644) là hệ thống AI tự chạy trọn vòng nghiên cứu (sinh ý tưởng $\rightarrow$ thí nghiệm $\rightarrow$ ablation $\rightarrow$ viết paper $\rightarrow$ tự review).  
> **Nên dùng để:** Xem cấu trúc một paper thực nghiệm hoàn chỉnh trông thế nào, cách tổ chức ablation, bảng kết quả và code replication package.

### 3 Luật Cấm Tuyệt Đối Khi Đọc ScientistTwo:
1. 🚫 **Không phải bằng chứng:** Paper do AI sinh, chưa qua peer review $\rightarrow$ **KHÔNG** đưa vào evidence table, **KHÔNG** đếm vào PRISMA, **KHÔNG** trích làm nguồn cho ngưỡng hay baseline.
2. 🚫 **Không lấy về:** Không lấy RQ, ý tưởng, code hay câu chữ từ các paper này đưa vào bài của nhóm.
3. 📝 **Có tham khảo thì ghi rõ:** Ghi rõ trong proposal (mục phương pháp) đọc paper nào, học được gì về cách trình bày hoặc tái lập.
