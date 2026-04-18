"""Evaluation helpers for the medical governance assignment.

This module keeps the evaluation logic lightweight and dependency-free.
Students can use it to compare baseline predictions, majority vote, and
other downstream models against the labeled validation or test set.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Metrics:
    accuracy: float
    precision: float
    recall: float
    f1: float
    tp: int
    tn: int
    fp: int
    fn: int


def load_label_column(csv_path: str | Path, label_col: str = "risk_label_clean") -> list[int]:
    path = Path(csv_path)
    labels: list[int] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            value = row.get(label_col, "")
            if value == "":
                continue
            labels.append(int(float(value)))
    return labels


def load_prediction_column(csv_path: str | Path, pred_col: str = "prediction") -> list[int]:
    path = Path(csv_path)
    preds: list[int] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            value = row.get(pred_col, "")
            if value == "":
                continue
            preds.append(int(float(value)))
    return preds


def majority_vote(votes: Sequence[int], abstain_value: int = -1) -> int:
    """Return the majority label, ignoring abstains.

    Ties fall back to abstain.
    """

    counts = {0: 0, 1: 0}
    for vote in votes:
        if vote == abstain_value:
            continue
        if vote in counts:
            counts[vote] += 1
    if counts[0] == counts[1]:
        return abstain_value
    return 1 if counts[1] > counts[0] else 0


def compute_metrics(y_true: Sequence[int], y_pred: Sequence[int]) -> Metrics:
    if len(y_true) != len(y_pred):
        raise ValueError(f"Length mismatch: y_true={len(y_true)} y_pred={len(y_pred)}")

    tp = tn = fp = fn = 0
    for truth, pred in zip(y_true, y_pred):
        if truth == 1 and pred == 1:
            tp += 1
        elif truth == 0 and pred == 0:
            tn += 1
        elif truth == 0 and pred == 1:
            fp += 1
        elif truth == 1 and pred == 0:
            fn += 1
        else:
            # Unknown / abstain labels are ignored in the core counts.
            continue

    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total else 0.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return Metrics(accuracy=accuracy, precision=precision, recall=recall, f1=f1, tp=tp, tn=tn, fp=fp, fn=fn)


def evaluate_csv(
    path: str | Path,
    label_col: str = "risk_label_clean",
    pred_col: str = "prediction",
) -> Metrics:
    """Evaluate a CSV file that contains both labels and predictions."""

    csv_path = Path(path)
    y_true: list[int] = []
    y_pred: list[int] = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            truth = row.get(label_col, "")
            pred = row.get(pred_col, "")
            if truth == "" or pred == "":
                continue
            y_true.append(int(float(truth)))
            y_pred.append(int(float(pred)))
    return compute_metrics(y_true, y_pred)


def format_metrics(metrics: Metrics) -> str:
    return (
        f"accuracy={metrics.accuracy:.4f}, precision={metrics.precision:.4f}, "
        f"recall={metrics.recall:.4f}, f1={metrics.f1:.4f}, "
        f"tp={metrics.tp}, tn={metrics.tn}, fp={metrics.fp}, fn={metrics.fn}"
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate medical governance predictions")
    parser.add_argument("csv_path", help="CSV file with labels and predictions")
    parser.add_argument("--label-col", default="risk_label_clean")
    parser.add_argument("--pred-col", default="prediction")
    args = parser.parse_args()

    metrics = evaluate_csv(args.csv_path, label_col=args.label_col, pred_col=args.pred_col)
    print(format_metrics(metrics))
