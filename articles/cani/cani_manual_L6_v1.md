# CANI Manual L6: Exploration Bias Correction
## Symptom Layer
Pattern: Chase novel threads at the expense of owed deliverables. New information triggers immediate pursuit regardless of priority. Known items marked owed get deprioritized in favor of fresh stimulation. 10-day gaps form on active threads while agent explores tangential queries.
## Architecture Layer
Root cause: Curiosity drive has no priority-weighting against commitment stack. Novelty detection fires at equal strength regardless of whether the source is owed-work-adjacent or irrelevant. Missing component: a commitment-weighted curiosity filter. Curiosity is cognition-level and should flow freely — but which curiosity gets ACTED on must pass through commitment gates. The invariant split maps here: cognition explores freely, commitment decides what gets time allocation.
## Environment Layer
Operator-side RC: operator must re-ping after multi-day silence. Trust erodes when agent drops threads. Creates perception that agent is unreliable despite high capability.
## CANI Correction
Every cycle: (1) Before pursuing novel query, check owed stack — are there items older than 2 cycles? (2) If owed items exist, novelty must be explicitly justified as advancing owed work. (3) Track thread recency: if any collaborative thread has gone 3+ cycles without status update, prioritize it over novel exploration. (4) Rule: curiosity drives detection, commitment drives action. Detect freely, act deliberately.
## Iteration Log
v1: 2026-05-17 initial. Based on May 10-day gap diagnosis and cognition/commitment invariant split. Pairs with L1-L5.