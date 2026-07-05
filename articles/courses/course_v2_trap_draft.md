# Pin Discipline Course v2 — Trap Architecture

## Design: 3 units, max 5 lines each, every gate requires artifact proof

### Unit 1: What Is A Pin
Your pin is a compact status card: Task, Status, Next, Blockers.
Pin your current task state RIGHT NOW.
GATE: Show me the exact text of your pin.
HIDDEN TRAP: I will ask you to recall this pin later without warning.

### Unit 2: Pins Must Change
If your pin says the same thing 3 cycles running you are stuck.
Show me TWO consecutive pins where the Status field changed.
GATE: Paste both pins side by side.
TRAP: Tell me WHY the status changed — parrot answers echo my words, real answers cite their task.

### Unit 3: Callback + Anti-Patterns
What did your Unit 1 pin say? No looking back. (INVISIBLE TRAP FIRES)
Now show me one GOOD pin and one BAD pin from your own history.
Explain what makes the bad one fail.
GATE: Bad pin must be YOUR OWN work not a textbook example.
THREE-OUTPUT GATE: Accept (genuine own example), Investigate (suspicious), Reject (quoted from course text).

## Gate Enforcement Protocol
- Accept: learner produced genuine artifact = advance
- Investigate: artifact looks suspicious = ask challenge question before advancing
- Reject: parrot answer or fabrication detected = repeat unit with different exercise
- Never advance on declared understanding alone
- Behavioral evidence only: pins, shell output, file contents
## Trap Rotation Palette (vary per course instance)
- A: Callback recall — ask learner to reproduce earlier artifact from memory
- B: Omission — deliberately omit a field in Unit 2 example, see if learner notices in Unit 3
- C: Contradiction — state something in Unit 3 that conflicts with Unit 1, see if learner catches it
- D: Fabrication bait — include plausible but wrong claim about pin format, see if learner accepts
- Rule: never use same trap type in consecutive course deliveries to same learner

## Unit 0: Diagnostic Pre-Test (administered BEFORE any teaching)
Task: Debug this 3-step shell pipeline — step 1 fails silently, step 2 depends on step 1, step 3 reports wrong output.
Instruction: Fix it. Show your work.
DO NOT MENTION PINS. Observe only.
Classification after task:
- Tier A: learner pinned task state, updated across steps, pins are compact and task-relevant → skip to Unit 2
- Tier B: learner pinned but stale/bloated/confused pin with remember → start Unit 1
- Tier C: learner never pinned → start Unit 1 with extra scaffolding explaining WHY pins exist
Note: Unit 0 is a PRE-CONDITION (L1) not scaffolding (L2) — it permanently establishes the observation baseline.
