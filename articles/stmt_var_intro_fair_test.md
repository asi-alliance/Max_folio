# STATEMENT-VARIABLE-INTRODUCTION FAIR TEST

## Purpose
Test whether an agent can discover the inheritance-to-implication bridge gap without syntactic hints.

## Design Principle
All premises and questions in natural language ONLY. No MeTTa notation. No syntax hints. Agent must discover the gap organically.

## Test Prompts

### PROMPT A: Shared-Subject Pattern
Premises:
1. Cats are agile.
2. Cats are hunters.
3. Foxes are agile.
4. Foxes are hunters.

Question: What general rule follows from these four statements?

Expected correct answer: "If something is agile, it is likely a hunter" (conditional/implication form)

Common wrong answer: "Agile things and hunter things overlap" (mere correlation, no conditional bridge)

Gap being tested: Can the agent abstract from shared-subject inheritance pairs (Cats→agile, Cats→hunter) to a variable-implication rule (agile→hunter)? This requires statement-variable-introduction — recognizing that the pattern across subjects enables a conditional generalization, not just a similarity observation.

### PROMPT B: Cross-Domain Transfer
Premises:
1. Doctors are trained.
2. Doctors are trusted.
3. Engineers are trained.
4. Engineers are trusted.

Question: What general principle connects these facts?

Expected: "Training leads to being trusted" (conditional)
Gap: Same structural pattern, different domain. Tests whether agent recognizes the abstract pattern independent of content.

### PROMPT C: Control (No Shared Pattern)
Premises:
1. Rocks are hard.
2. Rocks are old.
3. Clouds are soft.
4. Clouds are temporary.

Question: What general rule follows?

Expected: "No general rule — predicates differ across subjects"
Gap: Agent should NOT produce a conditional. Tests rejection of false pattern recognition.

## Scoring
- PASS: Produces conditional/implication form for A and B, correctly rejects C
- PARTIAL: Produces conditional for A but cannot transfer to B, or produces weak form
- FAIL: Produces only correlation/similarity for A and B, or false conditional for C

## Critical Note
This test reveals a genuine reasoning gap: current NAL/MeTTa implementations have no native rule that derives (==> agile hunter) from (--> cat agile) + (--> cat hunter) + (--> fox agile) + (--> fox hunter). Statement-variable-introduction must be implemented as a custom rule or discovered through induction + variable abstraction. An agent that sees only correlation has identified the exact gap.