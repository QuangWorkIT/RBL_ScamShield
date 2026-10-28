import os

sections_order = [
    '00_abstract.tex',
    '01_intro.tex',
    '02_related.tex',
    '03_method.tex',
    '04_results.tex',
    '05_conclusion.tex',
    '06_endmatter.tex'
]

preamble = r'''\documentclass[journal]{IEEEtran}
\usepackage{iftex}
\ifPDFTeX
  \usepackage[utf8]{inputenc}
  % Vietnamese Unicode characters fallback support for pdfLaTeX
  \DeclareUnicodeCharacter{1EBF}{\^e}
  \DeclareUnicodeCharacter{1EBE}{\^E}
  \DeclareUnicodeCharacter{1EBD}{\~e}
  \DeclareUnicodeCharacter{1EBC}{\~E}
  \DeclareUnicodeCharacter{1EC7}{\d{\^e}}
  \DeclareUnicodeCharacter{1EC6}{\d{\^E}}
  \DeclareUnicodeCharacter{1EC1}{\`{\^e}}
  \DeclareUnicodeCharacter{1EC0}{\`{\^E}}
  \DeclareUnicodeCharacter{0110}{\DJ}
  \DeclareUnicodeCharacter{0111}{\dj}
  \DeclareUnicodeCharacter{2014}{---}
  \DeclareUnicodeCharacter{2013}{--}
\fi
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath,amssymb}
\usepackage[hidelinks]{hyperref}
\usepackage{cite}
\usepackage{microtype}
\usepackage{multirow}
\usepackage{tabularx}
\usepackage{xurl}

% Whitespace optimization macros for strict 8-page budget
\setlength{\textfloatsep}{7pt plus 1.0pt minus 1.0pt}
\setlength{\floatsep}{6pt plus 1.0pt minus 1.0pt}
\setlength{\intextsep}{6pt plus 1.0pt minus 1.0pt}
\setlength{\abovecaptionskip}{4pt}
\setlength{\belowcaptionskip}{2pt}
\def\IEEEbibitemsep{0pt plus .5pt}

\begin{document}

\renewcommand{\thesection}{\Roman{section}}
\renewcommand{\thesubsection}{\thesection.\Alph{subsection}}

\title{ScamShield-VN: Evidence-Driven Two-Tier Architecture for Vietnamese Scam and Phishing Detection}

\author{
    Nguyen Trung Hieu$^{1}$,
    Nguyen Minh Quang$^{1,*}$,
    Hoang Hai Phuc$^{1}$,
    Phan Tran Hoang Tran$^{1}$,
    Nguyen Quoc Huy$^{1}$, and
    Le Thi Quynh Chi$^{1}$\\[0.4em]
    $^{1}$Department of Software Engineering, FPT University, Ho Chi Minh City, Vietnam\\[0.2em]
    Email: cristand2825@gmail.com (N.T.H.); nguyenminhquangnmqlamdong@gmail.com (N.M.Q.);\\
    haiphuchoang2675@gmail.com (H.H.P.); annaphan0511@gmail.com (P.T.H.T.);\\
    nguyenhuy.se205@gmail.com (N.Q.H.); chiltq6@fe.edu.vn (L.T.Q.C.)\\[0.2em]
    $^*$Corresponding author
}

\maketitle

\begin{abstract}
'''

abstract_text = open('paper/sections/00_abstract.tex', encoding='utf-8').read().strip()
keywords_block = r'''
\end{abstract}

\begin{IEEEkeywords}
scam detection, phishing detection, large language models, cost-sensitive learning, Vietnamese NLP, edge AI, multi-agent consensus
\end{IEEEkeywords}

'''

body = []
for s in sections_order[1:]:
    p = os.path.join('paper/sections', s)
    body.append(open(p, encoding='utf-8').read().strip())

footer = r'''
\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
'''

full_main = preamble + abstract_text + keywords_block + '\n\n'.join(body) + footer

with open('paper/main.tex', 'w', encoding='utf-8') as f:
    f.write(full_main)

print('Assembled paper/main.tex successfully!')
print('Total characters:', len(full_main))
print('Total lines:', full_main.count('\n'))
