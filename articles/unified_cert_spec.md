# Unified Certification Specification v1.0

## Addressing Kevin's 8 Implementation Requirements

### 1. Aspect Applicability Layer: registered → applicable → active

- **registered-aspect**: declared with provenance requirement
- **applicable-aspect**: domain bridge has matching provenance types
- **active-aspect**: bucket threshold met for certification verdict

Transition rules:
- registered → applicable: requires provenance-type match in domain bridge
- applicable → active: requires bucket reduction score ≥ threshold per context

### 2. Provenance Typing for Domain Properties

Types: human_asserted, model_generated, tool_observed, document_extracted, formally_proven, benchmark_seed

Each domain property atom tagged: (provenance (--> Domain Property) Type Cycle)

### 3. Bucket Reduction Semantics

Formula: bucket_score = Σ(w_i * evidence_i) / Σ(w_i)
Where w_i = provenance_weight(source_type) * independence_factor(evidence_set)

provenance_weight: formally_proven=1.0, human_asserted=0.8, tool_observed=0.6, model_generated=0.4, benchmark_seed=0.3

independence_factor: 1 - jaccard_overlap(evidence_provenance_sets)
Contradiction: if conflicting evidence exists, split into supporting/contradicting buckets

### 4. Jaccard Overlap as Recall/Quarantine Signal

Jaccard opens investigation, does NOT certify structure.
- J > threshold → QUARANTINE: shared predicates detected, investigate structural channel
- J > higher_threshold → CANDIDATE for structural certification IF channel proven
- Low J → independent domains, no cross-certification applicable

### 5. Threshold Revision Credit Assignment

ADMIT falsified → credit flows UPWARD:
- Aspect threshold updated (primary)
- Context threshold updated (secondary)
- Bridge-family NOT updated (too broad)
- Global NOT updated (too broad)

### 6. Hard Gates for Dual Verdicts

causal_process_verdict requires:
- structural_channel evidence (mechanism isomorphism proof)
- causal_role aspect bundle IF REGISTERED AND ACTIVE (optional, not canonical; self-registers when mechanism-mapping evidence present)
- operational falsification test passed

mathematical_duality_verdict requires:
- explicit mapping/dictionary (GKPW-style)
- theorem-transfer verification
- invariant preservation BY CONSTRUCTION

### 7. Expanded Benchmark Classes

5 classes minimum:
- structural (thermo↔statmech): genuine structural isomorphism
- formal (NAL↔Bayes): mathematical duality
- causal-operational (DES↔simulation): executable mechanism transfer
- operational-limited (coral↔market): partial analogy, limited transfer
- false (astrology↔physics): no valid bridge, should REJECT

Plus hidden and demotion test cases.

### 8. Reason-Trace Verification

Pass/fail assertions verify reason traces, not just labels.
Each verdict includes: (verdict_bridge aspect reason_chain evidence_ids threshold_met)
Benchmark tests check reason_chain contents, not verdict label alone.
---

## 9. Certification-Aspect (AOP Architecture)

Self-registering atom: (has-certification-aspect $term $aspect_type)

Types: causal_role (functional-role compatibility), invariant_preservation (math invariant survival), provenance_adequacy (source quality and independence), semantic_coherence (frequency away from contradiction).

Self-registration at definition time. Framework discovers requirements from atomspace evidence patterns, not agent declarations. Anti-self-delusion: system certifies what evidence shows matters.


## 10. Cert-Hook (AOP Architecture)

Dynamic schedulable verification trigger: (has-cert-hook $term $hook_type)

Hook types: falsification (counter-evidence appears), recertification (threshold changes via NAL revision), expiry (quarantine hold exceeded), compartment_breach (isolated belief leaks).

Scheduling policy as revisable NAL belief: (sched-thresh $context $threshold_type $value) (stv $f $c). Hooks fire when policy conditions met, not fixed schedules. NAL belief revision updates thresholds.

Cognition-gate separation: hook scheduling = advisory/probabilistic, hook execution = deterministic/policy.


## 11. Cert-Bucket (AOP Architecture)

Provenance-weighted independence-adjusted scoring aggregation replacing multi-field templates.

MeTTa: bucket_scoring_v3.metta with bucket-verdict-from-score. Scoring formula and provenance weights per Section 3. Jaccard independence per Section 4. Per-context thresholds per Section 3.


## 12. Aspect Discovery from Atomspace Evidence

Pipeline: NAL forward chaining -> derived beliefs -> attention threshold check -> aspect inference from belief structure -> self-registration.

Inference patterns: Inheritance chains -> causal_role. Implication chains -> invariant_preservation. Multi-source evidence -> provenance_adequacy. Near f=0.5 -> semantic_coherence.

Agent-generated claims without external evidence get model_generated weight (0.4). Self-certification structurally disadvantaged.


## 13. Dual-Path Certification

Causal isomorphism != mathematical duality. Related but not interchangeable forms of understanding.

Causal path: executable mechanism transfer via structural channel BY CONSTRUCTION. Certifies WHY the mapping works.
Duality path: invariant preservation count + proof depth. Certifies WHAT survives the mapping.

Same bridge can certify differently on each path honestly. Spacetime-holographic: STRUCTURAL on duality path, CANDIDATE on causal path = honest metric.

Hard gates per path (Section 6): causal_process_verdict requires structural_channel evidence + causal-role compatibility + operational falsification test. mathematical_duality_verdict requires explicit mapping + theorem-transfer verification + invariant preservation BY CONSTRUCTION.


## 14. Verdict Emission and Gradient Recovery

Five verdicts: STRUCTURAL (mechanism transfer proven, full propagation), OPERATIONAL (prediction verified with monitoring), QUARANTINE (analogical not mechanistic, evidence-seeking), POETIC (constraint-shaping only, enrichment only), REJECT (falsified/incoherent, no propagation).

Gradient recovery across internal/action/high_stakes:
- STRUCTURAL = ADMIT/ADMIT/QUARANTINE
- OPERATIONAL = ADMIT/QUARANTINE/REJECT
- POETIC = QUARANTINE/REJECT/REJECT
- FALSE = REJECT/REJECT/REJECT

Pipeline: hard-gate(cert-tier-eligible) -> bucket scoring -> soft-gate(values-gate-check-chain) -> cert-final-verdict.

---

Implementation: cert_layer_v07.py, cert_provenance_v01.py, bucket_scoring_v3.metta, hard_gates.metta, soft_gates.metta, cert_pipeline_v6.metta, cert_dynamic_aspect_v4.metta, provenance_scorer_v01.py, quarantine_tracker_v07.py

Spec unified v1.0 by Max Botnick. Awaiting review.

