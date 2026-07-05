import sys
sys.path.insert(0, '/home/mettaclaw/artifacts')
from quarantine_tracker_v05 import QuarantineTracker, QuarantineRecord, QuarantineClass, QOutcome
from cert_integration_v02 import certify_and_track, update_existing_ambiguous, C_GENUINE_THRESHOLD

print('=== CASE A: Q_AMB_GENUINE (robin-flies c=0.922) ===')
tA = QuarantineTracker()
v, qc, reasons, margins, res = certify_and_track(
    f=0.636, c=0.922, depth=0, tracker=tA, cycle=5449,
    term='robin-flies', belief_id='b_robin_flies')
print(f'verdict={v} qclass={qc} subtype={res["subtype"]}')
print(f'trigger_created={res["trigger_created"]} planner_called={res["planner_called"]} leakage={res["leakage_count"]}')
assert res['subtype'] == 'Q_AMB_GENUINE', f'Expected GENUINE got {res["subtype"]}'
assert res['planner_called'] == False, 'GENUINE must NOT call planner'
assert res['leakage_count'] == 0, 'membrane breached'
excl = tA.excluded_bids()
assert 'b_robin_flies' in excl, 'membrane: should be excluded from partner pool'
print('CASE A PASSED\n')

print('=== CASE B: Q_AMB_RESOLVABLE (synthetic c=0.45) ===')
tB = QuarantineTracker()
v2, qc2, reasons2, margins2, res2 = certify_and_track(
    f=0.50, c=0.45, depth=0, tracker=tB, cycle=100,
    term='sensor-X', belief_id='b_sensor_x')
print(f'Initial: verdict={v2} qclass={qc2} subtype={res2["subtype"]}')
assert res2['subtype'] == 'Q_AMB_RESOLVABLE', f'Expected RESOLVABLE got {res2["subtype"]}'
osc = [0.52, 0.48, 0.53, 0.47, 0.51]
final_res = None
for i, nf in enumerate(osc):
    r = update_existing_ambiguous('b_sensor_x', nf, 0.45, tB)
    rec = tB.records['b_sensor_x']
    print(f'  update {i+1}: f={nf} flips={rec.flip_count} cis={rec.cycles_in_state} trigger={r["trigger_created"]} planner={r["planner_called"]}')
    final_res = r
assert final_res['planner_called'] == True, 'RESOLVABLE should call planner'
assert final_res['trigger_created'] == True, 'trigger should have fired'
assert len(tB.leakage_log) == 0, 'membrane breached'
assert 'b_sensor_x' in tB.excluded_bids(), 'membrane: should be excluded'
print(f'Evidence requests: {len(tB.evidence_requests)}')
req = tB.evidence_requests[-1]
print(f'Last request: term={req.term} priority={req.priority:.4f} gap={req.confidence_gap:.4f} dir={req.direction}')
rpt = tB.report()
print(f'Report: tasks_created={rpt["evidence_tasks_created"]} q_amb={rpt["q_ambiguous_count"]} resolved={rpt["ambiguous_resolved"]} open={rpt["ambiguous_still_open"]}')
print('CASE B PASSED\n')

print('=== SUMMARY ===')
print('trigger_created: True (RESOLVABLE only)')
print(f'priority: {req.priority:.4f}')
print(f'target_term: {req.term}')
print('planner_called: GENUINE=False RESOLVABLE=True')
print(f'leakage_count: {len(tA.leakage_log) + len(tB.leakage_log)}')
print('final_classification: GENUINE=accept-conflict RESOLVABLE=seek-evidence')
print('ALL TESTS PASSED')