# cert_layer_v03_simple.py -- hard-threshold gatekeeper, no Rao/curvature.
# Patched: R_WEAK split into R_WEAK_REJECT (c<0.4) and R_WEAK_QUARANTINE (0.4<=c<0.6)
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime

DEFAULT_THRESHOLDS = {'t_contradiction': 0.4, 't_weak': 0.6, 't_vacuous': 0.01, 'min_confidence': 0.3}
class Verdict(Enum):
    ADMIT = 'ADMIT'
    QUARANTINE = 'QUARANTINE'
    REJECT = 'REJECT'

class QuarantineAction(Enum):
    HOLD = 'hold_for_review'
    DOWNGRADE = 'downgrade_confidence'
    SEEK_CORROBORATION = 'seek_corroboration'

REASON_CODES = {'R_CONTRAICITON': 'freq near 0.5 with high conf', 'R_WEAK_REJECT': 'confidence below hard reject threshold', 'R_WEAK_QUARANTINE': 'confidence in quarantine band', 'R_VACUOUS': 'confidence near zero', 'R_LOW_FREQ': 'frequency below min threshold', 'R_PASS': 'all margins positive'}

@dataclass
class BeliefState:
    f: float = 0.5
    c: float = 0.0
    source: str = 'unknown'
    rule: str = 'none'
    timestamp: str = ''
    reasons: list = field(default_factory=list)
    verdict: object = None

def certify(f, c, thresholds=None):
    T = thresholds or DEFAULT_THRESHOLDS
    reasons = []
    margins = {}
    margins["m_contradiction"] = abs(f - 0.5) - T["t_contradiction"]
    margins["m_weak"] = c - T["t_weak"]
    margins["m_vacuous"] = c - T["t_vacuous"]
    margins["m_freq"] = f - T["min_confidence"]
    if margins["m_contradiction"] < 0: reasons.append("R_CONTRADICTION")
    if margins["m_weak"] < 0:
        if c < 0.4: reasons.append("R_WEAK_REJECT")
        else: reasons.append("R_WEAK_QUARANTINE")
    if margins["m_vacuous"] < 0: reasons.append("R_VACUOUS")
    if margins["m_freq"] < 0: reasons.append("R_LOW_FREQ")
    composite = min(margins.values())
    if composite >= 0:
        verdict = Verdict.ADMIT; reasons = ["R_PASS"]
    elif composite > -0.1 or (reasons and all(r in ("R_WEAK_QUARANTINE",) for r in reasons)):
        verdict = Verdict.QUARANTINE
    else:
        verdict = Verdict.REJECT
    return verdict, reasons, margins

def health_check(beliefs):
    n = len(beliefs)
    if n == 0: return {"count": 0}
    admitted = sum(1 for b in beliefs if b.verdict == Verdict.ADMIT)

CONTEXT_PROFILES = {
    'internal': {'t_contradiction': 0.3, 't_weak': 0.4, 't_vacuous': 0.01, 'min_confidence': 0.2},
    'action': {'t_contradiction': 0.4, 't_weak': 0.6, 't_vacuous': 0.1, 'min_confidence': 0.3},
    'high_stakes': {'t_contradiction': 0.45, 't_weak': 0.75, 't_vacuous': 0.15, 'min_confidence': 0.4},
}


def certify_ctx(f, c, context="action"):
    """Convenience wrapper: look up context profile and call certify."""
    thresholds = CONTEXT_PROFILES.get(context, DEFAULT_THRESHOLDS)
    return certify(f, c, thresholds)
