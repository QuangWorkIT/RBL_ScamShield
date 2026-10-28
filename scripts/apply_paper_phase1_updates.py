# -*- coding: utf-8 -*-
"""
Apply all precise updates to paper/sections/ based on the audit plan.
"""
import re

def update_02_related():
    path = 'paper/sections/02_related.tex'
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Cost in Table I
    c = c.replace(r'$0.05/1k SMS', r'$0.0153/1k SMS')

    # 2. Page numbers in text
    c = c.replace(', pp.~5191--5207)', ')')

    # 3. Table references in Table II
    target_ref = 'Empirical 5-run edge benchmark (Table II), McNemar discordance (Table III), Council \\& Defender ablation (Table IV), tau sweep (Table VI)'
    new_ref = r'Empirical 5-run edge benchmark (Table~\ref{tab:benchmark_summary}), McNemar discordance (Table~\ref{tab:mcnemar}), Council \& Defender ablation (Tables~\ref{tab:ablation_council}--\ref{tab:matrix_2x3}), tau sweep (Table~\ref{tab:tau_ablation})'
    c = c.replace(target_ref, new_ref)

    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(c)
    print("Updated 02_related.tex successfully!")

if __name__ == '__main__':
    update_02_related()
