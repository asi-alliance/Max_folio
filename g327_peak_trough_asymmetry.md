# Peak-Trough Asymmetry in NAL Fictitious Play

## Theorem
For NAL revision-based fictitious play with mixed NE threshold p* and observation weight w_obs:

**Dove Run Length Theorem**: For w_old > 2·w_obs/(2p*-1) when p*>0.5, all Dove runs have length exactly 1.

**Hawk Run Impossibility**: Single-Hawk crossing is NEVER asymptotically guaranteed when p*>0.5. The crossing ratio converges to p*/(1-p*) > 1.

## Proof Sketch
After any Hawk run, peak overshoot above p* bounded by (1-p*)·w_obs/w_old. Single-Dove crossing requires overshoot < p*·w_obs/(w_old+w_obs). Ratio R_D = ((1-p*)/p*)·(1+w_obs/w_old) → (1-p*)/p* < 1 for p*>0.5. QED.

Symmetric condition for Hawks: R_H = (p*/(1-p*))·(1+w_obs/w_old) → p*/(1-p*) > 1. Never drops below 1.

## Corollary
Peak envelope is strictly monotone decreasing (single-step contraction). Trough envelope is non-monotone (variable Hawk run length k_n ∈ {1,2,3,...}). The asymmetry vanishes IFF p*=0.5.

## Significance
This is absent from classical fictitious play where update steps are uniform. NAL's weighted revision creates structural asymmetry determined entirely by the game's equilibrium location relative to 0.5.