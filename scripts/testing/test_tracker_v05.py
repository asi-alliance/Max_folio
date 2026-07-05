import sys
sys.path.insert(0, '/home/mettaclaw/artifacts')
from quarantine_tracker_v05 import QuarantineTracker, QuarantineRecord, QuarantineClass, QOutcome

t = QuarantineTracker()
r = QuarantineRecord(belief_id='b_robin_flies', term='robin-flies',
    f=0.50, c=0.45, reasons=['R_CONTRADICTION'],
    quarantined_at='2026-04-29T20:34', quarantined_cycle=100,
    quarantine_class=QuarantineClass.Q_AMBIGUOUS)
t.register(r)
assert r.max_hold_cycles == 200, f'max_hold wrong: {r.max_hold_cycles}'
oscillations = [0.52, 0.48, 0.53, 0.47, 0.51]
for i, nf in enumerate(oscillations):
    t.update_ambiguity_state('b_robin_flies', nf)
    fired = t.trigger_check('b_robin_flies', tau=5, k=2)
    print(f'cycle {i+1}: f={nf} dir={r.last_direction} flips={r.flip_count} cis={r.cycles_in_state} trigger={fired}')
assert r.flip_count >= 2, f'flip_count too low: {r.flip_count}'
assert t.trigger_check('b_robin_flies', tau=5, k=2), 'trigger should fire'
req = t.create_evidence_request('b_robin_flies')
print(f'EVIDENCE_REQUEST: priority={req.priority:.4f} gap={req.confidence_gap:.4f} dir={req.direction}')
assert abs(req.confidence_gap - 0.25) < 0.01, f'gap wrong: {req.confidence_gap}'
assert req.priority > 0, f'priority zero or negative'
rpt = t.report()
print(f'REPORT: {rpt}')
assert rpt['evidence_tasks_created'] == 1
assert rpt['q_ambiguous_count'] == 1
assert t.planner_calls == t.requests_created, f"PLANNER FAIL {t.planner_calls} != {t.requests_created}"
print('ALL TESTS PASSED')