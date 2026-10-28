import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('parsed_tracker_v3.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print("="*80)
print("ALL NEW ISSUES N01 - N14")
print("="*80)
for it in items:
    if it['id'].startswith('N'):
        print(f"[{it['id']}] (Priority: {it['priority']}, Section: {it['section']})")
        print(f"Issue: {it['issue']}")
        print(f"Feedback/Lý do: {it['feedback']}")
        print("-" * 60)
