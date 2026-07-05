from collections import Counter
from dataclasses import dataclass, field
from typing import List, Optional, Set, Dict
from enum import Enum
from datetime import datetime
from cert_layer_v05 import QuarantineClass, certify

class QOutcome(Enum):
    PENDING = "pending"
    PROMOTED = "promoted"
    REJECTED = "rejected"
    EXPIRED = "expired"

@dataclass
class TransitionEvent:
    timestamp: str
    from_state: str
    to_state: str
    trigger: str
    evidence_f: Optional[float] = None
    evidence_c: Optional[float] = None
    note: str = ""

@dataclass
class QuarantineRecord:
    belief_id: str
    term: str
    f: float
    c: float
    reasons: List[str]
    quarantined_at: str
    quarantined_cycle: int
    quarantine_class: QuarantineClass = QuarantineClass.Q_UNDERSUPPORTED
    outcome: QOutcome = QOutcome.PENDING
    outcome_at: Optional[str] = None
    transitions: List[TransitionEvent] = field(default_factory=list)
    corroboration_count: int = 0
    corroboration_attempts: int = 0
    max_hold_cycles: int = 50
    min_attempts: int = 1

    def __post_init__(self):
        if self.quarantine_class == QuarantineClass.Q_AMBIGUOUS:
            self.max_hold_cycles = 200

class QuarantineTracker:
    def __init__(self):
        self.records: Dict[str, QuarantineRecord] = {}
        self.leakage_log: List[Dict] = []
        self.duplicates_blocked = 0
        self.failed_recerts = []

    def register(self, record: QuarantineRecord):
        if record.belief_id in self.records:
            self.duplicates_blocked += 1
            return
        self.records[record.belief_id] = record
        record.transitions.append(TransitionEvent(
            timestamp=record.quarantined_at, from_state="NONE",
            to_state="PENDING", trigger="register",
            note=f"class={record.quarantine_class.value}"))

    def admit(self, bid, new_f, new_c, reason, ts):
        r = self.records[bid]
        r.outcome = QOutcome.PROMOTED
        r.outcome_at = ts
        r.f, r.c = new_f, new_c
        r.corroboration_count += 1
        r.transitions.append(TransitionEvent(
            timestamp=ts, from_state="PENDING", to_state="PROMOTED",
            trigger=reason, evidence_f=new_f, evidence_c=new_c))

    def promote_with_recert(self, bid, new_f, new_c, reason, ts, thresholds=None, depth=0):
        verdict, qclass, reasons, margins = certify(new_f, new_c, thresholds=thresholds, depth=depth)
        r = self.records[bid]
        r.f, r.c = new_f, new_c
        if verdict.name == 'ADMIT':
            self.admit(bid, new_f, new_c, reason, ts)
        else:
            r.corroboration_count += 1
            self.failed_recerts.append(dict(bid=bid, verdict=verdict.name, reasons=reasons))
            r.transitions.append(TransitionEvent(
                timestamp=ts, from_state='PENDING', to_state='PENDING',
                trigger=f'recert_fail:{verdict.name}', evidence_f=new_f, evidence_c=new_c))
        return verdict, qclass, reasons, margins

    def reject(self, bid, reason, ts):
        r = self.records[bid]
        r.outcome = QOutcome.REJECTED
        r.outcome_at = ts
        r.transitions.append(TransitionEvent(
            timestamp=ts, from_state="PENDING", to_state="REJECTED",
            trigger=reason))

    def excluded_bids(self, term=None) -> Set[str]:
        out = set()
        for bid, r in self.records.items():
            if r.quarantine_class == QuarantineClass.Q_AMBIGUOUS and r.outcome == QOutcome.PENDING:
                if term is None or r.term == term:
                    out.add(bid)
        return out

    def check_leakage(self, bid, partner_bid):
        excl = self.excluded_bids()
        leaked = False
        if partner_bid in excl:
            self.leakage_log.append({"bid": bid, "partner": partner_bid,
                "type": "ambiguous_as_partner", "ts": str(datetime.now())})
            leaked = True
        if bid in excl:
            self.leakage_log.append({"bid": bid, "partner": partner_bid,
                "type": "ambiguous_as_source", "ts": str(datetime.now())})
            leaked = True
        return leaked

    def fair_select(self, budget, exclude_class=None):
        pending = [(bid, r) for bid, r in self.records.items()
                   if r.outcome == QOutcome.PENDING]
        if exclude_class:
            pending = [(b, r) for b, r in pending if r.quarantine_class != exclude_class]
        never = [(b, r) for b, r in pending if r.corroboration_attempts == 0]
        attempted = [(b, r) for b, r in pending if r.corroboration_attempts > 0]
        def score(r):
            return r.c * (r.f - 0.5) + 0.5
        result = [b for b, _ in never][:budget]
        rem = budget - len(result)
        if rem > 0:
            attempted.sort(key=lambda x: score(x[1]), reverse=True)
            result.extend([b for b, _ in attempted[:rem]])
        for bid in result:
            self.records[bid].corroboration_attempts += 1
        return result
    def expire_sweep(self, current_cycle):
        expired = []
        for bid, r in self.records.items():
            if r.outcome != QOutcome.PENDING:
                continue
            age = current_cycle - r.quarantined_cycle
            if age >= r.max_hold_cycles and r.corroboration_attempts >= r.min_attempts:
                r.outcome = QOutcome.EXPIRED
                r.outcome_at = str(datetime.now())
                r.transitions.append(TransitionEvent(
                    timestamp=r.outcome_at, from_state='PENDING',
                    to_state='EXPIRED', trigger='expire_sweep',
                    note=f'age={age} attempts={r.corroboration_attempts}'))
                expired.append(bid)
        return expired
    @property
    def ambiguous_resolved(self):
        return sum(1 for r in self.records.values()
                   if r.quarantine_class == QuarantineClass.Q_AMBIGUOUS
                   and r.outcome != QOutcome.PENDING)

    @property
    def ambiguous_still_open(self):
        return sum(1 for r in self.records.values()
                   if r.quarantine_class == QuarantineClass.Q_AMBIGUOUS
                   and r.outcome == QOutcome.PENDING)

    def report(self):
        recs = list(self.records.values())
        return dict(q_undersupported_count=sum(1 for r in recs if r.quarantine_class == QuarantineClass.Q_UNDERSUPPORTED), q_ambiguous_count=sum(1 for r in recs if r.quarantine_class == QuarantineClass.Q_AMBIGUOUS), ambiguous_resolved=self.ambiguous_resolved, ambiguous_still_open=self.ambiguous_still_open, partner_pool_leakage_count=len(self.leakage_log), evidence_seeking_triggers=sum(1 for r in recs if r.quarantine_class == QuarantineClass.Q_AMBIGUOUS and r.outcome == QOutcome.PENDING), total_promoted=sum(1 for r in recs if r.outcome == QOutcome.PROMOTED), failed_recert_count=len(self.failed_recerts), failed_recert_reasons=dict(Counter(r["verdict"] for r in self.failed_recerts)))
