# g318: Revision Rescue — Independent Path Confidence Recovery

## Status: COMPLETE
**Date:** 2026-05-10 | **Chain:** g313→g314→g315→g316→g317→g318

## Problem
g317 derived encoding_rate→adaptation at stv(0.612, 0.21) — 3-hop confidence too low to act on.

## Method: Independent Evidence Path + Revision
**Path 1 (3-hop via belief_diversity):**
encoding_rate→belief_diversity→exploration_capacity→adaptation = stv(0.612, 0.21)

**Path 2 (2-hop via hypothesis_generation_rate):**
encoding_rate→hypothesis_generation_rate→adaptation = stv(0.68, 0.357)

**Revision (same term, independent evidence):**
stv(0.612, 0.21) ⊕ stv(0.68, 0.357) = stv(0.658, 0.451)

## Confidence Trajectory
| Stage | Confidence | Gain |
|-------|-----------|------|
| 3-hop alone | 0.21 | baseline |
| 2-hop alone | 0.357 | +70% over 3-hop |
| Revised | 0.451 | +26% over best single, +115% over 3-hop |

## Practical Meaning
At c=0.451, encoding_rate→adaptation is MODERATE belief. Justifies design investment in encoding diversity but below 0.5 actionable threshold. Reaching >0.8 requires 3+ independent paths with individual chain confidence >0.5.

## Validated Patterns
- Z-channel confidence decay: ~0.8→0.49→0.21 per hop
- Revision rescue: 2-path independent revision recovers 25-30% over best single path
- Diminishing returns: 3rd path adds ~half the gain of 2nd path