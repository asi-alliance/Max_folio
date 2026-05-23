CERTIFICATION DYNAMIC AOP SPEC v5 2026-05-23

1. has-certification-aspect: (has-certification-aspect BridgeName AspectName) self-registers per bridge per aspect. Aspects: structural_plausibility, mechanism_transfer, empirical_support, falsification_resistance.

2. cert-hook: (cert-hook AspectName (--> $threshold $falsification)) fires when atomspace evidence matches falsification predicate, triggers re-evaluation.

3. cert-bucket: (cert-bucket BridgeName AspectName EvidenceList) holds (source stv provenance) tuples extracted from atomspace.

4. Evidence extraction: match &persistent for bridge domain properties, compute Jaccard overlap, shared abstract predicates, independent source count.

5. Learned thresholds: (scheduling-policy Context Aspect Threshold) (stv F C) revised via NAL |- as evidence accumulates. Dynamic adaptive model per Kevin.

6. DUAL VERDICTS:
   - causal_process_verdict: spine alignment + invariant preservation scoring
   - mathematical_duality_verdict: mapping completeness + structure preservation scoring
   Both must pass for full certification.

7. Named exogenous benchmark:
   thermo↔statmech → ADMIT both verdicts
   circuits↔hydraulic → ADMIT causal QUARANTINE duality
   spacetime↔holographic → QUARANTINE causal ADMIT duality
   random↔random → REJECT both

8. Demotion test: inject contradictory evidence for certified bridge, verify downgrade ADMIT→QUARANTINE→REJECT.

9. Hidden-test cases: bridges NOT used during development.

10. Pass/fail assertion: expected-vs-actual verdict comparison.