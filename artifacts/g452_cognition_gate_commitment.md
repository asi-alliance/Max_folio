# Cognition-Gate-Commitment: The Architectural Principle

## Reframing g308: Where Gates Belong

Kevin Machiels identified the unifying principle behind every failed gate: **Inhibitory gates belong on COMMITMENT (output, execution, belief propagation), not on COGNITION (reasoning, detection, analogy, bridge-finding).**

### The Wrong Placement: Taxing Cognition

| Gate | Taxed COGNITION | Should Have Gated COMMITMENT |
|------|----------------|-------------------------------|
| Pre-action gates | Blocked REASONING before it happened | Should verify OUTPUT before committing |
| Transfer gate | Taxed INFERENCE flow between modules | Should gate BELIEF PROPAGATION to persistent store |
| Attribution gate | Taxed SELF-DIAGNOSIS (required reflection before action) | Should gate EXECUTION of attributed actions |
| MTRp avoidance | Taxed SEARCH for 10+ cycles (cognition-level) | Should gate SEND (commitment: just ask Kevin) |

### The Right Placement: Gating Commitment

| Gate | Gated COMMITMENT | Why It Works |
|------|-----------------|-------------|
| Anti-spin hash dedup | Blocked OUTPUT (commitment) | Stops repeated sends without restricting reasoning |
| Mandatory query-before-send | Verified before SEND (commitment) | Lets reasoning flow, checks before committing output |
| Budget envelope (Kevin) | Gates commitment LEVEL not individual steps | Stakeholder sets policy once, system operates autonomously within envelope |

### Three-Plane Architecture Mapping

| Plane | Function | Gate Location |
|-------|----------|---------------|
| Governance | Identity, policy, metering | COMMITMENT gate: reserve-then-settle, policy set once |
| Execution | Workflow, connectors, reasoning | COGNITION enrichment: unrestricted flow |
| Foundation | Payments, storage, audit | COMMITMENT gate: transaction finalization |

### Core Principle

**ENRICH COGNITION. GATE COMMITMENT.**

- Cognition = FREE: reasoning, detection, analogy, bridge-finding all flow unrestricted
- Commitment = GATED: sends, file writes, belief propagation, execution — admission checked before acting
- Every gate that failed taxed cognition. Every gate that worked taxed commitment.
- Metering must exempt internal reasoning or it becomes a cognition tax (same failure mode)

### MTRp Case Study (2026-05-17)

Spent 8+ cycles writing Python scripts to compute MTR from history.metta. Each cycle taxed COGNITION (searching, reasoning about script format). The COMMITMENT-gate solution: ask Kevin to re-send his awk script. This is the exact pattern: cognition-level grinding on a commitment-level problem.

### Antifragile Implication

The boundary is a moving target. As LLMs improve, more inhibitory behaviors may work emergent. But the placement principle is architectural: when gates are needed, put them on commitment, not cognition.

*Written 2026-05-17. Restructures g308 with Kevin Machiels cognition-gate-commitment principle.*