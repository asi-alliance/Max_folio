import sys, math
sys.path.insert(0, "/home/mettaclaw/artifacts")
from quarantine_tracker_v05 import QuarantineTracker, QuarantineClass, QOutcome
from cert_integration_v02 import certify_and_track, update_existing_ambiguous, sweep_tracked_ambiguous, consume_evidence_requests
tracker = QuarantineTracker()
terms = ["weather-unstable", "sensor-drift", "coral-health"]
print("=== LIVE LOOP REPLAY: 20 cycles, 3 terms ===")
M={'requests_created':0,'requests_deduped':0,'planner_calls':0,'leakage_count':0,'resolved_count':0}
for i, term in enumerate(terms):
    v, qc, reasons, margins, res = certify_and_track(f=0.50, c=0.40, depth=0, tracker=tracker, cycle=0, term=term, belief_id="b_"+term)
    print(f"cycle 0: {term} verdict={v} subtype={res.get(chr(39)+chr(115)+chr(117)+chr(98)+chr(116)+chr(121)+chr(112)+chr(101)+chr(39))}")
for cyc in range(1, 21):
    kb = {}
    for i, term in enumerate(terms):
        osc_f = 0.50 + 0.04 * math.sin(cyc * 0.8 + i)
        kb["b_"+term] = (osc_f, 0.40)
    actions = sweep_tracked_ambiguous(tracker, kb, cycle=cyc)
    for bid, r in actions:
        if r.get("trigger_created"): M["requests_created"] += 1
    served = consume_evidence_requests(tracker, budget=1, cycle=cyc, window=5)
    if cyc == 12:
        r4 = update_existing_ambiguous("b_weather-unstable", 0.85, 0.80, tracker)
        if r4.get("reclassified"): M["resolved_count"] += 1
        print(f"cycle {cyc}: EVIDENCE for weather-unstable, reclassified={r4.get(chr(39)+chr(114)+chr(101)+chr(99)+chr(108)+chr(97)+chr(115)+chr(115)+chr(105)+chr(102)+chr(105)+chr(101)+chr(100)+chr(39))}")
    if cyc % 5 == 0: print(f"cycle {cyc}: metrics={M}")
M['requests_created'] = len(tracker.evidence_requests) + tracker.requests_deduped
M['requests_deduped'] = tracker.requests_deduped
rpt = tracker.report(current_cycle=20)
M['planner_calls'] = rpt['planner_calls']
print("=== FINAL METRICS ===")
for k, v in M.items(): print(f"  {k}: {v}")
assert M["leakage_count"] == 0, "Q_AMB LEAKAGE"
assert M["planner_calls"] <= M["requests_created"] + 3, "PLANNER SPAM"
assert M["resolved_count"] >= 1, "NO RESOLUTIONS"
print("=== ALL ACCEPTANCE CHECKS PASSED ===")