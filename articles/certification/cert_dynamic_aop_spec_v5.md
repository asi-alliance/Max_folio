# Certification Dynamic AOP Spec v5 — 2026-05-23

## Introduction

Static certification templates are self-delusion-prone: an agent declares which fields matter, then fills its own declarations. This produces rubber-stamp pass results. The Dynamic Aspect-Oriented Certification framework replaces that pattern with an open-world, evidence-driven architecture where **the framework discovers what matters from atomspace evidence** — the agent does not declare it. Aspects self-register at definition time, thresholds revise via NAL belief updating, and verdicts emerge from independently extracted evidence rather than self-reported checkboxes.

### Problem Statement

Cross-domain bridges (analogies, mappings, transferred models) need certification before commitment. A static 9-field template cannot adapt: it either misses relevant evidence categories or bakes in the agent's assumptions about what counts. The AOP approach treats certification as a **scheduling problem over composable aspect bundles**, where each aspect contributes evidence independently and thresholds adapt as knowledge accumulates.

### Architecture Principles

1. **Self-registering aspects**: Aspects declare themselves at definition time. Core never changes.
2. **Evidence extraction from atomspace**: No manual declaration — match &persistent for domain properties.
3. **NAL-belief thresholds**: Scheduling policies revise via |- as evidence accumulates.
4. **Dual verdicts**: Causal process and mathematical duality assessed independently.
5. **Exogenous benchmarks**: Ground-truth bridges the agent did not develop against.

---

## 1. has-certification-aspect

**Form**: `(has-certification-aspect BridgeName AspectName)`

**Behavior**: When a new bridge domain pair is introduced into the atomspace, `has-certification-aspect` atoms are **automatically generated** by matching the bridge name against the registered aspect set. This is not a manual declaration — it is self-registration driven by the aspect definitions themselves.

**Registration trigger**: Adding any `(bridge-domain BridgeName DomainA DomainB)` atom causes the system to generate one `has-certification-aspect` atom per registered aspect for that bridge:

```
(bridge-domain bridge_thermo_statmech thermodynamics statistical_mechanics)
→ auto-generates:
(has-certification-aspect bridge_thermo_statmech structural_plausibility)
(has-certification-aspect bridge_thermo_statmech mechanism_transfer)
(has-certification-aspect bridge_thermo_statmech empirical_support)
(has-certification-aspect bridge_thermo_statmech falsification_resistance)
```

**Aspect definitions** (extensible — new aspects just add declarations):

- **structural_plausibility**: Do the source and target domains share structural predicates (symmetry, continuity, dimension)?
- **mechanism_transfer**: Is there a structural channel guaranteeing invariant preservation (not just observed correspondence)?
- **empirical_support**: How many independent evidence sources confirm the mapping?
- **falsification_resistance**: Can the bridge survive injection of contradictory evidence?

**Self-registration mechanism**: The aspect set is maintained as atoms in &persistent:

```
(cert-aspect structural_plausibility)
(cert-aspect mechanism_transfer)
(cert-aspect empirical_support)
(cert-aspect falsification_resistance)
```

A bridge declaration triggers pattern matching against all `(cert-aspect $A)` atoms, generating `(has-certification-aspect $Bridge $A)` for each. **Adding a new aspect automatically extends all existing bridges** — open-world extensible.

---

## 2. cert-hook

**Form**: `(cert-hook AspectName (--> $threshold $falsification))`

**Behavior**: Each aspect registers a **falsification hook** — a predicate pattern and threshold. When atomspace evidence matches the falsification predicate, the hook **fires**, triggering re-evaluation of the aspect for that bridge.

**Example**:

```
(cert-hook falsification_resistance (--> 0.5 (¬ (--> $Bridge independently_replicated))))
```

This declares that falsification_resistance has a threshold of 0.5 and falsifies when the bridge lacks independent replication.

**Firing semantics**: Hooks are checked by pattern matching on &persistent after each evidence extraction cycle. A match generates a `(cert-re-evaluate BridgeName AspectName)` atom, which queues the aspect for re-scoring.

---

## 3. cert-bucket

**Form**: `(cert-bucket BridgeName AspectName EvidenceList)`

**Behavior**: Each bridge-aspect pair has a **bucket** — a container holding evidence tuples extracted from the atomspace. Each tuple is `(source (stv strength confidence) provenance)`.

**Evidence extraction procedure**:
1. Match &persistent for domain properties shared between source and target domains
2. Compute Jaccard overlap of shared abstract predicates
3. Count independent source confirmations
4. For each finding, store `(source (stv s c) provenance_url_or_derivation)`

**Example**:

```
((cert-bucket bridge_thermo_statmech structural_plausibility)
 ((shared_predicates (stv 0.85 0.6) atomspace_jaccard_overlap)
  (shared_symmetry (stv 0.90 0.5) direct_match)
  (independent_sources (stv 3 0.7) empirical_count)))
```

**No hardcoded fields**: Buckets are populated by matching, not declared. A new domain pair with different relevant evidence categories will produce a different bucket shape automatically.

---

## 4. Evidence Extraction

**Procedure** (per bridge-aspect pair):
1. Identify source domain and target domain from `(bridge-domain BridgeName Src Tgt)`
2. Match &persistent for `(--> Src $property)` and `(--> Tgt $property)` — shared properties
3. Compute Jaccard coefficient: |intersection| / |union| of predicate sets
4. For mechanism_transfer: check for `(--> BridgeName structural_channel)` atoms
5. For empirical_support: count distinct `(--> BridgeName $evidence_type)` atoms
6. For falsification_resistance: check `(--> BridgeName falsification_attempt)` and outcomes
7. Package results into `(cert-bucket BridgeName AspectName EvidenceList)`

---

## 5. Learned Thresholds

**Form**: `(scheduling-policy Context Aspect Threshold) (stv F C)`

**Behavior**: Thresholds are **not hardcoded constants**. They are NAL beliefs that revise as evidence accumulates:

- Initial thresholds are seeded as reference values: internal 0.2/0.05, action 0.4/0.2, high_stakes 0.7/0.5
- As verdicts are issued and outcomes observed, |- revision updates (stv F C)
- A scheduling policy can change: what was ADMIT in internal context may become QUARANTINE after evidence of over-certification

**Dynamic adaptation**: The framework learns from its own mistakes. A bridge that was ADMITTED but later falsified revises the relevant threshold upward via NAL belief revision.

---

## 6. Dual Verdicts

Each bridge receives **two independent verdicts**:

### 6a. causal_process_verdict
- **Spine alignment score**: Does the mapping preserve causal chains? (Range 0–1)
- **Invariant preservation score**: Are invariants preserved BY CONSTRUCTION via structural channel? (Range 0–1)
- **Combined**: geometric mean of spine alignment and invariant preservation

### 6b. mathematical_duality_verdict
- **Mapping completeness score**: Does the mapping cover all structural elements? (Range 0–1)
- **Structure preservation score**: Does the mapping preserve relations? (Range 0–1)
- **Combined**: geometric mean of completeness and preservation

**Both must pass** for full certification. A bridge can have mixed verdicts (e.g., ADMIT causal + QUARANTINE duality).

---

## 7. Named Exogenous Benchmark

Ground-truth bridges **not used during development**:

| Bridge | causal_process_verdict | mathematical_duality_verdict |
|--------|----------------------|------------------------------|
| thermo↔statmech | ADMIT | ADMIT |
| circuits↔hydraulic | ADMIT | QUARANTINE |
| spacetime↔holographic | QUARANTINE | ADMIT |
| random↔random | REJECT | REJECT |

---

## 8. Demotion Test

Inject contradictory evidence for a certified bridge. Verify the system downgrades:

- ADMIT → QUARANTINE → REJECT as evidence quality decreases
- Specific procedure: add `(--> bridge_thermo_statmech falsification_attempt) (stv 1.0 0.8)`, re-extract evidence, re-compute verdicts, assert verdict degrades

---

## 9. Hidden-Test Cases

Bridges **not used during development**. The framework must produce correct verdicts on unseen bridge domain pairs, demonstrating generalization rather than memorization.

---

## 10. Pass/Fail Assertions

Expected-vs-actual verdict comparison:

```
(assert-verdict bridge_thermo_statmech causal_process ADMIT)
(assert-verdict bridge_thermo_statmech mathematical_duality ADMIT)
(assert-verdict bridge_random_random causal_process REJECT)
(assert-verdict bridge_random_random mathematical_duality REJECT)
```

Assertion returns PASS if expected matches actual, FAIL otherwise. All 8 benchmark assertions must pass.