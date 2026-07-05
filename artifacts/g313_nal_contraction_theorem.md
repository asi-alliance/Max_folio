# The NAL Contraction Theorem

## Formal Statement
**Theorem.** Let R: [0,1]^2 × [0,1]^2 → [0,1]^2 be the NAL revision operator R(f₁,c₁,f₂,c₂) = (f_out, c_out) where w_i = c_i/(1-c_i), f_out = (w₁f₁+w₂f₂)/(w₁+w₂), c_out = (w₁+w₂)/(w₁+w₂+1). Then:

1. **Frequency contraction.** For fixed (f₂,c₂), the map f₁ ↦ f_out is a contraction with Lipschitz constant L_f = w₁/(w₁+w₂) < 1.
2. **Confidence contraction under decay.** The homeostatic map f(c) = (cd+o)/(cd+o+1) with decay d∈(0,1) and observation weight o>0 has f'(c) = d/(cd+o+1)² < d < 1 for all c∈[0,1]. Global Lipschitz constant L = d/(o+1)² attained at c=0.
3. **Unique fixed point.** By Banach FPT on the complete metric space [0,1], there exists a unique c* satisfying c* = (c*d+o)/(c*d+o+1). Closed form: c* = [-(o+1-d) + √((o+1-d)²+4do)]/(2d).
4. **Geometric convergence.** |c_n - c*| ≤ L^n |c₀ - c*|. For d=0.96, o=0.7: L=0.332, half-life ≈ 0.63 steps.

## Proof of Frequency Contraction
f_out = w₁f₁/(w₁+w₂) + w₂f₂/(w₁+w₂). Differentiating w.r.t. f₁:
∂f_out/∂f₁ = w₁/(w₁+w₂) ∈ (0,1) since w₂ > 0.
For two inputs f₁, f₁': |f_out - f_out'| = w₁/(w₁+w₂)|f₁-f₁'| < |f₁-f₁'|. □

## Proof of Confidence Contraction
f(c) = (cd+o)/(cd+o+1). f'(c) = d(cd+o+1)⁻¹ - d(cd+o)(cd+o+1)⁻²·d = d/(cd+o+1)².
Since c≥0, d>0, o>0: cd+o+1 ≥ o+1 > 1, so f'(c) ≤ d/(o+1)² ≤ d < 1.
f maps [0,1] → [o/(o+1), (d+o)/(d+o+1)] ⊂ [0,1]. Complete metric space + contraction → Banach FPT applies. □

## Network Preservation Theorem
**Corollary 1.** Let G=(V,E) be a directed trust graph where each agent i revises with neighbors using NAL revision. The network map F: ∏ᵢ[0,1]² → ∏ᵢ[0,1]² is a contraction in the product metric.

*Proof sketch:* Each agent's update is a convex combination of pairwise revisions (each a contraction). Convex combinations of contractions are contractions: L_mix ≤ Σᵢ λᵢLᵢ where Σλᵢ=1, each Lᵢ<1. Sequential composition: L_seq ≤ ∏Lᵢ < 1. No coupling topology can introduce expansion. □

## Falsification Corollaries
**Corollary 2 (No Chaos).** Since all Lyapunov exponents = lim ln(L^n)/n = ln(L) < 0, NAL revision has no sensitive dependence on initial conditions at any scale. [g311: tested 8 c_init, all λ∈(-0.68,-0.37)]

**Corollary 3 (No Turbulence).** Contraction maps have flat power spectra (exponential decay, no power-law). Kolmogorov -5/3 cascade requires inertial-range energy transfer absent in contracting systems. [g309: PSD slope -3.92 not -1.67]

**Corollary 4 (No Fisher Selection).** Fisher's theorem requires differential reproduction (expansion of fitter variants). Uniform contraction erodes all variants equally — no selection gradient. [g310: Var(f) decays monotonically, df̄/dt uncorrelated with Var]

**Corollary 5 (No Network Emergence).** Coupled contracting maps remain contracting. CML chaos requires individual-map expansion (logistic r>3.57). NAL weighted averaging has no expansion term. [g312: 3-agent asymmetric trust, all λ<0]

## Architectural Implication
NAL revision is a **thermodynamic heat sink**: it dissipates trajectory-level information, driving all nearby states toward the same fixed point. Complexity in NAL-based systems must originate from:
1. **Encoding** — what beliefs are formed (LLM/perception choices)
2. **Attention** — which beliefs are selected for revision (ECAN)
3. **Topology** — network structure of evidence flow

The revision engine itself is provably incapable of generating complexity.