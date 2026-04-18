import pandas as pd
val_df = pd.read_csv('互评作业1/data/validation_small.csv')

mismatch = val_df[val_df['risk_label_noisy'] != val_df['risk_label_clean']]
print(f"Total mismatches: {len(mismatch)}")
print(mismatch[['department', 'chief_complaint', 'triage_note', 'risk_label_noisy', 'risk_label_clean']].head(20))
