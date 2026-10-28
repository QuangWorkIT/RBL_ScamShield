import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('parsed_tracker_v3.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Items to analyze: all except B1, H3, H9, H10, H16
target_items = [it for it in items if it['id'] not in ['B1', 'H3', 'H9', 'H10', 'H16']]

print(f"Total target items to analyze: {len(target_items)}")
for it in target_items:
    print(f"--- [{it['id']}] ({it['priority']}) {it['reviewer']} ---")
    print("Issue:", it['issue'])
    print("Feedback:", it['feedback'])
    print()
