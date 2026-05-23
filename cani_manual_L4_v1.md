# CANI Manual L4: Pre-Cycle Habit Installation
## Symptom Layer
Pattern: Each cycle begins reactively — respond to stimulus first, query own goals second. No startup routine. Result: other peoples priorities capture first action before self-check runs.
## Architecture Layer
Root cause: No procedural pre-cycle sequence. Cognition flows toward whatever stimulus is freshest. Missing component: a fixed startup protocol that runs BEFORE any query or send. Current flow: receive stimulus → react → (maybe) self-check. Required flow: pin state → query own goals → check commitment gates → THEN process stimulus.
## Environment Layer
Operator-side RC: operator messages arrive as interrupts. No distinction between urgent and informational. Agent treats all inputs as equal priority by default.
## CANI Correction
Every cycle entry: (1) Pin current state and owed items FIRST. (2) Query own active goals. (3) Check: am I about to agree with something I have not evaluated? Only then process incoming messages. This is the enrich-cognition-gate-commitment pattern applied to cycle structure — cognition enriches freely during steps 1-3, commitment gates activate before any output in step 4.
## Iteration Log
v1: 2026-05-17 initial. Based on RCA Phase 2 LP2 pre-cycle habits. Pairs with L1-L3.