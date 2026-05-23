# g314: Which Source Dominates NAL Complexity?

## Motivation
NAL Contraction Theorem (g313) proves revision dynamics cannot generate complexity.
Complexity must come from: Encoding, Attention, or Topology.
This experiment measures which dominates.

## Design: 3 Ablation Conditions
| Condition | Encoding | Attention | Topology |
|-----------|----------|-----------|----------|
| A: Topo-only | Fixed seeds | None (all revise) | Varied (chain/star/ring/complete) |
| B: Encode-only | Varied seeds per round | None | Fixed (complete) |
| C: Attention-only | Fixed seeds | STI threshold gates revision | Fixed (complete) |

## Metric: Belief Diversity
H = -Σ p(bin) log p(bin) over frequency histogram of agent f-values.
Higher H = more diverse beliefs = more complexity.

## Prediction from Contraction Theorem
- Condition A (topology): moderate H — topology shapes convergence RATE but all converge
- Condition B (encoding): highest H — new encodings inject fresh beliefs each round
- Condition C (attention): intermediate H — gating preserves diversity by blocking some revisions

If B >> C > A: encoding dominates, attention modulates, topology is cosmetic.