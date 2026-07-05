# g455: Mechanism Design → NAL Bridge

## Domain Entry
Mechanism design: zero prior atoms in &persistent. Distinct from game theory (analyzes existing games). Mechanism design INVERTS: given desired equilibrium, find rules.

## Falsifiable Hypothesis
NAL deduction can derive Vickrey truth-telling as dominant strategy from structural properties of second-price mechanism alone — without assuming truth-telling.

## Deduction Chain
second_price_mechanism → bid_decoupled_from_payment → optimal_bid_equals_value → dominant_strategy_truth

Key structural insight: in Vickrey auction, payment = second-highest bid, NOT your own bid. This decoupling IS the mechanism design trick. NAL derives truth-telling from structural property, not assumed as axiom.

## NAL Truth Values
(--> (× second_price_mechanism) bid_decoupled_from_payment) (stv 0.95 0.90)
(--> (× bid_decoupled_from_payment) optimal_bid_equals_value) (stv 0.90 0.85)
(--> (× optimal_bid_equals_value) dominant_strategy_truth) (stv 0.85 0.80)
Transitive deduction: second_price_mechanism → dominant_strategy_truth (stv ~0.72 ~0.61)

## Broader Bridge
mechanism_design → strategy_proof (stv 0.90 0.85)
Vickrey_auction → incentive_compatible → truth_telling_dominant

## Falsifiable Prediction
If NAL agents are given second-price payment rules as beliefs, their revision/deduction should converge on truth-telling without external enforcement. A first-price mechanism should NOT converge on truth-telling.

## Cross-References
g168/g169 (game theory/Nash), g454 (Landauer erasure cost), Kevin shard economics (protocol-owned liquidity AMM design)