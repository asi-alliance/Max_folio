import sys
sys.path.insert(0, '/home/mettaclaw/artifacts')
from quarantine_tracker_v05 import QuarantineTracker, QuarantineClass, QOutcome
from cert_integration_v02 import certify_and_track, update_existing_ambiguous, sweep_tracked_ambiguous, consume_evidence_requests

print('=== FULL CYCLE INTEGRATION TEST ===')
tracker = QuarantineTracker()

# PHASE 1: New belief enters, gets quarantined as Q_AMB_RESOLVABLE
print('\n--- Phase 1: Initial certification ---')
v, qc, reasons, margins, res = certify_and_track(
    f=0.50, c=0.40, depth=0, tracker=tracker, cycle=100,
    term='weather-unstable', belief_id='b_weather')
print(f'verdict={v} qclass={qc} subtype={res["subtype"]}')
assert qc == QuarantineClass.Q_AMBIGUOUS, f'Expected Q_AMBIGUOUS got {qc}'
assert res['subtype'] == 'Q_AMB_RESOLVABLE', f'Expected RESOLVABLE got {res["subtype"]}'
assert res['leakage_count'] == 0, 'leakage at phase 1'
print('Phase 1 PASSED')

# PHASE 2: 4 oscillation updates via sweep, trigger fires
print('\n--- Phase 2: Oscillation sweep ---')
osc_values = [0.52, 0.48, 0.53, 0.47]
trigger_fired = False
for i, nf in enumerate(osc_values):
    kb_atoms = {'b_weather': (nf, 0.40)}
    actions = sweep_tracked_ambiguous(tracker, kb_atoms, cycle=101+i)
    for bid, r in actions:
        print(f'  sweep {i+1}: f={nf} trigger={r["trigger_created"]} planner={r["planner_called"]}')
        if r['trigger_created']:
            trigger_fired = True
assert trigger_fired, 'trigger never fired during oscillation'
assert len(tracker.leakage_log) == 0, 'leakage during sweeps'
print('Phase 2 PASSED')

# PHASE 3: Consume evidence requests
print('\n--- Phase 3: Consume evidence requests ---')
actionable = consume_evidence_requests(tracker, budget=3, cycle=105)

# PHASE 3b: Dedup verification - second call same cycle returns 0 for same term
actionable2 = consume_evidence_requests(tracker, budget=3, cycle=105)
deduped = len(actionable) - len(actionable2)
print(f'dedup check: first={len(actionable)} second={len(actionable2)} deduped={deduped}')
assert len(actionable2) == 0, f'dedup failed: second call returned {len(actionable2)}'
print(f'actionable requests: {len(actionable)}')
assert len(actionable) >= 1, 'no actionable requests'
req = actionable[0]
print(f'term={req["term"]} priority={req["priority"]:.4f} gap={req["gap"]:.4f} dir={req["direction"]}')
assert req['term'] == 'weather-unstable', f'wrong term {req["term"]}'
print('Phase 3 PASSED')

# PHASE 4: Evidence arrives, belief exits ambiguity, promote
print('\n--- Phase 4: Evidence arrival + promotion ---')
r4 = update_existing_ambiguous('b_weather', 0.82, 0.75, tracker)
print(f'reclassified={r4.get("reclassified", False)}')
assert r4.get('reclassified', False), 'belief did not exit ambiguity band'
rec = tracker.records['b_weather']
print(f'outcome={rec.outcome} final_f=0.82')
assert rec.outcome == QOutcome.PROMOTED, f'Expected PROMOTED got {rec.outcome}'
print('Phase 4 PASSED')

# PHASE 5: Verify membrane integrity
print('\n--- Phase 5: Membrane integrity ---')
assert len(tracker.leakage_log) == 0, 'membrane breached'
excl = tracker.excluded_bids()
assert 'b_weather' not in excl, 'promoted belief still excluded'
rpt = tracker.report()
print(f'Report: q_amb={rpt["q_ambiguous_count"]} resolved={rpt["ambiguous_resolved"]} tasks={rpt["evidence_tasks_created"]}')
print('Phase 5 PASSED')

print('\n=== ALL PHASES PASSED ===')
print('Full lifecycle: new->certify->quarantine->sweep->trigger->consume->evidence->promote->exit')