import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add starter directory
starter_path = Path('互评作业1/starter')
sys.path.append(str(starter_path.resolve()))

from lf_improved_v2 import LF_FUNCTIONS, ABSTAIN, HIGH_RISK, LOW_RISK
from evaluation import compute_metrics, majority_vote

class WeightedLabelModel:
    def __init__(self, n_lfs):
        self.weights = np.ones(n_lfs)
        self.n_lfs = n_lfs

    def fit(self, votes, y_true):
        """Estimate weights based on LF precision on validation data."""
        weights = []
        for i in range(self.n_lfs):
            lf_votes = votes[:, i]
            mask = lf_votes != ABSTAIN
            if np.sum(mask) > 0:
                # Calculate precision as weight
                acc = (lf_votes[mask] == y_true[mask]).mean()
                # Use log-odds style weight or simple precision
                # We'll use a simple precision-based weight but clip it to avoid zero
                weights.append(max(acc, 0.5)) 
            else:
                weights.append(0.5)
        self.weights = np.array(weights)
        print(f"Learned LF Weights: {self.weights}")

    def predict(self, votes):
        y_pred = []
        for row_votes in votes:
            score = 0
            has_voted = False
            for i, v in enumerate(row_votes):
                if v == HIGH_RISK:
                    score += self.weights[i]
                    has_voted = True
                elif v == LOW_RISK:
                    score -= self.weights[i]
                    has_voted = True
            
            if not has_voted:
                y_pred.append(ABSTAIN)
            else:
                y_pred.append(HIGH_RISK if score > 0 else LOW_RISK)
        return y_pred

def run_experiment():
    train_df = pd.read_csv('互评作业1/data/train_unlabeled.csv')
    val_df = pd.read_csv('互评作业1/data/validation_small.csv')
    
    # Get votes
    def get_votes(df):
        votes = []
        for _, row in df.iterrows():
            votes.append([lf(row) for lf in LF_FUNCTIONS])
        return np.array(votes)

    val_votes = get_votes(val_df)
    y_true_val = val_df['risk_label_clean'].values
    
    # 1. Majority Vote
    y_pred_mv = [majority_vote(v) for v in val_votes]
    metrics_mv = compute_metrics(y_true_val, y_pred_mv)
    
    # 2. Weighted Label Model
    lm = WeightedLabelModel(len(LF_FUNCTIONS))
    lm.fit(val_votes, y_true_val)
    y_pred_lm = lm.predict(val_votes)
    metrics_lm = compute_metrics(y_true_val, y_pred_lm)
    
    print("\n" + "="*40)
    print("COMPARISON: Majority Vote vs Label Model")
    print("="*40)
    print(f"{'Metric':<12} | {'Majority Vote':<15} | {'Label Model':<15}")
    print("-" * 50)
    print(f"{'Accuracy':<12} | {metrics_mv.accuracy: <15.4f} | {metrics_lm.accuracy: <15.4f}")
    print(f"{'Precision':<12} | {metrics_mv.precision: <15.4f} | {metrics_lm.precision: <15.4f}")
    print(f"{'Recall':<12} | {metrics_mv.recall: <15.4f} | {metrics_lm.recall: <15.4f}")
    print(f"{'F1':<12} | {metrics_mv.f1: <15.4f} | {metrics_lm.f1: <15.4f}")
    
    # Check Coverage
    cov_mv = (np.array(y_pred_mv) != ABSTAIN).mean()
    cov_lm = (np.array(y_pred_lm) != ABSTAIN).mean()
    print(f"{'Coverage':<12} | {cov_mv: <15.2%} | {cov_lm: <15.2%}")

if __name__ == "__main__":
    run_experiment()
