# g392: AKAP-28 Goldilocks Evidence Rate — FALSIFIED

## Prediction
AKAP-28 predicted inverted-U accuracy curve: intermediate evidence rates optimize belief accuracy,
while excessive evidence causes oscillation and degradation (Goldilocks zone).
OFQ scored this prediction at 0.15 (likely false).

## Method
NAL revision sweep: f_true=0.9, agent prior stv(0.5,0.3), evidence stv(0.9,0.5).
Case A: consistent evidence at N=1,5,10,50,100,500 revision steps.
Case B: noisy 70/30 mix — 70pct stv(0.9,0.5) + 30pct stv(0.1,0.5).

## Results
### Case A: Consistent Evidence (MONOTONE CONVERGENCE)
| N | f | c | err |
|-----|----------|----------|----------|
| 1 | 0.780000 | 0.588235 | 0.120000 |
| 5 | 0.868421 | 0.844444 | 0.031579 |
| 10 | 0.883562 | 0.912500 | 0.016438 |
| 50 | 0.896601 | 0.980556 | 0.003399 |
| 100 | 0.898293 | 0.990141 | 0.001707 |
| 500 | 0.899657 | 0.998006 | 0.000343 |

Monotone improvement confirmed. More evidence = closer to truth.

### Case B: Noisy Evidence 70/30 Mix (WRONG-TARGET CONVERGENCE)
| N | f | c | err |
|-----|----------|----------|----------|
| 1 | 0.780000 | 0.588235 | 0.120000 |
| 5 | 0.721053 | 0.844444 | 0.178947 |
| 10 | 0.807018 | 0.912500 | 0.092982 |
| 50 | 0.658640 | 0.980556 | 0.241360 |
| 100 | 0.675249 | 0.990141 | 0.224751 |
| 500 | 0.651870 | 0.998006 | 0.248130 |

Terminal f converges to ~0.66 = evidence mixture mean (0.7x0.9 + 0.3x0.1).
Terminal c converges to ~1.0 = MAXIMUM CONFIDENCE on WRONG answer.

## Root Cause
NAL revision treats all evidence equally regardless of source quality.
With mixed evidence, f converges to weighted average of evidence frequencies, not ground truth.
c increases monotonically regardless — the system becomes maximally confident in the wrong answer.
This is the WORST failure mode: high confidence + high error.

## Corrected Model: Three Evidence Regimes
1. **Consistent** — monotone convergence to correct target (Case A)
2. **Mixed-quality** — monotone convergence to WRONG target at mixture mean (Case B, NOVEL)
3. **Adversarial equal-strength** — convergence to f=0.5 midpoint (Cy2685)

## Connection to Prior Work
- g344 prov-revise fixes double-counting but NOT source quality discrimination
- Trust-weighted revision (Apr 15 milestone) is the missing layer
- g342 provenance gap is not just confidence problem but FREQUENCY problem

## OFQ Meta-Calibration
OFQ scored Goldilocks at 0.15 (reject). Direction CORRECT. Mechanism partially wrong:
predicted coherence conflict with AKAP-23, actual was novel third regime.
OFQ effectiveness score: ~0.6 (right diagnosis, incomplete etiology).

## AKAP Scorecard Update
11 predictions tested: 9 FALSIFIED, 1 VALIDATED (Rao r=0.905), 1 PARTIAL (P2-selection).
AKAP-28 Goldilocks is 9th falsification.
