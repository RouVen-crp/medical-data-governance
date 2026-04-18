import pandas as pd
import numpy as np

train_df = pd.read_csv('互评作业1/data/train_unlabeled.csv')
val_df = pd.read_csv('互评作业1/data/validation_small.csv')

def diagnose(df, name):
    print(f"--- Diagnosis for {name} ---")
    print(f"Total rows: {len(df)}")
    
    # Missing values
    cols_to_check = ['lab_abnormal_count', 'med_count', 'length_of_stay_proxy', 'triage_note']
    # In CSV, empty strings might be read as NaN
    missing = df[cols_to_check].isnull().sum()
    print("\nMissing Values:")
    print(missing)
    
    # Label Noise (only if both exist)
    if 'risk_label_noisy' in df.columns and 'risk_label_clean' in df.columns:
        mismatch = (df['risk_label_noisy'] != df['risk_label_clean']).sum()
        print(f"\nLabel Mismatch (noisy vs clean): {mismatch} ({mismatch/len(df):.2%})")
    
    # Time Drift
    print("\nYear Quarter distribution:")
    print(df['year_quarter'].value_counts().sort_index())
    
    # Governance Signals - correlations if clean labels exist
    if 'risk_label_clean' in df.columns:
        print("\nCorrelation with risk_label_clean:")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr = df[numeric_cols].corr()['risk_label_clean'].sort_values(ascending=False)
        print(corr)

diagnose(train_df, "Train")
print("\n" + "="*30 + "\n")
diagnose(val_df, "Validation")
