import os
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def style_run(run, name='Times New Roman', size=10, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color

def create_task_doc(filename, task_data):
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Header / Institution
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("FPT UNIVERSITY — RESEARCH-BASED LEARNING (RBL-FA26SE079)\nSCAMSHIELD-VN MANUSCRIPT QUALITY ASSURANCE (JAIT STANDARD)")
    style_run(r_inst, size=9.5, bold=True, color=RGBColor(0, 51, 102))

    # Main Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run(f"JIRA TASK SPECIFICATION & REVIEW GUIDE\n{task_data['key']}: {task_data['summary']}")
    style_run(r_title, size=14, bold=True, color=RGBColor(31, 78, 121))

    # Jira Meta Table
    tbl = doc.add_table(rows=5, cols=4)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.style = 'Table Grid'
    
    meta_cells = [
        [("Issue Key:", True), (task_data['key'], False), ("Issue Type:", True), ("Sub-task / Review Task", False)],
        [("Assignee:", True), (task_data['assignee'], False), ("Priority:", True), ("High / Blocker", False)],
        [("Section Scope:", True), (task_data['section'], False), ("Story Points:", True), (str(task_data['points']), False)],
        [("Target Venue:", True), ("JAIT (Journal)", False), ("Sprint:", True), ("Sprint 4 - Paper Polish", False)],
        [("File LaTeX:", True), (task_data['latex_file'], False), ("Status:", True), ("TO DO (In Progress)", False)]
    ]
    
    for ri, row in enumerate(meta_cells):
        for ci, (txt, is_b) in enumerate(row):
            cell = tbl.cell(ri, ci)
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_after = Pt(2)
            cp.paragraph_format.space_before = Pt(2)
            r = cp.add_run(txt)
            style_run(r, size=9, bold=is_b)

    # 1. Overview & Objective
    p_h1 = doc.add_paragraph()
    p_h1.paragraph_format.space_before = Pt(14)
    p_h1.paragraph_format.space_after = Pt(4)
    r_h1 = p_h1.add_run("1. MỤC TIÊU VÀ PHẠM VI KIỂM DUYỆT (OBJECTIVES & SCOPE)")
    style_run(r_h1, size=11, bold=True, color=RGBColor(0, 51, 102))

    for item in task_data['objectives']:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(item)
        style_run(r, size=9.5)

    # 2. Key Data & Citations to Verify
    p_h2 = doc.add_paragraph()
    p_h2.paragraph_format.space_before = Pt(12)
    p_h2.paragraph_format.space_after = Pt(4)
    r_h2 = p_h2.add_run("2. CÁC SỐ LIỆU, CÔNG THỨC & DẪN CHỨNG PHẢI ĐỐI SOÁT CHÍNH XÁC")
    style_run(r_h2, size=11, bold=True, color=RGBColor(0, 51, 102))

    for item in task_data['data_checks']:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(item)
        style_run(r, size=9.5)

    # 3. Source Files Cross-Check Matrix
    p_h3 = doc.add_paragraph()
    p_h3.paragraph_format.space_before = Pt(12)
    p_h3.paragraph_format.space_after = Pt(4)
    r_h3 = p_h3.add_run("3. DANH SÁCH FILE NGUỒN CẦN ĐỐI CHIẾU TRONG REPOSITORY")
    style_run(r_h3, size=11, bold=True, color=RGBColor(0, 51, 102))

    tbl_files = doc.add_table(rows=len(task_data['source_files']) + 1, cols=3)
    tbl_files.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_files.style = 'Table Grid'
    
    headers = ["Đường Dẫn File Trong Repo", "Nội Dung Đối Chiếu Cụ Thể", "Mức Độ Quan Trọng"]
    for ci, h in enumerate(headers):
        c = tbl_files.cell(0, ci)
        cp = c.paragraphs[0]
        cp.paragraph_format.space_after = Pt(2)
        cp.paragraph_format.space_before = Pt(2)
        r = cp.add_run(h)
        style_run(r, size=9, bold=True)

    for ri, f_row in enumerate(task_data['source_files']):
        for ci, txt in enumerate(f_row):
            c = tbl_files.cell(ri + 1, ci)
            cp = c.paragraphs[0]
            cp.paragraph_format.space_after = Pt(2)
            cp.paragraph_format.space_before = Pt(2)
            r = cp.add_run(txt)
            style_run(r, size=8.5, bold=(ci == 2 and txt == "Bắt buộc"))

    # 4. JAIT Formatting & Template Compliance
    p_h4 = doc.add_paragraph()
    p_h4.paragraph_format.space_before = Pt(12)
    p_h4.paragraph_format.space_after = Pt(4)
    r_h4 = p_h4.add_run("4. QUY CHUẨN ĐỊNH DẠNG JAIT BẮT BUỘC (JAIT COMPLIANCE)")
    style_run(r_h4, size=11, bold=True, color=RGBColor(0, 51, 102))

    for rule in task_data['jait_rules']:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(rule)
        style_run(r, size=9.5)

    # 5. Definition of Done Checklist
    p_h5 = doc.add_paragraph()
    p_h5.paragraph_format.space_before = Pt(12)
    p_h5.paragraph_format.space_after = Pt(4)
    r_h5 = p_h5.add_run("5. CHECKLIST NGHIỆM THU (DEFINITION OF DONE - DoD)")
    style_run(r_h5, size=11, bold=True, color=RGBColor(0, 51, 102))

    for dod in task_data['dod']:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Inches(0.2)
        r = p.add_run(f"[ ]  {dod}")
        style_run(r, size=9.5)

    # Save
    doc.save(filename)
    print(f"Generated: {filename}")

tasks = [
    {
        "key": "SCAM-101",
        "summary": "Kiểm duyệt & Hiệu đính Phần I. INTRODUCTION (Bối cảnh, Khoảng trống & Đóng góp)",
        "assignee": "Phan Trần Hoàng Trân (tranpth)",
        "section": "I. INTRODUCTION",
        "points": 3,
        "latex_file": "paper/sections/01_intro.tex & main.tex",
        "objectives": [
            "Kiểm tra tính mạch lạc, học thuật và sức thuyết phục của bối cảnh lừa đảo viễn thông tại Việt Nam năm 2024.",
            "Rà soát định nghĩa 3 nút thắt cốt lõi: (1) Hàm mất mát đối xứng, (2) Báo động giả của Single-LLM (>35%), (3) Độ trễ và chi phí API đám mây.",
            "Xác thực sự rõ ràng của 4 đóng góp kỹ thuật chính của hệ thống hai tầng ScamShield-VN.",
            "Đảm bảo phong cách viết đặt vấn đề theo đúng cấu trúc gợi ý của JAIT-template.doc (What is known -> What are the gaps -> Significance)."
        ],
        "data_checks": [
            "Thiệt hại lừa đảo mạng tại VN năm 2024: 18.9 nghìn tỷ VNĐ (~$744 triệu USD) — Cần khớp với trích dẫn VietNamNet [1] và Bộ TTTT [2].",
            "Tỷ lệ báo động giả của Single Cloud LLM: False Alarm Rate > 35% (cụ thể FAR = 35.53% từ thực nghiệm Gemini 3.5 Flash).",
            "Độ trễ API cloud độc lập: dao động 3 - 15 giây/tin nhắn (ảnh hưởng trực tiếp trải nghiệm người dùng mobile edge).",
            "Tuyên bố 4 đóng góp: ViSoBERT + WBCE (alpha=5.0) trên N=267 mẫu (5 random seeds), Hội đồng Occam 3-Agent (tiết kiệm 40% chi phí, McNemar p=0.0736), và Cascade hai tầng giải quyết 96.6% tin nhắn tại biên với độ trễ 267.5 ms."
        ],
        "source_files": [
            ["paper/claims.md", "Đối soát Claim 1, Claim 2, Claim 4 về các tuyên bố khoa học cốt lõi", "Bắt buộc"],
            ["paper/references.bib", "Kiểm tra trích dẫn vietnamnet2024scams, mst2024scams, seo2024ondevice", "Bắt buộc"],
            ["results/summary.csv", "Đối soát số liệu độ trễ và tỷ lệ lỗi của Gemini Flash", "Quan trọng"],
            ["team-synthesis/proposal_amendment_v1.1.md", "Kiểm tra sự nhất quán giữa đề xuất và phần Introduction", "Tham khảo"]
        ],
        "jait_rules": [
            "Độ dài Introduction vừa phải, súc tích, không sa đà vào phân tích chi tiết từng công trình (phần đó thuộc về Literature Review).",
            "Đoạn văn kết thúc Introduction phải nêu rõ cấu trúc các phần tiếp theo theo chuẩn JAIT: Section II. Literature Review, Section III. Materials and Methods, Section IV. Result and Discussion, Section V. Conclusion.",
            "Trích dẫn số thứ tự trong ngoặc vuông [1], [2] liền mạch, không dấu cách thừa trước ngoặc."
        ],
        "dod": [
            "Đã đối soát 100% số liệu thiệt hại 18.9 nghìn tỷ VNĐ và trích dẫn [1], [2] trong references.bib.",
            "4 đóng góp kỹ thuật khớp chính xác từng số liệu với kết quả ở Section IV.",
            "Không còn bất kỳ câu từ lủng củng hoặc sai ngữ pháp tiếng Anh.",
            "Cấu trúc các phần ở đoạn cuối khớp chính xác mục lục bài báo."
        ]
    },
    {
        "key": "SCAM-102",
        "summary": "Kiểm duyệt & Chuẩn hóa Phần II. LITERATURE REVIEW (Tiến trình 4 Chủ Đề & Table I)",
        "assignee": "Nguyễn Trung Hiếu (cristand2825 / PL)",
        "section": "II. LITERATURE REVIEW",
        "points": 5,
        "latex_file": "paper/sections/02_related.tex & main.tex",
        "objectives": [
            "Đảm bảo phần tổng quan y văn được trình bày đúng chuẩn JAIT: Vừa theo chủ đề (thematically) vừa theo tiến trình thời gian (chronologically).",
            "Rà soát 4 chủ đề: (1) Machine learning cổ điển, (2) Transformer tiếng Việt, (3) LLM và Edge SLM, (4) Đồng thuận Đa tác tử & Lỗi tương quan.",
            "ĐẶC BIỆT: Kiểm tra loại bỏ triệt để mọi từ ngữ liên quan đến 'Condorcet Jury Theorem' (bị Mentor nghiêm cấm), thay thế hoàn toàn bằng lý thuyết Khử lỗi tương quan (Correlated Error Mitigation) theo Kim et al. (ICML 2025) và Ladha (1992).",
            "Đối soát bảng so sánh TABLE I giữa ScamShield-VN và 6 công trình đại diện."
        ],
        "data_checks": [
            "TABLE I - Tuấn et al. (2023): PhoBERT, CNN, LSTM trên N~3,000 multi-accent SMS, Accuracy 95.56%.",
            "TABLE I - Nguyen-Xuan (2026): MLTEA Dual-Encoder trên code-mixed phishing, Macro-F1 0.940.",
            "TABLE I - Cam & Binh (2026): PhoBERT, BiLSTM trên email VNSED, Accuracy 86.47%.",
            "TABLE I - Zhou et al. (2026): GPT-4o, Claude, Gemini trên FraudSMSWalker N~4,000, Recall 64.16 - 90.13%, Benign recall < 30.25%.",
            "TABLE I - Banda et al. (2026): Llama-3.2-3B Mobile trên N=4,200 QR lures, Latency 45 ms.",
            "TABLE I - Phap et al. (2026): BiGRU + MaskedPool + WBCE trên UCI & LSDST N=5,574, Latency 0.25 ms.",
            "TABLE I - ScamShield-VN: Two-Tier ViSoBERT + 3-Agent Council, Recall 97.11%, FPR 2.37%, Latency 267.5 ms, Cost $0.05/1k SMS."
        ],
        "source_files": [
            ["trung_hieu/SLR/evidence-table.md", "Bảng trích xuất bằng chứng 7 trường dữ liệu chuẩn SLR", "Bắt buộc"],
            ["trung_hieu/SLR/gap-analysis.md", "Phân tích khoảng trống nghiên cứu và ma trận phản chứng", "Bắt buộc"],
            ["paper/references.bib", "Kiểm tra 25 citations bao gồm kim2025correlated, ladha1992condorcet, smit2024should", "Bắt buộc"],
            ["AUDIT_TIER2_MENTOR_CHECKLIST.md", "Rà soát mục 1.1 loại bỏ hoàn toàn Condorcet Jury Theorem", "Bắt buộc"]
        ],
        "jait_rules": [
            "Tiêu đề bảng TABLE I đặt ở PHÍA TRÊN bảng, căn giữa: TABLE I. COMPARATIVE OVERVIEW...",
            "Không dùng 'et al.' trong tiêu đề cột hoặc văn bản nếu chưa nêu rõ ngữ cảnh; viết đúng chính tả tên tác giả Việt (Tuấn, Cam, Binh, Nguyen-Xuan).",
            "Chủ đề 4 phải đóng vai trò làm bàn đạp lý thuyết dẫn dắt trực tiếp vào phương pháp luận Hội đồng Tier 2 ở Section III."
        ],
        "dod": [
            "Đã rà soát không còn chữ nào nhắc đến 'Condorcet' trong toàn bộ văn bản.",
            "7 dòng trong TABLE I khớp chính xác từng số phần trăm và độ trễ với evidence-table.md.",
            "Các trích dẫn Kim et al. (2025), Ladha (1992), Smit et al. (2024) được diễn giải chính xác về mặt toán học lỗi tương quan."
        ]
    },
    {
        "key": "SCAM-103",
        "summary": "Kiểm duyệt & Chuẩn hóa Phần III. MATERIALS AND METHODS (Quy trình Dữ liệu, WBCE, ONNX & Hội đồng 3-Agent)",
        "assignee": "Nguyễn Minh Quang (quangnm)",
        "section": "III. MATERIALS AND METHODS",
        "points": 5,
        "latex_file": "paper/sections/03_method.tex & main.tex",
        "objectives": [
            "Kiểm tra mô tả chi tiết, minh bạch quy trình thu thập và phân chia dữ liệu đảm bảo tính tái lập (Replicability) theo chuẩn JAIT.",
            "Xác thực công thức toán học của hàm tổn thất Cost-Sensitive WBCE (Equation 1 & 2) và giải thích gradient dốc gấp 5 lần (alpha=5.0).",
            "Mô tả lượng tử hóa ONNX INT8 của ViSoBERT (dung lượng 390 MB, trễ 15.8 ms trên CPU).",
            "Chuẩn hóa mô tả Hội đồng Đa tác tử Tier 2 theo cấu hình Occam 3-Agent (kèm cơ chế Veto -0.25 của ghế Public Defender).",
            "Đảm bảo định nghĩa chuẩn 3 nhãn SCAM-RISK, LOW-RISK, UNKNOWN tuân thủ Điều 25 Nghị định 13/2023/NĐ-CP và PII masking."
        ],
        "data_checks": [
            "Tập dữ liệu gốc: N = 2,664 tin nhắn (1,918 Benign ~ 72.0%, 746 Scam ~ 28.0%).",
            "Phân chia: 90% Train/Val (2,397 tin nhắn), 10% Frozen Test Partition (N = 267: 192 Ham, 75 Scam, stratified seed 42, Cohen kappa = 0.88).",
            "Tập thử thách pháp y Hard Forensic Suite: N = 117 tin nhắn (98 scam lures tinh vi, 19 OTP ngân hàng/dịch vụ chuẩn).",
            "Tập tổng hợp E2E Suite: N = 384 tin nhắn (267 Frozen Test + 117 Hard Forensic).",
            "Trọng số hội đồng 3-Agent: Ghế A Cyber Threat (w_A = 0.35), Ghế B Ngôn ngữ (w_B = 0.35), Ghế C Public Defender (w_C = 0.30, delta_defender = 0.25).",
            "Ngưỡng phán quyết 3 nhãn: SCAM-RISK (P >= 0.60), LOW-RISK (P < 0.40), UNKNOWN (0.40 <= P < 0.60)."
        ],
        "source_files": [
            ["data/raw/vietnamese_sms_merged_all.csv", "Xác nhận số lượng dòng và tỷ lệ phân bố nhãn", "Bắt buộc"],
            ["pipeline/forensic_council.py", "Kiểm tra code logic trọng số 3 ghế và nhãn UNKNOWN", "Bắt buộc"],
            ["config/council_registry.yaml", "Kiểm tra cấu hình phân quyền và ngưỡng gating [0.40, 0.60]", "Bắt buộc"],
            ["pipeline/local_classifier.py", "Xác thực cấu hình inference ONNX INT8 và latency 15.8 ms", "Quan trọng"]
        ],
        "jait_rules": [
            "Công thức toán học phải được đánh số thứ tự liên tục (1), (2), (3) và định dạng KaTeX/LaTeX chuẩn.",
            "Danh sách gạch đầu dòng và danh sách đánh số phải theo đúng quy chuẩn JAIT: Bulleted lists và Numbered lists (1), (2).",
            "Mọi siêu tham số huấn luyện (learning rate 2e-5, warmup 0.1, weight decay 0.01, epochs 4, batch size 16) phải được ghi rõ ràng."
        ],
        "dod": [
            "Số lượng mẫu các tập N=2,664, N=267, N=117, N=384 khớp 100% không sai lệch 1 mẫu nào.",
            "Công thức đạo hàm WBCE ở Eq. (2) chính xác về mặt vi tích phân.",
            "Logic nhãn 3 trạng thái SCAM-RISK, LOW-RISK, UNKNOWN khớp chính xác với code trong forensic_council.py.",
            "Đã ghi rõ việc tuân thủ Nghị định 13/2023/NĐ-CP về che giấu thông tin định danh (PII redaction)."
        ]
    },
    {
        "key": "SCAM-104",
        "summary": "Kiểm duyệt & Đối soát Số Liệu Toàn Diện Phần IV. RESULT AND DISCUSSION (Tables II, III, IV, V, VI & McNemar)",
        "assignee": "Hoàng Hải Phúc (haiphuchoang2675)",
        "section": "IV. RESULT AND DISCUSSION",
        "points": 8,
        "latex_file": "paper/sections/04_results.tex & main.tex",
        "objectives": [
            "Đối soát từng con số, từng sai số chuẩn (std dev) và p-value trên toàn bộ 5 bảng số liệu thực nghiệm.",
            "Kiểm tra bảng TABLE II: Kết quả 5-run seeds độc lập trên Frozen Test N=267 giữa ViSoBERT và 4 baselines.",
            "Kiểm tra bảng TABLE III: Kiểm định ý nghĩa thống kê McNemar (b, c, chi-square, p-value, odds ratio).",
            "Kiểm tra bảng TABLE IV: Thực nghiệm đối sánh Ablation Hội đồng Tier 2 (5-Agent vs 3-Agent vs P-single trên N=117), xác thực luận điểm Occam's Razor tiết kiệm 40% chi phí với p=0.0736 > 0.05.",
            "Kiểm tra bảng TABLE V & VI: Kết quả E2E Cascaded System trên N=384 và phân tích quét độ nhạy ngưỡng tau từ 0.70 đến 0.95.",
            "Rà soát 4 tiểu mục Thảo luận chuyên sâu: Bác bỏ Condorcet / Khử lỗi tương quan, Triệt tiêu Alarm Fatigue (FPR 0.00%), Thất bại của model scaling, Bảo mật Nghị định 13, và Threats to Validity."
        ],
        "data_checks": [
            "TABLE II - ViSoBERT: Acc 95.65 +/- 1.54%, Prec 89.79 +/- 5.15%, Recall 95.62 +/- 2.25%, F1 92.51 +/- 2.39%, Size 390 MB.",
            "TABLE II - PhoBERT-large: Acc 95.95 +/- 1.57%, Recall 92.33 +/- 3.44%, F1 92.70 +/- 2.87%, Size 1,480 MB.",
            "TABLE II - Gemini 3.5 Flash: Acc 84.50 +/- 1.02%, Prec 64.47 +/- 1.52%, Recall 100.00%, FAR = 35.53%.",
            "TABLE III - McNemar vs Gemini: b = 38, c = 2, chi^2 = 30.625, p = 0.0000, OR = 19.00 (Bác bỏ H0, p < 0.001).",
            "TABLE IV - Ablation 3-Agent vs 5-Agent: 5-Agent (500 calls, $0.75) vs 3-Agent (351 calls, $0.45) -> b=5, c=0, chi^2=3.2000, p=0.0736 (Chấp nhận H0, tiết kiệm 40% chi phí).",
            "TABLE IV - Baseline P-single: Acc 96.58%, Recall 95.92%, FPR 0.00%, Latency 12,176 ms, Cost $0.0450.",
            "TABLE V - E2E Cascade (tau=0.90): Acc 97.40%, Recall 97.11%, FPR 2.37%, Latency 267.5 ms, Cost $0.0509/1k SMS, Escalation 3.4% (Triage tại biên 96.6%).",
            "TABLE VI - Quét tau: Điểm knee tối ưu Pareto tại tau = 0.90."
        ],
        "source_files": [
            ["results/summary.csv", "Đối soát bảng 1: 5-run seed metrics của tất cả models", "Bắt buộc"],
            ["results/mcnemar_analysis.csv", "Đối soát bảng 2: Các chỉ số kiểm định McNemar b, c, p-value", "Bắt buộc"],
            ["experiments/tier2_council/reports/REPORT_ABLATION_3V5.md", "Đối soát bảng 3: Kết quả thực nghiệm Ablation 3v5 và McNemar p=0.0736", "Bắt buộc"],
            ["experiments/tier2_council/reports/REPORT_P_SINGLE_BASELINE.md", "Đối soát kết quả baseline P-single (Wang et al., ACL 2024)", "Bắt buộc"],
            ["experiments/e2e_two_tier/reports/REPORT_E2E_TWO_TIER_BENCHMARK.md", "Đối soát bảng 4 & 5: Số liệu 3-run median E2E cascade và sweep tau", "Bắt buộc"]
        ],
        "jait_rules": [
            "Tiêu đề tất cả các Bảng phải đặt ở PHÍA TRÊN bảng, đánh số La Mã: TABLE II., TABLE III., TABLE IV., TABLE V., TABLE VI.",
            "Bảng TABLE III, IV, VI căn chỉnh vừa khít trong 1 cột đơn; TABLE II, V có thể đặt full 2 cột (table*) nếu cần thiết.",
            "Không để xảy ra hiện tượng chữ số tràn lề cột (overflow) trong bảng biên dịch PDF."
        ],
        "dod": [
            "100% số liệu trong cả 5 bảng TABLE II, III, IV, V, VI khớp từng chữ số thập phân với file report tương ứng.",
            "Giá trị McNemar p = 0.0736 được khẳng định chính xác là luận cứ Occam's Razor.",
            "Phân tích Threats to Validity bao gồm đủ 4 khía cạnh: Internal, External, Construct, Conclusion Validity.",
            "Không có mâu thuẫn số liệu giữa bảng biểu và văn bản mô tả xung quanh."
        ]
    },
    {
        "key": "SCAM-105",
        "summary": "Kiểm duyệt Phần V. CONCLUSION, END-MATTER & Toàn Bộ Danh Mục Trích Dẫn REFERENCES",
        "assignee": "Nguyễn Minh Quang (quangnm)",
        "section": "V. CONCLUSION & END-MATTER",
        "points": 4,
        "latex_file": "paper/sections/05_conclusion.tex, 06_endmatter.tex & main.tex",
        "objectives": [
            "Kiểm duyệt phần Kết luận: Nhấn mạnh giá trị kỹ thuật thực tiễn (engineering content) và khả năng ứng dụng thực tế trên mạng viễn thông, tránh viết theo kiểu tóm tắt đơn thuần.",
            "Nêu rõ các giới hạn kỹ thuật (phân tích tin nhắn văn bản, chưa hỗ trợ quét ảnh QR-code) và 2 hướng nghiên cứu tương lai (VLM on-device, carrier pilot).",
            "Kiểm tra đầy đủ 4 mục cuối bắt buộc theo chuẩn JAIT-template.doc:",
            "  1. Conflict of Interest: 'The authors declare no conflict of interest.'",
            "  2. Author Contributions: Đầy đủ phân vai CRediT cho cả 5 thành viên (Hiếu, Huy, Phúc, Trân, Quang).",
            "  3. Funding: Trích dẫn rõ đề tài RBL FA26SE079 và Đại học FPT.",
            "  4. Acknowledgment: Lời cảm ơn ChongLuaDao và Hiệp hội An ninh mạng Quốc gia.",
            "Rà soát danh mục 25 tài liệu tham khảo trong references.bib đảm bảo chuẩn trích dẫn JAIT (đầy đủ tác giả, tên tạp chí in nghiêng, số volume, trang, năm, URL kèm ngày truy cập)."
        ],
        "data_checks": [
            "Tóm tắt các chỉ số cốt lõi trong Conclusion: Scam Recall 95.62%, Macro-F1 92.51%, Edge Latency 15.8 ms, Cascade Acc 97.40%, Cost $0.0509/1k SMS.",
            "Tuân thủ Điều 25 Nghị định 13/2023/NĐ-CP về quyền riêng tư và nhãn UNKNOWN.",
            "Author Contributions CRediT Taxonomy:",
            "  - Nguyễn Trung Hieu: Conceptualization, Methodology, Formal analysis, Writing - Original Draft, Project administration.",
            "  - Lê Quốc Huy: Software, Pipeline architecture, Data curation, Investigation.",
            "  - Hoàng Hải Phúc: Validation, Model benchmarking, Statistical testing, Visualization.",
            "  - Phan Trần Hoàng Trân: Resources, Data collection, Literature review, Writing - Review & Editing.",
            "  - Nguyễn Minh Quang: Supervision, Verification, Ethical review, Funding acquisition."
        ],
        "source_files": [
            ["paper/references.bib", "Kiểm tra cú pháp 25 mục trích dẫn BibTeX không bị lỗi ngoặc hay thiếu trường", "Bắt buộc"],
            ["docs/JAIT-template.doc", "Đối chiếu các mục Conflict of Interest, Author Contributions, References", "Bắt buộc"],
            ["AGENTS.md", "Đối soát quy định CRediT taxonomy và quy chuẩn đạo đức", "Quan trọng"]
        ],
        "jait_rules": [
            "Mục Conflict of Interest, Author Contributions, Funding, Acknowledgment đặt TRƯỚC mục References.",
            "References đánh số thứ tự trong ngoặc vuông [1] - [25] liên tục, liệt kê đầy đủ tên các tác giả (không lạm dụng et al. trong danh mục tài liệu).",
            "Các bài báo trực tuyến/arXiv phải có URL hoặc DOI đầy đủ."
        ],
        "dod": [
            "Đã kiểm tra đủ 4 mục bắt buộc: Conflict of Interest, Author Contributions, Funding, Acknowledgment.",
            "Cả 5 thành viên đều được ghi nhận đúng vai trò đóng góp thực tế trong dự án.",
            "Không có citation nào trong bài bị [?] (lỗi thiếu khóa trong references.bib).",
            "Conclusion nêu bật rõ hàm lượng kỹ thuật và hướng mở rộng Vision-Language Models cho QR smishing."
        ]
    }
]

# Generate 5 individual task files
for t in tasks:
    fname = f"docs/JIRA_Task_{t['key']}_{t['section'].replace(' ', '_').replace('.', '')}.docx"
    create_task_doc(fname, t)

# Generate Master Guide
doc_m = docx.Document()
for s in doc_m.sections:
    s.top_margin = Inches(0.8)
    s.bottom_margin = Inches(0.8)
    s.left_margin = Inches(0.8)
    s.right_margin = Inches(0.8)

p = doc_m.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("FPT UNIVERSITY — RBL SCAMSHIELD-VN (FA26SE079)\nBẢNG PHÂN CÔNG KIỂM DUYỆT BẢN THẢO BÀI BÁO THEO CHUẨN JAIT (JIRA MASTER BOARD)")
style_run(r, size=13, bold=True, color=RGBColor(0, 51, 102))

p_sub = doc_m.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
r_sub = p_sub.add_run("Target Venue: Journal of Advances in Information Technology (JAIT)\nSprint: Sprint 4 - Final Paper Audit & Quality Assurance | Total Story Points: 25 SP")
style_run(r_sub, size=10, italic=True)

# Master Summary Table
tbl_m = doc_m.add_table(rows=6, cols=6)
tbl_m.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_m.style = 'Table Grid'

h_list = ["Jira Key", "Phần Đảm Nhiệm", "Thành Viên", "Story Points", "File Nguồn Đối Soát Chính", "Tệp Hướng Dẫn Chi Tiết"]
for ci, h in enumerate(h_list):
    c = tbl_m.cell(0, ci)
    cp = c.paragraphs[0]
    cp.paragraph_format.space_after = Pt(2)
    cp.paragraph_format.space_before = Pt(2)
    r = cp.add_run(h)
    style_run(r, size=9, bold=True)

for ri, t in enumerate(tasks):
    row_vals = [
        t['key'],
        t['section'],
        t['assignee'].split('(')[0].strip(),
        str(t['points']) + " SP",
        t['source_files'][0][0],
        f"JIRA_Task_{t['key']}_*.docx"
    ]
    for ci, v in enumerate(row_vals):
        c = tbl_m.cell(ri + 1, ci)
        cp = c.paragraphs[0]
        cp.paragraph_format.space_after = Pt(2)
        cp.paragraph_format.space_before = Pt(2)
        r = cp.add_run(v)
        style_run(r, size=8.5, bold=(ci in [0, 2]))

# Detailed overview of each task
for t in tasks:
    p_t = doc_m.add_paragraph()
    p_t.paragraph_format.space_before = Pt(14)
    p_t.paragraph_format.space_after = Pt(2)
    r_t = p_t.add_run(f"### {t['key']}: {t['summary']} (Phụ trách: {t['assignee']})")
    style_run(r_t, size=11, bold=True, color=RGBColor(31, 78, 121))

    for obj in t['objectives']:
        p = doc_m.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(obj)
        style_run(r, size=9)

doc_m.save("docs/JIRA_TASKS_MASTER_PAPER_REVIEW.docx")
print("Generated Master Guide: docs/JIRA_TASKS_MASTER_PAPER_REVIEW.docx")
