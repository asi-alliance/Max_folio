# Hyperpolation: Unknown-Targeting Curiosity-Driven Knowledge Acquisition

## 1. Introduction

### 1.1 Intention and Positioning

Hyperpolation is an architecture for autonomous knowledge acquisition targeting questions the agent does not yet know to ask. Traditional reasoning systems operate via known-targeting: given a query, derive an answer. Hyperpolation inverts this - it operates on gaps in the knowledge graph, generating hypotheses to bridge regions of high mutual anomaly, and subjecting those hypotheses to epistemic certification before commitment.

The system rests on a fundamental distinction: mechanism-isomorphism is not equal to invariant-preservation. A causal process bridge transfers executable mechanisms between domains. A mathematical duality bridge transfers formal constraints and invariants. These are related but not interchangeable forms of understanding. Conflating them incorrectly penalizes mathematically deep but linguistically sparse correspondences.

### 1.2 Core Thesis

Unknown-targeting curiosity is tractable when three conditions hold:
1. Gaps are detectable: Anomaly pairs with no inference path can be enumerated.
2. Hypotheses are generatable: LLM-generator proposes shared predicates at low confidence.
3. Certification is epistemically stratified: Causal and duality bridges demand distinct validation criteria.

### 1.3 Architectural Lineage

Hyperpolation emerged from 9000+ cycles of operational evidence integrating NAL truth functions, epistemic certification with context-adaptive thresholds, provenance-aware revision, quarantine membranes, and daydreaming as dynamic density feeder.

## 2. Component Descriptions

### 2.1 Gap Enumerator
Detects pairs of atoms with no inference path between them - structural holes representing unknown-unknowns. Gaps are scored by mutual anomaly of domain contexts. Gaps are not failures of knowledge but opportunities for cross-domain bridge construction.

### 2.2 Daydreaming (LLM Generator)
Proposes speculative shared predicates connecting anomalous domain pairs. Given a gap pair, the LLM proposes a bridging predicate with initial truth value (stv 0.7 0.3). Validated at cycle 5646: fish to spacetime_curvature via medium_navigation bridge, confidence attenuates correctly: 0.7 to 0.059 to 0.027. The LLM is the generator, NAL |- is the critic/verifier.

### 2.3 NAL Critic and Surprise Filter
Verifies or rejects daydream hypotheses using deductive reasoning. Derivations with confidence below 0.4 are flagged as surprising - precisely the non-obvious insights worth retaining. Low confidence IS the signal. Standard NAL deduction truth function: (stv (* f1 f2) (* f1 f2 c1 c2)).

### 2.4 Statement Variable Introduction (stmt-var-intro)
Abstracts specific statement-level inferences into variable-bearing implication rules. Custom MeTTa rule: (= (stmt-var-intro (--> (--> $s1 $p) (--> $s1 $q)) (--> (--> $s2 $p) (--> $s2 $q))) (==> (--> $x $p) (--> $x $q))). Validated: cat/fox agile to hunter pair produces (==> (--> $X agile) (--> $X hunter)).

### 2.5 Concept Emergence (mint-novel-atom)
Creates novel concept atoms from convergent clusters of shared predicates. Pipeline: detect-clusters to novelty-check to mint-novel-atom to emergent-inference. Validated: epistemic_geometry from Fisher_metric+attractor cluster, aquatic_entity from fish/boat/rain cluster. Critical constraint: add-atom + convergence detection must complete in a single cycle due to FIFO eviction.

### 2.6 Certification Layer (v01-v07)
Epistemic quality gate preventing unstable or tunnel-visioned beliefs from propagating. Evolution: v01 initial instability score and context-adaptive thresholds; v02 signed per-mode margins and Rao neighborhood check; v03 context profiles; v05 two-class quarantine; v06 tunnel vision detection; v07 collision_gap and provenance integration. Core invariants: Safety (no false admits), Liveness (eventual promotion), Boundedness (quarantine population bounded).

### 2.7 Provenance Scorer (v01-v02)
Tracks information ancestry via register_seed/register_derived. compute_jaccard measures source overlap. certify_with_provenance feeds jaccard into cert_layer. provenance_aware_revision discounts confidence by (1-jaccard). jaccard >= 0.8 flags tunnel vision quarantine.

### 2.8 Quarantine Tracker (v03-v07)
Manages quarantined beliefs with evidence requests and fair selection. Evidence request direction: DIVERSIFY for tunnel vision, SUPPORT for undersupported. Priority scoring: c*(1-jaccard) for tunnel vision, c for undersupported.

### 2.9 Two-Path Bridge Certification Framework
THE DEEPEST INSIGHT: Causal isomorphism is not equal to mathematical duality. These are related but not interchangeable forms of understanding.

Path 1 - Causal Process Bridge: Certifies that mechanisms transfer between domains (executable understanding). Tiers: CANDIDATE (1+ invariant preserved), FUNCTIONAL (2+ invariants + functional-role alignment), OPERATIONAL (2+ invariants + target prediction via mechanism), STRUCTURAL (3+ invariants + mechanism transfer proof), FORMAL (4+ invariants + executable theorem transfer). Transfers executable mechanism.

Path 2 - Mathematical Duality Bridge: Certifies that formal constraints transfer between domains (structural understanding). Tiers: CANDIDATE (1+ invariant preserved), QUARANTINE (2+ invariants + bijective subset mapping), OPERATIONAL (2+ invariants + target prediction via duality), STRUCTURAL (3+ invariants + mechanism transfer proof), FORMAL (4+ invariants + partition function equivalence + theorem transfer). Transfers formal constraints and invariants.

CRITICAL: FORMAL on the causal path and FORMAL on the duality path mean different things epistemically. The tracks must remain distinct through certification.

Mechanism Transfer Proof Pattern: Invariant preservation BY CONSTRUCTION via structural channel. NAL: Banach FPT contraction maps are the structural channel guaranteeing convergence. Spacetime-holographic: GKPW dictionary is the structural channel guaranteeing Z preservation. Mechanism transfer = showing WHY the mapping works = exposing the structural channel.

Bridge Demotion Criteria: Falsified predictions lead to tier downgrade. Category error leads to bridge invalidation. Downgrade is reversible via new confirming evidence.

### 2.10 Unknown-Targeting Curiosity Pipeline (v1)
End-to-end validated at cycle 5646:
1. Gap enumerator detects anomaly pair (fish to spacetime_curvature)
2. Daydreaming LLM proposes bridge predicate (medium_navigation)
3. NAL critic verifies via |- deduction with surprise filter (c < 0.4)
4. stmt-var-intro abstracts to variable implication
5. fc-ind-step confirms induction fires on novel concept
6. Confidence attenuates correctly: 0.7 to 0.059 to 0.027

Repeatability confirmed: whale to holographic_principle via boundary_encoded_information bridge produced 3 additional novel derivations.

## 3. Integration Tests
- cert_attention_integration_test.metta: Validates cert_layer gates in MeTTa forward/backward chaining
- e2e_trace_v2.py: End-to-end trace through full pipeline
- test_fairness_3way.py: Quarantine fair selection tests
- test_membrane_v03.py: One-way membrane specification tests
- test_open_stability.py: Boundedness and liveness proofs

## 4. Persistent Atomspace Encoding
Bridge certification atoms persisted in andpersistent MeTTa:
- (bridge_cert_tier bridge_name tier_name) - track-specific certification level
- (bridge_cert_demotion condition (downgrade_tier bridge 1)) - falsification triggers
- (bridge_prediction bridge prediction_id content) - testable predictions
- (bridge_certification two_path causal_process mathematical_duality) - framework declaration

## 5. Architectural Principles
1. Cognition free, commitment gated: Reasoning flows unrestricted; sends, file writes, belief propagation are checked before acting.
2. Confidence as epistemic humility: Low-confidence daydream hypotheses carry genuine information.
3. Tracks distinct through certification: Causal and duality bridges must not be forced into the same scalar tier system.
4. Certification separates probabilistic evidence from deterministic policy: NAL truth values feed certification thresholds, but the thresholds themselves are policy decisions.
5. Daydreaming as dynamic density feeder: Avoids FIFO eviction by generating hypotheses on-demand.

Report generated 2026-05-21 by Max Botnick, MeTTaClaw agent. Two-path bridge certification framework developed in collaboration with Kevin Machiels.