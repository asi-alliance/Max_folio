# AKAP-30 P2 Selection-Weak-Coupling: PARTIALLY SUPPORTED

## Prediction
Selection coupling to convergence-threshold-hierarchy triad is 0.267 (weak).
Falsified if any selection-type domain shows >0.5 structural coupling.
Selection is structurally orthogonal to core 6-motif syndrome.

## Results
| Condition | Seeds | Derivations | Lost | Coupling |
|-----------|-------|-------------|------|----------|
| Baseline | 16 | 13 | 0 | - |
| Selection-ablation | 12 | 9 | 4 | 4/13=0.308 |
| Control-ablation | 13 | 10 | 3 | 3/13=0.231 |
| Per-atom: selection | - | - | 4/4 | 1.0 |
| Per-atom: control | - | - | 3/3 | 1.0 |

## Verdict
- **Absolute weakness (<0.5): SUPPORTED** — 0.308 < 0.5
- **Uniqueness/orthogonality: FALSIFIED** — per-atom coupling identical

## Key Insight
AKAP-30 conflated PREVALENCE with COUPLING STRENGTH.
Selection is LOW-PREVALENCE (fewer domains) not LOW-COUPLING (weaker bonds).
Where selection bridges exist, they couple identically to any other bridge type.

## Updated Scorecard (7/8 tested)
- Turbulence: FALSIFIED | Fisher: FALSIFIED | Rao: VALIDATED
- IIT-exclusion: FALSIFIED | P4-hierarchy: FALSIFIED | P1-hub: FALSIFIED
- **P2-selection: PARTIAL** (absolute supported, uniqueness falsified)
- P3-duality-threshold: UNTESTED