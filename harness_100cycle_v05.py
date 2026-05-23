import sys
sys.path.insert(0, "/home/mettaclaw/artifacts")
from quarantine_tracker_v05 import QuarantineTracker, QuarantineRecord, QOutcome
from cert_layer_v05 import QuarantineClass

t = QuarantineTracker(stale_threshold=10, default_cooldown=5)
terms = ["A","B","C","D","E"]
for term in terms:
    rec = QuarantineRecord(belief_id=term, term=term, f=0.6, c=0.5,
        reasons=["test"], quarantined_at="2026-01-01", quarantined_cycle=0)
    t.register(rec)
rows = []
for cycle in range(101):
    for i in range(2):
        term = terms[(cycle + i) % len(terms)]
        t.create_evidence_request(term, cycle=cycle, cooldown_cycles=5)
    if cycle % 8 == 0 and cycle > 0:
        unres = [e for e in t.evidence_requests if not e.resolved]
        if unres:
            unres[0].resolved = True
            unres[0].resolved_at_cycle = cycle
    rep = t.report(current_cycle=cycle)
    rows.append((cycle, rep.get("same_term_recreated_too_soon",0), rep.get("stale_request_count",0), rep.get("reopened_after_cooldown",0)))
print("cycle,deduped,stale,reopened")
for r in rows:
    print(f"{r[0]},{r[1]},{r[2]},{r[3]}")
d = [r[1] for r in rows]
s = [r[2] for r in rows]
o = [r[3] for r in rows]
print(f"\n--- SUMMARY ---")
print(f"max(deduped)={max(d)}")
print(f"max(stale)={max(s)}")
print(f"total(reopened)={o[-1]}")
print(f"trend_stale_last10={s[-10:]}")
print(f"trend_reopen_last10={o[-10:]}")
