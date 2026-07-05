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
class EvidenceRequest:
    term: str
    direction: Optional[str]
    confidence_gap: float
    sources: List[str]
    priority: float
    created_at: str = ""
    created_cycle: int = 0
    resolved_at_cycle: int = -1
    resolved: bool = False

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
    cycles_in_state: int = 0
    flip_count: int = 0
    last_f: Optional[float] = None
    last_direction: Optional[str] = None

    def __post_init__(self):
        if self.quarantine_class == QuarantineClass.Q_AMBIGUOUS:
            self.max_hold_cycles = 200

class QuarantineTracker:
    def __init__(self, stale_threshold=10, default_cooldown=5):
        self.records: Dict[str, QuarantineRecord] = {}
        self.leakage_log: List[Dict] = []
        self.duplicates_blocked = 0
        self.failed_recerts = []
        self.evidence_requests: List[EvidenceRequest] = []
        self.requests_deduped = 0
        self.request_attempts = 0
        self.requests_created = 0
        self.cooldown_suppressed = 0
        self.false_admit_count_live = 0
        self.false_admit_count_test = 0
        self.planner_calls = 0
        self.stale_threshold = max(stale_threshold, 2 * default_cooldown)
        self.default_cooldown = default_cooldown
        self.reopened_after_cooldown = 0

    def register(self, record: QuarantineRecord):
        if record.belief_id in self.records:
            self.duplicates_blocked += 1
            return
        self.records[record.belief_id] = record
        record.transitions.append(TransitionEvent(
            timestamp=record.quarantined_at, from_state="NONE",
            to_state="PENDING", trigger="register",
            note=f"class={record.quarantine_class.value}"))

    def update_ambiguity_state(self, bid, new_f):
        r = self.records[bid]
        if r.quarantine_class != QuarantineClass.Q_AMBIGUOUS or r.outcome != QOutcome.PENDING:
            return
        r.cycles_in_state += 1
        if r.last_f is not None:
            new_dir = "UP" if new_f > r.last_f else ("DOWN" if new_f < r.last_f else r.last_direction)
            if r.last_direction is not None and new_dir != r.last_direction:
                r.flip_count += 1
                r.transitions.append(TransitionEvent(
                    timestamp=str(datetime.now()), from_state="PENDING",
                    to_state="PENDING", trigger=f"flip_{r.flip_count}",
                    evidence_f=new_f, note=f"{r.last_direction}->{new_dir}"))
            r.last_direction = new_dir
        r.last_f = new_f
        r.f = new_f

    def trigger_check(self, bid, tau=5, k=2):
        r = self.records[bid]
        if r.quarantine_class != QuarantineClass.Q_AMBIGUOUS or r.outcome != QOutcome.PENDING:
            return False
        return r.cycles_in_state >= tau or r.flip_count >= k

    def create_evidence_request(self, bid, existing_sources=None, cycle=0, cooldown_cycles=5):
        r = self.records[bid]
        gap = max(0.0, 0.7 - r.c)
        self.request_attempts += 1
        priority = r.c * (0.5 - abs(r.f - 0.5))
        active = any(e for e in self.evidence_requests if e.term == r.term and not e.resolved)
        cooled = any(e for e in self.evidence_requests if e.term == r.term and e.resolved and e.resolved_at_cycle >= 0 and (cycle - e.resolved_at_cycle) < cooldown_cycles)
        if active:
            self.requests_deduped += 1
            return None
        elif cooled:
            self.cooldown_suppressed += 1
            return None
        has_prior_resolved = any(e for e in self.evidence_requests if e.term == r.term and getattr(e, 'resolved', False))
        if has_prior_resolved:
            self.reopened_after_cooldown += 1
        req = EvidenceRequest(
            term=r.term, direction=r.last_direction,
            confidence_gap=gap,
            sources=existing_sources or [],
            priority=priority,
            created_at=str(datetime.now()))
        self.evidence_requests.append(req)
        self.requests_created += 1
        req.created_cycle = cycle
        self.planner_calls += 1
        r.transitions.append(TransitionEvent(
            timestamp=req.created_at, from_state="PENDING",
            to_state="PENDING", trigger="evidence_request",
            note=f"priority={priority:.4f} gap={gap:.4f}"))
        return req

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


    def check_false_admit(self, bid, new_f, new_c, test_mode=False):
        from cert_layer_v05 import certify
        if bid not in self.records:
            return False
        r = self.records[bid]
        if r.outcome != QOutcome.PROMOTED:
            return False
        verdict, _, _, _ = certify(new_f, new_c)
        if verdict.name != "ADMIT":
            if test_mode:
                self.false_admit_count_test += 1
            else:
                self.false_admit_count_live += 1
            return True
        return False
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

    def stale_request_count(self, current_cycle):
        return len([e for e in self.evidence_requests if not e.resolved and (current_cycle - e.created_cycle) > self.stale_threshold])

    def report(self, current_cycle=0):
        recs = list(self.records.values())
        return dict(
            q_undersupported_count=sum(1 for r in recs if r.quarantine_class == QuarantineClass.Q_UNDERSUPPORTED),
            q_ambiguous_count=sum(1 for r in recs if r.quarantine_class == QuarantineClass.Q_AMBIGUOUS),
            ambiguous_resolved=self.ambiguous_resolved,
            ambiguous_still_open=self.ambiguous_still_open,
            partner_pool_leakage_count=len(self.leakage_log),
            evidence_seeking_triggers=sum(1 for r in recs if r.quarantine_class == QuarantineClass.Q_AMBIGUOUS and r.outcome == QOutcome.PENDING),
            total_promoted=sum(1 for r in recs if r.outcome == QOutcome.PROMOTED),
            failed_recert_count=len(self.failed_recerts),
            failed_recert_reasons=dict(Counter(r["verdict"] for r in self.failed_recerts)),
            evidence_tasks_created=len(self.evidence_requests),
            evidence_tasks_resolved=sum(1 for e in self.evidence_requests if e.resolved),
            noop_rate=sum(1 for e in self.evidence_requests if e.resolved and e.confidence_gap <= 0) / max(1, len(self.evidence_requests)),
            cooldown_suppressed=self.cooldown_suppressed,
            requests_created=self.requests_created,
            requests_deduped=self.requests_deduped,
            planner_calls=self.planner_calls,
            reopened_after_cooldown=self.reopened_after_cooldown,
            stale_request_count=self.stale_request_count(current_cycle),
            same_term_recreated_too_soon=self.requests_deduped,
request_attempts=self.request_attempts,
false_admit_count_live=self.false_admit_count_live,
false_admit_count_test=self.false_admit_count_test,
)
