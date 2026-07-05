# g401: NAL Revision Compression Landscape

## Correcting g400: Three-Factor Decomposition is Position-Dependent

**Date:** 2026-05-12 | **Method:** 20x20 sweep over (f,c) space, E=(0.5,0.5)

### The Three Factors

1. **Leverage** = w_E/(w_prior+w_E) — monotonically decreases with c_prior
2. **Sigmoid Compression** = 1.0 everywhere for frequency shifts (trivial — NAL revision IS linear in w-space for f)
3. **Fisher Compression** = rao(P,R)/rao(P,E) — POSITION-DEPENDENT, ranges 0.025x to 7x

### Critical Boundary: fisher_comp = 1.0 at c_prior ≈ 0.63

| Zone | c_prior | fisher_comp | Mechanism |
|------|---------|-------------|----------|
| Amplification | < 0.63 | 1.0 – 7.0x | c-overshoot: c_r >> c_E, Rao path longer than chord to E |
| Dampening | > 0.63 | 0.025 – 1.0x | f-compression overcomes c-overshoot |

Peak amplification 6-7x at (f≈0.48, c≈0.48). Peak dampening 0.025x at c=0.95.

### g400 Correction

Original g400 claimed 0.135x Fisher compression as universal. This was a HIGH-c snapshot.
The geometry does NOT uniformly brake revision — it amplifies at moderate confidence.

### Connection to g381 Anisotropy Island

Amplification zone (c<0.63) contains lower half of g381 frequency-dominance island (c_lo=0.311 at f=0.5).
Overlap region: geometry amplifies AND frequency-direction dominates.