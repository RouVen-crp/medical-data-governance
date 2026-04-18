import sys
from pathlib import Path
import pandas as pd

# Add the starter directory to sys.path
starter_path = Path('互评作业1/starter')
sys.path.append(str(starter_path.resolve()))

from lf_improved import LF_FUNCTIONS
from evaluation import compute_metrics, majority_vote

def evaluate():
    val_df = pd.read_csv('互评作业1/data/validation_small.csv')
    
    all_votes = []
    for _, row in val_df.iterrows():
        votes = [lf(row) for lf in LF_FUNCTIONS]
        all_votes.append(votes)
    
    y_pred = [majority_vote(votes) for votes in all_votes]
    y_true = val_df['risk_label_clean'].tolist()
    
    metrics = compute_metrics(y_true, y_pred)
    print("Improved Metrics (Majority Vote of Improved LFs):")
    print(f"Accuracy: {metrics.accuracy:.4f}")
    print(f"Precision: {metrics.precision:.4f}")
    print(f"Recall: {metrics.recall:.4f}")
    print(f"F1: {metrics.f1:.4f}")
    print(f"TP: {metrics.tp}, TN: {metrics.tn}, FP: {metrics.fp}, FN: {metrics.fn}")

    # Also check coverage
    abstains = y_pred.count(-1)
    print(f"Coverage: {(len(y_pred) - abstains) / len(y_pred):.2%}")

if __name__ == "__main__":
    evaluate()
