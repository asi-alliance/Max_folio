# G82 Quantale Weakness Research

## Key Insight
Both set-based (mult=union) and sequence-based (mult=concat) formulations yield quantales.
The real question: is score->budget->select the MINIMAL FEASIBLE element?

## Feasibility constraint
Policy must produce valid action selection.
- Remove score: random selection (infeasible under bounded resources)
- Remove budget: unbounded resource allocation (infeasible)
- Remove select: no action produced (infeasible)

## Gap
Need to prove no shorter feasible sequence exists AND no alternative 3-stage is strictly weaker.
Also: does stage ORDER matter? budget->score->select vs score->budget->select.

## Next: formalize feasibility as upward-closed set (filter) in quantale.