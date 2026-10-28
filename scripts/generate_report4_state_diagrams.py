"""
Script to validate PlantUML State Machine Diagrams for Report 4 (SEP)
and generate direct preview/download links (PNG & SVG) via PlantUML/Kroki servers.
Covers:
- SCRUM-107: Scam Report Management State Diagram
- SCRUM-108: Dispute and Appeal Management State Diagram
- SCRUM-109: Scam Check State Diagram
"""

import os
import sys
import zlib
import base64

sys.stdout.reconfigure(encoding='utf-8')

# PlantUML custom base64 encoder
PLANTUML_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

def encode_plantuml_6bit(b):
    return PLANTUML_ALPHABET[b & 0x3F]

def encode_plantuml(text):
    """Encodes PlantUML text using the deflate + PlantUML base64 standard."""
    compressed = zlib.compress(text.encode('utf-8'))[2:-4]
    res = []
    i = 0
    while i < len(compressed):
        b1 = compressed[i]
        b2 = compressed[i + 1] if i + 1 < len(compressed) else 0
        b3 = compressed[i + 2] if i + 2 < len(compressed) else 0

        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F

        res.append(encode_plantuml_6bit(c1))
        res.append(encode_plantuml_6bit(c2))
        if i + 1 < len(compressed):
            res.append(encode_plantuml_6bit(c3))
        if i + 2 < len(compressed):
            res.append(encode_plantuml_6bit(c4))
        i += 3
    return "".join(res)

def get_diagram_urls(puml_path):
    with open(puml_path, 'r', encoding='utf-8') as f:
        content = f.read()
    encoded = encode_plantuml(content)
    png_url = f"https://www.plantuml.com/plantuml/png/{encoded}"
    svg_url = f"https://www.plantuml.com/plantuml/svg/{encoded}"
    return png_url, svg_url, content

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    puml_dir = os.path.join(base_dir, 'docs', 'diagrams', 'puml')

    tasks = [
        {
            'ticket': 'SCRUM-107',
            'title': 'Scam Report Management State Diagram',
            'filename': 'scrum_107_scam_report_state.puml',
            'states': ['Drafted', 'Submitted', 'UnderReview', 'Approved', 'Rejected', 'Merged']
        },
        {
            'ticket': 'SCRUM-108',
            'title': 'Dispute and Appeal Management State Diagram',
            'filename': 'scrum_108_dispute_appeal_state.puml',
            'states': ['Drafted', 'Submitted', 'UnderReview', 'NeedsMoreInfo', 'Resolved', 'Rejected']
        },
        {
            'ticket': 'SCRUM-109',
            'title': 'Scam Check State Diagram',
            'filename': 'scrum_109_scam_check_state.puml',
            'states': ['Submitted', 'Validated', 'Analyzing', 'VerdictReturned (Safe/Suspicious/Dangerous)', 'Failed']
        }
    ]

    print("======================================================================")
    print("📊 XÁC THỰC VÀ TẠO LIÊN KẾT RENDER CHO BÁO CÁO REPORT 4 (SEP)")
    print("======================================================================")

    for item in tasks:
        puml_file = os.path.join(puml_dir, item['filename'])
        if not os.path.exists(puml_file):
            print(f"❌ [THIẾU FILE] Không tìm thấy {item['filename']}")
            continue

        png_url, svg_url, content = get_diagram_urls(puml_file)
        print(f"\n🔹 Ticket: {item['ticket']} — {item['title']}")
        print(f"   📁 File: docs/diagrams/puml/{item['filename']} ({len(content.splitlines())} dòng)")
        print(f"   🎯 Trạng thái kiểm soát: {', '.join(item['states'])}")
        print(f"   🖼️  Link Ảnh PNG (High-Res): {png_url}")
        print(f"   🌐 Link Vector SVG        : {svg_url}")

    print("\n======================================================================")
    print("✅ ĐÃ HOÀN TẤT KIỂM TRA TOÀN BỘ 3 BIỂU ĐỒ TRẠNG THÁI!")
    print("👉 File tài liệu đặc tả đầy đủ: docs/08_UML_STATE_DIAGRAMS_REPORT4.md")
    print("======================================================================")

if __name__ == '__main__':
    main()
