"""
==============================================================================
ScamShield-VN: Comprehensive Report Generator (.docx)
BÁO CÁO KHOA HỌC: ĐÁNH GIÁ TOÀN DIỆN HẠN CHẾ CỦA KIẾN TRÚC TẦNG 2 CŨ VÀ
ĐỀ XUẤT HỆ THỐNG PHÁP Y ĐA CHUYÊN GIA DỰA TRÊN BẰNG CHỨNG (EVIDENCE-GROUNDED)
==============================================================================
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_report():
    doc = docx.Document()

    # Page Setup (A4, 2cm margins)
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.79)
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(0.79)
        section.right_margin = Inches(0.79)

    # Color Palette
    COLOR_NAVY = RGBColor(15, 42, 74)       # #0F2A4A - Tiêu đề chính, Header
    COLOR_BLUE = RGBColor(26, 82, 118)      # #1A5276 - Subtitle, H2
    COLOR_TEAL = RGBColor(17, 120, 100)     # #117864 - Đề xuất, Thành công
    COLOR_DARK = RGBColor(35, 35, 35)       # #232323 - Text body
    COLOR_MUTED = RGBColor(100, 100, 100)   # #646464 - Meta, chú thích
    COLOR_RED = RGBColor(180, 40, 40)       # #B42828 - Cảnh báo, Lỗi cũ

    def set_cell_background(cell, hex_color):
        tcPr = cell._element.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._element.get_or_add_tcPr()
        tcMar = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="{top}" w:type="dxa"/>'
            f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
            f'<w:left w:w="{left}" w:type="dxa"/>'
            f'<w:right w:w="{right}" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tcPr.append(tcMar)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(15.0)
        run.font.bold = True
        run.font.color.rgb = COLOR_NAVY
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(10.0)
        run.font.italic = True
        run.font.color.rgb = COLOR_BLUE
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(12.0)
        run.font.bold = True
        run.font.color.rgb = COLOR_NAVY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_BLUE
        return p

    def add_p(text, bold=False, italic=False, color=COLOR_DARK):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3.5)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(9.5)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = color
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.12
        r1 = p.add_run(bold_prefix)
        r1.font.name = 'Arial'
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DARK
        r2 = p.add_run(text)
        r2.font.name = 'Arial'
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_DARK
        return p

    def add_callout(text, title='THÔNG ĐIỆP CỐT LÕI (CORE RATIONALE)', bg_color='EBF5FB', border_color='1A5276'):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=80, bottom=80, left=140, right=140)
        cell.width = Inches(6.69)
        
        tcPr = cell._element.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
            f'<w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        r_title = p.add_run(f'📌 {title}\n')
        r_title.font.name = 'Arial'
        r_title.font.size = Pt(9.5)
        r_title.font.bold = True
        r_title.font.color.rgb = COLOR_NAVY
        
        r_text = p.add_run(text.strip())
        r_text.font.name = 'Arial'
        r_text.font.size = Pt(9.0)
        r_text.font.color.rgb = COLOR_DARK
        p.paragraph_format.line_spacing = 1.12
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    def add_code_snippet(code_text, caption=""):
        if caption:
            p_cap = doc.add_paragraph()
            p_cap.paragraph_format.space_before = Pt(4)
            p_cap.paragraph_format.space_after = Pt(1)
            r_cap = p_cap.add_run(f"💻 {caption}")
            r_cap.font.name = 'Arial'
            r_cap.font.size = Pt(8.5)
            r_cap.font.bold = True
            r_cap.font.color.rgb = COLOR_BLUE

        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F4F6F6")
        set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
        cell.width = Inches(6.69)

        tcPr = cell._element.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="16" w:space="0" w:color="7F8C8D"/>'
            f'<w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run(code_text.strip())
        r.font.name = 'Courier New'
        r.font.size = Pt(8.0)
        r.font.color.rgb = COLOR_DARK
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    # =========================================================
    # HEADER & COVER SECTION
    # =========================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("TRƯỜNG ĐẠI HỌC FPT — BỘ MÔN KỸ THUẬT PHẦN MỀM / KHOA HỌC DỮ LIỆU\nCHƯƠNG TRÌNH NGHIÊN CỨU KHOA HỌC DỰA TRÊN THỰC TIỄN (RBL)")
    r_inst.font.name = 'Arial'
    r_inst.font.size = Pt(9.0)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_MUTED

    add_title("BÁO CÁO KHOA HỌC & ĐỀ XUẤT GIẢI PHÁP:\nPHÂN TÍCH TOÀN DIỆN HẠN CHẾ CỦA KIẾN TRÚC TẦNG 2 CŨ VÀ ĐỀ XUẤT HỆ THỐNG PHÁP Y ĐA CHUYÊN GIA DỰA TRÊN BẰNG CHỨNG (EVIDENCE-GROUNDED FORENSIC COUNCIL)")
    add_subtitle("Mổ Xẻ Sự Cố Recall 0% Trên Frozen Test Set (N=267), Phản Biện Chuyên Sâu GPT-6 Astra và Kế Hoạch Chuyển Đổi Kiến Trúc Chuẩn Hóa RBL-No-HARKing")

    # Metadata Table
    tbl_meta = doc.add_table(rows=4, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Đề tài nghiên cứu:", "ScamShield-VN: Nền tảng Giám định và Cảnh báo Tin nhắn Lừa đảo Tiếng Việt"),
        ("Tài liệu tham chiếu:", "Phản biện kiến trúc GPT-6 Astra, RBL Master Framework, SLR Synthesis v1.1"),
        ("Nhóm thực hiện:", "ScamShield Core Research Team (Phụ trách LLM & Evaluation: Nguyễn Minh Quang)"),
        ("Phiên bản kiến trúc:", "Proposal Transformation v2.0 (Tháng 10/2026)")
    ]
    for row_idx, (k, v) in enumerate(meta_data):
        c0, c1 = tbl_meta.cell(row_idx, 0), tbl_meta.cell(row_idx, 1)
        c0.width, c1.width = Inches(2.2), Inches(4.49)
        set_cell_background(c0, "F2F4F4")
        set_cell_background(c1, "FAFAFA")
        set_cell_margins(c0, 40, 40, 80, 80)
        set_cell_margins(c1, 40, 40, 80, 80)
        p0 = c0.paragraphs[0]; r0 = p0.add_run(k); r0.font.bold = True; r0.font.size = Pt(8.5); r0.font.name = 'Arial'
        p1 = c1.paragraphs[0]; r1 = p1.add_run(v); r1.font.size = Pt(8.5); r1.font.name = 'Arial'

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_callout(
        "Báo cáo khoa học này được thiết lập nhằm phân tích và giải trình độc lập hai nội dung cốt lõi: "
        "(1) Mổ xẻ chi tiết những hạn chế nghiêm trọng của kiến trúc Tầng 2 cũ, làm rõ nguyên nhân gốc rễ dẫn đến sự cố "
        "Recall sụp đổ về 0% trong bài kiểm thử Kaggle 267 mẫu; (2) Trình bày thiết kế kỹ thuật của kiến trúc đề xuất mới — "
        "Hệ thống Pháp y Đa Chuyên gia Dựa trên Bằng chứng (Evidence-Grounded Forensic Council). "
        "Toàn bộ tài liệu tuân thủ tuyệt đối quy tắc liêm chính khoa học (No-HARKing), phân định rạch ròi giữa lỗi vận hành "
        "hạ tầng và năng lực phân loại ngữ nghĩa, đồng thời xác lập chuẩn mực thực nghiệm 3 trạng thái (SCAM / HAM / REVIEW) "
        "chuẩn hóa cho đề tài ScamShield-VN.",
        title="TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)"
    )

    # =========================================================
    # PHẦN 1: MỔ XẺ TOÀN DIỆN CÁC HẠN CHẾ CỦA GIẢI PHÁP CŨ
    # =========================================================
    add_h1("PHẦN 1: MỔ XẺ TOÀN DIỆN CÁC HẠN CHẾ CỐT LÕI CỦA GIẢI PHÁP CŨ")
    add_p(
        "Trong các phiên bản thử nghiệm ban đầu của dự án ScamShield-VN, Tầng 2 được định hình dưới dạng 'Hội đồng 5 Tác tử "
        "(5-Agent Council)' vận hành dựa trên cơ chế đóng vai (Role-playing Prompts) kết hợp với mô hình chuyển tiếp phân tầng (Cascade Router). "
        "Mặc dù ý tưởng này có cơ sở lý thuyết ban đầu, quá trình thực nghiệm thực tế trên nền tảng Kaggle và sự soi chiếu từ các phản biện "
        "chuyên sâu đã bộc lộ 7 lỗ hổng mang tính hệ thống như sau:"
    )

    # 1.1
    add_h2("1.1. Lỗi Pipeline 'Nuốt Ngoại Lệ Thành HAM' — Thủ Phạm Trực Tiếp Gây Recall 0%")
    add_p(
        "Một trong những sự cố thực nghiệm chấn động nhất trong quá trình đánh giá mô hình LLM Tầng 2 (bạn Quang thực hiện trên Kaggle) "
        "là chỉ số Recall đối với lớp lừa đảo (SCAM) sụp đổ hoàn toàn về 0.00%. Ban đầu, hiện tượng này bị nhầm lẫn là do LLM không có khả năng "
        "nhận diện tiếng Việt. Tuy nhiên, sau khi mổ xẻ mã nguồn thực tế tại Cell 5 của file hướng dẫn thực nghiệm, nguyên nhân thực sự "
        "đã được định vị chính xác:"
    )

    code_fail = """# Đoạn mã thực nghiệm Cell 5 gây ra sự cố Recall 0% (generate_full_cells_guide_docx.py):
pred_label = 0
try:
    resp = requests.post(url, json=payload, timeout=10)
    elapsed_ms = (time.perf_counter() - start_t) * 1000
    gemini_latencies.append(elapsed_ms)
    
    if resp.status_code == 200:
        text_out = resp.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        pred_label = 1 if '1' in text_out else 0
except Exception as e:
    gemini_latencies.append(1500.0)
    pred_label = 0  # <--- BẪY CHẾT NGƯỜI: Âm thầm nuốt ngoại lệ thành HAM!

gemini_preds.append(pred_label)"""
    add_code_snippet(code_fail, "Mã nguồn lỗi tại Cell 5 Benchmark Kaggle")

    add_p("Cơ chế nguy hiểm này kích hoạt chuỗi sụp đổ dữ liệu như sau:")
    add_bullet("Nuốt lỗi hạ tầng:", "Khi gọi API Gemini gặp mã lỗi HTTP 429 (Rate Limit do hết quota hoặc gọi quá nhanh) hoặc HTTP 404 (do endpoint mô hình 'gemini-2.5-flash' chưa tồn tại ở thời điểm đó, hoặc tên phiên bản sai), biểu thức `resp.status_code == 200` trả về False. Toàn bộ khối điều kiện bị bỏ qua và chương trình giữ nguyên `pred_label = 0`.")
    add_bullet("Nuốt lỗi Schema / Parse:", "Khi mô hình trả về từ chối an toàn (Safety Refusal), phản hồi rỗng, hoặc sinh text có chứa ký tự markdown bọc ngoài JSON, khối lệnh `try...except` bắt ngoại lệ và tự động gán `pred_label = 0`.")
    add_bullet("Hệ quả toán học:", "Trong 267 mẫu kiểm thử (gồm 158 mẫu lừa đảo SCAM và 109 mẫu lành tính HAM), toàn bộ 267 dự đoán đều bị ép thành nhãn 0 (HAM). Số lượng True Positive TP = 0, False Negative FN = 158. Do đó, Recall = TP / (TP + FN) = 0 / 158 = 0.00%!")
    add_bullet("Lỗi phương pháp luận:", "Không tìm thấy bằng chứng độc hại (Negative Detection) bị đánh đồng tuyệt đối với việc không lấy được bằng chứng do lỗi hệ thống (System Failure). Đây là sai sót nghiêm trọng làm vô hiệu hóa giá trị đo đạc.")

    # 1.2
    add_h2("1.2. Sai Lệch Toán Học Trong Cơ Chế Định Tuyến Router & Lỗ Hổng Cascade")
    add_p(
        "Trong kiến trúc cũ (file `pipeline/two_tier_router.py`), cơ chế định tuyến được cài đặt như sau:"
    )
    code_router_old = """# Router cũ trong pipeline/two_tier_router.py
t1_result = self.tier1_classifier.predict(message)
t1_confidence = t1_result["confidence"]  # Confidence là max(p, 1-p) >= 0.5
t1_is_sure = (t1_confidence >= self.tau) # Ngưỡng đơn tau = 0.90
if t1_is_sure and not force_tier2:
    return TIER_1_DIRECT_FASTPATH"""
    add_code_snippet(code_router_old, "Logic định tuyến Router cũ")

    add_p("Đoạn mã trên bộc lộ hai khiếm khuyết toán học và kiến trúc nghiêm trọng:")
    add_bullet("Sai lệch định nghĩa độ tin cậy:", "Trong bài toán phân loại nhị phân (Binary Classification), giá trị confidence của softmax là max(p, 1-p), do đó giá trị này luôn nằm trong khoảng [0.5, 1.0]. Việc tài liệu cũ ghi 'vùng bất định [0.4, 0.85]' là mâu thuẫn hoàn toàn với toán học. Nếu muốn định tuyến vùng phân vân, hệ thống bắt buộc phải sử dụng xác suất dự đoán của lớp mục tiêu p_1(x) = P(Y=SCAM|x) với hai ngưỡng riêng biệt: t_L (ngưỡng dưới) và t_H (ngưỡng trên).")
    add_bullet("Lỗ hổng Cascade không thể cứu vãn (Cascade Fatal Flaw):", "Điểm yếu lớn nhất của kiến trúc cascade là Tầng 2 không bao giờ nhìn thấy những mẫu mà Tầng 1 đã tự tin phân loại. Nếu một tin nhắn lừa đảo tinh vi (ví dụ: dùng ký tự homoglyph hoặc kịch bản zero-day) đánh lừa được mô hình cục bộ ViSoBERT/PhoBERT khiến Tầng 1 tự tin gán nhãn HAM với p > 0.90, router cũ sẽ kết luận ngay tại thiết bị. Mẫu lừa đảo này sẽ lọt lưới 100% mà Tầng 2 không có cơ hội can thiệp.")
    add_bullet("Thiếu chuyển tuyến bắt buộc (Forced Escalation):", "Router cũ hoàn toàn mù quáng trước các tín hiệu kỹ thuật ngoại lai, không có cờ cảnh báo khi phát hiện đầu vào ngoài phân phối (OOD), ký tự bị làm nhiễu (Obfuscation), hoặc mâu thuẫn giữa nhãn văn bản và hạ tầng kỹ thuật (Technical Conflict).")

    # 1.3
    add_h2("1.3. Ảo Tưởng 'Đa Dạng Vai Diễn' (Role Diversity) Thiếu 'Đa Dạng Bằng Chứng' (Evidence Diversity)")
    add_p(
        "Giải pháp cũ tự hào thiết lập 5 Persona chuyên gia (Cyber Threat, Social Engineering, Teencode, Banking, Public Defender). "
        "Tuy nhiên, trên thực tế triển khai, đây chỉ là 5 đoạn System Prompt khác nhau cùng được gửi tới một mô hình LLM duy nhất "
        "(hoặc cùng đọc một chuỗi văn bản SMS trần không có công cụ hỗ trợ):"
    )
    add_bullet("Tư duy bầy đàn (Groupthink) & Ảo giác tập thể:", "Năm mô hình LLM dù mang 5 vai diễn khác nhau nhưng nếu cùng đọc một đoạn văn bản thiếu dữ kiện (ví dụ: một tin nhắn chỉ có link rút gọn hoặc một chuỗi mã hóa vô nghĩa), cả 5 mô hình đều sẽ suy đoán dựa trên thiên kiến tham số bên trong (parametric bias) và có thể cùng đồng thuận đưa ra một kết luận sai.")
    add_bullet("Không có công cụ kiểm chứng (Zero Verification Tools):", "Chuyên gia URL không thực sự phân giải tên miền, không kiểm tra WHOIS, không bóc tách Punycode IDNA, không kiểm tra chứng chỉ SSL. Chuyên gia Ngân hàng không có cơ sở dữ liệu tra cứu các quy định thực tế (như Quyết định 2345/QĐ-NHNN). Toàn bộ nhận định hoàn toàn dựa vào khả năng sinh từ phỏng đoán của LLM.")
    add_bullet("Đa dạng thực sự đòi hỏi gì?:", "Nghiên cứu an ninh mạng chỉ ra rằng: Đa dạng vai trò < Đa dạng họ mô hình < Đa dạng nguồn bằng chứng. Giải pháp cũ chỉ dừng lại ở tầng thấp nhất (Đa dạng vai trò) nhưng lại giả định hệ thống đạt độ tin cậy cấp chuyên gia pháp y.")

    # 1.4
    add_h2("1.4. Lệch Nhãn Hệ Thống (Systemic Label Bias) Do Public Defender Ép Buộc")
    add_p(
        "Nhằm giải quyết hội chứng Alarm Fatigue (báo động giả làm phiền người dùng), giải pháp cũ đã đưa vào nhân vật Public Defender. "
        "Tuy nhiên, cách hiện thực hóa trong file `config/council_registry.yaml` và `pipeline/forensic_council.py` đã tạo ra tác dụng phụ tiêu cực:"
    )
    code_pd_old = """# Cấu hình Public Defender cũ (council_registry.yaml):
prompt_template: |
  Bạn là Luật sư Bào chữa Công cộng (Public Defender)...
  Nhiệm vụ sống còn của bạn là CHỐNG BÁO ĐỘNG GIẢ...
  Nếu không có bằng chứng lừa đảo rõ ràng, bạn BẮT BUỘC bỏ phiếu là HAM (Hợp pháp).
weight: 1.3
public_defender_veto_boost: 0.25 # Trừ thẳng 25% điểm rủi ro!"""
    add_code_snippet(code_pd_old, "Thiết kế cũ của Public Defender")

    add_bullet("Ép buộc nhãn định kiến (Forced Labeling):", "Mệnh lệnh 'BẮT BUỘC bỏ phiếu là HAM' tước đoạt quyền trung lập của agent. Ngay cả khi đối diện với một tin nhắn lừa đảo tinh vi mà bằng chứng chưa đủ rõ, agent này vẫn phải bỏ phiếu HAM thay vì ABSTAIN (bỏ phiếu trắng).")
    add_bullet("Trừ điểm cảm tính (Arbitrary Veto Boost):", "Quy tắc trừ cứng 0.25 (25%) vào xác suất lừa đảo tổng thể khiến nhiều trường hợp 4 agent kỹ thuật đã nhận diện nguy cơ cao (ví dụ xác suất 0.70) lập tức bị kéo xuống dưới ngưỡng 0.45, chuyển đổi mẫu SCAM thành HAM hoặc phân vân.")
    add_bullet("Đổi Recall lấy Precision ảo:", "Giảm báo động giả bằng cách biến nhiều mẫu SCAM thành HAM không phải là một cải tiến thuật toán. Nó gây ra cái giá đắt đỏ nhất trong an ninh mạng: Bỏ sót cuộc tấn công (False Negative).")

    # 1.5
    add_h2("1.5. Lỗi Ngữ Nghĩa Toán Học Của Biểu Đồ Radar XAI 5 Trục")
    add_p(
        "Giải pháp cũ đề xuất vẽ biểu đồ Radar 5 trục đại diện cho 5 chuyên gia để giải thích cho người dùng. "
        "Tuy nhiên, thiết kế này mắc một lỗi ngữ nghĩa toán học cơ bản:"
    )
    add_bullet("Mâu thuẫn chiều hướng trục:", "Bốn trục đầu tiên (Cyber Threat, Social Engineering, Teencode, Banking) đo lường mức độ nguy cơ độc hại (Scam Risk - càng cao càng nguy hiểm). Nhưng trục thứ năm (Public Defender) lại đo lường bằng chứng lành tính (Benign/Legitimacy - càng cao càng an toàn).")
    add_bullet("Vô nghĩa về mặt diện tích:", "Việc nối 5 đỉnh này lại thành một đa giác hoặc tính tổng diện tích radar để suy ra mức độ nguy hiểm là hoàn toàn sai lệch về mặt thống kê. Một tin nhắn an toàn có điểm Defender cao sẽ làm đa giác phình to, tạo cảm giác trực quan rằng tin nhắn đó cực kỳ nguy hiểm!")

    # 1.6
    add_h2("1.6. Khủng Hoảng Tài Nguyên, Bẫy Rate Limit & Thiếu Khả Năng Kiểm Soát Concurrency")
    add_p(
        "Khi triển khai trên 267 mẫu kiểm thử, giải pháp cũ giả định có thể gọi song song 5 agent cho mỗi tin nhắn:"
    )
    add_bullet("Bùng nổ request đồng thời:", "267 mẫu × 5 agent = 1.335 API requests. Nếu chương trình bắn đồng thời các coroutine vào API Gemini Free Tier (giới hạn 15 RPM) mà không có semaphore điều tiết, 90% số request sẽ lập tức nhận mã lỗi HTTP 429.")
    add_bullet("Thiếu cơ chế điều tiết (Throttling) & Circuit Breaker thực chất:", "Hệ thống cũ không có hàng đợi giới hạn (Bounded Queue), không có cơ chế Token Bucket, và thời gian chờ retry không có ngẫu nhiên hóa (Jitter), dẫn đến hiện tượng đàn linh dương dẫm đạp (Thundering Herd) lên API.")

    # 1.7
    add_h2("1.7. Hạn Chế Khi Đối Mặt Với Ký Tự Obfuscation & Homoglyphs")
    add_p(
        "Kẻ lừa đảo thường xuyên chèn ký tự Unicode giả mạo (ví dụ: chữ 'а' tiếng Cyrillic thay cho chữ 'a' Latinh trong tên miền ngân hàng), "
        "chèn ký tự vô hình (Zero-Width Space), hoặc viết teencode lách luật viễn thông. "
        "Giải pháp cũ kỳ vọng chuỗi suy luận Chain-of-Thought (CoT) của LLM sẽ tự động nhìn xuyên qua các biến thể này. "
        "Tuy nhiên, về mặt kỹ thuật NLP:"
    )
    add_bullet("Tokenizer bị vỡ trước khi LLM suy luận:", "Bộ phân tách từ tố (Subword Tokenizer như BPE/SentencePiece) sẽ băm nát từ bị biến dạng thành các token vô nghĩa hoặc token lạ trước khi đưa vào transformer. Khi đầu vào đã bị méo mó, CoT chỉ làm nhiệm vụ hợp thức hóa một kết luận sai bằng một đoạn văn giải thích nghe có vẻ logic.")
    add_bullet("Thiếu tầng tiền xử lý chuẩn hóa:", "Hệ thống cũ hoàn toàn thiếu bộ chuyển đổi chuẩn hóa Unicode theo tiêu chuẩn bảo mật quốc tế Unicode UTS #39 (Confusable Skeleton), không có khả năng trích xuất URL dạng `hxxp` hoặc dấu chấm trong ngoặc `[.]`.")

    # =========================================================
    # PHẦN 2: ĐỐI CHIẾU CƠ SỞ KHOA HỌC & CHUẨN HÓA THƯ MỤC
    # =========================================================
    add_h1("PHẦN 2: ĐỐI CHIẾU CƠ SỞ KHOA HỌC & CHUẨN HÓA THƯ MỤC HỌC THUẬT")
    add_p(
        "Nhằm tuân thủ tuyệt đối nguyên tắc liêm chính học thuật RBL (No-HARKing & Zero Fabricated Data), "
        "báo cáo này tiến hành đính chính, đối chiếu và chuẩn hóa toàn bộ các tài liệu tham khảo nền tảng được trích dẫn trong đề tài:"
    )

    tbl_lit = doc.add_table(rows=6, cols=4)
    tbl_lit.alignment = WD_TABLE_ALIGNMENT.CENTER
    lit_headers = ["Công trình / Tác giả", "Venue & Năm Xác Minh", "Điểm Tiếp Thu Hợp Lý", "Lưu Ý Giới Hạn Khi Áp Dụng Cho ScamShield-VN"]
    lit_widths = [Inches(1.5), Inches(1.2), Inches(2.0), Inches(1.99)]
    
    for c_idx, h in enumerate(lit_headers):
        cell = tbl_lit.cell(0, c_idx)
        cell.width = lit_widths[c_idx]
        set_cell_background(cell, "0F2A4A")
        set_cell_margins(cell, 60, 60, 70, 70)
        p = cell.paragraphs[0]; r = p.add_run(h)
        r.font.name = 'Arial'; r.font.bold = True; r.font.size = Pt(8.5); r.font.color.rgb = RGBColor(255, 255, 255)

    lit_rows = [
        ("PhishLLM (Liu et al.)", "USENIX Security 2024\n(Đính chính: Không phải IEEE TDSC)", 
         "Cơ chế phát hiện lừa đảo dựa trên đối chiếu danh tính thực thể (Reference-based) và phân tích hành vi thu thập thông tin đăng nhập.",
         "Phạm vi gốc là phân tích mã nguồn trang web HTML phishing; không thể áp dụng trực tiếp nguyên bản cho tin nhắn SMS chỉ có text thô."),
        ("MultiPhishGuard (2025)", "arXiv v1 (05/2025)\n(Cần ghi rõ bản v1 do v2 2026 đổi tên)", 
         "Mô hình đa tác tử chuyên môn hóa: Text, URL, Metadata, Explanation và Adversarial Agent.",
         "Được huấn luyện bằng PPO trên tập email tiếng Anh quy mô lớn. Không nên vội vàng áp dụng PPO phức tạp khi tập dữ liệu tiếng Việt còn giới hạn."),
        ("ChatEval (Chan et al.)", "ICLR 2024\n(Mã nguồn công khai GitHub)", 
         "Cơ chế tranh luận đa agent (Multi-agent Debate) giúp cải thiện độ chính xác và tính khách quan so với một giám khảo đơn lẻ.",
         "Nhiệm vụ gốc là đánh giá chất lượng văn bản; phát hiện lừa đảo có chi phí False Negative cực cao và yêu cầu độ trễ tính bằng mili-giây."),
        ("PoLL (Verga et al.)", "arXiv 2024\n(Replacing Judges with Juries)", 
         "Hội đồng các mô hình ngôn ngữ nhỏ và đa dạng (Jury of LLMs) có thể vượt trội một mô hình khổng lồ đắt đỏ.",
         "Ủng hộ giả thuyết đa dạng họ mô hình. Nhắc nhở rằng 5 prompt trên cùng một mô hình không tạo ra 5 nguồn đánh giá độc lập."),
        ("BitAbuse (2025)", "Findings of NAACL 2025\n(Dataset 325.580 mẫu)", 
         "Tập dữ liệu chuẩn mực về biến dạng thị giác (Visual Perturbations) và phương pháp khôi phục nội dung chống lừa đảo.",
         "Độ chính xác khôi phục ký tự 96% không đồng nghĩa với Recall phát hiện phishing đạt 96%. Dùng làm tập benchmark kiểm thử độ bền (robustness).")
    ]
    for r_idx, row in enumerate(lit_rows):
        for c_idx, val in enumerate(row):
            cell = tbl_lit.cell(r_idx + 1, c_idx)
            cell.width = lit_widths[c_idx]
            bg = "FFFFFF" if r_idx % 2 == 0 else "F9FAFA"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 45, 45, 65, 65)
            p = cell.paragraphs[0]; r = p.add_run(val)
            r.font.name = 'Arial'; r.font.size = Pt(8.0)
            if c_idx == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_NAVY

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_p(
        "Về quy trình PRISMA 2020: Báo cáo khẳng định số lượng bài viết đưa vào biểu đồ PRISMA trong luận văn phải là số lượng "
        "phát sinh thực tế từ nhật ký tìm kiếm (Search Logs) trên các cơ sở dữ liệu học thuật (ArXiv, IEEE, ACM, OpenAlex), "
        "tuyệt đối không sử dụng các con số ước lượng hoặc làm tròn giả định."
    )

    # =========================================================
    # PHẦN 3: KIẾN TRÚC GIẢI PHÁP ĐỀ XUẤT MỚI
    # =========================================================
    add_h1("PHẦN 3: KIẾN TRÚC GIẢI PHÁP ĐỀ XUẤT MỚI — HỆ THỐNG PHÁP Y DỰA TRÊN BẰNG CHỨNG")
    add_p(
        "Nhằm khắc phục toàn bộ 7 hạn chế nêu trên, kiến trúc Tầng 2 được tái thiết kế toàn diện theo mô hình: "
        "Hệ Thống Pháp Y Đa Chuyên Gia Dựa Trên Bằng Chứng (Evidence-Grounded Forensic Council). "
        "Các thành phần cốt lõi được đặc tả kỹ thuật như sau:"
    )

    # 3.1
    add_h2("3.1. Luồng Xử Lý End-to-End & Nguyên Tắc Phân Loại 3 Trạng Thái (3-State Classification)")
    add_p(
        "Hệ thống thiết lập nguyên tắc bất khả xâm phạm: Mọi sự cố hạ tầng, cạn quota, lỗi kết nối mạng hoặc thiếu bằng chứng "
        "tuyệt đối KHÔNG ĐƯỢC ÉP VỀ NHÃN HAM. Thay vào đó, hệ thống vận hành theo cơ chế phân loại 3 trạng thái:"
    )
    add_bullet("SCAM (Lừa đảo nguy hiểm):", "Đã thu thập đủ bằng chứng kỹ thuật hoặc đồng thuận chuyên gia vượt ngưỡng rủi ro an toàn.")
    add_bullet("HAM (Tin nhắn hợp pháp):", "Đã kiểm chứng đầy đủ các dấu hiệu giao dịch thông thường và không có bất kỳ bằng chứng vi phạm nào.")
    add_bullet("REVIEW (Cần chuyên viên rà soát / Cảnh báo bất định):", "Áp dụng khi hệ thống gặp lỗi API, timeout, độ bao phủ bằng chứng không đạt chuẩn, hoặc có mâu thuẫn gay gắt giữa các chuyên gia. Hệ thống sẽ phát cảnh báo thận trọng cho người dùng thay vì ru ngủ họ bằng nhãn an toàn giả tạo.")

    # 3.2
    add_h2("3.2. Router 2 Ngưỡng (Dual-Threshold) & Cơ Chế Chuyển Tuyến Bắt Buộc (Forced Escalation)")
    add_p(
        "Cơ chế Router được chuẩn hóa lại về mặt toán học. Thay vì dùng một ngưỡng đơn tau trên confidence, hệ thống sử dụng "
        "xác suất dự đoán lớp lừa đảo p_1(x) = P(Y=SCAM|x) từ mô hình ViSoBERT Tầng 1 đã qua hiệu chuẩn nhiệt độ (Temperature Scaling):"
    )
    add_callout(
        "Quy tắc chuyển tuyến hoàn chỉnh:\n\n"
        "route(x) = 1  KHI VÀ CHỈ KHI:\n"
        "  (0.35 <= p_1(x) <= 0.85)  [Vùng phân vân xác suất]\n"
        "  HOẶC OOD(x) == True        [Phát hiện đầu vào ngoài phân phối]\n"
        "  HOẶC Obfuscation(x) == True [Phát hiện ký tự Unicode lạ / Punycode / Teencode dị thường]\n"
        "  HOẶC TechnicalConflict(x) == True [Mâu thuẫn: Text có vẻ bình thường nhưng chứa URL lạ/OTP ngân hàng]\n\n"
        "Nếu route(x) == 0: Trả về kết quả trực tiếp tại Edge (HAM nếu p_1 < 0.35; SCAM nếu p_1 > 0.85).\n"
        "Nếu route(x) == 1: Bắt buộc chuyển tiếp lên Tầng 2 (Forensic Council).",
        title="CÔNG THỨC ĐỊNH TUYẾN ROUTER CHUẨN HÓA"
    )

    # 3.3
    add_h2("3.3. Kho Bằng Chứng Đa Nguồn & Tầng Tiền Xử Lý Đa Góc Nhìn (Multi-View Evidence Store)")
    add_p(
        "Thay vì gửi trực tiếp văn bản thô cho LLM, tin nhắn sẽ đi qua Tầng Tiền Xử Lý Kỹ Thuật để trích xuất bằng chứng khách quan "
        "và lưu vào kho dữ liệu có định danh (Evidence Store):"
    )
    add_bullet("Bảo toàn chứng cứ gốc:", "Văn bản thô được lưu nguyên trạng kèm mã băm SHA-256 và bản đồ vị trí ký tự (Source Span Offset Map).")
    add_bullet("Chuẩn hóa Unicode UTS #39 Confusable Skeleton:", "Phát hiện chính xác các ký tự tương đồng thị giác (ví dụ ký tự Cyrillic 'а', 'о', 'р' chèn vào chuỗi Latinh) mà không làm biến dạng số tài khoản hay mã giao dịch.")
    add_bullet("Trích xuất URL chuyên sâu:", "Tách URL không phụ thuộc scheme, hỗ trợ định dạng lách luật như `hxxp://`, `[.]com`, và phân giải Hostname qua Public Suffix List (PSL) để xác định đúng tên miền gốc.")
    add_bullet("Đối chiếu Cơ sở Tri thức Pháp lý Ngân hàng:", "Kiểm tra tự động các dấu hiệu vi phạm Quyết định 2345/QĐ-NHNN của Ngân hàng Nhà nước (Ví dụ: Ngân hàng không bao giờ gửi link SMS yêu cầu cập nhật dữ liệu sinh trắc học).")
    add_bullet("Gắn mã định danh bằng chứng:", "Mỗi bằng chứng tìm thấy được đánh mã: `EVID-URL-01`, `EVID-BANK-01`, `COUNTER-EVID-01` để các agent bắt buộc phải trích dẫn.")

    # 3.4
    add_h2("3.4. Tái Cấu Trúc 5 Chuyên Gia Dựa Trên Bằng Chứng & Schema Hợp Đồng Nghiêm Ngặt")
    add_p(
        "Mỗi chuyên gia trong Hội đồng được tái cấu trúc thành một kiểm định viên độc lập với thẩm quyền giới hạn, "
        "giao tiếp qua Schema Pydantic có cấu trúc chặt chẽ:"
    )

    code_pydantic = """class AgentAssessment(BaseModel):
    schema_version: Literal["2.0"]
    role_id: str
    verdict: Literal["SCAM", "HAM", "ABSTAIN"]
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_ids: List[str] = Field(max_length=10)        # Bắt buộc tham chiếu bằng chứng
    counterevidence_ids: List[str] = Field(max_length=10) # Bằng chứng bào chữa lành tính
    reason_codes: List[str] = Field(max_length=6)
    summary: str = Field(max_length=500)"""
    add_code_snippet(code_pydantic, "Hợp đồng dữ liệu Pydantic đầu ra của Agent")

    add_bullet("Cyber URL Inspector:", "Chỉ diễn giải kết quả từ công cụ trích xuất hạ tầng mạng; tuyệt đối không tự bịa ra trạng thái blacklist.")
    add_bullet("Social Engineering Profiler:", "Chỉ ra chính xác đoạn văn bản (text span) chứa thủ đoạn thao túng tâm lý sợ hãi, khẩn cấp hoặc bẫy lòng tham.")
    add_bullet("Vietnamese Linguistic Analyst:", "Bóc tách teencode và biến thể lách lọc; lỗi ngữ pháp chỉ được coi là tín hiệu yếu chứ không tự biến thành bằng chứng lừa đảo.")
    add_bullet("Banking Protocol Verifier:", "Đối chiếu trực tiếp với quy chuẩn NHNN; không dùng trí nhớ tham số mơ hồ để xác nhận quy trình giao dịch.")
    add_bullet("Public Defender (Tái định nghĩa thành Counter-Evidence Auditor):", "Không còn nghĩa vụ 'bắt buộc bảo vệ HAM'. Nhiệm vụ duy nhất là tìm kiếm giả thuyết lành tính có căn cứ (ví dụ: OTP chuẩn từ SMS Brandname đã xác thực). Khi không có bằng chứng lành tính, agent bắt buộc phải chọn `ABSTAIN` thay vì bỏ phiếu HAM giả mạo.")

    # 3.5
    add_h2("3.5. Quyền Phủ Quyết Kỹ Thuật Đủ Điều Kiện (Qualified Security Veto) & Thuật Toán Consensus")
    add_p(
        "Hệ thống bãi bỏ quy tắc trừ điểm cảm tính 0.25 của Defender và thay thế bằng hai cơ chế toán học chuẩn xác:"
    )
    add_bullet("Qualified Security Veto (Quyền lực thuộc về Bằng chứng):", "Một chuyên gia kỹ thuật chỉ được kích hoạt Veto SCAM khi thỏa mãn đồng thời: (1) Agent kỹ thuật có thẩm quyền, (2) Đánh giá SCAM với độ tự tin hiệu chuẩn cao, (3) Có bằng chứng kỹ thuật xác thực trong Evidence Store (ví dụ: URL lừa đảo rõ ràng), và (4) Bằng chứng thực sự đóng vai trò đích hành động trong ngữ cảnh tin nhắn.")
    add_bullet("Consensus Borda phân định rõ Độ Nghiêng (Margin) & Độ Bao Phủ (Coverage):", "Hệ thống tính toán riêng biệt hai đại lượng: Độ nghiêng đồng thuận M = (S_SCAM - S_HAM) / Tổng trọng số, và Độ bao phủ bằng chứng hợp lệ Q = Tổng trọng số hợp lệ / Tổng trọng số kỳ vọng. Nếu Q < 0.60 (quá nhiều agent gặp lỗi hoặc timeout), hệ thống tự động đưa ra nhãn REVIEW chứ không ép về HAM.")
    add_bullet("Early-Exit Toán Học Chặt Chẽ:", "Hệ thống chỉ dừng sớm các request còn lại khi khoảng cách điểm dẫn trước D > W_R (tổng trọng số các agent chưa phản hồi không thể đảo ngược kết quả) VÀ đã thỏa mãn độ bao phủ chuyên gia bắt buộc.")

    # 3.6
    add_h2("3.6. XAI Radar 5 Trục Chuẩn Hóa Cùng Chiều (Homogeneous Risk Dimensions)")
    add_p(
        "Nhằm khôi phục tính toàn vẹn toán học và ngữ nghĩa trực quan cho người dùng, biểu đồ Radar XAI được tái thiết kế "
        "với 5 trục đều đo lường mức độ rủi ro (Risk Dimensions, thang điểm từ 0.0 đến 1.0):"
    )
    add_bullet("Trục 1: Rủi ro Hạ tầng & URL Phishing", "(URL & Infrastructure Risk Score)")
    add_bullet("Trục 2: Mức độ Thao túng Tâm lý Xã hội", "(Social Engineering & Coercion Score)")
    add_bullet("Trục 3: Mức độ Che giấu & Biến dạng Ký tự", "(Obfuscation & Evasion Anomaly Score)")
    add_bullet("Trục 4: Mức độ Lệch Quy trình Ngân hàng", "(Banking Protocol Violation Score)")
    add_bullet("Trục 5: Mức độ Bất thường Ngữ cảnh & Mạo danh", "(Contextual Anomaly & Impersonation Score)")
    add_p(
        "Điểm số của Public Defender được tách ra thành một thanh tiến trình kiểm định độc lập: "
        "'Thước đo Bằng chứng Bào chữa (Counter-Evidence Defense Score)'. Khi có bằng chứng lành tính đanh thép, thanh này sẽ sáng rõ "
        "để minh giải cho người dùng lý do tin nhắn được bảo vệ an toàn."
    )

    # 3.7
    add_h2("3.7. Hạ Tầng Phục Vụ Bền Vững (Serving Layer Resilience)")
    add_p(
        "Để triệt tiêu triệt để nguy cơ nghẽn mạng và lỗi HTTP 429 trên Kaggle và môi trường thực tế, hệ thống bổ sung:"
    )
    add_bullet("Bộ điều tiết Token Bucket & Concurrency Semaphore:", "Giới hạn nghiêm ngặt tối đa 5 request đồng thời và tuân thủ định mức RPM của nhà cung cấp.")
    add_bullet("Exponential Backoff với Full Jitter:", "Thời gian chờ khi bị rate limit: d_k = Uniform(0, min(d_max, d_0 * 2^k)), triệt tiêu hiện tượng dẫm đạp request.")
    add_bullet("Dynamic Model Registry & Multi-Provider Fallback Pool:", "Tự động phân giải tên mô hình chính xác (Gemini 1.5 Flash -> Gemini 2.0 Flash -> Groq LLaMA-3.3-70B -> Local Rule Fallback).")

    # =========================================================
    # PHẦN 4: MA TRẬN SO SÁNH GIẢI PHÁP CŨ VS ĐỀ XUẤT MỚI
    # =========================================================
    add_h1("PHẦN 4: MA TRẬN SO SÁNH TOÀN DIỆN GIỮA GIẢI PHÁP CŨ VÀ ĐỀ XUẤT MỚI")
    add_p(
        "Bảng tổng hợp dưới đây đối chiếu chi tiết 12 khía cạnh kiến trúc và phương pháp luận giữa hai thế hệ giải pháp:"
    )

    tbl_comp = doc.add_table(rows=13, cols=3)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_headers = ["Khía Cạnh Đánh Giá", "Kiến Trúc Cũ (Vấn Đề & Hạn Chế)", "Kiến Trúc Đề Xuất Mới (Evidence-Grounded)"]
    comp_widths = [Inches(1.8), Inches(2.4), Inches(2.49)]

    for c_idx, h in enumerate(comp_headers):
        cell = tbl_comp.cell(0, c_idx)
        cell.width = comp_widths[c_idx]
        set_cell_background(cell, "0F2A4A")
        set_cell_margins(cell, 60, 60, 70, 70)
        p = cell.paragraphs[0]; r = p.add_run(h)
        r.font.name = 'Arial'; r.font.bold = True; r.font.size = Pt(8.5); r.font.color.rgb = RGBColor(255, 255, 255)

    comp_data = [
        ("1. Triết lý vận hành Tầng 2", "5 Persona đóng vai (Role-playing), tranh luận ngôn ngữ tự nhiên không kiểm chứng.", "Hệ thống điều phối bằng chứng pháp y, chuyên gia độc lập có công cụ kiểm chứng."),
        ("2. Cơ chế Định tuyến Router", "Ngưỡng đơn tau = 0.90 trên confidence; không cứu được mẫu Tầng 1 tự tin sai.", "Dual-threshold [0.35, 0.85] trên P(SCAM|x) kết hợp Chuyển tuyến bắt buộc (Forced Escalation)."),
        ("3. Xử lý Lỗi Ngoại lệ Pipeline", "Nuốt exception thành HAM (pred_label = 0), dẫn đến sự cố sụp đổ Recall 0%.", "Tách bạch chuỗi 7 trạng thái; lỗi hạ tầng trả về nhãn REVIEW, cấm fallback về HAM."),
        ("4. Định dạng Đầu ra (Contract)", "JSON lỏng lẻo bọc trong markdown, parse bằng regex tìm từ khóa thô sơ.", "Pydantic Schema nghiêm ngặt; bắt buộc trích dẫn evidence_ids có thực."),
        ("5. Bản chất Đa dạng Tác tử", "Đa dạng vai diễn (Role diversity) trên cùng 1 LLM đọc text trần; dễ bị Groupthink.", "Đa dạng bằng chứng (Evidence diversity): URL parser, UTS #39, Banking knowledge base."),
        ("6. Vai trò Public Defender", "Ép buộc 'BẮT BUỘC bỏ phiếu HAM', trừ cứng 0.25; tạo label bias, kéo tụt Recall.", "Counter-Evidence Auditor: Phản biện khi có chứng cứ lành tính; không có thì ABSTAIN."),
        ("7. Quyền Phủ quyết (Veto Rule)", "Veto cảm tính dựa trên điểm confidence do LLM tự khai báo.", "Qualified Security Veto: Bắt buộc kèm bằng chứng kỹ thuật khách quan đã xác minh."),
        ("8. Thuật toán Đồng thuận", "Borda gộp chung cả ABSTAIN; chia trung bình đơn giản không kiểm tra độ bao phủ.", "Đo lường riêng biệt Margin M và Coverage Q; nếu Q < 0.60 chuyển sang REVIEW."),
        ("9. Cơ chế Dừng Sớm (Early-Exit)", "Đếm cơ học 4/5 phiếu mà không xét trọng số các agent còn lại có thể lật kèo.", "Chỉ dừng khi khoảng cách điểm D > W_R (không thể lật ngược) và thỏa mãn coverage."),
        ("10. Xử lý Obfuscation / Teencode", "Trông chờ vào Chain-of-Thought của LLM (bị vỡ tokenizer trước khi suy luận).", "Tầng tiền xử lý đa góc nhìn: Hash gốc, Unicode UTS #39 Skeleton, Public Suffix List."),
        ("11. Cấu trúc Radar Giải thích (XAI)", "4 trục đo nguy cơ lừa đảo trộn với 1 trục đo tính lành tính; sai lệch ngữ nghĩa.", "5 trục cùng chiều đo rủi ro [0.0, 1.0]; hiển thị riêng thanh Counter-Evidence Defense."),
        ("12. Kiểm soát Tải & Rate Limit", "Gọi đồng thời 1.335 request không kiểm soát; thường xuyên nhận lỗi HTTP 429.", "Token Bucket, Bounded Queue, Exponential Backoff với Jitter, Multi-provider pool.")
    ]

    for r_idx, (k, old_v, new_v) in enumerate(comp_data):
        c0, c1, c2 = tbl_comp.cell(r_idx + 1, 0), tbl_comp.cell(r_idx + 1, 1), tbl_comp.cell(r_idx + 1, 2)
        c0.width, c1.width, c2.width = comp_widths[0], comp_widths[1], comp_widths[2]
        bg = "FFFFFF" if r_idx % 2 == 0 else "F9FAFA"
        set_cell_background(c0, bg); set_cell_background(c1, "FDEDEC" if r_idx % 2 == 0 else "FADBD8"); set_cell_background(c2, "EAFAF1" if r_idx % 2 == 0 else "D5F5E3")
        set_cell_margins(c0, 45, 45, 60, 60); set_cell_margins(c1, 45, 45, 60, 60); set_cell_margins(c2, 45, 45, 60, 60)
        
        p0 = c0.paragraphs[0]; r0 = p0.add_run(k); r0.font.bold = True; r0.font.size = Pt(8.0); r0.font.name = 'Arial'; r0.font.color.rgb = COLOR_NAVY
        p1 = c1.paragraphs[0]; r1 = p1.add_run(old_v); r1.font.size = Pt(8.0); r1.font.name = 'Arial'; r1.font.color.rgb = COLOR_RED
        p2 = c2.paragraphs[0]; r2 = p2.add_run(new_v); r2.font.size = Pt(8.0); r2.font.name = 'Arial'; r2.font.color.rgb = COLOR_TEAL

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================
    # PHẦN 5: KẾ HOẠCH THỰC NGHIỆM ĐỐI CHỨNG & LỘ TRÌNH TRIỂN KHAI
    # =========================================================
    add_h1("PHẦN 5: KẾ HOẠCH THỰC NGHIỆM ĐỐI CHỨNG & LỘ TRÌNH TRIỂN KHAI")
    add_p(
        "Để chứng minh giá trị thực nghiệm của kiến trúc đề xuất mới một cách khoa học, nhóm nghiên cứu xác lập lộ trình 7 bước "
        "thực hiện từ ưu tiên cấp bách đến mở rộng:"
    )

    add_bullet("Bước 1 — Sửa dứt điểm lỗi Pipeline Kaggle:", "Cập nhật Cell 5 trong file hướng dẫn của bạn Quang; loại bỏ lệnh fallback về 0 khi có ngoại lệ; ghi nhận riêng biệt số mẫu thành công và số mẫu lỗi hệ thống.")
    add_bullet("Bước 2 — Ổn định hạ tầng phục vụ:", "Tích hợp Bounded Concurrency Semaphore (tối đa 5 luồng đồng thời) và Exponential Backoff có Jitter để dập tắt hoàn toàn mã lỗi HTTP 429.")
    add_bullet("Bước 3 — Triển khai Tầng Tiền Xử Lý Bằng Chứng:", "Viết module `pipeline/evidence_store.py` hỗ trợ bóc tách URL, chuẩn hóa Unicode UTS #39 Confusable Skeleton và checklist quy chuẩn ngân hàng.")
    add_bullet("Bước 4 — Chuẩn hóa Router 2 Ngưỡng & Forced Escalation:", "Cập nhật `pipeline/two_tier_router.py` theo công thức toán học hai ngưỡng [0.35, 0.85] kết hợp cờ kích hoạt bắt buộc.")
    add_bullet("Bước 5 — Tái lập Baseline Hội Đồng Độc Lập:", "Chạy benchmark trên tập Frozen Test Set (N=267) với Hội đồng kiểm định bằng chứng độc lập (chưa cần vòng debate phức tạp).")
    add_bullet("Bước 6 — Đo lường tác động của Counter-Evidence Auditor:", "Thực hiện phép thử ablation đối chứng khi có và không có Public Defender để chứng minh khả năng giảm FPR mà không làm sụt giảm Scam Recall.")
    add_bullet("Bước 7 — Xuất Báo Cáo Thực Nghiệm Hai Lớp:", "Báo cáo song song hai bảng số liệu: Bảng Năng lực Phân loại (Precision, Recall, F1 trên các mẫu hợp lệ) và Bảng Năng lực Vận hành (Tỷ lệ Coverage, Tỷ lệ REVIEW, Độ trễ E2E, và Chi phí token USD).")

    # Conclusion Callout
    add_callout(
        "Luận điểm khoa học cốt lõi cần bảo vệ trong đề tài ScamShield-VN là: 'Một kiến trúc phân tầng kết hợp giữa mô hình cục bộ "
        "(PhoBERT/ViSoBERT) và Hội đồng Pháp y Đa Chuyên gia được trang bị công cụ kiểm chứng bằng chứng có khả năng triệt tiêu hội chứng "
        "Alarm Fatigue, bảo toàn Scam Recall vượt trội và tối ưu hóa chi phí vận hành'.\n"
        "Báo cáo này xác lập cơ sở kỹ thuật vững chắc để toàn đội ngũ tự tin bước vào giai đoạn bảo vệ đề tài trước Hội đồng Chuyên môn.",
        title="KẾT LUẬN & CAM KẾT LIÊM CHÍNH KHOA HỌC (NO-HARKING)",
        bg_color="EAFAF1",
        border_color="117864"
    )

    # Save document
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, "docs", "BAO_CAO_DE_XUAT_GIAI_PHAP_VA_HAN_CHE_TIER2.docx")
    doc.save(output_path)
    # Ensure stdout encoding
    if sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    print(f"[OK] Bao cao da duoc tao thanh cong tai: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_report()
