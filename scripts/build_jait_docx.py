import re
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def create_jait_document():
    doc = docx.Document()

    # Section 1: Title & Authors (1 Column Full Width)
    s1 = doc.sections[0]
    s1.top_margin = Inches(0.75)
    s1.bottom_margin = Inches(0.75)
    s1.left_margin = Inches(0.75)
    s1.right_margin = Inches(0.75)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run('ScamShield-VN: Evidence-Grounded Two-Tier Architecture for Vietnamese Scam and Phishing Detection')
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(18)
    r_title.font.bold = True

    # Authors
    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_after = Pt(4)
    r_auth = p_auth.add_run('Nguyen Trung Hieu1,*, Le Quoc Huy1, Hoang Hai Phuc1, Phan Tran Hoang Tran1, and Nguyen Minh Quang1')
    r_auth.font.name = 'Times New Roman'
    r_auth.font.size = Pt(10.5)
    r_auth.font.bold = True

    # Affiliation & Email & Corresponding Author
    p_aff = doc.add_paragraph()
    p_aff.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aff.paragraph_format.space_after = Pt(14)
    r_aff = p_aff.add_run('1 Department of Software Engineering, FPT University, Ho Chi Minh City, Vietnam\n')
    r_aff.font.name = 'Times New Roman'
    r_aff.font.size = Pt(9.5)
    r_mail = p_aff.add_run('Email: cristand2825@gmail.com (N.T.H.); huylq@fpt.edu.vn (L.Q.H.); haiphuchoang2675@gmail.com (H.H.P.);\ntranpth@fpt.edu.vn (P.T.H.T.); quangnm@fpt.edu.vn (N.M.Q.)\n*Corresponding author')
    r_mail.font.name = 'Times New Roman'
    r_mail.font.size = Pt(9)

    # Section 1 ends at p_aff with continuous break; Section 2 (two columns) begins at paragraph 3 (Abstract)
    pPr = p_aff._p.get_or_add_pPr()
    sectPr = OxmlElement('w:sectPr')
    type_el = OxmlElement('w:type')
    type_el.set(qn('w:val'), 'continuous')
    sectPr.append(type_el)
    pgMar = OxmlElement('w:pgMar')
    pgMar.set(qn('w:top'), '1080')
    pgMar.set(qn('w:bottom'), '1080')
    pgMar.set(qn('w:left'), '1080')
    pgMar.set(qn('w:right'), '1080')
    sectPr.append(pgMar)
    pPr.append(sectPr)

    s2 = doc.sections[1]
    s2.top_margin = Inches(0.75)
    s2.bottom_margin = Inches(0.75)
    s2.left_margin = Inches(0.75)
    s2.right_margin = Inches(0.75)

    sectPr2 = s2._sectPr
    cols = sectPr2.find(qn('w:cols'))
    if cols is None:
        cols = OxmlElement('w:cols')
        sectPr2.append(cols)
    cols.set(qn('w:num'), '2')
    cols.set(qn('w:space'), '450') # 450 twips = 0.31 inch gap

    with open('paper/FULL_PAPER_PREVIEW.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_table = False
    table_lines = []

    for line in lines:
        raw = line.rstrip('\r\n')
        sline = raw.strip()

        # Skip headers already added in Section 1
        if sline.startswith('# ScamShield-VN:') or sline.startswith('> **Authors:**') or \
           sline.startswith('> **Target Venue:**') or sline.startswith('> **Affiliation:**') or \
           sline.startswith('> **Emails:**') or sline.startswith('> **Status:**') or \
           sline == '---' or sline.startswith('## Abstract'):
            continue

        # Abstract in Left Column
        if sline.startswith('Telecommunications fraud and smishing') or sline.startswith('Telecommunications scam and phishing'):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.05
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            r1 = p.add_run('Abstract—')
            r1.font.name = 'Times New Roman'
            r1.font.size = Pt(9)
            r1.font.bold = True
            r1.font.italic = True
            r2 = p.add_run(sline)
            r2.font.name = 'Times New Roman'
            r2.font.size = Pt(9)
            continue

        # Keywords in Left Column
        if sline.startswith('**Keywords:**'):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(10)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            r1 = p.add_run('Keywords—')
            r1.font.name = 'Times New Roman'
            r1.font.size = Pt(9)
            r1.font.bold = True
            r1.font.italic = True
            r2 = p.add_run(sline.replace('**Keywords:**', '').strip())
            r2.font.name = 'Times New Roman'
            r2.font.size = Pt(9)
            continue

        # Tables parsing
        if sline.startswith('```') and not in_table:
            in_table = True
            table_lines = []
            continue
        elif sline.startswith('```') and in_table:
            in_table = False
            if table_lines:
                header_title = ''
                content_rows = []
                for tl in table_lines:
                    if tl.startswith('TABLE '):
                        header_title = tl
                    elif '|' in tl:
                        parts = [p.strip() for p in tl.split('|')[1:-1]]
                        if any(c != '-' and c != '+' for c in ''.join(parts)):
                            content_rows.append(parts)
                if header_title:
                    hp = doc.add_paragraph()
                    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    hp.paragraph_format.space_before = Pt(8)
                    hp.paragraph_format.space_after = Pt(3)
                    hr = hp.add_run(header_title)
                    hr.font.name = 'Times New Roman'
                    hr.font.size = Pt(8.5)
                    hr.font.bold = True
                if content_rows:
                    t = doc.add_table(rows=len(content_rows), cols=len(content_rows[0]))
                    t.alignment = WD_TABLE_ALIGNMENT.CENTER
                    t.style = 'Table Grid'
                    for ri, row_data in enumerate(content_rows):
                        for ci, val in enumerate(row_data):
                            cell = t.cell(ri, ci)
                            cell.text = val
                            cp = cell.paragraphs[0]
                            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            cr = cp.runs[0]
                            cr.font.name = 'Times New Roman'
                            cr.font.size = Pt(7.5)
                            if ri == 0:
                                cr.font.bold = True
            table_lines = []
            continue

        if in_table:
            table_lines.append(sline)
            continue

        # Major Headings (Centered, Small Caps / All Caps Roman)
        if sline.startswith('## I. ') or sline.startswith('## II. ') or sline.startswith('## III. ') or \
           sline.startswith('## IV. ') or sline.startswith('## V. '):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(sline.replace('## ', ''))
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.font.bold = True
            continue

        # Subsections Level 2
        if sline.startswith('### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(3)
            r = p.add_run(sline.replace('### ', ''))
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.font.bold = True
            continue

        # Subsections Level 3
        if sline.startswith('#### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(sline.replace('#### ', ''))
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            r.font.italic = True
            continue

        # End-Matter Headings
        if sline.startswith('## Conflict of Interest') or sline.startswith('## Author Contributions') or \
           sline.startswith('## Funding') or sline.startswith('## Acknowledgment') or sline.startswith('## References'):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(sline.replace('## ', ''))
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.font.bold = True
            continue

        # Bullets
        if sline.startswith('- ') or sline.startswith('* '):
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(2)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            r = p.add_run(sline[2:])
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            continue

        # Numbered items in text
        if re.match(r'^\d+\.\s', sline):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.left_indent = Inches(0.2)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            r = p.add_run(sline)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            continue

        # References entries
        if sline.startswith('[') and ']' in sline[:5]:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.left_indent = Inches(0.2)
            p.paragraph_format.first_line_indent = Inches(-0.2)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            r = p.add_run(sline)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8)
            continue

        # Regular Body Paragraphs
        if sline:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.first_line_indent = Inches(0.15)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            r = p.add_run(sline)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)

    try:
        doc.save('paper/ScamShield_JAIT_Manuscript.docx')
        print('Updated paper/ScamShield_JAIT_Manuscript.docx')
    except PermissionError:
        print('ScamShield_JAIT_Manuscript.docx is open in Word. Saving to ScamShield_JAIT_TwoColumn.docx instead!')
    doc.save('paper/ScamShield_JAIT_TwoColumn.docx')
    print('Successfully generated paper/ScamShield_JAIT_TwoColumn.docx in exact JAIT 2-column layout!')

if __name__ == '__main__':
    create_jait_document()
