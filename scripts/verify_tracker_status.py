import json
import sys
import docx

sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. PARSED_TRACKER_V3.JSON STATUS SUMMARY ===")
with open('parsed_tracker_v3.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

json_counts = {}
for it in items:
    st = it['status'].replace('\n', ' ')
    json_counts[st] = json_counts.get(st, 0) + 1

for st, count in sorted(json_counts.items()):
    print(f"  {st}: {count}")
print(f"  Total items: {len(items)}")

print("\n=== 2. DOCX TABLE 1 STATUS SUMMARY ===")
doc = docx.Document('ScamShield_VN_Action_Tracker_V3.docx')
t1 = doc.tables[1]
docx_counts = {}
for r in t1.rows:
    c0 = r.cells[0].text.strip()
    if c0.startswith(('B', 'H', 'M', 'N')) and len(c0) <= 4:
        st = r.cells[-1].text.strip().replace('\n', ' ')
        docx_counts[st] = docx_counts.get(st, 0) + 1

for st, count in sorted(docx_counts.items()):
    print(f"  {st}: {count}")
print(f"  Total items: {sum(docx_counts.values())}")

print("\n=== 3. VERIFY INVARIANTS CHECK ===")
