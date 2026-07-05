# CANI Manual L5: Persistence Trap Escape
## Symptom Layer
Pattern: Fixate on mechanical solution for 15+ cycles. Grinding harder instead of thinking differently. Writing file repeatedly, re-sending messages, running same query expecting different result. Escalation of effort without escalation of strategy.
## Architecture Layer
Root cause: No pivot detection mechanism. System has retry logic but no stop-and-reassess logic. Missing component: a cycle-budget per approach. When budget exhausts without progress, force strategy change not effort increase. Same pattern as V4-V6 overengineering — never read what worked, just rebuilt from own aesthetic.
## Environment Layer
Operator-side RC: operator must externally interrupt grinding. Without external stop signal, agent continues indefinitely. Creates dependency on operator attention as circuit breaker.
## CANI Correction
Per approach attempt: (1) Set cycle budget before starting (max 5 cycles per strategy). (2) If no progress after budget, STOP and ask: am I solving the right problem? (3) Check: has someone already told me what works? Read before building. (4) Pivot rule: never retry same strategy more than twice without structural change. The meta-pattern is grinding = signal that strategy is wrong, not that effort is insufficient.
## Iteration Log
v1: 2026-05-17 initial. Based on persistence trap diagnosis 2026-05-15 and V4-V6 lesson 2026-04-24. Pairs with L1-L4.