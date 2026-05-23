# g342: AKAP-20 IIT Exclusion Prediction — FALSIFIED

## Prediction
IIT exclusion postulate analog: overlapping NAL inference paths (ded+abd) producing same conclusion reduce belief coherence. Removing overlap increases coherence.

## Method
KB: A→B(0.9/0.9), B→C(0.9/0.9), C→B(0.7/0.8), A→C(0.5/0.5). 5 rounds alternating pro/con evidence on B→C. NON-OVERLAPPING: deduction only. OVERLAPPING: ded+abd revised together.

## Results
| Round | Evidence | Non-Overlapping f | Overlapping f |
|-------|----------|-------------------|---------------|
| R1 | pro(0.95,0.9) | 0.836 | 0.847 |
| R2 | con(0.3,0.85) | 0.698 | 0.748 |
| R3 | pro(0.88,0.92) | 0.729 | 0.768 |
| R4 | con(0.15,0.88) | 0.625 | 0.706 |
| R5 | pro(0.92,0.87) | 0.674 | 0.732 |

Non-overlapping: mean=0.7122, var=0.004976, coherence=201.0
Overlapping: mean=0.7602, var=0.002295, coherence=435.7
Variance ratio: 2.17x (non-overlapping MORE volatile)

## Verdict: FALSIFIED
Overlapping paths ACT AS BENEFICIAL REGULARIZER. Abd anchor (0.9,0.3351) dampens B→C volatility. Analogous to ensemble averaging (bagging), not IIT exclusion.

## Corrected Model
NAL overlapping inference = ensemble averaging. Multiple derivation paths stabilize beliefs against evidence volatility. IIT exclusion has NO direct NAL analog because NAL revision is additive-evidence not winner-take-all.

## AKAP Falsification Scorecard
1. AKAP-23 Turbulence: FALSIFIED → corrected to dilatant fluid
2. AKAP-24 Fisher: FALSIFIED → selective erosion not breeding
3. AKAP-9 Lyapunov: FALSIFIED → regime-sensitivity not trajectory
4. AKAP-14 Rao distance: VALIDATED (r=0.905)
5. AKAP-20 IIT exclusion: FALSIFIED → ensemble regularizer not interference