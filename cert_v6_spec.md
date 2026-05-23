# Cert Dynamic Aspect v6 Specification

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
- causal-role compatibility (9-field check)
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