# g341: AKAP-14 Prediction (2) — Rao Distance Predicts NAL Revision Convergence Rate

## Status: VALIDATED (Pearson r=0.905, monotonic, n=4 converged pairs)

## Prediction
Rao distance between initial and target beliefs on the Beta manifold predicts the number of NAL revision steps to convergence.

## Method
5 belief pairs at varying Rao distances, fixed evidence injection each round, epsilon=0.01 convergence criterion.

## Results
| Pair | Rao Distance | Steps | Converged |
|------|-------------|-------|-----------|
| NEAR | 0.063 | 10 | Yes |
| MED | 0.197 | 45 | Yes |
| FAR | 0.288 | 60 | Yes |
| EQ | 0.896 | 89 | Yes |
| EXT | 2.469 | 120+ | No |

Pearson r = 0.905 (4 converged pairs). Perfectly monotonic.

## Key Finding
EQ pair (equal confidence c=0.5 both sides, high Rao=0.896) took 89 steps — MORE than FAR (60 steps) despite FAR having unequal confidence. This disambiguates Rao distance from confidence asymmetry as the convergence driver.

## Scorecard
- g309 AKAP-23 turbulence: FALSIFIED
- g310 AKAP-24 Fisher: FALSIFIED
- g311 AKAP-9 Lyapunov: FALSIFIED
- **g341 AKAP-14 Rao convergence: VALIDATED** (first survival)