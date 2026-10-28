# -*- coding: utf-8 -*-
import os, sys, re

def main():
    print("=== FIXING LATEX COMPILATION ERRORS ===")

    # 1. Fix 02_related.tex (Council & Defender -> Council \& Defender)
    related_path = 'paper/sections/02_related.tex'
    with open(related_path, 'r', encoding='utf-8') as f:
        related_text = f.read()
    
    if 'Council & Defender' in related_text:
        related_text = related_text.replace('Council & Defender', r'Council \& Defender')
        with open(related_path, 'w', encoding='utf-8') as f:
            f.write(related_text)
        print("Fixed unescaped '&' in paper/sections/02_related.tex")
    else:
        print("Council & Defender not found in 02_related.tex")

    # 2. Fix 03_method.tex (Restore missing $ in Table III and paragraph)
    method_path = 'paper/sections/03_method.tex'
    with open(method_path, 'r', encoding='utf-8') as f:
        method_text = f.read()

    # Find the corrupted block from 'Table~\\ref{tab:dataset_sources} summarizes' to '\end{table}'
    start_str = r'Table~\ref{tab:dataset_sources} summarizes'
    idx_start = method_text.find(start_str)
    if idx_start != -1:
        idx_end = method_text.find(r'\end{table}', idx_start) + len(r'\end{table}')
        old_block = method_text[idx_start:idx_end]
        
        new_block = (
            r'Table~\ref{tab:dataset_sources} summarizes the sample counts and class balance across data sources and partitions. '
            r'Table~\ref{tab:partition_overlap} reports the overlap analysis across evaluation partitions. '
            r'The Frozen Test Partition ($N=267$) shares \textbf{zero exact text overlap} with the Training Partition ($N=2,397$); '
            r'near-duplicate overlap (character 4-gram Jaccard $\ge 0.85$) is present in $63/267$ samples ($23.6\%$), reflecting ubiquitous carrier notification boilerplate. '
            r'The Hard Forensic Challenge Suite ($N=117$) includes $109$ text payloads drawn from the corpus ($99$ from the training split and $10$ from the frozen test split) '
            r'alongside $8$ external adversarial lures from national threat feeds (\texttt{canhbao.khonggianmang.vn}) and synthetic variations. '
            r'In the combined exploratory suite ($N=384$), joining the frozen test partition with the challenge suite introduces 10 overlapping text strings and 99 training-derived templates; '
            r'we therefore explicitly treat this combined suite as an exploratory development benchmark rather than a fully disjoint test set.'
            '\n\n'
            r'\begin{table}[h]' + '\n'
            r'\centering' + '\n'
            r'\caption{Source Breakdown and Class Balance Across Corpus Partitions}' + '\n'
            r'\label{tab:dataset_sources}' + '\n'
            r'\resizebox{\columnwidth}{!}{%' + '\n'
            r'\begin{tabular}{lcccc}' + '\n'
            r'\toprule' + '\n'
            r'\textbf{Corpus Partition} & \textbf{Corpus Origin} & \textbf{External Feeds} & \textbf{Ham ($y=0$)} & \textbf{Scam ($y=1$)} \\' + '\n'
            r'\midrule' + '\n'
            r'Training / Internal Val ($N=2,397$) & 2,397 (2,363 uitnlp, 34 phishing) & 0 & 1,726 ($72.0\%$) & 671 ($28.0\%$) \\' + '\n'
            r'Frozen Test Partition ($N=267$)    & 267 (266 uitnlp, 1 phishing)     & 0 & 192 ($71.9\%$)   & 75 ($28.1\%$) \\' + '\n'
            r'Hard Forensic Suite ($N=117$)       & 109 (99 train, 10 frozen test)   & 8 & 19 ($16.2\%$)    & 98 ($83.8\%$) \\' + '\n'
            r'Combined Exploratory ($N=384$)      & 376 (with 10 duplicate strings)  & 8 & 211 ($54.9\%$)   & 173 ($45.1\%$) \\' + '\n'
            r'\midrule' + '\n'
            r'\textbf{Total Unified Corpus ($N=2,664$)} & \textbf{2,664 (2,629 uitnlp, 35 phishing)} & \textbf{0} & \textbf{1,918 ($72.0\%$)} & \textbf{746 ($28.0\%$)} \\' + '\n'
            r'\bottomrule' + '\n'
            r'\end{tabular}%' + '\n'
            r'}' + '\n'
            r'\end{table}'
        )
        method_text = method_text[:idx_start] + new_block + method_text[idx_end:]
        with open(method_path, 'w', encoding='utf-8') as f:
            f.write(method_text)
        print("Fixed Table III and math environments in paper/sections/03_method.tex")
    else:
        print("Could not find start_str in 03_method.tex")

    # 3. Update sync_main_tex.py to fix lines 10-11 in main.tex preamble
    sync_path = 'scripts/sync_main_tex.py'
    with open(sync_path, 'r', encoding='utf-8') as f:
        sync_code = f.read()

    # In main.tex, check lines 10-11
    main_path = 'paper/main.tex'
    with open(main_path, 'r', encoding='utf-8') as f:
        main_text = f.read()

    main_text = main_text.replace(r'\DeclareUnicodeCharacter{1EC1}{\{\^e}}', r'\DeclareUnicodeCharacter{1EC1}{\`{\^e}}')
    main_text = main_text.replace(r'\DeclareUnicodeCharacter{1EC0}{\{\^E}}', r'\DeclareUnicodeCharacter{1EC0}{\`{\^E}}')

    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(main_text)
    print("Fixed DeclareUnicodeCharacter in paper/main.tex")

if __name__ == '__main__':
    main()
