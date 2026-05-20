from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
import time

class Direction(Enum):
    DIVERSIFY = auto()
    DISAMBIGUATE = auto()
    SUPPORT = auto()
    BRIDGE = auto()

class QuarantineClass(Enum):
    Q_TUNNEL_VISION = auto()
    Q_AMBIGUOUS = auto()
    Q_UNDERSUPPORTED = auto()
    Q_COMPARTMENTALIZED = auto()

@dataclass
class QuarantineRecord:
    belief_id: str
    quarantine_class: QuarantineClass
    direction: Direction
    evidence_request: str
    priority: float
    enter_time: float
    max_hold: int = 100
    theta_gap: float = 0.0
    context_pair: Optional[tuple] = None

QUARANTINE_CONFIG = {
    QuarantineClass.Q_TUNNEL_VISION: {'direction': Direction.DIVERSIFY, 'max_hold': 100},
    QuarantineClass.Q_AMBIGUOUS: {'direction': Direction.DISAMBIGUATE, 'max_hold': 80},
    QuarantineClass.Q_UNDERSUPPORTED: {'direction': Direction.SUPPORT, 'max_hold': 120},
    QuarantineClass.Q_COMPARTMENTALIZED: {'direction': Direction.BRIDGE, 'max_hold': 150},
}

class QuarantineTracker:
    def __init__(self):
        self.quarantined: Dict[str, QuarantineRecord] = {}
        self.excluded_bids: Set[str] = set()

    def register(self, belief_id, quarantine_class, priority=0.0, evidence_request="", theta_gap=0.0, context_pair=None):
        if quarantine_class not in QUARANTINE_CONFIG:
            return None
        config = QUARANTINE_CONFIG[quarantine_class]
        record = QuarantineRecord(belief_id=belief_id, quarantine_class=quarantine_class, direction=config['direction'], evidence_request=evidence_request, priority=priority, enter_time=time.time(), max_hold=config['max_hold'], theta_gap=theta_gap, context_pair=context_pair)
        self.quarantined[belief_id] = record
        self.excluded_bids.add(belief_id)
        return record

    def admit(self, belief_id):
        if belief_id in self.quarantined:
            del self.quarantined[belief_id]
            self.excluded_bids.discard(belief_id)
            return True
        return False

    def fair_select(self, candidates, exclude_quarantined=True):
        if exclude_quarantined:
            return [c for c in candidates if c not in self.excluded_bids]
        return list(candidates)

    def compartmentalization_resolved(self, belief_id, collision_gap, t_collision):
        if belief_id not in self.quarantined:
            return False
        record = self.quarantined[belief_id]
        if record.quarantine_class != QuarantineClass.Q_COMPARTMENTALIZED:
            return False
        return collision_gap <= t_collision

if __name__ == '__main__':
    tracker = QuarantineTracker()
    r1 = tracker.register("honesty_work", QuarantineClass.Q_COMPARTMENTALIZED, priority=0.51, evidence_request="context_bridge_corroboration", theta_gap=0.51, context_pair=("work", "social"))
    print(f"T1_registered={r1 is not None} class={r1.quarantine_class.name} dir={r1.direction.name}")
    candidates = ["honesty_work", "effort_work", "loyalty_social"]
    selected = tracker.fair_select(candidates)
    print(f"T2_selected={selected} excluded={'honesty_work' not in selected}")
    resolved = tracker.compartmentalization_resolved("honesty_work", collision_gap=0.2, t_collision=0.286)
    print(f"T3_resolved={resolved}")
    tracker.admit("honesty_work")
    selected2 = tracker.fair_select(candidates)
    print(f"T4_after_admit={selected2} back={'honesty_work' in selected2}")
    print("QUARANTINE_TRACKER_V07_TEST_DONE")