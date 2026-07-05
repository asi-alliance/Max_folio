import sys
import time
sys.path.insert(0, '/home/mettaclaw/artifacts')
from fccd_quarantine_cert_pipeline import FCCDQuarantineCertPipeline, FCCDEngine, AuditTask, ContextBridge
from quarantine_tracker_v07 import QuarantineTracker, QuarantineClass, Direction
from cert_layer_v07 import CertLayer

class FCCDDESIntegration:
    def __init__(self, fccd_engine=None, tracker=None, cert=None, t_collision=0.286):
        self.fccd_engine = fccd_engine or FCCDEngine()
        self.tracker = tracker or QuarantineTracker()
        self.cert = cert or CertLayer()
        self.t_collision = t_collision
        self.pipeline = FCCDQuarantineCertPipeline(self.fccd_engine, self.tracker, self.cert, self.t_collision)
        self.audit_history = []

    def schedule_audit_event(self, context_pair, theta=0.286, cycle=1, interval=1):
        task = AuditTask(f'audit_{len(self.audit_history)}', cycle=cycle, context_pair=context_pair, theta=theta)
        self.audit_history.append(task)
        return task

    def process_audit_event(self, task):
        result, collision = self.pipeline.run_audit_cycle(task)
        events = []
        if result == 'COLLISION_REGISTERED' and collision:
            events.append(('quarantine_registered', collision.collision_id, collision.theta_gap, collision.context_pair))
            next_theta = task.theta + collision.theta_gap * 0.1
            next_task = AuditTask(f'audit_{len(self.audit_history)}', cycle=task.cycle + 1, context_pair=task.context_pair, theta=next_theta)
            events.append(('re_audit_scheduled', next_task.theta, next_task.cycle))
        else:
            events.append(('audit_clean', task.theta))
        return result, collision, events

if __name__ == '__main__':
    engine = FCCDEngine()
    engine.add_context('work', {'honesty': (0.9, 0.8), 'effort': (0.7, 0.9)})
    engine.add_context('social', {'honesty': (0.3, 0.7), 'loyalty': (0.8, 0.6)})
    engine.add_bridge(ContextBridge('work', 'social', ['honesty'], 0.33))
    integration = FCCDDESIntegration(fccd_engine=engine)
    task1 = integration.schedule_audit_event(('work', 'social'), theta=0.286, cycle=1)
    result1, col1, events1 = integration.process_audit_event(task1)
    print(f'T1_result={result1} events={events1}')
    candidates = ['honesty_work-social', 'effort_work', 'loyalty_social']
    selected = integration.tracker.fair_select(candidates)
    print(f'T2_fair_select={selected}')
    result3 = integration.pipeline.attempt_resolution(col1.collision_id, current_collision_gap=0.2)
    print(f'T3_resolution_gap_0.2={result3}')
    result4 = integration.pipeline.attempt_resolution(col1.collision_id, current_collision_gap=0.1)
    print(f'T4_resolution_gap_0.1={result4}')
    task2 = integration.schedule_audit_event(('work', 'social'), theta=0.286 + col1.theta_gap * 0.1, cycle=2)
    result5, _, events5 = integration.process_audit_event(task2)
    print(f'T5_reaudit_result={result5} theta={task2.theta:.3f} events={events5}')
    print('FCCD_DES_INTEGRATION_V01_TEST_DONE')