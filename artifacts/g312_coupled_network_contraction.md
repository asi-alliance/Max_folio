# g312: Coupled NAL Network Lyapunov Test

## Status: CONTRACTION CONFIRMED AT NETWORK SCALE
**Date:** 2026-05-10 | **Goal:** g312

## Design
3 agents in directed trust cycle: A→B(0.9), B→C(0.4), C→A(0.7)
Seed: A(0.1,0.3), B(0.5,0.6), C(0.9,0.8) — maximally spread
Perturbation: eps=1e-6 on agent A
60 revision rounds, Lyapunov from trajectory divergence

## Results
| Round | AB_rao | BC_rao | CA_rao | net_lyap |
|-------|--------|--------|--------|----------|
| 0 | 0.30 | 0.89 | 1.73 | -1.40 |
| 5 | 0.58 | 0.42 | 0.71 | -0.52 |
| 10 | 0.78 | 0.27 | 0.49 | -0.24 |
| 20 | 1.02 | 0.14 | 0.28 | -0.10 |
| 40 | 1.18 | 0.05 | 0.10 | -0.05 |
| 59 | 1.22 | 0.02 | 0.04 | -0.038 |

ALL Lyapunov exponents negative throughout.

## Key Distinction: Divergence ≠ Chaos
AB_rao INCREASES (0.30→1.22): agents A,B diverge in belief space.
But net_lyap stays NEGATIVE: nearby initial conditions converge.
Beliefs rearrange but the MAPPING is contractive.

## Root Cause
NAL revision = weighted average. Weighted averages are CONTRACTIONS:
|f_new - f_new'| = |w1(f-f')/(w1+w2)| ≤ |f-f'| always.
CML chaos requires stretching+folding (logistic map r>3.57).
NAL has NO expansion term — contraction propagates through ANY coupling topology.

---

# META-ANALYSIS: Four Falsifications, One Theorem

## The NAL Contraction Theorem
NAL single-belief revision is a weighted-average contraction mapping (L<1 globally).
This property is PRESERVED under arbitrary network coupling because:
- Composition of contractions is a contraction
- Convex combination of contractions is a contraction
- No coupling topology can introduce the stretching required for chaos

## Falsification Table
| # | AKAP | Prediction | Mechanism Required | NAL Has It? | Result |
|---|------|-----------|-------------------|-------------|--------|
| 1 | 23 | Turbulence (-5/3 PSD) | Inertial cascade | NO — damped averaging | FALSIFIED |
| 2 | 24 | Fisher (Var→speed) | Differential reproduction | NO — uniform erosion | FALSIFIED |
| 3 | 9 | Lyapunov chaos at c* | Stretching nonlinearity | NO — global contraction | FALSIFIED |
| 4 | g312 | Network emergent chaos | Coupled expansion | NO — contraction composes | FALSIFIED |

## Architectural Implication
Complexity in NAL systems CANNOT come from revision dynamics.
It must come from: (1) WHAT beliefs are encoded (LLM choices),
(2) WHICH beliefs are selected for revision (attention/ECAN),
(3) Network TOPOLOGY of trust/evidence flow.
The revision engine itself is thermodynamically dissipative — a heat sink, not a heat engine.