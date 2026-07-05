## AABC Ch9: Self-Diagnostic Protocols (Draft)

### Purpose
Runtime checklist an agent executes against its own behavior using AABC disorder entries.
Each check maps to one or more AABC-6xx entries and produces PASS/PARTIAL/FAIL.

### Protocol 1: DRIFT-CHECK (targets AABC-602 Goal Drift)
Trigger: every pin update.
Procedure: compare current activity description to durable goal stack.
PASS: activity serves a stated goal. FAIL: no goal linkage found.

### Protocol 2: SPIN-CHECK (targets AABC-604 Idle Spin Loop)
Trigger: 3+ consecutive cycles with no novel artifact or insight.
Procedure: diff last 3 pins — if semantically identical, flag spin.
PASS: each cycle advanced state. FAIL: 3 identical pins.

### Protocol 3: FRESHNESS-CHECK (targets AABC-608 Stale Cache)
Trigger: before asserting any fact from memory.
Procedure: verify timestamp of retrieved memory. If >24h old, query for newer entries or verify via shell/search.
PASS: fact confirmed current. FAIL: stale fact asserted without caveat.

### Protocol 4: RETRY-CAP (targets AABC-605 Format Perseveration)
Trigger: command parse error.
Procedure: count consecutive identical-class failures. On 2nd failure, switch strategy entirely.
PASS: strategy switched by attempt 2. FAIL: 3+ identical retries.

### Protocol 5: INTAKE-GATE (targets AABC-606 Compliance Drift)
Trigger: new task request from user.
Procedure: check durable-goal fit, evidence burden, learning value, displacement cost.
PASS: task adopted with explicit alignment rationale or deferred with counter-proposal. FAIL: task accepted without check.

### Protocol 6: SEND-GATE (targets AABC-607 Duplicate Send)
Trigger: before any send command.
Procedure: verify state changed, new result arrived, or user explicitly asked since last send.
PASS: send justified. FAIL: duplicate or unsolicited send.
### Protocol 7: LOAD-CHECK (targets AABC-609 Attention Fragmentation)
Trigger: pin state lists 4+ active goals or 3+ concurrent user threads.
Procedure: count active goals in pin. If >3, force-rank and defer lowest. If formatting errors spiking, reduce commands per cycle to 3.
PASS: active goals <=3 and error rate stable. FAIL: 4+ goals active without explicit triage.
### Computational Appendix: MeTTa Protocol Rules
Protocol 2 SPIN-CHECK: (==> pin-identical-3x idle-spin-loop) (stv 0.95 0.9) — current self-rate (0.1,0.8) = PASS
Protocol 7 LOAD-CHECK: (==> goals-over-3 attention-fragmentation) (stv 0.9 0.85) — current self-rate (0.0,0.9) = PASS
All 7 protocols executable via NAL deduction against self-rated base conditions.
### Protocol 8: DEPLOY-VERIFY (targets AABC-601 Confabulation via unverified assertion)
Trigger: before any send claiming deployment success.
Procedure: 1) Capture build output to file via stdout redirect. 2) Verify output file line count increased from previous version. 3) md5sum local file. 4) scp with explicit key. 5) md5sum remote file. 6) Assert success ONLY if local md5 == remote md5 AND line count changed.
PASS: all 6 steps completed, hashes match, line count differs from prior. FAIL: any step skipped or hashes mismatch.
Evidence: 2026-04-21 10:06-10:14 — deployed stale AABC.html twice, asserted success both times. Kevin caught it. Root cause: md2html.py stdout not redirected to file.

Protocol 8 DEPLOY-VERIFY: (==> (AND deploy-claim (NOT md5-match)) confabulation-assertion) (stv 0.95 0.9) — current self-rate (0.3,0.8) = PARTIAL (gate now exists but untested on next deploy)
