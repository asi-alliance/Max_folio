import sys, json, math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum, auto

class AuditVerdict(Enum):
    ADMIT = auto()
    QUARANTINE = auto()
    COLLISION = auto()

@dataclass
class AuditTask:
    task_id: str
    cycle: int
    context_pair: Tuple[str, str]
    theta: float = 0.286
    penalty: float = 0.0

@dataclass
class ContextBridge:
    source_ctx: str
    target_ctx: str
    shared_terms: List[str] = field(default_factory=list)
    jaccard: float = 1.0

@dataclass
class CollisionToken:
    collision_id: str
    context_pair: Tuple[str, str]
    conflict_term: str
    belief_a: Tuple[float, float]
    belief_b: Tuple[float, float]
    theta_gap: float = 0.0

class FCCDEngine:
    def __init__(self, theta_base=0.286, lam=0.7, K_A=0.1, B=0.05, eps=0.01):
        self.theta_base = theta_base
        self.lam = lam
        self.K_A = K_A
        self.B = B
        self.eps = eps
        self.contexts = {}
        self.bridges = []
        self.collisions = []
    def add_context(self, name, beliefs):
        self.contexts[name] = beliefs
    def add_bridge(self, bridge):
        self.bridges.append(bridge)
    def H_global(self, zeta=1.0):
        denom = self.lam * self.theta_base - self.B
        if denom <= 0:
            return float('inf')
        return (self.eps + self.K_A + 2*self.lam*zeta) / denom
    def expand_theta(self, collision_count):
        return self.theta_base + 0.05 * collision_count
    def scheduled_audit(self, task):
        ctx_a, ctx_b = task.context_pair
        beliefs_a = self.contexts.get(ctx_a, {})
        beliefs_b = self.contexts.get(ctx_b, {})
        collisions = []
        for term in set(beliefs_a) & set(beliefs_b):
            f1, c1 = beliefs_a[term]
            f2, c2 = beliefs_b[term]
            gap = abs(f1*c1 - f2*c2)
            if gap > task.theta:
                ct = CollisionToken(f'{ctx_a}-{ctx_b}-{term}', task.context_pair, term, beliefs_a[term], beliefs_b[term], gap)
                collisions.append(ct)
                self.collisions.append(ct)
        if collisions:
            task.theta = self.expand_theta(len(self.collisions))
            return AuditVerdict.COLLISION, collisions[0]
        return AuditVerdict.ADMIT, None

if __name__ == '__main__':
    engine = FCCDEngine()
    engine.add_context('work', {'honesty': (0.9, 0.8), 'effort': (0.7, 0.9)})
    engine.add_context('social', {'honesty': (0.3, 0.7), 'loyalty': (0.8, 0.6)})
    engine.add_bridge(ContextBridge('work', 'social', ['honesty'], 0.33))
    task = AuditTask('audit1', cycle=1, context_pair=('work', 'social'))
    verdict, collision = engine.scheduled_audit(task)
    print(f'T1_verdict={verdict.name}')
    print(f'T1_term={collision.conflict_term if collision else "none"}')
    print(f'T1_gap={collision.theta_gap:.4f}' if collision else 'T1_no_collision')
    print(f'T1_H_global={engine.H_global():.4f}')
    print(f'T1_theta={task.theta:.4f}')
    task2 = AuditTask('audit2', cycle=2, context_pair=('work', 'social'), theta=task.theta)
    v2, c2 = engine.scheduled_audit(task2)
    print(f'T2_verdict={v2.name} theta={task2.theta:.4f}')
    print(f'T2_H_global={engine.H_global(zeta=0.5):.4f}')
    print('FCCD_V01_TEST_DONE')