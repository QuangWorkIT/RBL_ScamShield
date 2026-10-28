import json
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath('.'))
from pipeline.pii_sanitizer import MessagePIISanitizer

sanitizer = MessagePIISanitizer()

samples = []
with open('experiments/tier2_council/data/master_test_suite.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            samples.append(json.loads(line.strip()))

print(f"Total samples evaluated for PII Sanitization: {len(samples)}")

total_entities = {"phone": 0, "otp": 0, "account": 0, "citizen_id": 0, "balance": 0}
messages_with_pii = 0
redacted_samples = []

for idx, s in enumerate(samples):
    raw = s.get('raw_message', '')
    clean, manifest = sanitizer.sanitize(raw)
    
    sample_has_pii = False
    for k in total_entities:
        count = len(manifest.get(k, []))
        total_entities[k] += count
        if count > 0:
            sample_has_pii = True
            
    if sample_has_pii:
        messages_with_pii += 1
        redacted_samples.append({
            "sample_id": s.get("sample_id", f"S_{idx}"),
            "gold": s.get("gold_label"),
            "raw": raw,
            "clean": clean,
            "manifest": manifest
        })

print(f"Messages containing sensitive PII: {messages_with_pii}/{len(samples)} ({messages_with_pii/len(samples)*100:.1f}%)")
print("Entities detected and redacted:")
for k, v in total_entities.items():
    print(f"  - {k:<12}: {v} instances")

print("\nSample Before/After Redaction:")
for r in redacted_samples[:3]:
    print(f"ID: {r['sample_id']} [{r['gold']}]")
    print(f"  RAW  : {r['raw']}")
    print(f"  CLEAN: {r['clean']}")
    print(f"  PII  : {r['manifest']}")
    print()
