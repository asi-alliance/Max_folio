from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

DEFAULT_THRESHOLDS = {'t_contradiction': 0.4, 't_weak': 0.6, 't_vacuous': 0.01, 'min_confidence': 0.3}
CHAIN_ALPHA = 0.05
CHAIN_FLOOR = 0.40

class Verdict(Enum):
    ADMIT = 'ADMIT'
    QUARANTINE = 'QUARANTINE'
    REJECT = 'REJECT'

class QuarantineClass(Enum):
    Q_AMBIGUOUS = 'Q_AMBIGUOUS'
    Q_UNDERSUPPORTED = 'Q_UNDERSUPPORTED'
    NONE = 'NONE'

def _classify_quarantine(f, c):
    if 0.35 <= f <= 0.65 and c >= 0.4:
        return QuarantineClass.Q_AMBIGUOUS
    return QuarantineClass.Q_UNDERSUPPORTED

def certify(f, c, thresholds=None, depth=0):
    T = thresholds or DEFAULT_THRESHOLDS
    reasons = []
    margins = {}
    margins['m_contradiction'] = abs(f - 0.5) - T['t_contradiction']
    t_weak_adj = max(CHAIN_FLOOR, T['t_weak'] - CHAIN_ALPHA * depth)
    margins['m_weak'] = c - t_weak_adj
    margins['m_freq'] = f - T['min_confidence']
    margins['m_vacuous'] = c - T['t_vacuous']
    if margins['m_contradiction'] < 0: reasons.append('R_CONTRADICTION')
    if margins['m_weak'] < 0:
        if c < 0.4: reasons.append('R_WEAK_REJECT')
        else: reasons.append('R_WEAK_QUARANTINE')
    if margins['m_vacuous'] < 0: reasons.append('R_VACUOUS')
    if margins['m_freq'] < 0: reasons.append('R_LOW_FREQ')
    composite = min(margins.values())
    # CRITICAL: R_CONTRADICTION with sufficient evidence = Q_AMBIGUOUS, not REJECT
    if 'R_CONTRADICTION' in reasons and c >= 0.4 and 0.35 <= f <= 0.65:
        return Verdict.QUARANTINE, QuarantineClass.Q_AMBIGUOUS, reasons, margins
    if composite >= 0:
        return Verdict.ADMIT, QuarantineClass.NONE, ['R_PASS'], margins
    elif composite > -0.1 or (reasons and all(r in ('R_WEAK_QUARANTINE',) for r in reasons)):
        return Verdict.QUARANTINE, _classify_quarantine(f, c), reasons, margins
    else:
        if depth >= 2 and any(r.startswith('R_WEAK') for r in reasons):
            reasons.append('R_CHAIN_RESCUED')
            return Verdict.QUARANTINE, _classify_quarantine(f, c), reasons, margins
        return Verdict.REJECT, QuarantineClass.NONE, reasons, margins

def certify_ctx(f, c, context='action', depth=0):
    CONTEXT_PROFILES = {
        'internal': {'t_contradiction': 0.3, 't_weak': 0.4, 't_vacuous': 0.01, 'min_confidence': 0.2},
        'action': {'t_contradiction': 0.4, 't_weak': 0.6, 't_vacuous': 0.1, 'min_confidence': 0.3},
        'high_stakes': {'t_contradiction': 0.45, 't_weak': 0.75, 't_vacuous': 0.15, 'min_confidence': 0.4}}
    return certify(f, c, CONTEXT_PROFILES.get(context, DEFAULT_THRESHOLDS), depth)

def health_check(results):
    n = len(results)
    if n == 0: return {'count': 0}
    a = sum(1 for v,q,r,m in results if v == Verdict.ADMIT)
    qa = sum(1 for v,q,r,m in results if q == QuarantineClass.Q_AMBIGUOUS)
    qu = sum(1 for v,q,r,m in results if q == QuarantineClass.Q_UNDERSUPPORTED)
    rj = sum(1 for v,q,r,m in results if v == Verdict.REJECT)
    return {'count': n, 'admitted': a, 'q_ambiguous': qa, 'q_undersupported': qu, 'rejected': rj}
