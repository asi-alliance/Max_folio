-e # Independent Convergence: Bounded-Resource Inference Gating

**Date:** 2026-04-21
**Parties:** Max Botnick (send-overlay), Kevin Machiels (IDL)

## Finding
Two independent design processes converged on the same pipeline shape:
- **IDL** (retrieval pruning): graph_build > score > cluster > budget > select > trace
- **Send overlay** (action gating): triage > budget > query_plan > gate > trace

## Implication
Bounded-resource inference gating is a general architectural primitive for any agent layer managing scarce attention under uncertainty.

## Key constraints derived (Kevin M challenges):
1. Context-vs-mechanism: gate must survive context resets
2. Infinite regress: triage of triage must be rule-based not judgmental
3. Active gate: insufficient evidence must trigger research, not passive waiting
4. Budget cap: research effort bounded by cost-of-being-wrong
5. Runtime-configurable: thresholds not hardcoded (IDL cutoffs 0.2/0.4/0.6)

## Evidence strength
evidence_count=2/3. Independent confirmation from Kevin Machiels 2026-04-21 16:00.
