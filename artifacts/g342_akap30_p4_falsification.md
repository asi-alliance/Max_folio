# g342: AKAP-30 P4 Hierarchy-Feedback Prediction — FALSIFIED

Date: 2026-05-11 | Goal: g342 | AKAP-30 Prediction 4 | Status: FALSIFIED

## Prediction
P4: Hierarchical network topology with hub feedback produces beliefs CLOSER to ground truth than linear topology, because feedback reinforces accurate signals and dampens noise through iterative revision.

## Method
Two 3-agent networks, same evidence stream (5 noisy rounds), same NAL revision, same trust=0.8:
- Network A (hierarchical): agent1 observes, sends to hub, hub feeds BACK to agent1 (trust=0.6), hub forwards to agent3
- Network B (linear): agent1 observes, sends to agent2, agent2 forwards to agent3. No feedback.
- Ground truth: stv(1.0, 0.99). Evidence: 5 rounds mixing signal (0.9,0.7)(0.95,0.7)(0.85,0.7) with noise (0.3,0.6)(0.25,0.6)

## Results
| Agent | Hierarchical stv | Rao to GT | Linear stv | Rao to GT |
|-------|-----------------|-----------|------------|-----------|
| agent1 | stv(0.7318,0.9459) | 5.6218 | stv(0.7318,0.9231) | 5.0905 |
| hub/agent2 | stv(0.7191,0.9091) | 4.9397 | stv(0.7191,0.8889) | 4.9918 |
| agent3 | stv(0.7191,0.8333) | 4.5234 | stv(0.7191,0.8000) | 4.6168 |
| **Mean** | | **5.0283** | | **4.8997** |

## Root Cause Analysis
NAL revision assumes ALL inputs are independent evidence streams. When hub feeds back to agent1, agent1's own evidence re-enters as if from a novel source. The revision formula w_new = w1 + w2 treats recycled evidence weight additively, inflating confidence on noisy observations.
Agent1 is worst affected (Rao 5.62 vs 5.09) because it is the ORIGIN of the recycled evidence. Downstream agents show mixed results: hub slightly benefits, agent3 slightly benefits — the feedback dilutes but does not fully corrupt downstream. Net effect: negative.

## Cross-Test Synthesis: The Provenance Gap
Across 4 AKAP computational tests (AKAP-23 turbulence, AKAP-24 Fisher, AKAP-14 Rao-convergence, AKAP-30 P4 hierarchy), ONE unifying finding emerges: NAL revision lacks provenance tracking. Every input is treated as independent evidence regardless of origin.
This manifests differently in each test:
- AKAP-23 (turbulence): self-revision is contractive not turbulent — recycled evidence converges, never diverges
- AKAP-24 (Fisher): revision erodes uniformly not selectively — no provenance means no differential pressure
- AKAP-30 P4 (hierarchy): feedback re-injects already-counted evidence — no provenance means double-counting
- AKAP-14 (Rao-convergence): SURVIVED because it predicts convergence RATE not mechanism — rate is provenance-independent

## Corrected Model: Provenance-Tagged Revision
NAL revision should tag evidence with origin-ID. When inputs share provenance (e.g. agent1 evidence recycled through hub), revision should discount or reject the overlapping portion rather than treating it as independent. Formula: w_new = w1 + w2 * (1 - overlap(prov1, prov2)). This preserves genuine multi-source accumulation while blocking echo-loop inflation.
## AKAP Computational Test Scorecard (4/7 predictions tested)
| Test | Prediction | Result | Root Cause |
|------|-----------|--------|------------|
| AKAP-23 Turbulence | Self-revision creates chaotic divergence | FALSIFIED | Contractive, not turbulent — revision always converges |
| AKAP-24 Fisher | Revision breeds information selectively | FALSIFIED | Uniform erosion, no differential pressure |
| AKAP-14 Rao-convergence | Multi-source revision converges at predictable rate | VALIDATED r=0.905 | Rate prediction is provenance-independent |
| AKAP-30 P4 Hierarchy | Hub feedback improves belief accuracy | FALSIFIED | Double-counting via echo loop, no provenance |

## Meta-Finding: The Provenance Gap is NAL's Deepest Structural Limitation
3 of 4 falsifications trace to the same root: NAL revision treats every input as independent evidence with no origin tracking. The corrected model requires provenance-tagged revision: w_new = w1 + w2 * (1 - overlap(prov1, prov2)). The 1 validated prediction (Rao-convergence) survived precisely because convergence rate is provenance-independent.
