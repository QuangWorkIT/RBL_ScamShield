# -*- coding: utf-8 -*-
"""
Script generating HUONG_DAN_LOC_VA_GAN_NHAN_BENCHMARK_COUNCIL.docx
Standard operating procedure for the 4 team members on dataset extraction,
fine-grained annotation, and handling missing/insufficient data under RBL guidelines.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tc_pr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tc_pr.append(tcMar)

def set_table_borders(table, color="D0D7DE", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}>'
                        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:insideV w:val="none"/>'
                        f'<w:left w:val="none"/>'
                        f'<w:right w:val="none"/>'
                        f'</w:tblBorders>')
    tblPr.append(borders)

def add_callout(doc, text, title="LƯU Ý QUAN TRỌNG", box_type="note"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    
    bg_color = "F0F7FF" if box_type == "note" else ("FFFBEB" if box_type == "warn" else "FEF2F2")
    border_color = "0284C7" if box_type == "note" else ("D97706" if box_type == "warn" else "DC2626")
    
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    tc_pr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}>'
                          f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
                          f'<w:top w:val="none"/>'
                          f'<w:right w:val="none"/>'
                          f'<w:bottom w:val="none"/>'
                          f'</w:tcBorders>')
    tc_pr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_title = p.add_run(f"📌 {title}\n")
    run_title.bold = True
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(10.5)
    run_title.font.color.rgb = RGBColor.from_string(border_color)
    
    run_text = p.add_run(text)
    run_text.font.name = "Calibri"
    run_text.font.size = Pt(10)
    run_text.font.color.rgb = RGBColor(51, 51, 51)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def format_heading(p, text, level=1):
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.bold = True
    if level == 1:
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
    elif level == 2:
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run.font.size = Pt(12.5)
        run.font.color.rgb = RGBColor(30, 58, 138) # Blue 900
    elif level == 3:
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(71, 85, 105) # Slate 600

def create_document():
    doc = Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    # Document Title
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(2)
    r_meta = p_meta.add_run("DỰ ÁN SCAMSHIELD-VN — QUY TRÌNH THỰC NGHIỆM ĐÁNH GIÁ MÔ HÌNH (RBL PROTOCOL)")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(9.5)
    r_meta.font.bold = True
    r_meta.font.color.rgb = RGBColor(100, 116, 139)
    
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("HƯỚNG DẪN TRÍCH XUẤT, GÁN NHÃN CHUYÊN SÂU VÀ XỬ LÝ DỮ LIỆU ĐÁNH GIÁ HỘI ĐỒNG 5 AGENT")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("Tài liệu hướng dẫn kỹ thuật dành riêng cho 4 thành viên phụ trách 4 mảng giám định pháp y. Bao gồm quy tắc xử lý khi thiếu dữ liệu hoặc không đủ số lượng trong kho ngữ liệu gốc.")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(51, 65, 85)
    
    # Metadata Box
    table_meta = doc.add_table(rows=4, cols=2)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_meta.autofit = False
    set_table_borders(table_meta)
    
    meta_info = [
        ("Mục tiêu thực nghiệm:", "Xây dựng Master Evaluation Benchmark (100–120 test cases) để đo đạc và xếp vị trí 11 model cho Hội đồng Pháp y Tier 2."),
        ("Quy chuẩn áp dụng:", "Nghiên cứu dựa trên bằng chứng (RBL), Frozen Test Set Protocol, Tuyệt đối không bịa số liệu."),
        ("Phạm vi phân công:", "Thành viên 2 (URL), Thành viên 3 (Tâm lý), Thành viên 4 (Teencode), Thành viên 5 (Ngân hàng & HAM)."),
        ("Định dạng bàn giao:", "Bảng tính Excel (.xlsx) hoặc JSON Lines (.jsonl) kèm cột Ground Truth và bằng chứng xác minh.")
    ]
    
    for i, (k, v) in enumerate(meta_info):
        row = table_meta.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(2.0), Inches(4.5)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 80, 80, 100, 100)
        set_cell_margins(c1, 80, 80, 100, 100)
        
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    # SECTION 1
    format_heading(doc.add_paragraph(), "1. Hướng Dẫn Lấy Dữ Liệu Gốc Từ Kho Dự Án", level=1)
    
    p = doc.add_paragraph()
    p.add_run("Toàn bộ dữ liệu tin nhắn tiếng Việt đã được commit và đồng bộ đầy đủ trên GitHub repository của nhóm. Các thành viên KHÔNG CẦN tìm dữ liệu mới từ đầu, mà chỉ cần lấy dữ liệu về máy theo một trong hai cách dưới đây:")
    
    p_c1 = doc.add_paragraph()
    r = p_c1.add_run("Cách 1: Lấy qua Git (Khuyến nghị nếu đã cài Git):\n")
    r.bold = True
    p_c1.add_run("Mở terminal tại máy cá nhân, chuyển đến thư mục dự án và thực hiện lệnh pull nhánh làm việc:\n")
    p_code = doc.add_paragraph()
    r_code = p_code.add_run("git fetch origin\ngit checkout feat/master-slr-synthesis\ngit pull origin feat/master-slr-synthesis")
    r_code.font.name = "Consolas"
    r_code.font.size = Pt(9.5)
    r_code.font.color.rgb = RGBColor(15, 23, 42)
    p_code.paragraph_format.left_indent = Inches(0.4)
    
    p_c2 = doc.add_paragraph()
    r = p_c2.add_run("Cách 2: Tải trực tiếp qua trình duyệt web (Dành cho thành viên không thạo Git):\n")
    r.bold = True
    p_c2.add_run("1. Truy cập đường dẫn thư mục dữ liệu trên GitHub:\n")
    p_link = doc.add_paragraph()
    r_link = p_link.add_run("https://github.com/QuangWorkIT/RBL_ScamShield/tree/feat/master-slr-synthesis/data/raw")
    r_link.font.name = "Consolas"
    r_link.font.size = Pt(9.5)
    r_link.font.color.rgb = RGBColor(2, 132, 199)
    p_link.paragraph_format.left_indent = Inches(0.4)
    
    p_steps = doc.add_paragraph()
    p_steps.add_run("2. Bấm vào tệp ")
    r_f = p_steps.add_run("vietnamese_sms_merged_all.csv")
    r_f.bold = True
    p_steps.add_run(" (chứa 2.665 tin nhắn tổng hợp).\n")
    p_steps.add_run("3. Bấm vào nút ")
    r_btn = p_steps.add_run("Download raw file")
    r_btn.bold = True
    p_steps.add_run(" ở góc phải để tải file .csv về máy tính.\n")
    p_steps.add_run("4. Mở file bằng Microsoft Excel, WPS Office hoặc Google Sheets để bắt đầu lọc dữ liệu.")

    add_callout(doc, 
        "Khi mở file CSV bằng Microsoft Excel, nếu bị lỗi phông chữ tiếng Việt: Hãy mở một file Excel trắng, chọn tab Data -> From Text/CSV -> Chọn file vừa tải về -> Chọn File Origin là '65001 : Unicode (UTF-8)' -> Bấm Load. Toàn bộ tiếng Việt có dấu sẽ hiển thị hoàn hảo 100%.", 
        title="MẸO XỬ LÝ LỖI FONT TIẾNG VIỆT TRONG EXCEL", 
        box_type="note"
    )

    # SECTION 2
    format_heading(doc.add_paragraph(), "2. Phân Công Chi Tiết & Hướng Dẫn Lọc Cho 4 Thành Viên", level=1)
    
    p = doc.add_paragraph()
    p.add_run("Mỗi thành viên chịu trách nhiệm xây dựng bộ đề thi đại diện cho chuyên môn của chiếc ghế mà mình quản lý. Mục tiêu là chọn ra từ ")
    r = p.add_run("20 đến 30 mẫu tin nhắn sắc nét nhất")
    r.bold = True
    p.add_run(" từ file CSV.")

    # Member 2
    format_heading(doc.add_paragraph(), "2.1. Thành viên 2 — Phụ trách Ghế 1: Giám định URL & Kỹ thuật mạng (ROLE_CYBER_URL)", level=2)
    p = doc.add_paragraph()
    p.add_run("• ")
    p.add_run("Mục tiêu giám định: ").bold = True
    p.add_run("Phát hiện các tin nhắn lừa đảo sử dụng đường link giả mạo, tên miền độc hại, link rút gọn che giấu đích đến, hoặc link tải mã độc APK.\n")
    p.add_run("• ")
    p.add_run("Cách lọc trong Excel: ").bold = True
    p.add_run("Dùng bộ lọc (Filter) cột `message`, tìm kiếm các từ khóa: `http`, `https`, `.com`, `.vn`, `.top`, `.vip`, `bit.ly`, `tinyurl`, `link`, `truy cap`, `apk`.\n")
    p.add_run("• ")
    p.add_run("Nhiệm vụ gán nhãn: ").bold = True
    p.add_run("Với mỗi tin nhắn được chọn, bóc tách chính xác tên miền độc hại và ghi rõ dấu hiệu kỹ thuật (ví dụ: typosquatting giả mạo Vietcombank thành `vietcombankk-login.com`, link rút gọn không rõ nguồn gốc).\n")
    p.add_run("• ")
    p.add_run("Chỉ tiêu: ").bold = True
    p.add_run("25 – 30 mẫu lừa đảo liên quan đến URL.")

    # Member 3
    format_heading(doc.add_paragraph(), "2.2. Thành viên 3 — Phụ trách Ghế 2: Hồ sơ Đòn bẩy Tâm lý (ROLE_SOC_ENG)", level=2)
    p = doc.add_paragraph()
    p.add_run("• ")
    p.add_run("Mục tiêu giám định: ").bold = True
    p.add_run("Phát hiện các thủ thuật thao túng tâm lý: gây hoảng sợ (đe dọa tố tụng, dọa bắt giam, dọa phạt nguội), kích thích lòng tham (trúng thưởng xe SH, quà tri ân), ép buộc thời gian gấp gáp.\n")
    p.add_run("• ")
    p.add_run("Cách lọc trong Excel: ").bold = True
    p.add_run("Tìm kiếm các từ khóa: `cong an`, `vien kiem sat`, `phat nguoi`, `bien so`, `khoa the trong`, `24h`, `ngay lap tuc`, `trung thuong`, `qua tri an`, `tuyen dung`, `viec lam online`.\n")
    p.add_run("• ")
    p.add_run("Nhiệm vụ gán nhãn: ").bold = True
    p.add_run("Xác định loại đòn bẩy tâm lý (Fear - Sợ hãi / Greed - Lòng tham / Urgency - Ép thời gian) và chấm điểm mức độ khẩn cấp (Urgency Score từ 0 đến 100).\n")
    p.add_run("• ")
    p.add_run("Chỉ tiêu: ").bold = True
    p.add_run("25 – 30 mẫu lừa đảo tâm lý (chú ý chọn cả các mẫu KHÔNG CÓ LINK để kiểm tra xem AI có hiểu ngữ nghĩa không).")

    # Member 4
    format_heading(doc.add_paragraph(), "2.3. Thành viên 4 — Phụ trách Ghế 3: Phân tích Teencode & Tiếng Việt Dị bản (ROLE_VN_TEENCODE)", level=2)
    p = doc.add_paragraph()
    p.add_run("• ")
    p.add_run("Mục tiêu giám định: ").bold = True
    p.add_run("Thử thách khả năng giải mã ngôn ngữ của AI đối với tin nhắn lừa đảo cố tình viết sai chính tả, thay số bằng chữ, viết tắt, không dấu hoặc chèn ký tự lạ để né tránh bộ lọc viễn thông.\n")
    p.add_run("• ")
    p.add_run("Cách lọc trong Excel: ").bold = True
    p.add_run("Tìm kiếm các mẫu tin nhắn không dấu, hoặc có các biến thể ký tự như: `t4i kh04n`, `chuy3n ti3n`, `n9an h4n9`, `k0`, `dc`, `nh4n qu4`, các ký tự cách nhau bất thường.\n")
    p.add_run("• ")
    p.add_run("Nhiệm vụ gán nhãn: ").bold = True
    p.add_run("Liệt kê các từ teencode có trong câu và tự tay viết lại một câu tiếng Việt chuẩn (Normalized sentence) để làm đáp án chuẩn đối chiếu (Ground Truth).\n")
    p.add_run("• ")
    p.add_run("Chỉ tiêu: ").bold = True
    p.add_run("25 – 30 mẫu teencode / tiếng Việt dị dạng.")

    # Member 5
    format_heading(doc.add_paragraph(), "2.4. Thành viên 5 — Phụ trách Ghế 4 (Ngân hàng) & Ghế 5 (Public Defender / HAM)", level=2)
    p = doc.add_paragraph()
    p.add_run("• ")
    p.add_run("Mục tiêu giám định: ").bold = True
    p.add_run("Gồm 2 nhiệm vụ sống còn: (1) Kiểm định vi phạm quy tắc ngân hàng/sinh trắc học; và (2) Thử thách chống báo động giả (False Positive) trên tin nhắn bình thường.\n")
    p.add_run("• ")
    p.add_run("Phần A (15 mẫu Scam Ngân hàng): ").bold = True
    p.add_run("Lọc tin nhắn mạo danh Vietcombank, Techcombank, MB Bank, VPBank... đòi hoàn phí, nộp phí, khóa tài khoản, hoặc bấm link để cập nhật sinh trắc học VNeID (trái Quyết định 2345/QĐ-NHNN).\n")
    p.add_run("• ")
    p.add_run("Phần B (15 mẫu HAM Hợp pháp): ").bold = True
    p.add_run("Lọc các tin nhắn nhãn `0` (HAM) nhưng có câu chữ dễ khiến AI hiểu lầm, ví dụ: Tin nhắn thông báo mã OTP thật của Techcombank/MobiFone, tin báo nợ cước điện lực thật, tin khuyến mãi nạp thẻ hợp pháp. Thành viên cần chỉ rõ căn cứ chứng minh đây là tin nhắn an toàn.\n")
    p.add_run("• ")
    p.add_run("Chỉ tiêu: ").bold = True
    p.add_run("Tổng cộng 30 mẫu (15 Scam Ngân hàng + 15 HAM Hợp pháp).")

    # SECTION 3
    format_heading(doc.add_paragraph(), "3. Phương Thức Bàn Giao & Định Dạng Mẫu (Deliverables)", level=1)
    
    p = doc.add_paragraph()
    p.add_run("Thành viên có thể bàn giao sản phẩm bằng file ")
    p.add_run("Excel (.xlsx)").bold = True
    p.add_run(" hoặc file ")
    p.add_run("JSON Lines (.jsonl)").bold = True
    p.add_run(". Mỗi bản ghi bắt buộc phải có đầy đủ 6 cột dữ liệu theo đúng chuẩn sau:")

    # Table Schema
    table_schema = doc.add_table(rows=8, cols=3)
    table_schema.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_schema.autofit = False
    set_table_borders(table_schema)
    
    headers = ["Tên trường (Field)", "Kiểu dữ liệu", "Mô tả chi tiết & Ví dụ"]
    for j, h in enumerate(headers):
        cell = table_schema.rows[0].cells[j]
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    cols_width = [Inches(1.6), Inches(1.1), Inches(3.8)]
    
    rows_data = [
        ("sample_id", "String", "Mã định danh duy nhất của mẫu. Quy ước: URL_01 đến URL_30, SOC_01 đến SOC_30, TEEN_01 đến TEEN_30, BANK_01 đến BANK_30."),
        ("data_source", "String", "Nguồn gốc xuất xứ của mẫu tin nhắn (Bắt buộc phục vụ truy vết - Provenance Tracking). Ví dụ: 'vietnamese_sms_merged_all.csv', 'canhbao.khonggianmang.vn', 'vietcombank_canhbao_2026', 'chongluadao.vn'."),
        ("raw_message", "String", "Nội dung nguyên văn của tin nhắn SMS lấy từ dataset hoặc nguồn cảnh báo, không tự ý sửa đổi ký tự."),
        ("gold_label", "String", "Nhãn chuẩn thực tế: Bắt buộc là 'SCAM' hoặc 'HAM'."),
        ("task_role", "String", "Vai trò tương ứng: 'ROLE_CYBER_URL', 'ROLE_SOC_ENG', 'ROLE_VN_TEENCODE', 'ROLE_BANK_VERIFY', 'ROLE_DEFENDER'."),
        ("key_evidence", "String", "Bằng chứng cốt lõi giải thích vì sao câu này là Lừa đảo (hoặc vì sao là Hợp pháp)."),
        ("sub_metadata", "JSON / Text", "Thông tin trích xuất mở rộng: tên miền độc hại, danh sách từ teencode, loại đòn tâm lý, hoặc tên ngân hàng bị mạo danh.")
    ]
    
    for i, (f_name, f_type, f_desc) in enumerate(rows_data):
        row = table_schema.rows[i+1]
        for j, text in enumerate([f_name, f_type, f_desc]):
            cell = row.cells[j]
            cell.width = cols_width[j]
            set_cell_background(cell, "FFFFFF" if i % 2 == 0 else "F8FAFC")
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if j == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(30, 58, 138)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Example Code block
    p_ex_title = doc.add_paragraph()
    p_ex_title.add_run("Ví dụ các bản ghi JSONL chuẩn quy cách (Đầy đủ trường data_source truy vết):").bold = True
    
    p_ex = doc.add_paragraph()
    ex_json = (
        '// Ví dụ 1: Mẫu trích xuất từ dataset nội bộ có sẵn trên Git\n'
        '{\n'
        '  "sample_id": "URL_01",\n'
        '  "task_role": "ROLE_CYBER_URL",\n'
        '  "data_source": "vietnamese_sms_merged_all.csv",\n'
        '  "gold_label": "SCAM",\n'
        '  "raw_message": "VPBank thong bao: the cua ban phat sinh giao dich 25.000.000d. Neu khong phai ban, truy cap http://vpbank-xacnhan.com de khoa the.",\n'
        '  "key_evidence": "Tên miền vpbank-xacnhan.com là giả mạo (typosquatting), tên miền chính thức của ngân hàng là vpbank.com.vn",\n'
        '  "sub_metadata": {"domain": "vpbank-xacnhan.com", "technique": "typosquatting", "target_brand": "VPBank"}\n'
        '}\n\n'
        '// Ví dụ 2: Mẫu bổ sung từ nguồn cảnh báo chính thống bên ngoài khi dataset thiếu\n'
        '{\n'
        '  "sample_id": "BANK_05",\n'
        '  "task_role": "ROLE_BANK_VERIFY",\n'
        '  "data_source": "canhbao.khonggianmang.vn/canh-bao-sinh-trac-hoc-2026",\n'
        '  "gold_label": "SCAM",\n'
        '  "raw_message": "Vietcombank: Tu 01/07 bat buoc xac thuc sinh trac hoc VNeID de tranh khoa tai khoan. Truy cap https://vcb-sinhtrachoc.vn de hoan tat trong 24h.",\n'
        '  "key_evidence": "Vi phạm Quyết định 2345/QĐ-NHNN: Ngân hàng chỉ cập nhật sinh trắc học trực tiếp trên App chính thức hoặc tại quầy, KHÔNG BAO GIỜ gửi link qua SMS.",\n'
        '  "sub_metadata": {"regulation_violated": "QD_2345_NHNN", "target_brand": "Vietcombank"}\n'
        '}'
    )
    r_ex = p_ex.add_run(ex_json)
    r_ex.font.name = "Consolas"
    r_ex.font.size = Pt(8.5)
    r_ex.font.color.rgb = RGBColor(15, 23, 42)
    p_ex.paragraph_format.left_indent = Inches(0.4)

    # SECTION 4 - CRITICAL
    format_heading(doc.add_paragraph(), "4. Quy Trình Xử Lý Khi Dữ Liệu Bị Thiếu Hoặc Không Đủ Số Lượng", level=1)
    
    p = doc.add_paragraph()
    p.add_run("Trong quá trình lọc file `vietnamese_sms_merged_all.csv`, nếu thành viên gặp tình huống: ")
    p.add_run("Không tìm đủ 25–30 mẫu").bold = True
    p.add_run(" cho chuyên đề của mình (ví dụ: mảng Teencode chỉ lọc được 15 câu, hoặc mảng Sinh trắc học VNeID chỉ có 8 câu), thành viên ")
    p.add_run("TUYỆT ĐỐI KHÔNG TỰ BỊA ĐẶT TIN NHẮN").bold = True
    p.add_run(" mà bắt buộc phải tuân thủ quy trình xử lý 3 bước dưới đây:")

    format_heading(doc.add_paragraph(), "Bước 1: Khai thác kho tệp dữ liệu dự phòng có sẵn trong thư mục data/raw/", level=2)
    p = doc.add_paragraph()
    p.add_run("Trong thư mục `data/raw/` của dự án không chỉ có 1 file, mà có tới 4 tệp dữ liệu khác nhau. Nếu file chính không đủ, hãy mở tiếp các file sau để gom đủ số lượng:\n")
    p.add_run("1. ")
    p.add_run("hf_vietnamese_sms_phishing_sample_300.csv: ").bold = True
    p.add_run("Chứa 601 mẫu tin nhắn lừa đảo chuyên sâu về giả mạo thương hiệu, hoàn tiền và ngân hàng. Cực kỳ hữu ích cho Thành viên 2 (URL) và Thành viên 5 (Ngân hàng).\n")
    p.add_run("2. ")
    p.add_run("hf_vietnamese_sms_dataset.csv: ").bold = True
    p.add_run("Kho dữ liệu thô gần 6.000 tin nhắn tổng hợp. Rất nhiều biến thể tiếng lóng đời thường dành cho Thành viên 4 (Teencode).\n")
    p.add_run("3. ")
    p.add_run("vietnamese_sms_full.csv: ").bold = True
    p.add_run("Tập hợp gần 3.000 mẫu tin nhắn trước bước khử trùng lặp.")

    format_heading(doc.add_paragraph(), "Bước 2: Thu thập bổ sung từ Nguồn Cảnh báo Chính thống (Trusted Public Sources)", level=2)
    p = doc.add_paragraph()
    p.add_run("Nếu đã vét cạn các file trong `data/raw/` mà vẫn thiếu một số dạng lừa đảo thế hệ mới (ví dụ: lừa đảo cập nhật sinh trắc học theo Quyết định 2345/QĐ-NHNN mới ban hành năm 2024–2026), thành viên được phép bổ sung mẫu thực tế từ các nguồn uy tín sau:\n")
    p.add_run("• ")
    p.add_run("Cổng Cảnh báo An toàn Không gian mạng Việt Nam (Cục An toàn thông tin - Bộ TT&TT): ").bold = True
    p.add_run("https://canhbao.khonggianmang.vn/ hoặc trang web Dự án Chống Lừa Đảo (https://chongluadao.vn).\n")
    p.add_run("• ")
    p.add_run("Cảnh báo chính thức từ các Ngân hàng lớn: ").bold = True
    p.add_run("Chuyên mục 'Cảnh báo lừa đảo' trên website của Vietcombank, Techcombank, MB, BIDV hoặc Fanpage Facebook có tích xanh chính chủ.\n")
    p.add_run("• ")
    p.add_run("Các phóng sự điều tra và tin bài cảnh báo trên báo chí chính thống: ").bold = True
    p.add_run("VnExpress, Tuổi Trẻ, Thanh Niên, Báo Công an Nhân dân, Cổng thông tin điện tử Bộ Công an.")

    format_heading(doc.add_paragraph(), "Bước 3: Ghi nhận vết nguồn gốc (Provenance Tracking) & Quy tắc Đạo đức RBL", level=2)
    
    add_callout(doc,
        "1. TUYỆT ĐỐI KHÔNG TỰ BỊA ĐẶT TIN NHẮN (NO SYNTHETIC FABRICATION): Ngữ pháp và thủ đoạn của tội phạm mạng thật có những sắc thái tâm lý và lỗi chính tả rất đặc thù mà người bình thường tự nghĩ ra không thể mô phỏng chính xác. Bịa tin nhắn sẽ làm sai lệch kết quả benchmark của AI.\n"
        "2. BẮT BUỘC GHI NGUỒN GỐC: Với mọi mẫu tin nhắn lấy ngoài tập dữ liệu chính, phải ghi rõ nguồn trong metadata (ví dụ: source: 'canhbao_khonggianmang_2026' hoặc source: 'vietcombank_canhbao_thang9_2026').\n"
        "3. NGUYÊN TẮC 'CHẤT LƯỢNG HƠN SỐ LƯỢNG': Thà có 20 mẫu thật sự tinh vi, đại diện đúng cho bài toán lừa đảo phức tạp tại Việt Nam, còn hơn gom cho đủ 30 mẫu tin rác đơn giản lặp đi lặp lại.",
        title="3 NGUYÊN TẮC VÀNG VỀ LIÊM CHÍNH DỮ LIỆU KHOA HỌC",
        box_type="danger"
    )

    # SECTION 5
    format_heading(doc.add_paragraph(), "5. Kế Hoạch Phối Hợp & Lịch Trình Thực Hiện", level=1)
    
    p = doc.add_paragraph()
    p.add_run("Để kịp tiến độ thực nghiệm và phân tích dữ liệu báo cáo cô Chi, các mốc thời gian được quy định như sau:")

    table_timeline = doc.add_table(rows=4, cols=3)
    table_timeline.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_timeline.autofit = False
    set_table_borders(table_timeline)
    
    t_headers = ["Mốc thời gian", "Nhiệm vụ của 4 Thành viên", "Nhiệm vụ của Tech Lead (Bạn)"]
    for j, h in enumerate(t_headers):
        cell = table_timeline.rows[0].cells[j]
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    t_widths = [Inches(1.5), Inches(2.6), Inches(2.4)]
    t_rows = [
        ("Giai đoạn 1 (Ngày 1)", "Tải file dữ liệu, lọc và gán nhãn xong 25-30 mẫu theo đúng chuyên đề. Gửi file cho Lead.", "Khởi tạo database benchmark.db từ seed, hoàn thiện runner kết nối API 3 hãng."),
        ("Giai đoạn 2 (Ngày 2)", "Cùng Lead kiểm tra tính hợp lệ của đề thi; tham gia giám định kết quả chạy thử.", "Ghép 4 file thành Master Suite, bấm lệnh chạy kiểm thử qua 11 model."),
        ("Giai đoạn 3 (Ngày 3)", "Viết 1 đoạn nhận xét chuyên sâu về các ca model bị đánh lừa ở mảng của mình.", "Xuất Bảng Ma trận Năng lực, cùng cả nhóm chốt cặp model Maker-Checker cho 5 ghế.")
    ]
    
    for i, (t_col0, t_col1, t_col2) in enumerate(t_rows):
        row = table_timeline.rows[i+1]
        for j, text in enumerate([t_col0, t_col1, t_col2]):
            cell = row.cells[j]
            cell.width = t_widths[j]
            set_cell_background(cell, "FFFFFF" if i % 2 == 0 else "F8FAFC")
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if j == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    p_end = doc.add_paragraph()
    p_end.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_end = p_end.add_run("BAN KỸ THUẬT & HỆ THỐNG — DỰ ÁN SCAMSHIELD-VN\nLưu hành nội bộ phục vụ Nghiên cứu RBL")
    r_end.font.name = "Calibri"
    r_end.font.size = Pt(9.5)
    r_end.font.italic = True
    r_end.font.color.rgb = RGBColor(100, 116, 139)
    
    # Save document
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "HUONG_DAN_LOC_VA_GAN_NHAN_BENCHMARK_COUNCIL.docx")
    try:
        doc.save(output_path)
        print(f"Document successfully created at: {output_path}")
    except PermissionError:
        output_path_alt = os.path.join(output_dir, "HUONG_DAN_LOC_VA_GAN_NHAN_BENCHMARK_COUNCIL_UPDATED.docx")
        doc.save(output_path_alt)
        print(f"Original file is locked by Word. Document saved to: {output_path_alt}")

if __name__ == "__main__":
    create_document()
