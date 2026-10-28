# -*- coding: utf-8 -*-
with open('paper/main.tex', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    clean = l.replace(r'\$', '')
    if clean.count('$') % 2 != 0:
        print(f"Line {i+1} has odd $: {l.strip()}")
