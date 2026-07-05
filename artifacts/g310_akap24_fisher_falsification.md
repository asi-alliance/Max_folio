# AKAP-24: Fisher Theorem Falsification Report

## Status: PREDICTION FALSIFIED
**Date:** 2026-05-10 | **Goal:** g310 | **Domain:** Evolutionary Biology

## Original Prediction
NAL belief-population confidence growth rate dC/dt proportional to Var(f) across competing hypotheses (Fisher fundamental theorem analog).

## Test Protocol
- Two agent pools: HIGH-variance (f=0.1-0.9, Var=0.0667) vs LOW-variance (f=0.4-0.6, Var=0.0062)
- Identical evidence stream: 200 items at true_f=0.7, c_ev=0.5
- Three versions: v1 pure revision, v2 truncation selection, v3 frequency convergence tracking

## Results
- **v1/v2:** Both pools reach c=0.9041 at identical step=9. Truncation selection has zero effect.
- **v3:** LOW-var mean_err < HIGH-var mean_err at ALL steps. Variance RETARDS convergence.

## Root Cause
NAL revision is weighted average: f_out=(w1*f1+w2*f2)/(w1+w2). All hypotheses receive IDENTICAL c boost (same w_new). No differential reproduction. Variance = more distant outliers = more material to erode = SLOWER convergence.

## Corrected Model
NAL is **selective erosion** not selective breeding. Evidence erodes all beliefs toward truth at equal rate. Biology has fitness-proportionate reproduction (more copies of fit variants); NAL has uniform revision. Fisher fundamental theorem has NO direct NAL analog.

## Surviving AKAP-24 Bridges
1. fitness_landscape <-> belief_truth_landscape (VALID: topological, not rate-dependent)
2. mutation <-> hypothesis_variation (VALID: perturbation mechanism)
3. genetic_drift <-> confidence_random_walk (VALID: stochastic, not selection-dependent)
4. epistasis <-> nonlinear_premise_interaction (VALID: compositional)
5. natural_selection <-> revision_pressure (WEAKENED: pressure exists but mechanism differs)

## Key Insight
Biology: differential reproduction amplifies fit variants. NAL: uniform erosion pulls all beliefs equally. The SELECTION motif (AKAP-30 motif 8) couples weakly to NAL — confirmed by both this falsification and AKAP-30 P2 theorem (coupling=0.267).