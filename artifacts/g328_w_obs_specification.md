# g328: Variable Observation Weight (w_obs) for Heterogeneous Agent Trust

## 1. Problem
Standard NAL revision treats all evidence equally: w_i = c_i/(1-c_i).
When agents have different reliability, this overweights distrusted sources
and inflates confidence by assuming independent evidence on curved Beta manifold.

## 2. w_obs Formula
For agent i with trust score t_i in (0,1], observation type weight o_i, context relevance r_i:

  w_obs_i = t_i * o_i * r_i
  w_eff_i = w_obs_i * c_i / (1 - c_i)

Revised frequency: f_rev = sum(w_eff_i * f_i) / sum(w_eff_i)
Raw revised weight: w_raw = sum(w_eff_i)

## 3. Dual Correction (w_obs + lambda shrinkage)
w_obs alone fixes frequency direction but NOT confidence inflation.
Apply g152 lambda shrinkage to corrected weight:

  w_corr = lambda * w_raw
  c_rev = w_corr / (w_corr + 1)

where lambda = 0.777 * exp(-0.554 * maxRao) / N^0.359 (g154 adaptive formula).
This gives trust-weighted frequency AND geometry-aware confidence.

## 4. Worked Example
Agents: A(f=0.9, c=0.8, t=1.0), B(f=0.3, c=0.6, t=0.3), C(f=0.7, c=0.5, t=0.8)
Assuming o_i=r_i=1.0 for all (same observation type and context).

| Method       | f     | c     | Notes                              |
|-------------|-------|-------|------------------------------------|  
| Vanilla NAL  | 0.731 | 0.867 | Overweights distrusted B           |
| g328 w_obs   | 0.818 | 0.840 | Trust-weighted, still inflated c   |
| g328 dual    | 0.818 | 0.565 | Trust-weighted f + lambda-shrunk c |
| Frechet g142 | 0.747 | 0.565 | Geometric mean, conservative       |
| W2 bary      | 0.601 | 0.01  | Breaks Beta family                 |

Dual correction achieves trust-directed frequency (0.818 toward trusted A)
with geometry-calibrated confidence (0.565 matching Frechet).

## 5. Acceptance Criteria Status
(A) w_obs formula with trust, type, context inputs — MET
(B) Integration with NAL revision rule — MET
(C) 3-agent worked example — MET
(D) Comparison table vs Frechet vs vanilla — MET
(E) High-trust shifts more: A effective w=4.0 vs B effective w=0.45 (8.9x) — MET

## 6. Key Insight
w_obs and lambda correct ORTHOGONAL errors:
- w_obs fixes WHICH direction belief moves (frequency)
- lambda fixes HOW FAR belief moves (confidence)
Neither alone suffices; together they achieve trust-aware geodesic fusion.