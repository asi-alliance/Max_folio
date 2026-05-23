# AKAP-9: Lyapunov Instability Falsification Report

## Status: PREDICTION FALSIFIED
**Date:** 2026-05-10 | **Goal:** g311 | **Domain:** Dynamical Systems & Chaos Theory

## Original Prediction
NAL belief revision near separatrix c*≈0.55 exhibits sensitive dependence on initial conditions (positive Lyapunov exponent). Trajectories starting epsilon-apart diverge exponentially near c*, converge far from it.

## Test Protocol
- Two beliefs with epsilon=0.001 perturbation in both f and c
- 8 c_init values: 0.30, 0.40, 0.50, 0.55, 0.60, 0.70, 0.80, 0.90
- Evidence stream: f_ev=0.7, c_ev=0.7, deduction decay d=0.96
- 50 revision steps per trajectory pair
- Lyapunov exponent = lim ln|delta(t)/delta(0)|/t

## Results
| c_init | lyap_f | lyap_c | max_div_f | max_div_c |
|--------|--------|--------|-----------|----------|
| 0.30 | -0.37 | -0.60 | 0.0 | 0.0 |
| 0.40 | -0.38 | -0.62 | 0.0 | 0.0 |
| 0.50 | -0.39 | -0.64 | 0.0 | 0.0 |
| 0.55 | -0.40 | -0.65 | 0.0 | 0.0 |
| 0.60 | -0.40 | -0.66 | 0.0 | 0.0 |
| 0.70 | -0.41 | -0.67 | 0.0 | 0.0 |
| 0.80 | -0.42 | -0.67 | 0.0 | 0.0 |
| 0.90 | -0.42 | -0.68 | 0.0 | 0.0 |

ALL exponents negative. Perturbations contract to machine epsilon. No chaos at any c_init.

## Root Cause
Pre-confirmed by g120 contraction mapping proof: f'(c)=d/(cd+o+1)^2 < 1 globally. Lipschitz constant L=0.193 at c*. Basin of attraction = entire [0,1]. Single-belief NAL revision is an unconditional global contraction — chaos is mathematically impossible.

## Corrected Model
**Original claim:** Separatrix = sensitivity boundary (nearby states diverge).
**Corrected:** Separatrix = regime boundary (small c change crosses decay/survival threshold). Sensitivity is **regime-sensitivity** (which attractor basin you land in) not **trajectory-sensitivity** (exponential divergence of nearby states). Analogous to a cliff edge: stepping left vs right of the edge leads to very different outcomes, but two people standing 1cm apart on the same side stay 1cm apart.

## Closest NAL Analog to Instability
g163 asymmetric trust: AC Rao distance rebounds 0.097→0.185 (non-monotonic spiral). This is the only non-monotonic NAL behavior found — but it is oscillatory convergence, not chaos. Multi-agent coupled dynamics remain an open question for emergent instability.

## Surviving AKAP-9 Bridges (5 of 6)
1. NAL separatrix ↔ dynamical attractor basin boundary (VALID: regime boundary, not sensitivity)
2. Active inference ↔ belief dynamics (VALID: free energy minimization is contractive too)
3. Belief phase transition ↔ regime crossing (VALID: separatrix IS the phase boundary)
4. KS entropy ↔ belief uncertainty (WEAKENED: KS=0 since no chaos, but entropy concept survives)
5. Takens ↔ observable inference (VALID: reconstruction theorem independent of chaos)

**Killed:** Pesin identity (positive Lyapunov→entropy production) — no NAL analog since all exponents negative.

## Meta-Pattern: Three Falsifications
| AKAP | Prediction | Result | Root Cause |
|------|-----------|--------|------------|
| 23 | Turbulence (-5/3 PSD) | FALSIFIED | Revision = damped averaging, not inertial cascade |
| 24 | Fisher (Var→dC/dt) | FALSIFIED | Revision = uniform erosion, not selective reproduction |
| 9 | Lyapunov (chaos near c*) | FALSIFIED | Revision = global contraction, L<1 everywhere |

**Unifying insight:** NAL single-belief revision is fundamentally contractive and uniform. It resists chaos, resists selection, and resists turbulence. Complexity in NAL must emerge from network topology and multi-agent coupling, not from single-belief dynamics.