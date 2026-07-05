# g454: Landauer Principle → NAL Erasure Cost Bridge

## Falsifiable Hypothesis
NAL revision that contracts beliefs toward consensus pays an information-theoretic erasure cost analogous to Landauer's kT ln 2 per bit.

## Formal Derivation
NAL revision: f_new = (w1·f1 + w2·f2)/(w1+w2), where w=c/(1-c).
Evidence weight erased: E = w1·|f1 - f_new| + w2·|f2 - f_new|
Shannon info lost: H(prior|posterior) ≥ 0 (Gibbs inequality)
Landauer analog: minimum cost ∝ kT ln 2 × bits_erased

## Key Results
1. **Contraction = erasure** (g313 proven): revision contracts → entropy reduction → information destroyed
2. **Erasure has minimum cost**: Landauer bound → NAL revision cannot be "free" — collapsing evidence streams costs information
3. **Confidence-weighted cost**: higher confidence beliefs pay more erasure cost when revised (w∝c/(1-c) grows with c)
4. **Bridge chain**: belief_contraction → entropy_reduction → minimum_erasure_cost

## Falsifiable Prediction
NAL agents that revise more frequently (more contractions) should accumulate measurable information loss relative to agents that preserve evidence provenance. Track provenance → reduce erasure cost.

## Cross-References
g313 (NAL Contraction Theorem), g-akap-10 (Fluctuation Theorem), g297 (R(D) framework)