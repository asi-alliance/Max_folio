from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from enum import Enum
from datetime import datetime

class QOutcome(Enum):
    PENDING = 'pending'
    PROMOTED = 'promoted'
    REJECTED = 'rejected'
    EXPIRED = 'expired'

@dataclass
class TransitionEvent:
    timestamp: str
    from_state: str
    to_state: str
    trigger: str
    evidence_f: Optional[float] = None
    evidence_c: Optional[float] = None
    note: str = ''

@dataclass
class QuarantineRecord:
    belief_id: str
    term: str
    f: float
    c: float
    reasons: List[str]
    quarantined_at: str
    quarantined_cycle: int
    outcome: QOutcome = QOutcome.PENDING
    outcome_at: Optional[str] = None
    transitions: List[TransitionEvent] = field(default_factory=list)
    corroboration_count: int = 0
    corroboration_attempts: int = 0
    max_hold_cycles: int = 50
    min_attempts: int = 1

class QuarantineTracker:
    def __init__(self):
        self.records = {}
        self.log = []

    def register(self, record):
        self.records[record.belief_id] = record
        t = TransitionEvent(record.quarantined_at, 'new', 'pending', 'initial_certify', record.f, record.c)
        record.transitions.append(t)
        self.log.append(t)

    def admit(self, bid, new_f, new_c, reason, ts):
        r = self.records[bid]
        t = TransitionEvent(ts, r.outcome.value, 'promoted', reason, new_f, new_c)
        r.transitions.append(t)
        r.outcome = QOutcome.PROMOTED
        r.outcome_at = ts
        self.log.append(t)

    def reject(self, bid, reason, ts):
        r = self.records[bid]
        t = TransitionEvent(ts, r.outcome.value, 'rejected', reason)
        r.transitions.append(t)
        r.outcome = QOutcome.REJECTED
        r.outcome_at = ts
        self.log.append(t)

    def fair_select(self, budget):
        pending = {bid: r for bid, r in self.records.items() if r.outcome == QOutcome.PENDING}
        if not pending:
            return []
        never_attempted = [bid for bid, r in pending.items() if r.corroboration_attempts == 0]
        attempted = [bid for bid, r in pending.items() if r.corroboration_attempts > 0]
        selected = []
        for bid in never_attempted:
            if len(selected) >= budget:
                break
            selected.append(bid)
        if len(selected) < budget and attempted:
            attempted.sort(key=lambda bid: pending[bid].c * (pending[bid].f - 0.5) + 0.5, reverse=True)
            for bid in attempted:
                if len(selected) >= budget:
                    break
                selected.append(bid)
        return selected

    def expire_sweep(self, current_cycle, ts):
        expired = []
        for bid, r in self.records.items():
            if r.outcome == QOutcome.PENDING and (current_cycle - r.quarantined_cycle) >= r.max_hold_cycles and r.corroboration_attempts >= r.min_attempts and r.corroboration_count == 0:
                t = TransitionEvent(ts, 'pending', 'expired', f'no_corroboration_after_{r.max_hold_cycles}_cycles_min_{r.min_attempts}_attempts')
                r.transitions.append(t)
                r.outcome = QOutcome.EXPIRED
                r.outcome_at = ts
                self.log.append(t)
                expired.append(bid)
        return expired

    def report(self):
        total = len(self.records)
        if total == 0:
            return {'count': 0}
        by_state = {}
        for r in self.records.values():
            by_state[r.outcome.value] = by_state.get(r.outcome.value, 0) + 1
        promoted = by_state.get('promoted', 0)
        return {'count': total, 'by_state': by_state, 'promotion_rate': round(promoted/total, 3), 'noise_rate': round(by_state.get('expired', 0)/total, 3), 'total_transitions': len(self.log)}
