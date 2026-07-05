# g466: 9-Field Causal-Role Compatibility Check

## Purpose
Add causal-role compatibility verification to existing two-path bridge certification framework (hyperpolation_research_report.md). Stage 1 diffusion (cosine similarity role matching) already works. Stage 2 certification lacked HOW to verify mechanism transfer. This procedure fills that gap using Kevin Machiels' 9-field causal slot descriptions.

## 9-Field Causal Slot Description Template

For each bridge predicate, fill:

| Field | Definition | Example (aesthetic_constraint) |
|-------|-----------|-------------------------------|
| carrier | What carries the causal role | stylistic_preference |
| substrate | What the mechanism acts upon | solution_space |
| mechanism | How the role operates | constraint_shaping (narrows possibilities) |
| causal_position | Where in the causal chain | upstream_boundary_condition |
| direction | Causal direction | constraining (top-down) |
| timescale | Temporal scope | design_phase |
| observability | How observable the effect is | partially_observable |
| intervention_handle | How to manipulate it | adjust_constraint_set |
| failure_mode | How it breaks | over-constraining |

## Falsification Test

**Question**: Can the target domain achieve the same outcome WITHOUT the bridged mechanism?

- **Yes** = POETIC (constraint-shaping, not mechanism transfer)
  - The bridge narrows solution space but outcome achievable via other paths
  - Classification: CANDIDATE, quarantine semantic claims
  - Propagation: cognition enrichment only, no commitment

- **No** = CERTIFIED candidate (mechanism transfer)
  - The bridged mechanism is necessary for the outcome in target domain
  - Classification: advance toward OPERATIONAL
  - Propagation: eligible for commitment after provenance verification

## Mechanism Transfer vs Constraint Shaping

**Mechanism transfer** = structural channel making preservation NECESSARY (by construction)
- Example: Banach FPT contraction maps guarantee convergence (not just observed)
- Invariant preserved BY CONSTRUCTION via structural channel

**Constraint shaping** = solution space narrowing (contingent, not necessary)
- Example: aesthetic_constraint narrows design space but outcome reachable without it
- Invariant preserved contingently, not by construction

## Integration into cert_layer v07 Stage 2

After Stage 1 diffusion passes (cosine similarity >= threshold):

1. Fill 9-field causal slot descriptions for bridge predicate
2. Apply falsification test
3. Classify result: POETIC or CERTIFIED candidate
4. Route accordingly:
   - POETIC: mark CANDIDATE, restrict to cognition enrichment, no propagation
   - CERTIFIED candidate: advance to provenance_scorer, eligible for commitment

## Assessment: aesthetic_constraint bridges

All three aesthetic_constraint bridges (interviewing, ontology, negotiation) score POETIC:
- Real effect (constraint-shaping)
- Weak bridge (not mechanism transfer)
- Diffusion: PASSED
- Certification: FAILED (falsification test: target domains can achieve outcomes without aesthetic constraint)

Structural validity (TV determinism) confirmed = cognition enrichment.
Semantic validity (causal-role transfer) lacking = quarantined as CANDIDATE.

## Status
- g466 procedure drafted 2026-05-22
- Pending: integrate into cert_layer_v07.py as certification stage
- Pending: apply to g463/g464 bridges for re-classification