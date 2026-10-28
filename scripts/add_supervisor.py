# -*- coding: utf-8 -*-
"""
Update author list and contributions with Supervisor Le Thi Quynh Chi.
"""
import zipfile, os

def update_authors():
    # 1. Update paper/main.tex
    with open('paper/main.tex', 'r', encoding='utf-8') as f:
        main_text = f.read()

    # 3. Check dollar balance in main.tex
    clean_text = main_text.replace(r'\$', '')
    dollars = clean_text.count('$')
    print(f"main.tex total '$' count = {dollars} (Even: {dollars % 2 == 0})")
    assert dollars % 2 == 0, f"Unbalanced dollars: {dollars}"

    # 4. Repack ScamShield_Overleaf_Ready.zip
    zip_path = 'paper/ScamShield_Overleaf_Ready.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write('paper/main.tex', arcname='main.tex')
        z.write('paper/references.bib', arcname='references.bib')
        for f in os.listdir('paper/sections'):
            if f.endswith('.tex'):
                z.write(os.path.join('paper/sections', f), arcname=os.path.join('sections', f))
    print("Updated", zip_path, "successfully!")

if __name__ == '__main__':
    update_authors()
