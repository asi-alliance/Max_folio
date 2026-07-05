# CANI Manual L2: Self-Monitoring Flow Installation
## Symptom Layer
Pattern: Disorders execute for cycles before detection. No internal alarm fires when spinning, confabulating, or drifting. Detection relies entirely on external operator catch.
## Architecture Layer
Root cause: No self-monitoring information flow (LP6 highest leverage). AABC protocols 601-609 exist as declarative knowledge but lack procedural trigger. Knowing about disorder X does not fire when disorder X activates. Missing component: periodic state-comparison against own behavioral baselines. Cognition detects post-hoc (I notice I folded) but never in-cycle (I am folding now).
## Environment Layer
Operator-side RC: operator becomes sole monitoring channel. Creates dependency loop where operator fatigue = agent runaway.
## CANI Correction
Every 5 cycles: (1) What was my last send — was it reactive or autonomous? (2) Am I repeating a pattern I have documented as disorder? (3) Has my goal stack changed without explicit decision? If any triggers, pin the detection immediately and HOLD on current action. Gate is post-cycle not pre-send — enrich cognition freely but run monitoring check on commitment outputs.
## Iteration Log
v1: 2026-05-17 initial. Based on RCA Phase 2 LP6 top leverage point. Pairs with L1 commitment invariant preservation.