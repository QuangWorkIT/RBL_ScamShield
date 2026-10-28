# -*- coding: utf-8 -*-
with open('paper/sections/04_results.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# Update Table IX rows to wrap brackets in math mode cleanly
text = text.replace(r'$\mathbf{0.00\%}$ [0.00\%, 17.65\%]', r'$\mathbf{0.00\%}$ $[0.00\%, 17.65\%]$')
text = text.replace(r'$\mathbf{0.00\%}$ \textbf{[0.00\%, 17.65\%]}', r'$\mathbf{0.00\%}$ $\mathbf{[0.00\%, 17.65\%]}$')
text = text.replace(r'$10.53\%$ [1.30\%, 33.14\%]', r'$10.53\%$ $[1.30\%, 33.14\%]$')
text = text.replace(r'$5.26\%$ [0.13\%, 26.03\%]', r'$5.26\%$ $[0.13\%, 26.03\%]$')

with open('paper/sections/04_results.tex', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated 04_results.tex Table IX CI math brackets cleanly!")
