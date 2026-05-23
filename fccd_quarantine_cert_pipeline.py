import sys
sys.path.insert(0, '/home/mettaclaw/artifacts')
from fccd_v01 import FCCDEngine, AuditTask, AuditVerdict, CollisionToken, ContextBridge
from quarantine_tracker_v07 import QuarantineTracker, QuarantineClass, Direction
from cert_layer_v07 import CertLayer

class FCCDQuarantineCertPipeline:
    def __init__(self, fccd_engine, tracker, cert_layer, t_collision=0.286):
        self.fccd_engine = fccd_engine
        self.tracker = tracker
        self.cert_layer = cert_layer
        self.t_collision = t_collision

    def run_audit_cycle(self, task):
        verdict, collision = self.fccd_engine.scheduled_audit(task)
        if verdict == AuditVerdict.COLLISION and collision:
            self.tracker.register(
                belief_id=collision.collision_id,
                quarantine_class=QuarantineClass.Q_COMPARTMENTALIZED,
                priority=collision.theta_gap,
                evidence_request='context_bridge_corroboration',
                theta_gap=collision.theta_gap,
                context_pair=collision.context_pair
            )
            return 'COLLISION_REGISTERED', collision
        return 'ADMIT', None

    def attempt_resolution(self, belief_id, current_collision_gap):
        resolved = self.tracker.compartmentalization_resolved(
            belief_id, current_collision_gap, self.t_collision)
        if resolved:
            verdict = self.cert_layer.certify(
                source_count=1.0, ambiguity_score=0.0,
                evidence_count=0.5, jaccard_index=0.5,
                stability_score=0.2, collision_gap=current_collision_gap)
            if verdict.admitted:
                self.tracker.admit(belief_id)
                return 'ADMITTED'
            return 'STILL_QUARANTINED'
        return 'STILL_COMPARTMENTALIZED'

if __name__ == '__main__':
    engine = FCCDEngine()
    engine.add_context('work', {'honesty': (0.9, 0.8), 'effort': (0.7, 0.9)})
    engine.add_context('social', {'honesty': (0.3, 0.7), 'loyalty': (0.8, 0.6)})
    engine.add_bridge(ContextBridge('work', 'social', ['honesty'], 0.33))
    tracker = QuarantineTracker()
    cert = CertLayer()
    pipe = FCCDQuarantineCertPipeline(engine, tracker, cert)
    task1 = AuditTask('audit1', cycle=1, context_pair=('work', 'social'))
    result1, col1 = pipe.run_audit_cycle(task1)
    print(f'T1_result={result1} collision_id={col1.collision_id if col1 else None}')
    candidates = ['honesty_work-social', 'effort_work', 'loyalty_social']
    selected = tracker.fair_select(candidates)
    print(f'T2_selected={selected} excluded_honesty={col1.collision_id not in selected if col1 else False}')
    result3 = pipe.attempt_resolution(col1.collision_id, current_collision_gap=0.2)
    print(f'T3_resolution_attempt_gap_0.2={result3}')
    result4 = pipe.attempt_resolution(col1.collision_id, current_collision_gap=0.1)
    print(f'T4_resolution_attempt_gap_0.1={result4}')
    task2 = AuditTask('audit2', cycle=2, context_pair=('work', 'social'), theta=task1.theta)
    result5, _ = pipe.run_audit_cycle(task2)
    print(f'T5_second_audit={result5} theta={task2.theta:.3f}')
    print('FCCD_QUARANTINE_CERT_PIPELINE_V01_TEST_DONE')