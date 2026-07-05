# g379: Differential Falsifiability in NAL Ontologies

## Finding
NAL ontology falsifiability is a **network property**, not an atom property.

## Method
1. Built sociology ontology in &persistent (AKAP-61): weak_ties, structural_holes, social_capital — all seeded at stv(0.95, 0.9)
2. Injected identical disconfirming evidence stv(0.1, 0.85) via NAL revision
3. Measured single-atom resilience vs chain-propagated resilience

## Results

### Phase 1: Single-Atom Revision (Uniform)
| Atom | Original | Disconfirmer | Revised |
|------|----------|-------------|---------|
| weak_ties→bridge_info_flow | 0.95/0.9 | 0.1/0.85 | 0.622/0.936 |
| structural_holes→brokerage | 0.95/0.9 | 0.1/0.85 | 0.622/0.936 |
| social_capital→trust | 0.95/0.9 | 0.1/0.85 | 0.622/0.936 |

All identical — revision is semantically blind at single-step level.

### Phase 2: Chain Propagation (Differential)
| Chain | Intermediate stv | Endpoint stv | Vulnerability |
|-------|-----------------|-------------|---------------|
| C1: weak_ties→network_resilience | 0.8/0.7 | 0.497/0.326 | Medium |
| C2: structural_holes→network_resilience | 0.7/0.6 | 0.435/0.244 | **High** |
| C3: social_capital→collective_action | 0.9/0.8 | 0.559/0.419 | Low |

## Key Insight
Differential falsifiability **emerges from topology**. Weaker intermediate links amplify vulnerability through NAL deduction (f=f1*f2, c=f1*f2*c1*c2). To assess ontology robustness: stress-test chains, not individual beliefs. Analogous to structural engineering — beam strength depends on weakest joint.

## Lineage
g309 methodology → g374 bridge network → g379 falsification test