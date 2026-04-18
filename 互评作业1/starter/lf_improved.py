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

# --- High Precision Symptom Rules ---

def lf_emergency_symptoms(record: object) -> int:
    complaint = _text(record, "chief_complaint")
    triage = _text(record, "triage_note")
    text_blob = complaint + " " + triage
    
    high_risk_keywords = [
        "chest pain", "shortness of breath", "repeated fainting", 
        "severe headache", "oxygen level dropped", "abnormal ecg",
        "critical lab alert", "stroke symptoms", "unconscious"
    ]
    
    for kw in high_risk_keywords:
        if kw in text_blob:
            return HIGH_RISK
    return ABSTAIN

# --- Department & Unit Bias Rules ---

def lf_dept_bias(record: object) -> int:
    dept = _text(record, "department")
    complaint = _text(record, "chief_complaint")
    
    # High risk departments
    if dept in ["cardiology", "emergency", "neurology"]:
        # Only abstain if it's clearly routine
        if complaint in ["routine follow up", "medication refill", "minor rash"]:
            return ABSTAIN
        return HIGH_RISK
    
    # Low risk departments
    if dept in ["generalmedicine", "pulmonology"]:
        if complaint in ["routine follow up", "medication refill", "minor rash", "sleep issue", "mild cough"]:
            return LOW_RISK
            
    return ABSTAIN

def lf_unit_c_risk(record: object) -> int:
    unit = _text(record, "hospital_unit")
    if unit == "unit_c":
        return HIGH_RISK
    return ABSTAIN

# --- Numeric Thresholds ---

def lf_lab_med_thresholds(record: object) -> int:
    lab_abnormal = _num(record, "lab_abnormal_count", -1)
    med_count = _num(record, "med_count", -1)
    comorbidity = _num(record, "comorbidity_count", 0)
    
    if lab_abnormal >= 2 or comorbidity >= 4:
        return HIGH_RISK
    if lab_abnormal == 0 and med_count <= 1 and comorbidity <= 1:
        return LOW_RISK
    return ABSTAIN

# --- Time Drift Adjusted Rule ---

def lf_time_drift_risk(record: object) -> int:
    quarter = _text(record, "year_quarter")
    prior_visits = _num(record, "prior_visit_count", 0)
    
    # In later quarters, even moderate prior visits might indicate higher risk management
    if quarter in ["2024q3", "2024q4"] and prior_visits > 50:
        return HIGH_RISK
    return ABSTAIN

LF_FUNCTIONS: list[Callable[[object], int]] = [
    lf_emergency_symptoms,
    lf_dept_bias,
    lf_unit_c_risk,
    lf_lab_med_thresholds,
    lf_time_drift_risk
]
