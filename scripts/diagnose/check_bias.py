import pandas as pd
val_df = pd.read_csv('互评作业1/data/validation_small.csv')

def group_bias(df, col):
    print(f"\n--- Bias by {col} ---")
    summary = df.groupby(col)['risk_label_clean'].agg(['mean', 'count'])
    print(summary)

group_bias(val_df, 'department')
group_bias(val_df, 'age_group')
group_bias(val_df, 'hospital_unit')
group_bias(val_df, 'year_quarter')
