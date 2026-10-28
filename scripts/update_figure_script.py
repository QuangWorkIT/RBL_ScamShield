# -*- coding: utf-8 -*-
with open('scripts/generate_architecture_figure.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('110M Params', '97.57M Params')
c = c.replace('98.4 MB, 70.7 ms on CPU', '98.42 MB / 93.86 MiB, 70.7 ms on CPU')
c = c.replace('Occam-Optimized 3-Agent Specialist Panel', 'Consolidated 3-Agent Specialist Panel')
c = c.replace('Ablation Evidence (Table IV)', 'Ablation Evidence (Table IX)')
c = c.replace('Council Trade-off & P-single Baseline Context (Table IV)', 'Council Trade-off & P-single Baseline Context (Table VIII)')
c = c.replace('• Occam 3-Agent Council', '• Proposed 3-Agent Council')

old_save = 'img.save(output_path, "PNG", dpi=(300, 300))'
new_save = (
    'img.save(output_path, "PNG", dpi=(300, 300))\n'
    '    alt_path = "figures/pipeline_architecture.png"\n'
    '    os.makedirs(os.path.dirname(alt_path), exist_ok=True)\n'
    '    img.save(alt_path, "PNG", dpi=(300, 300))'
)
c = c.replace(old_save, new_save)

with open('scripts/generate_architecture_figure.py', 'w', encoding='utf-8', newline='') as f:
    f.write(c)
print("Updated scripts/generate_architecture_figure.py successfully!")
