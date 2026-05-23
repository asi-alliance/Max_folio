DES Dynamic Adaptive Model - 2026-05-22

Key insight from Kevin Machiels: Static Resource Capacity Modelling uses fixed parameters that compete (best selected). Dynamic Adaptive Model modifies itself during execution.

Architecture mapping:
- Scheduling policies are REVISABLE NAL beliefs (not fixed parameters)
- NAL belief revision IS the dynamic adaptation mechanism
- Four-layer separation: cognition enriches freely (probabilistic, advisory), commitment is gated (deterministic, policy)
- Aspects compose dynamically rather than transition between discrete states

Scheduling policies per role:
- Therapist: priority-by-emotional-urgency
- Inspector: priority-queue-by-evidence-weight
- Reporter: monte-carlo-probabilistic

Self-modifying loop: simulate -> observe -> revise policy belief -> commit under gate

DES cycle with dynamic adaptive scheduling:
1. Match events at current time
2. Agent selects min-time event
3. Remove event, add Perceived atom
4. fc-step5-novel-via derives new beliefs
5. NAL revision updates scheduling policy beliefs per evidence
6. Convert NOVEL results to future events
7. Add-atom each future event
8. GATE: commit only when check-gates pass