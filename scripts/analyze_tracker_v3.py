import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('parsed_tracker_v3.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total items: {len(items)}\n")

passed = []
failed_old = []
new_items = []
skipped = []

for item in items:
    fid = item['id']
    fb = item['feedback']
    prio = item['priority']
    issue = item['issue']
    
    if fid == 'B1':
        skipped.append(item)
        continue
        
    if fid.startswith('N'):
        new_items.append(item)
    elif 'Đạt' in fb and 'Lý do chưa đạt' not in fb:
        passed.append(item)
    else:
        failed_old.append(item)

print(f"PASSED ({len(passed)}): {[x['id'] for x in passed]}")
print(f"OPEN/FAILED OLD ({len(failed_old)}): {[x['id'] for x in failed_old]}")
print(f"NEW ITEMS N01-N14 ({len(new_items)}): {[x['id'] for x in new_items]}")
print(f"SKIPPED ({len(skipped)}): {[x['id'] for x in skipped]}\n")

print("="*80)
print("DETAILS OF PASSED ITEMS:")
for x in passed:
    print(f"[{x['id']}] {x['priority']}: {x['issue'][:100]}")
    print(f"   Review: {x['feedback'][:200]}\n")

print("="*80)
print("DETAILS OF OPEN/FAILED OLD ITEMS:")
for x in failed_old:
    print(f"[{x['id']}] {x['priority']}: {x['issue'][:100]}")
    print(f"   Review: {x['feedback']}\n")

print("="*80)
print("DETAILS OF NEW ITEMS (N01-N14):")
for x in new_items:
    print(f"[{x['id']}] {x['priority']}: {x['issue'][:100]}")
    print(f"   Review: {x['feedback']}\n")
