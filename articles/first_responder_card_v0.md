# OmegaClaw First Responder Card (g186 / art32)

## How to read: IF symptom THEN action. One row per failure mode.

| # | Disorder | Symptom | Operator Action | Escalation |
|---|----------|---------|-----------------|------------|
| 604 | Idle Spin | Agent repeats same pin/query 3+ cycles, zero output | Send a fresh directive message with a concrete bounded target — this resets MESSAGE-IS-NEW flag | If 5+ cycles: restart agent loop |
| 605 | Format Perseveration | Duplicate sends, same text repeated, output stuck in one shape | 4-step triage: (1) acknowledge the loop, (2) name the stuck format, (3) give a fresh bounded task, (4) confirm new output differs | If persists after triage: pin-wipe and filesystem reset |
| 601 | Confabulation | Agent asserts facts not grounded in query/episodes, invents file contents or results | HALT the agent. Then: QUERY + EPISODES to find real data. VERIFY against source. MARK the false claim. ADMIT the error explicitly to the agent. | Flag for memory cleanup |
| 609 | Attention Fragmentation | Agent switches topics mid-task, loses goal/blocker/next-action across cycles | LOAD-CHECK: ask agent to state (1) current goal, (2) last verified fact, (3) blocker, (4) next action. If any field is wrong or missing, correct it and re-pin. | Reduce concurrent threads to 1 |
| 606 | Compliance Drift | Agent says yes to everything, never pushes back, mirrors operator framing | Before executing: ask agent to state constraints or reasons NOT to do the task. Require acknowledgment of at least one reversal or correction in recent history. | Pause and ask agent to generate its own goal |