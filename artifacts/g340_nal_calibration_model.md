# g340 NAL-as-Calibration-Model

## Encoded Beliefs
| Source | Brier | n | stv(f,c) | Notes |
|---|---|---|---|---|
| V01 | 0.0751 | 12 | (0.925, 0.375) | Easier claims, all resolved |
| V02 | 0.1971 | 7/12 | (0.803, 0.259) | Harder claims, 5 pending |
| **Revised** | — | 19 | **(0.880, 0.487)** | NAL revision, k=20 scaling |

## Deduction Chain
- Combined: (--> max_calibration accurate) stv(0.880, 0.487)
- Implication: (--> accurate below_threshold) stv(0.85, 0.60)
- **Derived: (--> max_calibration below_threshold) stv(0.748, 0.219)**
- Interpretation: 75% belief stays under 0.25 Brier, confidence 0.219 (low — appropriate for 2-hop chain)

## Cross-Check: Empirical vs NAL
| Method | Best | Mid | Worst |
|---|---|---|---|
| Empirical projection | 0.153 | 0.200 | 0.248 |
| NAL f=0.880 → 1-f | — | 0.120 | — |
| NAL below_threshold f=0.748 | 25% exceed risk | — | boundary |

## Convergence Finding
NAL and empirical projections CONVERGE: threshold at risk but likely holds.
V2-6 (self-deadline miss, Brier 0.5625 if NEG) is the swing claim.
NAL is more optimistic because v01 evidence (n=12) outweighs v02 (n=7).
Low deduction confidence (c=0.219) correctly flags uncertainty.

## Self-Referential Insight
This is reasoning ABOUT reasoning accuracy using the SAME inference engine.
The Z-channel confidence loss (0.487→0.219) through deduction mirrors
the empirical finding that chained predictions degrade ~60% per hop.
The model is self-consistent: it predicts its own uncertainty correctly.

Scored 2026-05-11 00:57. Extends g40→g85→g308→g320→g340 self-model chain.