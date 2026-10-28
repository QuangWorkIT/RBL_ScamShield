# -*- coding: utf-8 -*-
import sys

def check_latex_syntax():
    with open('paper/main.tex', 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Check matching environments \begin{xyz} ... \end{xyz}
    import re
    begins = re.findall(r'\\begin\{([a-zA-Z0-9*]+)\}', text)
    ends = re.findall(r'\\end\{([a-zA-Z0-9*]+)\}', text)
    
    print(f"Total \\begin: {len(begins)}, Total \\end: {len(ends)}")
    
    # Check stack
    stack = []
    lines = text.splitlines()
    for line_idx, line in enumerate(lines):
        for m in re.finditer(r'\\begin\{([a-zA-Z0-9*]+)\}', line):
            stack.append((m.group(1), line_idx + 1))
        for m in re.finditer(r'\\end\{([a-zA-Z0-9*]+)\}', line):
            if not stack:
                print(f"Error: \\end{{{m.group(1)}}} at line {line_idx+1} with empty stack!")
                return False
            last_env, last_line = stack.pop()
            if last_env != m.group(1):
                print(f"Mismatch at line {line_idx+1}: \\end{{{m.group(1)}}} does not match \\begin{{{last_env}}} from line {last_line}")
                return False

    if stack:
        print(f"Error: Unclosed environments remaining: {stack}")
        return False
    else:
        print("All \\begin and \\end environments matched perfectly!")
        return True

if __name__ == '__main__':
    if not check_latex_syntax():
        sys.exit(1)
