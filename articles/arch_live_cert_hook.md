# Live Certification Hook Architecture

## Entry Point
`agent_cycle_entry.py::cycle_entry()` → `phase3_run_pipeline()` → returns `{new_atoms, pipeline}`

## Hook A: New Belief Intercept
- Location: inside `phase3_run_pipeline()`, after `phase2_compress()` returns `new_atoms`
- For each atom in new_atoms, parse (term, f, c)
- Call `certify_and_track(f, c, depth=0, tracker, cycle, term, bid=hash(term))`
- ADMIT → inject into agent_kb.json normally
- QUARANTINE → store in tracker only, do NOT inject into KB
- This prevents unvetted beliefs from entering the persistent store

## Hook B: Per-Cycle Ambiguity Sweep
- Function: `sweep_tracked_ambiguous(tracker, kb_atoms, cycle)`
- Runs EVERY cycle, before or after pipeline
- Iterates tracker.records where outcome==PENDING and qclass==Q_AMBIGUOUS
- For each: lookup latest f from inference output or KB
- Call `update_existing_ambiguous(bid, new_f, new_c, tracker)`
- Subtype routing: GENUINE→log only, RESOLVABLE→trigger_check→evidence_request

## Hook C: Evidence Request Consumer
- Function: `consume_evidence_requests(tracker, cycle, budget=3)`
- Calls `tracker.fair_select(budget, exclude_class=Q_UNDERSUPPORTED)`
- For each selected bid:
  1. Generate query cue from EvidenceRequest.term
  2. Run H5 query+search fusion (query LTM + web search)
  3. Atomize results via atomize_v3
  4. NAL revision: revise Q_AMB belief (old_f,old_c) with (new_evidence_f, new_evidence_c)
  5. Call `tracker.promote_with_recert(bid, revised_f, revised_c, reason, ts)`
  6. If ADMIT → inject into KB, mark EvidenceRequest.resolved=True
  7. If still QUARANTINE → increment corroboration_count, keep seeking

## Hook D: Resolution Gateway
- Promoted atoms pass through `deploy_filter()` normally
- Expired atoms (expire_sweep) are logged and dropped
- Rejected atoms are logged with rejection reason

## Invariants
- Membrane: Q_AMB atoms NEVER enter KB until promoted via recert
- Budget: only Q_AMB_RESOLVABLE consumes evidence-seeking cycles
- Leakage: check_leakage called before any cross-atom inference involving quarantined bids
- Fairness: fair_select ensures round-robin across pending beliefs