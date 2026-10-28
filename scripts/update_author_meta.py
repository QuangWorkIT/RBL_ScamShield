# -*- coding: utf-8 -*-
with open('paper/main.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update author block
old_author = '''\\author{
    Nguyen Trung Hieu$^{1,*}$,
    Nguyen Minh Quang$^{1}$,
    Hoang Hai Phuc$^{1}$,
    Phan Tran Hoang Tran$^{1}$, and
    Nguyen Quoc Huy$^{1}\\\\[0.4em]
    $^{1}$Department of Software Engineering, FPT University, Ho Chi Minh City, Vietnam\\\\[0.2em]
    Email: cristand2825@gmail.com (N.T.H.); nguyenminhquangnmqlamdong@gmail.com (N.M.Q.); haiphuchoang2675@gmail.com (H.H.P.);\\\\
    pthoangtran0511@gmail.com (P.T.H.T.); nguyenhuy.se205@gmail.com (N.Q.H.)\\\\[0.2em]
    $^*$Corresponding author
}'''

new_author = '''\\author{
    Nguyen Trung Hieu$^{1}$,
    Nguyen Minh Quang$^{1,*}$,
    Hoang Hai Phuc$^{1}$,
    Phan Tran Hoang Tran$^{1}$, and
    Nguyen Quoc Huy$^{1}\\\\[0.4em]
    $^{1}$Department of Software Engineering, FPT University, Ho Chi Minh City, Vietnam\\\\[0.2em]
    Email: cristand2825@gmail.com (N.T.H.); nguyenminhquangnmqlamdong@gmail.com (N.M.Q.); haiphuchoang2675@gmail.com (H.H.P.);\\\\
    annaphan0511@gmail.com (P.T.H.T.); nguyenhuy.se205@gmail.com (N.Q.H.)\\\\[0.2em]
    $^*$Corresponding author
}'''

# Replace regardless of CRLF
text = text.replace(old_author.replace('\r\n', '\n'), new_author.replace('\r\n', '\n'))
text = text.replace(old_author.replace('\n', '\r\n'), new_author.replace('\n', '\r\n'))

# 2. Update Author Contributions in main.tex
old_contrib = '''\\section*{Author Contributions}
Nguyen Trung Hieu: Conceptualization, Methodology, Formal analysis, Writing -- Original Draft, Project administration.
Nguyen Minh Quang: Supervision, Verification, Ethical review, Acquisition of Funds.
Hoang Hai Phuc: Validation, Model benchmarking, Statistical testing, Visualization. 
Phan Tran Hoang Tran: Resources, Data collection, Literature review, Writing -- Review \\& Editing.
Nguyen Quoc Huy: Software, Pipeline architecture, Data curation, Investigation. 
All authors have read and agreed to the published version of the manuscript.'''

new_contrib = '''\\section*{Author Contributions}
Nguyen Trung Hieu: Conceptualization, Methodology, Formal analysis, Writing -- Original Draft, Project administration. 
Nguyen Minh Quang: Supervision, Verification, Ethical review. 
Hoang Hai Phuc: Validation, Model benchmarking, Statistical testing, Visualization. 
Phan Tran Hoang Tran: Resources, Data collection, Literature review, Funding acquisition, Writing -- Review \\& Editing. 
Nguyen Quoc Huy: Software, Pipeline architecture, Data curation, Investigation. 
All authors have read and agreed to the published version of the manuscript.'''

text = text.replace(old_contrib.replace('\r\n', '\n'), new_contrib.replace('\r\n', '\n'))
text = text.replace(old_contrib.replace('\n', '\r\n'), new_contrib.replace('\n', '\r\n'))

with open('paper/main.tex', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated paper/main.tex with confirmed team metadata!')
