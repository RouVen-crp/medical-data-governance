import pandas as pd
import numpy as np

# Load data
train_df = pd.read_csv('互评作业1/data/train_unlabeled.csv')
val_df = pd.read_csv('互评作业1/data/validation_small.csv')

def analyze_missingness(df, cols):
    print("\n--- 1. Missingness Analysis (MAR check by Department) ---")
    for col in cols:
        missing_by_dept = df.groupby('department')[col].apply(lambda x: x.isnull().mean())
        print(f"Missing rate for '{col}' per department:")
        print(missing_by_dept)

def analyze_label_noise(df):
    print("\n--- 2. Label Noise Profiling (Noisy vs Clean Accuracy) ---")
    if 'risk_label_noisy' in df.columns and 'risk_label_clean' in df.columns:
        df['correct'] = (df['risk_label_noisy'] == df['risk_label_clean'])
        noise_by_dept = df.groupby('department')['correct'].mean()
        print("Noisy label 'Accuracy' by department:")
        print(noise_by_dept)
        
        print("\nNoise Type Analysis (False Positives vs False Negatives by Dept):")
        # 1 = High Risk, 0 = Low Risk
        # FP: noisy=1, clean=0
        # FN: noisy=0, clean=1
        fp = df[(df['risk_label_noisy'] == 1) & (df['risk_label_clean'] == 0)]
        fn = df[(df['risk_label_noisy'] == 0) & (df['risk_label_clean'] == 1)]
        print(f"Global FP count: {len(fp)}, FN count: {len(fn)}")
        print("\nFP count by department:")
        print(fp['department'].value_counts())
        print("\nFN count by department:")
        print(fn['department'].value_counts())

def analyze_temporal_and_subgroup(df):
    print("\n--- 3. Temporal Drift ---")
    drift = df.groupby('year_quarter')['risk_label_clean'].mean()
    print("Clean Risk Mean by Quarter:")
    print(drift)
    
    print("\n--- 4. Subgroup Bias (Clean Risk Mean) ---")
    age_bias = df.groupby('age_group')['risk_label_clean'].mean()
    print("Age Group Risk:")
    print(age_bias)
    
    unit_bias = df.groupby('hospital_unit')['risk_label_clean'].mean()
    print("\nHospital Unit Risk:")
    print(unit_bias)

# Execution
missing_cols = ['lab_abnormal_count', 'med_count', 'length_of_stay_proxy', 'triage_note']
analyze_missingness(train_df, missing_cols)
analyze_label_noise(val_df)
analyze_temporal_and_subgroup(val_df)
