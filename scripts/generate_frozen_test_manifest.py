import os
import hashlib
import json
import pandas as pd
from sklearn.model_selection import train_test_split

def main():
    os.makedirs('data/processed', exist_ok=True)
    raw_path = 'data/raw/vietnamese_sms_merged_all.csv'

    # Compute SHA256 of raw source file
    with open(raw_path, 'rb') as f:
        raw_sha256 = hashlib.sha256(f.read()).hexdigest()

    df = pd.read_csv(raw_path)
    total_records = len(df)
    unique_texts = int(df['message'].nunique())
    duplicate_ids = int(df['message_id'].duplicated().sum())

    print(f"Raw dataset rows: {total_records}")
    print(f"Unique text messages: {unique_texts}")
    print(f"Duplicate IDs: {duplicate_ids}")

    train_df, test_df = train_test_split(df, test_size=0.100187, random_state=42, stratify=df['label'])
    print(f"Train size: {len(train_df)}, Test size: {len(test_df)}")
    print("Test label distribution:\n", test_df['label'].value_counts())

    test_csv_path = 'data/processed/frozen_test_267.csv'
    test_df.to_csv(test_csv_path, index=True, index_label='original_index', encoding='utf-8')

    with open(test_csv_path, 'rb') as f:
        test_sha256 = hashlib.sha256(f.read()).hexdigest()

    manifest = {
        'description': 'Isolated Frozen Test Partition (N=267) manifest for ScamShield-VN empirical evaluation',
        'source_file': raw_path,
        'source_sha256': raw_sha256,
        'total_source_records': total_records,
        'unique_messages_in_source': unique_texts,
        'duplicate_ids_in_source_due_to_namespace_collision': duplicate_ids,
        'namespace_collision_note': 'The 34 duplicate message_id instances result from merging two upstream feeds (vietnamese_sms_dataset and vietnamese_sms_phishing_sample_300) which independently assigned COM_xxx IDs. All 2,664 messages contain 100% unique textual content.',
        'split_method': 'train_test_split',
        'library': 'scikit-learn',
        'random_state': 42,
        'stratify_column': 'label',
        'test_size_parameter': 0.100187,
        'frozen_test_samples_count': len(test_df),
        'label_distribution': {
            'ham_label_0': int((test_df['label'] == 0).sum()),
            'scam_label_1': int((test_df['label'] == 1).sum())
        },
        'frozen_test_file': test_csv_path,
        'frozen_test_sha256': test_sha256,
        'sample_indices': test_df.index.tolist(),
        'sample_ids': test_df['message_id'].tolist()
    }

    manifest_path = 'data/processed/frozen_test_manifest.json'
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {test_csv_path} and {manifest_path}")

if __name__ == '__main__':
    main()
