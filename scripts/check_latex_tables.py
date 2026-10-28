# -*- coding: utf-8 -*-
import re

def check_tables():
    with open('paper/main.tex', 'r', encoding='utf-8') as f:
        text = f.read()

    # Find tabular blocks properly
    blocks = re.findall(r'\\begin\{tabular\*?\}(.*?)\\end\{tabular\*?\}', text, re.DOTALL)
    print(f"Total tabular blocks: {len(blocks)}")
    
    for idx, block in enumerate(blocks):
        # The first non-empty line or parameter is the column spec
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        first_line = lines[0]
        # match braces at start
        m = re.match(r'\{([^\}]+(?:\}[^\}]+\})*)\}', first_line)
        col_spec = m.group(1) if m else first_line
        
        # count cols
        cols = len(re.findall(r'[lcrX]|p\{', col_spec))
        max_amps = cols - 1
        
        for l_num, line in enumerate(lines[1:]):
            if '&' in line:
                line_no_escaped = line.replace(r'\&', '')
                amps = line_no_escaped.count('&')
                if amps != max_amps:
                    # check if multicolumn is used
                    if '\\multicolumn' not in line:
                        print(f"Table {idx+1} line {l_num+2}: has {amps} '&' (expected {max_amps}): {line[:90]}")
                    
    print("Table column check completed!")

if __name__ == '__main__':
    check_tables()
