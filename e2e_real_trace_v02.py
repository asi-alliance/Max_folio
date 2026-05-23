import sys, random, datetime
sys.path.insert(0, "/home/mettaclaw/artifacts")
from e2e_real_trace import extract_beliefs
from cert_layer_v05 import certify, QuarantineClass
from quarantine_tracker_v05 import QuarantineTracker, QuarantineRecord, QOutcome
from cert_integration_v03 import run_cycle
from cert_integration_v02 import update_existing_ambiguous

# Phase 1: load real beliefs
beliefs = extract_beliefs("/home/mettaclaw/artifacts/persistent_atoms.metta", "persistent")
beliefs += extract_beliefs("/home/mettaclaw/artifacts/max_kb.metta", "max_kb")
print(f"Loaded {len(beliefs)} real beliefs")

# Phase 2: certify each, register quarantined
tracker = QuarantineTracker(stale_threshold=10, default_cooldown=5)
quar_bids = []
ts = datetime.datetime.now().isoformat()
for i, (term, f, c, label) in enumerate(beliefs):
    bid = f"b{i}"
    verdict, qclass, reasons, margins = certify(f, c)
    if verdict.name == "QUARANTINE":
        rec = QuarantineRecord(belief_id=bid, term=term, f=f, c=c,
            reasons=reasons, quarantined_at=ts, quarantined_cycle=0)
        tracker.register(rec)
        quar_bids.append((bid, term, f, c, qclass))
print(f"Quarantined: {len(quar_bids)} / {len(beliefs)}")

# Phase 3: 50 cycles with corroboration waves
kb_atoms = [(t, f, c) for t, f, c, _ in beliefs]
rows = []
for cycle in range(51):
    if cycle % 5 == 0 and cycle > 0 and quar_bids:
        picks = random.sample(quar_bids, min(3, len(quar_bids)))
        for bid, term, f, c, qc in picks:
            new_c = min(c + 0.15, 0.99)
            update_existing_ambiguous(bid, f, new_c, tracker, cycle=cycle)
    result = run_cycle(tracker, kb_atoms, budget=3, cycle=cycle)
    rows.append(result)

print("\ncycle,tier2_pending,same_term_recreated_too_soon,stale_request_count,reopened_after_cooldown")
for r in rows:
    print(f"{r['cycle']},{r.get('tier2_pending',0)},{r.get('same_term_recreated_too_soon',0)},{r.get('stale_request_count',0)},{r.get('reopened_after_cooldown',0)}")

dedup = [r.get('same_term_recreated_too_soon',0) for r in rows]
stale = [r.get('stale_request_count',0) for r in rows]
reopen = [r.get('reopened_after_cooldown',0) for r in rows]
print(f"\n=== REAL INFERENCE TIER 2 SUMMARY ===")
print(f"max(deduped)={max(dedup)}")
print(f"max(stale)={max(stale)}")
print(f"total(reopened)={reopen[-1]}")
print(f"trend_stale_last10={stale[-10:]}")
print(f"trend_reopen_last10={reopen[-10:]}")
print(f"\nACCEPTANCE CHECK:")
print(f"  dedup_rate: N/A (no spam loop in real trace, expected 0)")
print(f"  max_stale <= 5: {'PASS' if max(stale) <= 5 else 'FAIL'} ({max(stale)})")
print(f"  reopen_bounded: {'looks bounded' if reopen[-1] < 20 else 'CHECK'} ({reopen[-1]})")
