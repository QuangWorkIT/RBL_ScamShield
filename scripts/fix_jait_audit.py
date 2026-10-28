# -*- coding: utf-8 -*-
"""
Fix all issues identified in paper/quality/jait_compliance_audit_report.md
"""
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Headings to ALL CAPS
    content = content.replace(r'\section{Introduction}', r'\section{INTRODUCTION}')
    content = content.replace(r'\section{Literature Review}', r'\section{LITERATURE REVIEW}')
    content = content.replace(r'\section{Materials and Methods}', r'\section{MATERIALS AND METHODS}')
    content = content.replace(r'\section{Result and Discussion}', r'\section{RESULT AND DISCUSSION}')
    content = content.replace(r'\section{Conclusion}', r'\section{CONCLUSION}')

    # 2. Section cross-reference
    content = content.replace(r'Section~\ref{sec:methods}', r'Section~\ref{sec:method}')

    # 3. Model size in Table
    content = content.replace(r'& \textbf{390 MB} \\', r'& \textbf{98.4 MB (INT8)} \\')

    # 4. Intro contribution
    content = content.replace(
        r'quantize the model via ONNX INT8 ($390\text{ MB}$, $15.8\text{ ms}$ on CPU)',
        r'quantize the model via ONNX INT8 ($98.4\text{ MB}$, $70.7\text{ ms}$ on consumer CPU; baseline FP32: $390.5\text{ MB}$)'
    )

    # 5. Conclusion
    idx = content.find('exporting via ONNX INT8 quantization')
    if idx != -1:
        end_idx = content.find(', the Tier 1', idx)
        if end_idx != -1:
            target = content[idx:end_idx]
            replacement = r'exporting via ONNX INT8 quantization ($98.4\text{ MB}$, $70.7\text{ ms}$ on consumer CPU)'
            content = content.replace(target, replacement, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    new_abstract = (
        r'Telecommunications fraud and smishing campaigns in Vietnam inflict severe losses by exploiting '
        r'localized linguistic evasion, including regional slang, teencode abbreviations, and diacritic-stripped text. '
        r'Existing defenses either suffer from elevated false-negative rates under symmetric loss functions or induce '
        r'severe alarm fatigue when relying on cloud Large Language Models. We propose ScamShield-VN, an evidence-grounded '
        r'two-tier architecture pairing an on-device edge screener with an Occam-optimized three-agent forensic council. '
        r'Tier 1 deploys ViSoBERT fine-tuned with Cost-Sensitive Weighted Binary Cross-Entropy loss ($\alpha=5.0$) '
        r'and quantized via ONNX INT8. Ambiguous edge cases are escalated to Tier 2, which incorporates an adversarial '
        r'Public Defender agent to eliminate false alarms on legitimate banking notifications. Evaluated across five '
        r'deterministic seeds on an isolated frozen test partition ($N=267$) from a curated corpus of 2,664 Vietnamese '
        r'messages (1,918 Ham, 746 Scam), ViSoBERT achieves a Scam Recall of $95.62\% \pm 2.25\%$ and Macro-F1 of '
        r'$92.51\% \pm 2.39\%$, outperforming Gemini 3.5 Flash ($p < 0.0001$, McNemar test) while operating at '
        r'$70.7\text{ ms}$ on consumer CPU with a $98.4\text{ MB}$ footprint. On the combined benchmark ($N=384$), '
        r'the system resolves $96.6\%$ of traffic locally, achieving $97.40\%$ accuracy, $97.11\%$ scam recall, and '
        r'$0.00\%$ false alarms on banking alerts at $267.5\text{ ms}$ mean latency. McNemar testing demonstrates no '
        r'statistically significant difference between three-agent and five-agent council configurations ($p = 0.0736$), '
        r'while reducing API costs by $40\%$. These findings validate that coupling cost-sensitive edge encoders with '
        r'deliberative multi-agent councils delivers Pareto-optimal telecommunications fraud defense.'
    )

    # 1. Fix modular sections
    with open('paper/sections/00_abstract.tex', 'w', encoding='utf-8') as f:
        f.write(new_abstract)

    for sec in ['01_intro.tex', '02_related.tex', '03_method.tex', '04_results.tex', '05_conclusion.tex']:
        fix_file(f'paper/sections/{sec}')

    # 2. Fix paper/main.tex
    with open('paper/main.tex', 'r', encoding='utf-8') as f:
        main_tex = f.read()

    # Roman numeral formatting
    roman_decl = (
        '\\begin{document}\n\n'
        '\\renewcommand{\\thesection}{\\Roman{section}}\n'
        '\\renewcommand{\\thesubsection}{\\thesection.\\Alph{subsection}}'
    )
    if '\\renewcommand{\\thesection}{\\Roman{section}}' not in main_tex:
        main_tex = main_tex.replace('\\begin{document}', roman_decl, 1)

    # Replace abstract in main.tex
    main_tex = re.sub(
        r'(\\begin\{abstract\}).*?(\\end\{abstract\})',
        r'\1\n' + new_abstract.replace('\\', '\\\\') + r'\n\2',
        main_tex,
        flags=re.DOTALL
    )

    with open('paper/main.tex', 'w', encoding='utf-8') as f:
        f.write(main_tex)

    fix_file('paper/main.tex')
    print('All files fixed according to jait_compliance_audit_report.md successfully.')

if __name__ == '__main__':
    main()
