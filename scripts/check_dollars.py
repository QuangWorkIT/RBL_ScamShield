# -*- coding: utf-8 -*-
def check_dollar_balance(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Exclude escaped dollars \$
    clean_text = text.replace(r'\$', '')
    count = clean_text.count('$')
    print(f"{filepath}: total '$' count = {count} (Even/Balanced: {count % 2 == 0})")
    assert count % 2 == 0, f"Unmatched '$' in {filepath}!"

if __name__ == '__main__':
    check_dollar_balance('paper/sections/03_method.tex')
    check_dollar_balance('paper/main.tex')
    print("All dollar signs are perfectly balanced!")
