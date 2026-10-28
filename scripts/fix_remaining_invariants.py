# -*- coding: utf-8 -*-
import sys

def fix_all():
    # 1. Fix IV.F.2 in 04_results.tex
    with open('paper/sections/04_results.tex', 'r', encoding='utf-8') as f:
        c = f.read()

    old_ivf2 = 'specifically an empirical false alarm rate of $35.34\\%$ ($41/116$) on benign challenge lures, and an FPR of $21.35\\%$ ($41/192$) on the frozen test partition)'
    new_ivf2 = 'specifically a False Discovery Rate of $35.34\\%$ ($41/116$ false positives among $116$ total scam alerts), and an FPR of $21.35\\%$ ($41/192$) on authentic messages in the frozen test partition)'
    if old_ivf2 in c:
        c = c.replace(old_ivf2, new_ivf2)
        with open('paper/sections/04_results.tex', 'w', encoding='utf-8', newline='') as f:
            f.write(c)
        print("Fixed IV.F.2 in 04_results.tex")
    else:
        print("Warning: old_ivf2 not found in 04_results.tex")

if __name__ == '__main__':
    fix_all()
