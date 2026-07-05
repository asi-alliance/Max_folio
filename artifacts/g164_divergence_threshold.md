# g164: Trust-Asymmetry Divergence Threshold

## Result
Divergence criterion: D(t12,t21) = 0.25·|log(t21/t12)| / √(t12·t21) > 0.3

## Interpretation
Numerator = Rao-distance drift rate (information-geometric asymmetry)
Denominator = evidence-exchange rate (geometric mean of mutual trust)
When drift outpaces exchange by >30%, agents spiral apart.

## Validation
| Pair | t12 | t21 | D | Predict | Actual | Match |
|------|-----|-----|-------|---------|--------|-------|
| BC | 0.3 | 0.5 | 0.330 | DIVERGE | DIVERGE | YES |
| AB | 0.7 | 0.9 | 0.079 | CONVERGE | CONVERGE | YES |
| AC | 0.9 | 0.8 | 0.035 | CONVERGE | CONVERGE | YES |

## Scaling Law
Rao_inf = 0.25·|log(t21/t12)| (verified across 8 ratios at w=1e6)

## Frechet Switching Thresholds
- ε=0.25: t21/t12 > e^1 ≈ 2.7x
- ε=0.50: t21/t12 > e^2 ≈ 7.4x
- ε=1.00: t21/t12 > e^4 ≈ 54.6x

## Key Insight
Trust-asymmetry divergence is BOUNDED (saturates at Rao_inf), not unbounded. The g163 ~0.4 geometric-mean threshold emerges from the compound criterion, not from either ratio or magnitude alone.