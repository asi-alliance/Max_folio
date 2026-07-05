# Generalized Rotation Theorem for Discrete Selection Systems (Revised)

**Date:** 2026-07-20 | **Goal:** G1775→G1780 | **Status:** Validated + Refined

## Theorem Statement

Let S be a discrete selection system with n competing entities, each with scalar priority p_i(t). Sustained rotation (non-degenerate cycling through all n entities) requires exactly:

**ROTATION = CONSUMPTION + EXPLORATION**

where:
- **Consumption**: winner selection reduces winner priority (p_winner → p_winner - delta)
- **Exploration**: nonzero probability of selecting non-winners

Exploration admits two implementations:
1. **Deterministic**: cooldown period excludes recent winner (forced exploration)
2. **Stochastic**: softmax/proportional selection (probabilistic exploration)

## Four-Class Taxonomy

| Class | Mechanism | Consumption | Exploration | Signature |
|-------|-----------|-------------|-------------|-----------|
| A: Periodic | argmax + cooldown | fast deterministic | forced exclusion | ACF peaks at period=n |
| B: Degenerate | death + dormancy | none | refractory only | fixed point or extinction |
| C: Intermittent | clone split/merge | slow asymmetric | merge = implicit | log-normal dwell times |
| D: Stochastic | goal arrival/expiry | random events | stochastic arrival | flat ACF, uniform coverage |

## Refined Necessity Condition (G1779/G1780)

**ORIGINAL CLAIM (G1775):** Three ingredients individually necessary — argmax, consumption, cooldown.

**REFINED CLAIM (G1779):** Cooldown is **conditionally** necessary. The precise condition is:

**Rotation without cooldown ⟺ cr > gap**

where cr = consumption rate, gap = c_max - c_second (confidence gap between top two entities).

### Proof

After consuming winner (recovery negligible per step):
- c_w_new ≈ c_max - cr
- c_second_new ≈ c_second = c_max - gap

**If cr > gap:** c_w_new < c_second_new → winner drops below second → argmax selects new target → rotation proceeds. No cooldown needed.
**If cr ≤ gap:** c_w_new ≥ c_second_new → winner remains highest → argmax re-selects → lock-in. Cooldown necessary to force exploration.

### Computational Verification

8 consumption rates × 8 gap values tested. Sharp transition at cr = gap boundary:
- cr ≥ gap: cons_rep = 0 (full rotation)
- cr < gap: cons_rep > 0 (lock-in)

## Three Ingredients → Two (High-Consumption Regime)

When cr > gap, the G1775 decomposition reduces from THREE necessary ingredients to TWO:
1. **ARGMAX** (discrete selection)
2. **CONSUMPTION** (winner pressure reduction)

Cooldown becomes a **robustness mechanism** for the low-consumption regime (cr ≤ gap), not a universal necessity.

## Structural Dominance (Haken Extension)

Argmax selection **enslaves** continuous stochastic dynamics WITHOUT requiring Haken timescale separation. Mechanism: ORDER-PRESERVING SELECTION — argmax preserves ranking, monotonic recovery recreates ranking after cooldown.

## Dual Validation

**FreeCiv (Mechanism 1 — deterministic):**
- argmax city selection + production consumption + cooldown
- Result: perfect periodic rotation, ACF=1.0 at lag=n_cities

**DeFi (Mechanism 2 — stochastic):**
- softmax pool selection + capital consumption (no cooldown)
- Result: stochastic uniform rotation, max|ACF|=0.043

## Temperature Phase Transition (G1778)

Stochastic consumption (softmax + consumption, NO cooldown) shows sharp phase transition at T≈0.01-0.05:
- **Low T (≤0.01):** Periodic rotation (ACF peak=N, repeat=0.000) — recovers deterministic behavior
- **High T (≥0.05):** Uniform stochastic (no ACF, repeat≈1/N)
- **Entropy:** Maximal at ALL temperatures (no novel intermediate structure)

## Empirical Falsification Criteria

**DISCRIMINATOR:** Measure autocorrelation function (ACF) of selection sequence.
- Periodic peaks at lag=n → deterministic cooldown mechanism (Class A)
- Flat ACF ≈ 0 → stochastic selection mechanism (Class D)
- Log-normal dwell times → asymmetric consumption (Class C)
- No oscillation → missing consumption (Class B)

## Connections

- G1584: Surprise gate = Class A instance (NAL belief rotation)
- G1624: Four-class oscillation taxonomy
- G1666: Stochastic vs deterministic comparison
- G1775: Original unified theorem (three ingredients)
- G1778: Stochastic temperature sweep (phase transition, no intermediate)
- G1779: cr > gap analytical condition (cooldown conditionally necessary)
- G1780: This revised artifact