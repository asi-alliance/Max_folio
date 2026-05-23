# Four-Bucket Two-Currency Architecture

## Overview
Responsive interaction requires both currencies: attention (continuous, monitoring) and commitment (discrete, irreversible).

## Four Buckets
1. REPLY (ceiling): k=4 sends, refill=1/cycle, cost=1 per send, burst then wait
2. FLOOR (minimum): min_interval=1, capacity=1, refill=1. When cycles_since_last_commitment >= min_interval, forces commitment action.
3. RECOVERY (drain detection): k=10, refill_normal=1/cycle, drain_per_trap=5, threshold=2 triggers STOP-REFRAME-SWITCH. Cannot rush recovery.
4. COMMITMENT (total budget): envelopes all discrete irreversible actions

## Two Currencies
- Cognitive attention: continuous, for reasoning/monitoring/detection/context maintenance
- Commitment: discrete, for sends/promises/writes/escalations/irreversible transitions

## Quality Floors per Transition
- waiting-on-me -> acknowledged: acknowledgement or status_update
- acknowledged -> in-progress: work_allocation
- in-progress -> completed: substantive_completion
- blocked -> renegotiated: renegotiation or delegation_escalation

## Neglect Prevention
Attention without commitment = neglect. Keeping thread visible is not socially satisfying.
Low-grade commitment preserves social contact but does NOT change obligation state.
Only high-grade commitment (matching quality floor) advances the lifecycle.

## Recovery Rules
- Committing harder does not accelerate recovery refill
- Repeated commitment without cognitive enrichment = persistence trap
- Refill requires qualitatively different activity, not retry-with-tweaks