import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np

# --- Path Management ---
# Add project root and starter directory to sys.path
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
starter_path = project_root / '互评作业1' / 'starter'
data_dir = project_root / '互评作业1' / 'data'

sys.path.append(str(starter_path.resolve()))

from lf_template import LF_FUNCTIONS, ABSTAIN, HIGH_RISK, LOW_RISK
from evaluation import compute_metrics, majority_vote

class FinalWeightedModel:
    """Uses weights derived from Label Model experiments for final inference."""
    def __init__(self):
        # Optimized weights from our experiment
        self.weights = np.array([1.0, 0.90, 0.65, 0.54, 0.50])

    def predict(self, votes):
        score = 0
        has_voted = False
        for i, v in enumerate(votes):
            if v == HIGH_RISK:
                score += self.weights[i]
                has_voted = True
            elif v == LOW_RISK:
                score -= self.weights[i]
                has_voted = True
        
        if not has_voted:
            return ABSTAIN
        return HIGH_RISK if score > 0 else LOW_RISK

def run_final_evaluation():
    test_df = pd.read_csv(data_dir / 'test_labeled.csv')
    print(f"Loaded {len(test_df)} test samples.")

    # 1. Apply LFs
    all_votes = []
    for _, row in test_df.iterrows():
        votes = [lf(row) for lf in LF_FUNCTIONS]
        all_votes.append(votes)
    
    # 2. Inference
    model = FinalWeightedModel()
    y_pred = [model.predict(v) for v in all_votes]
    y_true = test_df['risk_label_clean'].tolist()

    # 3. Compute Metrics
    metrics = compute_metrics(y_true, y_pred)
    
    # 4. Generate Output Files
    # predictions.csv
    pred_results = pd.DataFrame({
        'visit_id': test_df['visit_id'],
        'predicted_risk_label': y_pred
    })
    results_dir = project_root / 'results'
    results_dir.mkdir(exist_ok=True)
    pred_results.to_csv(results_dir / 'predictions.csv', index=False)
    
    # evaluation_results.txt
    with open(results_dir / 'evaluation_results.txt', 'w', encoding='utf-8') as f:
        f.write("=== FINAL TEST SET EVALUATION ===\n")
        f.write(f"Accuracy:  {metrics.accuracy:.4f}\n")
        f.write(f"Precision: {metrics.precision:.4f}\n")
        f.write(f"Recall:    {metrics.recall:.4f}\n")
        f.write(f"F1 Score:  {metrics.f1:.4f}\n")
        f.write(f"Coverage:  {(len(y_pred) - y_pred.count(-1))/len(y_pred):.2%}\n\n")
        
        f.write("--- Subgroup Performance (Accuracy) ---\n")
        test_df['y_pred'] = y_pred
        test_df['y_true'] = y_true
        for name, group in test_df.groupby('department'):
            valid = group[group['y_pred'] != ABSTAIN]
            if len(valid) > 0:
                acc = (valid['y_pred'] == valid['y_true']).mean()
                f.write(f"Dept {name:<16}: {acc:.4f} (n={len(valid)})\n")

    print(f"Successfully generated results in {results_dir}")
    print(f"Test F1 Score: {metrics.f1:.4f}")

if __name__ == "__main__":
    run_final_evaluation()
