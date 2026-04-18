import sys
from pathlib import Path
import pandas as pd

starter_path = Path('互评作业1/starter')
sys.path.append(str(starter_path.resolve()))

from lf_template import LF_FUNCTIONS
from evaluation import compute_metrics, majority_vote

def evaluate_by_quarter():
    val_df = pd.read_csv('互评作业1/data/validation_small.csv')
    
    for quarter in sorted(val_df['year_quarter'].unique()):
        q_df = val_df[val_df['year_quarter'] == quarter]
        all_votes = []
        for _, row in q_df.iterrows():
            votes = [lf(row) for lf in LF_FUNCTIONS]
            all_votes.append(votes)
        
        y_pred = [majority_vote(votes) for votes in all_votes]
        y_true = q_df['risk_label_clean'].tolist()
        
        metrics = compute_metrics(y_true, y_pred)
        abstains = y_pred.count(-1)
        coverage = (len(y_pred) - abstains) / len(y_pred)
        
        print(f"--- Quarter: {quarter} ---")
        print(f"Metrics: F1={metrics.f1:.4f}, Prec={metrics.precision:.4f}, Rec={metrics.recall:.4f}, Cov={coverage:.2%}")

if __name__ == "__main__":
    evaluate_by_quarter()
