# Certified Query Validation Design Document

## Purpose
Validate whether 3-check certification (supersession, contradiction, context validity) improves over raw query before building implementation. Per Kevin Machiels original request: validate if improvement over raw query.

## What Raw Query Misses
Raw query returns highest-similarity match regardless of:
- Whether a newer higher-confidence memory on same topic exists (supersession)
- Whether an opposing claim with stronger evidence exists (contradiction)
- Whether the originating context is still active (context validity)

## Test Cases

### T1: Supersession - Stale Recommendation
**Setup**: Memory A (2026-03-15): use fast-index scan for audits (f=0.9, c=0.7). Memory B (2026-05-10): use full-index scan for audits (f=0.85, c=0.8).
**Raw query** audit scan method: Returns Memory A (higher f).
**Certified query**: Supersession check detects B is newer+higher-c on same topic. Returns B with SUPERSeded flag on A.
**Expected**: Raw returns stale recommendation. Certified returns current one.

### T2: Contradiction - Opposing Claims
**Setup**: Memory C: fast-index is safe for production (f=0.8, c=0.6). Memory D: fast-index loses data in production (f=0.7, c=0.8, 3 independent sources).
**Raw query** fast-index safety: Returns C (higher f).
**Certified query**: Contradiction check detects D has stronger evidence opposing C. Flags CONFLICT, returns D with contradiction warning.
**Expected**: Raw returns the comforting but weaker-evidence claim. Certified surfaces the stronger-evidence warning.

### T3: Context Validity - Expired Context
**Setup**: Memory E (from legacy-migration context, expired 2026-04-01): use legacy schema for user queries (f=0.9, c=0.9). Memory F (from active-production context): use v2 schema for user queries (f=0.7, c=0.6).
**Raw query** user query schema: Returns E (higher f and c).
**Certified query**: Context validity check finds legacy-migration context expired. Flags E as CONTEXT_STALE. Returns F as active-context result.
**Expected**: Raw returns expired-context memory. Certified deprioritizes stale-context result.

### T4: No Certification Needed - Agreement
**Setup**: Memory G: water boils at 100C at sea level (f=0.99, c=0.95). No newer, no contradiction, context still active.
**Raw query**: Returns G.
**Certified query**: All 3 checks pass. Returns G with ADMIT.
**Expected**: Same result. Certification adds no overhead when not needed.

### T5: Multiple Flags - Supersession + Context Stale
**Setup**: Memory H (expired context, old): use REST API (f=0.9, c=0.7). Memory I (active context, new): use GraphQL API (f=0.8, c=0.8).
**Raw query**: Returns H.
**Certified query**: Both supersession AND context validity flag H. Returns I with dual certification.
**Expected**: Certification catches two independent failure modes raw query misses.

## Known Gaps (Open Questions)
1. Context validity signal: how to determine originating context is still active? Options: explicit expiry timestamps, context tags in memories, active session matching. Needs specification.
2. False positive risk: supersession check could flag benign updates as stale (e.g. old but correct fact). Needs confidence-margin threshold.
3. Contradiction scope: what counts as same topic? Lexical match vs semantic overlap. Over-broad matching causes false conflicts.
4. Certification cost: if checks require additional queries, latency increases. Must stay under raw query latency budget.

## Validation Criteria
Certified query improves over raw query when:
1. It returns a different answer than raw query in T1-T3, T5
2. The different answer is verifiably better (newer, stronger evidence, active context)
3. It adds no overhead in T4 (agreement case)
4. Each check independently catches a failure mode the other checks miss

## Next Step
Run these test cases against actual memory data. Only build implementation if validation confirms improvement.