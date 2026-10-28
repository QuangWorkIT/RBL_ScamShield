# -*- coding: utf-8 -*-
"""
Move supervisor Le Thi Quynh Chi to the last position in author list and contributions.
"""
import zipfile, os

def update_authors_last():
    # 1. Update main.tex
    with open('paper/main.tex', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find author block
    start_auth = None
    end_auth = None
    for i, line in enumerate(lines):
        if r'\author{' in line:
            start_auth = i
        if start_auth is not None and line.strip() == '}':
            end_auth = i
            break

    assert start_auth is not None and end_auth is not None

    new_author_lines = [
        "\\author{\n",
        "    Nguyen Trung Hieu$^{1}$,\n",
        "    Nguyen Minh Quang$^{1,*}$,\n",
        "    Hoang Hai Phuc$^{1}$,\n",
        "    Phan Tran Hoang Tran$^{1}$,\n",
        "    Nguyen Quoc Huy$^{1}$, and\n",
        "    Le Thi Quynh Chi$^{1}$\\\\[0.4em]\n",
        "    $^{1}$Department of Software Engineering, FPT University, Ho Chi Minh City, Vietnam\\\\[0.2em]\n",
        "    Email: cristand2825@gmail.com (N.T.H.); nguyenminhquangnmqlamdong@gmail.com (N.M.Q.);\\\\\n",
        "    haiphuchoang2675@gmail.com (H.H.P.); annaphan0511@gmail.com (P.T.H.T.);\\\\\n",
        "    nguyenhuy.se205@gmail.com (N.Q.H.); chiltq6@fpt.edu.vn (L.T.Q.C.)\\\\[0.2em]\n",
        "    $^*$Corresponding author\n",
        "}\n"
    ]

    lines[start_auth:end_auth+1] = new_author_lines

    # Find Author Contributions in main.tex
    start_contrib = None
    end_contrib = None
    for i, line in enumerate(lines):
        if r'\section*{Author Contributions}' in line:
            start_contrib = i
        if start_contrib is not None and r'\section*{Funding}' in line:
            end_contrib = i - 1
            break

    assert start_contrib is not None and end_contrib is not None

    new_contrib_lines = [
        "\\section*{Author Contributions}\n",
        "Nguyen Trung Hieu: Conceptualization, Methodology, Formal analysis, Writing -- Original Draft, Project administration.\n",
        "Nguyen Minh Quang: Supervision, Verification, Ethical review.\n",
        "Hoang Hai Phuc: Validation, Model benchmarking, Statistical testing, Visualization.\n",
        "Phan Tran Hoang Tran: Resources, Data collection, Literature review, Funding acquisition, Writing -- Review \\& Editing.\n",
        "Nguyen Quoc Huy: Software, Pipeline architecture, Data curation, Investigation.\n",
        "Le Thi Quynh Chi: Academic supervision, Conceptual validation, Writing -- Review \\& Editing.\n",
        "All authors have read and agreed to the published version of the manuscript.\n",
        "\n"
    ]

    lines[start_contrib:end_contrib+1] = new_contrib_lines

    with open('paper/main.tex', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Updated paper/main.tex successfully!")

    # 2. Update paper/sections/06_endmatter.tex
    with open('paper/sections/06_endmatter.tex', 'r', encoding='utf-8') as f:
        end_lines = f.readlines()

    start_em_contrib = None
    end_em_contrib = None
    for i, line in enumerate(end_lines):
        if r'\section*{Author Contributions}' in line:
            start_em_contrib = i
        if start_em_contrib is not None and r'\section*{Funding}' in line:
            end_em_contrib = i - 1
            break

    assert start_em_contrib is not None and end_em_contrib is not None
    end_lines[start_em_contrib:end_em_contrib+1] = new_contrib_lines

    with open('paper/sections/06_endmatter.tex', 'w', encoding='utf-8') as f:
        f.writelines(end_lines)
    print("Updated paper/sections/06_endmatter.tex successfully!")

    # 3. Check dollar balance in main.tex
    with open('paper/main.tex', 'r', encoding='utf-8') as f:
        full_text = f.read()
    clean_text = full_text.replace(r'\$', '')
    dollars = clean_text.count('$')
    print(f"main.tex total '$' count = {dollars} (Even: {dollars % 2 == 0})")
    assert dollars % 2 == 0, f"Unbalanced dollars: {dollars}"

    # 4. Repack ScamShield_Overleaf_Ready.zip
    zip_path = 'paper/ScamShield_Overleaf_Ready.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write('paper/main.tex', arcname='main.tex')
        z.write('paper/references.bib', arcname='references.bib')
        for f in os.listdir('paper/sections'):
            if f.endswith('.tex'):
                z.write(os.path.join('paper/sections', f), arcname=os.path.join('sections', f))
    print("Updated", zip_path, "successfully!")

if __name__ == '__main__':
    update_authors_last()
