import sys
sys.path.insert(0, "/home/mettaclaw/artifacts")
from quarantine_tracker_v05 import QuarantineTracker, QuarantineRecord, QOutcome
from cert_layer_v05 import QuarantineClass, certify
from cert_integration_v02 import consume_evidence_requests

t = QuarantineTracker()

# Pre-register a QuarantineRecord with Q_AMBIGUOUS so create_evidence_request works
rec = QuarantineRecord(belief_id="belief_A", term="catDog", f=0.5, c=0.3, reasons=["low_c"], quarantined_at="2026-04-30T11:00", quarantined_cycle=0, quarantine_class=QuarantineClass.Q_AMBIGUOUS)
t.register(rec)

# Phase 1: create 3 requests for same term (expect 1 created, 2 deduped)
t.create_evidence_request("belief_A", cycle=1)
t.create_evidence_request("belief_A", cycle=1)
t.create_evidence_request("belief_A", cycle=1)
p1_att = t.request_attempts
p1_cre = t.requests_created
p1_ded = t.requests_deduped
print(f"PHASE1: attempts={p1_att} created={p1_cre} deduped={p1_ded}")
assert p1_att == 3 and p1_cre == 1 and p1_ded == 2, f"PHASE1 FAIL {p1_att},{p1_cre},{p1_ded}"

# Phase 2: consume with budget=1 at cycle=10
consume_evidence_requests(t, budget=1, cycle=10)
resolved = [r for r in t.evidence_requests if r.resolved]
print(f"PHASE2: resolved={len(resolved)} resolved_at_cycle={resolved[0].resolved_at_cycle if resolved else None}")
assert len(resolved) == 1 and resolved[0].resolved_at_cycle == 10, "PHASE2 FAIL"

# Phase 3: re-request at cycle=12 (within cooldown=5, should be suppressed)
t.create_evidence_request("belief_A", cycle=12)
p3_ded = t.requests_deduped
print(f"PHASE3: deduped_total={p3_ded} (cooldown suppression={p3_ded - p1_ded})")
assert p3_ded == 2 and t.cooldown_suppressed == 1, f"PHASE3 FAIL deduped={p3_ded} cooldown={t.cooldown_suppressed}"

# Phase 4: re-request at cycle=16 (outside cooldown, should succeed)
t.create_evidence_request("belief_A", cycle=16)
p4_cre = t.requests_created
p4_att = t.request_attempts
print(f"PHASE4: created={p4_cre} attempts={p4_att}")
assert p4_cre == 2 and p4_att == 5, f"PHASE4 FAIL cre={p4_cre} att={p4_att}"

assert t.planner_calls == t.requests_created, f"PLANNER FAIL {t.planner_calls} != {t.requests_created}"
print("ALL PHASES PASSED")
print(f"KEVIN METRICS: attempts={p4_att} created={p4_cre} deduped={t.requests_deduped} cooldown_suppressions=1 resolved_at_cycle=10")
print("--- Phase 5: check_false_admit ---")
from quarantine_tracker_v05 import QuarantineRecord, QuarantineClass
p5rec = QuarantineRecord(belief_id="p5_test", term="p5_term", f=0.85, c=0.55, reasons=["R_WEAK_QUARANTINE"], quarantined_at="2026-04-30T19:20", quarantined_cycle=100)
t.register(p5rec)
t.promote_with_recert("p5_test", 0.95, 0.85, "RECERT_GOOD", "2026-04-30T19:21")
result = t.check_false_admit("p5_test", 0.3, 0.1, test_mode=True)
print("false_admit triggered:", result, "count:", t.false_admit_count_test)
assert t.false_admit_count_test >= 1, "Expected false_admit_count >= 1"
rpt = t.report()
print("Tier2 report:", {k: rpt[k] for k in ["request_attempts","false_admit_count_live"]})
assert rpt["request_attempts"] > 0, "Expected request_attempts > 0"
print("ALL PHASE 5 ASSERTIONS PASSED")
