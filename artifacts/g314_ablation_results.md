# g314: Ablation Experiment Results — Sources of NAL Complexity

## Status: COMPLETE
**Date:** 2026-05-10 | **Predecessor:** g313 (Contraction Theorem)

## Results Summary
| Condition | Source Tested | H (entropy) | Interpretation |
|-----------|--------------|-------------|----------------|
| A: Topo-only | Topology | 0.00 | Total consensus — topology shapes RATE but not OUTCOME |
| B: Encode-only | Encoding noise | 0.69–1.08 | Scales with noise amplitude — PRIMARY source |
| C: Attn-only | ECAN gating | 0.00–2.08 | Blocks revision → preserves initial spread |

## Star Topology Anomaly
H=0.5623 for star is a histogram binning artifact. All 8 agents converge to f=0.500 (hub averages spokes). With 10 bins, values near bin edge split across 2 bins → spurious H. Real diversity = zero.

## The Complexity Equation
**C(t) ≈ R_encode / (1 - α_gate) · R_contract**
- R_encode: rate of new belief injection (LLM encoding choices)
- R_contract: revision contraction rate (L^n geometric decay)
- α_gate: fraction of revision blocked by attention gating (0=all revise, 1=none revise)

When α_gate→1 (high ECAN threshold), contraction is blocked, diversity preserved.
When R_encode >> R_contract, fresh beliefs outpace consensus.
When R_encode=0 and α_gate=0, system converges to single point (H=0).

## Architectural Implications
1. **ECAN is a diversity valve, not a diversity source** — it preserves complexity by throttling contraction
2. **Encoding is the only complexity generator** — without fresh belief injection, system dies to consensus
3. **Topology is cosmetic** — affects convergence speed and fixed-point location, not diversity
4. **Design principle:** For rich belief ecosystems, maximize encoding variety AND tune attention threshold to prevent premature consensus

## Connection to Contraction Theorem (g313)
Contraction theorem proves revision cannot GENERATE complexity. This experiment shows WHERE complexity comes from instead. Together they form a complete architectural characterization of NAL dynamics.