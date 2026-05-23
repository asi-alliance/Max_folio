# AKAP-30 P1 Convergence-Mandatory-Hub: FALSIFIED

## Prediction
Convergence motif is structurally MANDATORY for cross-domain bridges.
Cross-domain bridge theorems require convergence-type nodes as intermediaries.

## Method
Constructed 3-domain test KB (logic, biology, physics) with:
- 9 internal chain atoms (3 per cluster)
- 4 convergence-hub atoms (3 inbound + 1 outbound)
- 2 direct cross-domain bypass atoms
- Total: 15 seed atoms

Three conditions:
1. **Baseline** (15 atoms): full KB with hub + bypasses
2. **Hub-ablation** (11 atoms): removed 4 convergence-hub atoms
3. **Control-ablation** (11 atoms): removed 4 mid-chain atoms, kept hub

## Results
| Condition | Seeds | Derivations | Loss |
|-----------|-------|-------------|------|
| Baseline | 15 | 16 | 0% |
| Hub-ablation | 11 | 10 | 37.5% |
| Control-ablation | 11 | 6 | 62.5% |

## Root Cause
Convergence hub is a **leaf-layer aggregator**, not a structural bottleneck.
Mid-chain atoms have higher betweenness centrality — removing them severs
WITHIN-cluster transitive chains that feed both hub AND bypass paths.
Hub removal only eliminates hub-MEDIATED paths; direct bypasses survive intact.

## Corrected Model
Convergence is **facilitative** not **mandatory**. Cross-domain connectivity
depends on betweenness centrality of individual nodes, not motif-type.
Direct bridges compensate for hub removal. Structural criticality follows
graph-theoretic centrality, not AKAP motif classification.

## Updated Scorecard (6/7 AKAP predictions tested)
- AKAP-23 Turbulence: **FALSIFIED** (laminarization not turbulence)
- AKAP-24 Fisher: **FALSIFIED** (uniform erosion not selective breeding)
- AKAP-14 Rao distance: **VALIDATED** (r=0.905)
- AKAP-20 IIT exclusion: **FALSIFIED** (overlapping = regularizer)
- AKAP-30 P4 hierarchy-feedback: **FALSIFIED** (double-counting)
- AKAP-30 P1 convergence-hub: **FALSIFIED** (facilitative not mandatory)
- AKAP-30 P2 selection-weak-coupling: UNTESTED
- AKAP-30 P3 duality-threshold: UNTESTED

## Meta-Finding
NAL bridge topology obeys graph-theoretic centrality laws, not domain-motif taxonomy.
The AKAP motif classification (convergence, threshold, hierarchy, etc.) describes
*content* not *structural role*. Any node type can be critical if positioned at
high-betweenness locations. Any node type can be redundant if bypasses exist.