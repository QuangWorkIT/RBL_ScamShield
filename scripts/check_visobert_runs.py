import csv, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('results/summary_5runs_detailed.csv', 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        if row['model'].startswith('ViSoBERT'):
            print(f"Seed {row['seed']}: acc={row['accuracy']}, prec={row['precision']}, rec={row['recall_scam']}, f1={row['f1_score']}")
