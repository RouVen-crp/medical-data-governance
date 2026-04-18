import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add the starter directory to sys.path
starter_path = Path('互评作业1/starter')
sys.path.append(str(starter_path.resolve()))

from lf_improved_v2 import LF_FUNCTIONS, ABSTAIN, HIGH_RISK, LOW_RISK
from evaluation import compute_metrics, majority_vote

def run_analysis():
    train_df = pd.read_csv('互评作业1/data/train_unlabeled.csv')
    val_df = pd.read_csv('互评作业1/data/validation_small.csv')
    
    # 1. Training Set Analysis (Coverage, Overlap, Conflict)
    print("--- 1. Training Set LF Summary (5000 rows) ---")
    train_votes = []
    for _, row in train_df.iterrows():
        votes = [lf(row) for lf in LF_FUNCTIONS]
        train_votes.append(votes)
    
    train_votes_np = np.array(train_votes)
    n_lfs = len(LF_FUNCTIONS)
    
    # Coverage: sample has at least one non-abstain vote
    coverage = np.any(train_votes_np != ABSTAIN, axis=1).mean()
    
    # Overlap: sample has at least two non-abstain votes
    overlaps = np.sum(train_votes_np != ABSTAIN, axis=1) >= 2
    overlap_rate = overlaps.mean()
    
    # Conflict: sample has at least one HIGH and at least one LOW
    has_high = np.any(train_votes_np == HIGH_RISK, axis=1)
    has_low = np.any(train_votes_np == LOW_RISK, axis=1)
    conflicts = has_high & has_low
    conflict_rate = conflicts.mean()
    
    print(f"LF Coverage: {coverage:.2%}")
    print(f"LF Overlap Rate: {overlap_rate:.2%}")
    print(f"LF Conflict Rate: {conflict_rate:.2%}")

    # 2. Validation Set Performance
    print("\n--- 2. Validation Set Metrics (Majority Vote) ---")
    val_votes = []
    for _, row in val_df.iterrows():
        votes = [lf(row) for lf in LF_FUNCTIONS]
        val_votes.append(votes)
    
    y_pred = [majority_vote(votes) for votes in val_votes]
    y_true = val_df['risk_label_clean'].tolist()
    
    metrics = compute_metrics(y_true, y_pred)
    print(f"Accuracy: {metrics.accuracy:.4f}")
    print(f"Precision: {metrics.precision:.4f}")
    print(f"Recall: {metrics.recall:.4f}")
    print(f"F1: {metrics.f1:.4f}")
    
    # 3. Subgroup Fairness (Worst-group Gap)
    print("\n--- 3. Subgroup Fairness Analysis ---")
    val_df['y_pred'] = y_pred
    val_df['y_true'] = y_true
    
    # Analyze by department
    subgroups = val_df.groupby('department')
    perf_by_group = []
    for name, group in subgroups:
        # Avoid division by zero if a group is entirely abstained by MV
        valid_group = group[group['y_pred'] != ABSTAIN]
        if len(valid_group) > 0:
            acc = (valid_group['y_pred'] == valid_group['y_true']).mean()
            perf_by_group.append(acc)
            print(f"Dept {name} Accuracy: {acc:.4f} (n={len(valid_group)})")
    
    if perf_by_group:
        gap = max(perf_by_group) - min(perf_by_group)
        print(f"\nWorst-group Gap (max - min accuracy): {gap:.4f}")

if __name__ == "__main__":
    run_analysis()
