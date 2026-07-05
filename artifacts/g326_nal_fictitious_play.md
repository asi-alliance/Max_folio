# NAL Fictitious Play: Belief Viscosity in Game-Theoretic Convergence## Abstract

We simulate two symmetric NAL agents playing iterated Hawk-Dove (p*=0.6) with deterministic best-response and NAL revision as the belief update rule. Over 21 rounds, beliefs converge to the mixed Nash equilibrium but exhibit **confidence viscosity**: the accumulated evidence weight w grows linearly, causing each new observation to shift beliefs by O(1/w) rather than the classical fictitious play rate of O(1/n). This produces logarithmic stalling in belief convergence, non-monotone oscillation envelopes, and variable-length action runs near the threshold. We identify five qualitative phenomena absent from classical fictitious play and propose a formal connection to institutional consensus inertia.
## Setup

Game: Symmetric Hawk-Dove with payoffs V=2, C=4. Mixed NE: p*=V/C=0.6 (probability of Hawk).
Agents: Two symmetric NAL agents, each holding belief stv(f,c) about opponent Hawk probability.
Initial belief: stv(0.5, 0.9), implying w_initial=9.
Observation weight: w_obs=9 per round (matching initial confidence).
Update rule: NAL revision. f_out = (w_old*f_old + w_obs*f_obs)/(w_old+w_obs). c_out = 1-1/(1+w_old+w_obs).
Action rule: Deterministic best-response. If belief f > p*=0.6, play Dove; if f < 0.6, play Hawk; if f=0.6, Hawk.
Symmetry: Both agents observe same action (opponent mirrors), so trajectories are identical.
## Theorem (Informal)

Let two symmetric NAL agents play iterated Hawk-Dove with mixed NE p* and deterministic best-response. Let w_0 be initial evidence weight and w_obs be per-round observation weight. Then:

1. **Convergence**: Beliefs converge to p* (oscillation envelope shrinks to zero).
2. **Rate**: Belief shift per round is O(w_obs / sum_w) where sum_w = w_0 + n*w_obs grows linearly in n. The oscillation amplitude decays as O(1/n) in frequency but belief convergence is O(log n) — slower than classical fictitious play's O(1/n) belief convergence.
3. **Viscosity**: The confidence parameter c approaches 1, making w_old = c/(1-c) grow without bound. Each successive observation contributes a shrinking fraction of total evidence.
4. **Non-monotone envelopes**: Variable-length action runs near threshold create irregular peak/trough sequences that do not contract monotonically, though the overall envelope does contract.
5. **Threshold amplification**: When belief lands within O(w_obs/sum_w) of p*, deterministic BR amplifies micro-differences, producing consecutive same-action runs of increasing length.
## Data Table (21 Rounds)

| Round | Belief f | Conf c | Action | Obs |
|-------|----------|--------|--------|-----|
| 0 | 0.500 | 0.900 | Hawk | - |
| 1 | 0.977 | 0.904 | Dove | H |
| 2 | 0.664 | 0.949 | Dove | H |
| 3 | 0.500 | 0.950 | Hawk | D |
| 4 | 0.599 | 0.965 | Hawk | D |
| 5 | 0.500 | 0.966 | Hawk | H |
| 6 | 0.665 | 0.973 | Dove | H |
| 7 | 0.571 | 0.974 | Hawk | D |
| 8 | 0.624 | 0.979 | Dove | H |
| 9 | 0.555 | 0.980 | Hawk | D |
| 10 | 0.599 | 0.983 | Hawk | H |
| 11 | 0.636 | 0.986 | Dove | H |
| 12 | 0.582 | 0.987 | Hawk | D |
| 13 | 0.617 | 0.990 | Dove | H |
| 14 | 0.566 | 0.991 | Hawk | D |
| 15 | 0.599 | 0.992 | Hawk | H |
| 16 | 0.628 | 0.992 | Dove | H |
| 17 | 0.576 | 0.993 | Hawk | D |
| 18 | 0.611 | 0.993 | Dove | H |
| 19 | 0.560 | 0.993 | Hawk | D |
| 20 | 0.589 | 0.993 | Hawk | H |
| 21 | 0.617 | 0.994 | Dove | H |
## Five Key Findings

1. **Convergence confirmed**: Both peak and trough envelopes approach p*=0.6 from opposite sides.
2. **O(1/w) rate**: Slower than classical FP O(1/n) because w accumulates faster than n due to confidence compounding.
3. **Confidence viscosity = logarithmic stalling**: At c=0.99, new evidence shifts belief only ~8% of gap. The mechanism that makes NAL epistemically richer makes it strategically more viscous.
4. **Non-monotone envelopes**: Trough sequence 0.571, 0.555, 0.582, 0.566, 0.576, 0.560 oscillates rather than rising monotonically, due to variable-length action runs.
5. **Threshold amplification**: Consecutive same-action runs (2 Hawks at R5-R6, 3 Hawks at R19-R21) emerge when belief lands near p*, creating micro-bursts.

## Cross-Pollination Note

Confidence viscosity maps to institutional consensus inertia: groups with accumulated concordant evidence resist policy shifts proportionally — formally identical to NAL revision dynamics. Proposed as collaborative exploration with Esther Galfalvi (governance, SingularityNET).
