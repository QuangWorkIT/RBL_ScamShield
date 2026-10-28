# -*- coding: utf-8 -*-
import os, sys, re

def check_dollars(filepath):
    print(f"=== CHECKING {filepath} ===")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    issues = 0
    for idx, line in enumerate(lines):
        line_num = idx + 1
        
        # Check unescaped dollars parity on this line (unless multiline math)
        # In LaTeX tables and paragraphs, math $...$ is usually on the same line
        # Count unescaped dollars:
        # Replace \$ with nothing
        cleaned = re.sub(r'\\\$', '', line)
        # Remove comments
        if '%' in cleaned:
            cleaned = cleaned.split('%')[0]
        
        dollar_count = cleaned.count('$')
        if dollar_count % 2 != 0:
            print(f"Line {line_num}: Odd number of '$' ({dollar_count}): {line.strip()[:100]}")
            issues += 1
            
        # Check for truncated patterns like '(=', '(.', '(%', '(='
        if re.search(r'\([=.]', line):
            print(f"Line {line_num}: Suspicious truncated math: {line.strip()[:100]}")
            issues += 1
            
        # Check for unescaped '&' outside of tabular
        # In tabular, check unescaped '&' count vs column definition
        # Especially words like 'Council & Defender'
        if re.search(r'\b[A-Za-z]+\s*&\s*[A-Za-z]+\b', line):
            print(f"Line {line_num}: Possible unescaped '&' in text: {line.strip()[:100]}")
            issues += 1

    return issues

def main():
    total = 0
    files = [
        'paper/sections/00_abstract.tex',
        'paper/sections/01_intro.tex',
        'paper/sections/02_related.tex',
        'paper/sections/03_method.tex',
        'paper/sections/04_results.tex',
        'paper/sections/05_conclusion.tex',
        'paper/sections/06_endmatter.tex',
        'paper/main.tex'
    ]
    for f in files:
        if os.path.exists(f):
            total += check_dollars(f)
    print(f"\nTotal syntax warnings: {total}")

if __name__ == '__main__':
    main()
