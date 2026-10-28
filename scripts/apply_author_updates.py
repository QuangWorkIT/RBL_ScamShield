# -*- coding: utf-8 -*-
with open('paper/main.tex', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_author_lines = [
    "\\author{\n",
    "    Nguyen Trung Hieu$^{1}$,\n",
    "    Nguyen Minh Quang$^{1,*}$,\n",
    "    Hoang Hai Phuc$^{1}$,\n",
    "    Phan Tran Hoang Tran$^{1}$, and\n",
    "    Nguyen Quoc Huy$^{1}$\\\\[0.4em]\n",
    "    $^{1}$Department of Software Engineering, FPT University, Ho Chi Minh City, Vietnam\\\\[0.2em]\n",
    "    Email: cristand2825@gmail.com (N.T.H.); nguyenminhquangnmqlamdong@gmail.com (N.M.Q.); haiphuchoang2675@gmail.com (H.H.P.);\\\\\n",
    "    annaphan0511@gmail.com (P.T.H.T.); nguyenhuy.se205@gmail.com (N.Q.H.)\\\\[0.2em]\n",
    "    $^*$Corresponding author\n",
    "}\n"
]

# Find \author{ and \maketitle
start_idx = -1
end_idx = -1
for i, l in enumerate(lines):
    if l.strip().startswith(r'\author{'):
        start_idx = i
    if l.strip().startswith(r'\maketitle'):
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    lines[start_idx:end_idx] = new_author_lines + ["\n"]
    print("Replaced author lines successfully from index", start_idx, "to", end_idx)

# Find and replace Author Contributions
contrib_start = -1
contrib_end = -1
for i, l in enumerate(lines):
    if r'\section*{Author Contributions}' in l:
        contrib_start = i
    if r'\section*{Funding}' in l:
        contrib_end = i
        break

new_contrib_lines = [
    "\\section*{Author Contributions}\n",
    "Nguyen Trung Hieu: Conceptualization, Methodology, Formal analysis, Writing -- Original Draft, Project administration.\n",
    "Nguyen Minh Quang: Supervision, Verification, Ethical review.\n",
    "Hoang Hai Phuc: Validation, Model benchmarking, Statistical testing, Visualization.\n",
    "Phan Tran Hoang Tran: Resources, Data collection, Literature review, Funding acquisition, Writing -- Review \\& Editing.\n",
    "Nguyen Quoc Huy: Software, Pipeline architecture, Data curation, Investigation.\n",
    "All authors have read and agreed to the published version of the manuscript.\n",
    "\n"
]

if contrib_start != -1 and contrib_end != -1:
    lines[contrib_start:contrib_end] = new_contrib_lines
    print("Replaced Author Contributions successfully from index", contrib_start, "to", contrib_end)

with open('paper/main.tex', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Updated paper/main.tex successfully!")
