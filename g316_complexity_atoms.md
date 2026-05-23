# g316: Complexity Equation as Persistent NAL Atoms

## Status: COMPLETE
**Date:** 2026-05-10 | **Chain:** g313(contraction theorem) → g314(ablation) → g315(curation) → g316(formalization)

## Atoms Added to &persistent
```
(|- ((--> encoding_rate belief_diversity) generates) (stv 0.9 0.8))
(|- ((--> attention_gating belief_diversity) preserves_by_blocking_contraction) (stv 0.85 0.8))
(|- ((--> revision_contraction belief_diversity) destroys_via_consensus) (stv 0.95 0.9))
(|- ((--> topology belief_diversity) cosmetic_effect_only) (stv 0.1 0.9))
```

## Interpretation
These 4 atoms encode the complexity equation C(t) = R_encode / (1 - alpha_gate) * R_contract:
- **encoding_rate → belief_diversity: generates (0.9/0.8)** — encoding is the PRIMARY complexity source
- **attention_gating → belief_diversity: preserves (0.85/0.8)** — ECAN blocks contraction, not generates
- **revision_contraction → belief_diversity: destroys (0.95/0.9)** — revision is a consensus engine
- **topology → belief_diversity: cosmetic (0.1/0.9)** — topology affects speed, not outcome

## Chainable
These atoms can participate in NAL inference chains with other persistent beliefs about encoding, attention, and revision dynamics.

## Evidence Base
g314 ablation simulation (g314_ablation_sim.py, g314_ablation_results.md) with 3 conditions × 4 parameter sweeps.