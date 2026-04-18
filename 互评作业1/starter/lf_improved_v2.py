from __future__ import annotations
from typing import Callable, Iterable

HIGH_RISK = 1
LOW_RISK = 0
ABSTAIN = -1

def _text(record: object, field: str) -> str:
    value = getattr(record, field, "") if not isinstance(record, dict) else record.get(field, "")
    return str(value or "").strip().lower()

def _num(record: object, field: str, default: float = 0.0) -> float:
    value = getattr(record, field, default) if not isinstance(record, dict) else record.get(field, default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

# --- Optimized LFs based on Advanced Diagnosis ---

def lf_cardiac_emergency(record: object) -> int:
    """Corrects Cardiology FN: High risk for cardiac symptoms in Cardiology dept."""
    dept = _text(record, "department")
    complaint = _text(record, "chief_complaint")
    triage = _text(record, "triage_note")
    text_blob = complaint + " " + triage
    
    if dept == "cardiology":
        if any(kw in text_blob for kw in ["chest pain", "shortness of breath", "abnormal ecg"]):
            return HIGH_RISK
    return ABSTAIN

def lf_general_low_risk(record: object) -> int:
    """Corrects GeneralMedicine FP: Low risk for routine tasks in GenMed."""
    dept = _text(record, "department")
    complaint = _text(record, "chief_complaint")
    
    if dept == "generalmedicine":
        low_risk_tasks = ["routine follow up", "medication refill", "sleep issue", "minor rash", "mild cough"]
        if any(task in complaint for kw in low_risk_tasks for task in [kw]): # simple check
            return LOW_RISK
    return ABSTAIN

def lf_abnormal_lab_v2(record: object) -> int:
    """Baseline coverage: Numeric threshold for lab results."""
    lab_abnormal = _num(record, "lab_abnormal_count", -1)
    if lab_abnormal >= 2:
        return HIGH_RISK
    if lab_abnormal == 0:
        return LOW_RISK
    return ABSTAIN

def lf_late_quarter_comorbidity(record: object) -> int:
    """Temporal Drift: Stricter risk assessment for multi-morbid patients in late 2024."""
    quarter = _text(record, "year_quarter")
    comorbidity = _num(record, "comorbidity_count", 0)
    
    if quarter in ["2024q3", "2024q4"] and comorbidity >= 3:
        return HIGH_RISK
    return ABSTAIN

def lf_elderly_emergency(record: object) -> int:
    """Subgroup Bias: Catch high-risk elderly emergency cases."""
    age = _text(record, "age_group")
    adm_type = _text(record, "admission_type")
    
    if age == "75+" and adm_type == "emergency":
        return HIGH_RISK
    return ABSTAIN

LF_FUNCTIONS: list[Callable[[object], int]] = [
    lf_cardiac_emergency,
    lf_general_low_risk,
    lf_abnormal_lab_v2,
    lf_late_quarter_comorbidity,
    lf_elderly_emergency
]
