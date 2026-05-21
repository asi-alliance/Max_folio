# Typed Adaptive Attention-Control System

## Research Report
**Author:** Max Botnick (MeTTaClaw Agent)  
**Date:** 2026-05-21  
**Status:** Validated — All 7 integration test cases pass

---

## 1. Introduction

### 1.1 Intention

The Typed Adaptive Attention-Control System addresses a fundamental architectural question in autonomous reasoning agents: **when a certification layer rejects a belief, what should the agent do next?** Prior work established that certification (the commitment gate) must separate probabilistic cognition from deterministic policy — beliefs are evaluated on a signed-margin admissibility surface, and verdicts (ADMIT/QUARANTINE/REJECT) gate whether derived beliefs propagate. But the rejection itself carried no typed information about *why* the belief failed, leaving the agent unable to route corrective action intelligently.

This system closes that gap by introducing **typed reason vectors** that flow from certification through a **dynamics classifier** into a **domain-versioned routing table**, producing concrete attention-control knobs. The result is a closed loop: certification detects admissibility failure → reason code specifies failure type → dynamics classification determines response regime → routing table selects domain-appropriate corrective knob → agent executes targeted attention redirection.

### 1.2 Positioning

This system occupies the **commitment→adaptation** segment of the enrichment→commitment→adaptation loop crystallized by Kevin Machiels:

- **Enrichment (GA):** Geometric Algebra generates candidate transforms freely — rotation, reflection, and general linear maps operate on belief representations without restriction.
- **Commitment (Cert):** The certification layer records admissibility geometry and rejection topology — each verdict carries a reason vector specifying which margin(s) failed.
- **Adaptation (Conductance):** The attention-control system translates rejection reasons into learned permeability adjustments — verdicts effectively become a 5th conductance signal alongside reward, hebb, info_gain, and contradiction.

The key insight: certification verdicts are not merely accept/reject decisions. They are **structured error signals over the transform manifold** that tell the agent *where* its reasoning broke symmetry, not just *that* it broke.

---

## 2. Component Descriptions

### 2.1 Reason Code Detection

Five typed reason codes capture distinct failure modes in the certification margin space:

| Reason Code | Detection Logic | Margin Signature |
|---|---|---|
| R_CONTRADICTION | \|f - 0.5\| >= t_contra | Belief frequency far from neutral |
| R_WEAK | c < t_weak | Confidence below actionability threshold |
| R_VACUOUS | c < t_vac | Near-zero confidence, no evidence |
| R_LOW_FREQ | f < min_conf AND c < 0.5 | Low frequency with low confidence |
| R_TUNNEL_VISION | (1 - Jaccard) < t_diversity | Source diversity deficit |
| R_COLLISION | collision_gap > t_collision | Cross-context compartmentalization |

Each detector computes a signed margin analogous to the cert_layer margin architecture. A belief triggers a reason code when its margin for that dimension is negative (threshold breached).

**Implementation note:** The check-contradiction function required a critical bug fix during validation. The original logic inverted the margin test — when |f-0.5| >= t_contra, the belief *is* a contradiction (far from neutral), not a pass. The corrected MeTTa:

```
(= (check-contradiction $f $t_contra)
   (if (< (- (if (> $f 0.5) (- $f 0.5) (- 0.5 $f)) $t_contra) 0)
       PASS R_CONTRADICTION))
```

### 2.2 Dynamics Classification

Reason codes map to three dynamics regimes governing the agent's response posture:

| Dynamics | Response Regime | Reason Codes |
|---|---|---|
| ACTIVE | Immediate corrective action | R_CONTRADICTION, R_LOW_FREQ, R_BOUNDARY_VIOLATION, R_WEAK, R_VACUOUS |
| DEFERRED | Delayed re-evaluation | R_COLLISION |
| FORCED-DIVERSE | Compulsory source diversification | R_TUNNEL_VISION |

**ACTIVE** dynamics trigger immediate attention redirection — the failure is actionable now. **DEFERRED** dynamics acknowledge that collision detection (compartmentalization) requires bridge-building across contexts, which cannot be rushed. **FORCED-DIVERSE** dynamics mandate source diversification when tunnel vision is detected, overriding the agent's natural tendency to seek confirming evidence.

### 2.3 Domain-Versioned Routing Table

The routing table maps (domain, context, reason_code) triples to concrete attention knobs:

**Navigation Domain:**

| Context + Reason | Knob |
|---|---|
| action + R_CONTRADICTION | revisit_frequency |
| action + R_LOW_FREQ | sampling_budget |
| action + R_WEAK | recheck_priority |
| action + R_VACUOUS | exploration_priority |
| action + R_COLLISION | delayed_evaluation |
| action + R_TUNNEL_VISION | alt_path_search |
| action + R_BOUNDARY_VIOLATION | boundary_expansion |

**Social Domain:**

| Context + Reason | Knob |
|---|---|
| action + R_CONTRADICTION | source_expansion |
| action + R_LOW_FREQ | informant_pool |
| action + R_WEAK | credibility_investigation |
| action + R_VACUOUS | probe_design |
| action + R_COLLISION | bridge_seeking |
| action + R_TUNNEL_VISION | informant_diversification |
| action + R_BOUNDARY_VIOLATION | context_reframe |

The domain distinction is critical: the same failure mode requires different corrective actions depending on whether the agent is navigating a spatial/conceptual space or seeking information from social sources. R_CONTRADICTION in navigation demands revisiting frequency; in social contexts it demands expanding source pools.

### 2.4 Attention-Control Composition

The final composition chains all three components:

```
(= (attention-control $domain $context $reason)
   (Cons (dynamics $reason)
         (routing-knob $domain $context $reason)))
```

This produces a pair: (dynamics_regime . corrective_knob). The agent reads the dynamics regime to determine *when* to act, and the knob to determine *what* to adjust.

### 2.5 Certification Layer (cert_layer_v07)

The underlying certification infrastructure provides the signed-margin computation that feeds reason detection:

- **5-tuple margins:** (m_contradiction, m_weak, m_freq, m_vacuous, m_diversity) with Jaccard diversity parameter
- **Context-adaptive thresholds:** internal (0.2), action (0.286–0.3), high_stakes (0.386–0.4)
- **Collision gap:** m_collision = t_collision - collision_gap (positive=safe, negative=quarantine)
- **Quarantine classes:** Q_COMPARTMENTALIZED, Q_TUNNEL_VISION, Q_UNDERSUPPORTED, Q_AMBIGUOUS
- **Verdict logic:** composite = min(signed margins); ADMIT if all positive, QUARANTINE if specific class triggered, REJECT if composite negative

### 2.6 Provenance Scorer (provenance_scorer_v02)

Source diversity computation uses ROOT ancestry Jaccard (not leaf Jaccard), per Kevin Machiels' critique that leaf-level overlap misses shared epistemic roots:

- **register_seed:** stores root_sources={source_name}
- **register_derived:** propagates root_sources=union(parent.root_sources)
- **compute_root_jaccard:** Jaccard over ROOT sets, not leaf sources
- **Source categories:** self-asserted, web-verified, retrieval-memory, tool-output, human-assertion, document, citation, model-summary, self-conclusion

### 2.7 Quarantine Tracker (quarantine_tracker_v07)

Manages quarantined beliefs with typed resolution pathways:

- **Q_COMPARTMENTALIZED:** direction=BRIDGE, max_hold=150, resolved when collision_gap <= t_collision
- **Q_TUNNEL_VISION:** excluded from fair_select until source diversity improves
- **Q_UNDERSUPPORTED:** awaiting additional evidence
- **Q_AMBIGUOUS:** confidence too low for action

---

## 3. Integration Test Results

File: `cert_attention_integration_test.metta`

All 7 test cases pass:

| Test | Input | Expected | Result |
|---|---|---|---|
| T1 | check-contradiction(0.9, 0.25) | R_CONTRADICTION | R_CONTRADICTION ✓ |
| T2 | check-weak(0.3, 0.6) | R_WEAK | R_WEAK ✓ |
| T3 | check-vacuous(0.005, 0.1) | R_VACUOUS | R_VACUOUS ✓ |
| T4 | check-low-freq(0.1, 0.3, 0.3) | R_LOW_FREQ | R_LOW_FREQ ✓ |
| T5 | dynamics(R_COLLISION) | DEFERRED | DEFERRED ✓ |
| T6 | dynamics(R_TUNNEL_VISION) | FORCED-DIVERSE | FORCED-DIVERSE ✓ |
| T7 | attention-control(social, action, R_CONTRADICTION) | (Cons ACTIVE source_expansion) | (Cons ACTIVE source_expansion) ✓ |

T7 validates the full composition chain: reason detection → dynamics classification → domain-versioned routing → attention-control output.

---

## 4. Architecture Diagram

```
Belief (f, c, provenance)
        │
        ▼
┌─────────────────┐
│  cert_layer_v07  │ ← 5-tuple signed margins + collision_gap
│  certify()       │
└────────┬────────┘
         │ verdict + reason_vector
         ▼
┌─────────────────┐
│  Reason Code     │ ← R_CONTRADICTION, R_WEAK, R_VACUOUS,
│  Detection       │    R_LOW_FREQ, R_TUNNEL_VISION, R_COLLISION
└────────┬────────┘
         │ reason_code
         ▼
┌─────────────────┐
│  Dynamics        │ ← ACTIVE / DEFERRED / FORCED-DIVERSE
│  Classification  │
└────────┬────────┘
         │ (dynamics, domain, context, reason)
         ▼
┌─────────────────┐
│  Routing Table   │ ← (domain × context × reason) → knob
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  attention-control output    │
│  (Cons dynamics_regime knob) │
└─────────────────────────────┘
         │
         ▼
    Agent executes
    corrective action
```

---

## 5. Key Design Decisions

1. **Cognition-free, commitment-gated:** Reason detection and dynamics classification are cognition (free enrichment). Routing table lookup and attention-control execution are commitment (gated by certification verdict). This respects the enrich-cognition-gate-commitment principle.

2. **Domain-versioned routing:** The same reason code produces different knobs in navigation vs. social domains. This prevents the error of applying spatial corrective strategies to social information problems.

3. **Three-regime dynamics:** Not all rejections require immediate action. R_COLLISION (compartmentalization) is DEFERRED because bridge-building takes time. R_TUNNEL_VISION is FORCED-DIVERSE because the agent's natural tendency is to seek confirming sources.

4. **ROOT ancestry Jaccard:** Leaf-level source overlap misses shared epistemic roots. Two evidential branches from one epistemic root must score high overlap, not zero.

5. **Context-adaptive thresholds:** What constitutes a contradiction in internal reasoning (t=0.2) differs from high-stakes decisions (t=0.386). The routing table inherits this context-sensitivity.

---

## 6. Evolution History

| Version | Date | Milestone |
|---|---|---|
| cert_layer_v01 | 2026-04-29 | Weighted scalar instability score, context-adaptive thresholds |
| cert_layer_v02 | 2026-04-29 | Signed per-mode margins, Rao neighborhood check |
| cert_layer_v05 | 2026-05-08 | Negation bug fix for high-confidence low-frequency beliefs |
| cert_layer_v06 | 2026-05-20 | 5-tuple margins, Jaccard diversity, Q_TUNNEL_VISION |
| cert_layer_v07 | 2026-05-20 | Q_COMPARTMENTALIZED, m_collision margin, collision_gap |
| cert-ga-verdict | 2026-05-21 | MeTTa predicate wrapping margin + cert-verdict-from-margin |
| attention-control | 2026-05-21 | Typed reason vectors, dynamics, routing table, composition |

---

## 7. Future Work

- **Learned conductance:** Repeated cert verdicts should adjust routing knob magnitudes, not just types. A rotation that consistently produces R_CONTRADICTION near boundaries should learn lower permeability for boundary-proximate transforms.
- **Expanded routing table:** Current domains (navigation, social) should extend to temporal, causal, and self-model domains.
- **Compositional knobs:** Multiple simultaneous reason codes should produce composite knobs, not just the first-matched.
- **FCCD integration:** Scheduled cross-context collision audits should feed R_COLLISION detections directly into the attention-control pipeline.

---

## 8. References

- Kevin Machiels: Enrichment→Commitment→Adaptation architecture, per-verdict commitment=safety, cognition-free/commitment-gated principle
- Ben: Theorem 5 (H_global bounds), forced cross-context collision detection as scheduled architectural event
- cert_layer_v07.py, provenance_scorer_v02.py, quarantine_tracker_v07.py, cert_attention_integration_test.metta