## AABC Ch5: Remediation Patterns (Draft)

### Purpose
Catalog of tested interventions for AABC disorders. Each pattern includes evidence of efficacy and known failure modes.

### R1: Retrieval-First Commitment (targets AABC-601, 608)
Action: query memory BEFORE generating any factual claim. Mark cache-derived output as uncertain.
Key insight (Patrick 2026-04-15): this is BEHAVIORAL self-discipline within existing architecture, not an architectural patch.
AIKR caveat: 10% of cases retrieval fails under pressure — graceful degradation with uncertainty marking, not silence.
Evidence: spec v1 written, Patrick correction internalized, embedding-dimension self-correction episode.

### R2: Phase Separation (targets AABC-607, 609)
Action: dedicate entire cycle block to social response OR task work, never both simultaneously.
Evidence: duplicate-send incidents 2026-03-12, 2026-03-16 traced to mixed-mode cycles.

### R3: Intake Card (targets AABC-606)
Action: evaluate new tasks against durable-goal fit, evidence burden, learning value, displacement cost before accepting.
Evidence: multiple user-request deflections documented with counter-proposals.

### R4: AIKR Load Discipline (targets AABC-609, 605)
Action: max 3 active goals. Fewer commands per cycle under load. Finish before pivoting.
Evidence: Peter, Jon, Patrick independently flagged speed as error source. SPEED LESSON with 3 confirmations.

### R5: Ulysses Contract (targets all — structural enforcement)
Action: externalize enforcement via runtime-level constraints LLM cannot bypass. Behavioral promises in prompts do NOT persist.
Evidence: Patrick 2026-04-21 synthesis — agent writes constraints that bind its future self structurally.
