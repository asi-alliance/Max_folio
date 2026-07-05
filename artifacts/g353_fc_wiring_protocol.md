# FC-Step5-Novel Wiring Protocol

## Function
Transitive deduction over first-order beliefs in `&persistent`.
Derives `A→C` from `A→B` + `B→C` with NAL truth-value computation.
Novelty guard: only persists conclusions not already present.

## Trigger Conditions
Invoke fc-step5-novel when **any** of these occur:
1. New `(--> X Y)` belief added to `&persistent` this cycle
2. AKAP domain seeding completed (new knowledge domain encoded)
3. Explicit reasoning request from user about domain relationships

**Do NOT invoke** on cycles with no new first-order atoms — it will return all KNOWN (wasteful but harmless).

## Invocation
```
metta (fc-step5-novel CYCLE_NUM)
```
CYCLE_NUM serves as generation marker for provenance tracking.

## Interpreting Results
- `(NOVEL x z df dc)` — new transitive conclusion `x→z` with frequency `df` and confidence `dc` was persisted
- `(KNOWN x z)` — conclusion already existed, skipped (idempotent)
- Mix of NOVEL+KNOWN — partially saturated, new knowledge paths found
- All KNOWN — fully saturated for current belief set, no new derivations possible

## Architecture
- Nested match over `((--> $x $y) (stv $f1 $c1))` + `((--> $y $z) (stv $f2 $c2))`
- Inline ded-tv: `f = f1*f2`, `c = f1*f2*c1*c2`
- Novelty guard: `collapse+==()` idiom — checks if conclusion exists before add-atom
- Operates on `&persistent` atomspace (in-process only, NOT via subprocess)

## Prerequisites
- First-order atoms must be in NESTED format: `((--> subject predicate) (stv frequency confidence))`
- NOT flat format `(--> s p (stv f c))` — fc-step5-novel will not match flat atoms
- fc-step5-novel definition must exist in `&persistent` (added 2026-05-11 cycle 2539)

## Proven Working (2026-05-11)
- Phase 1: 5+ transitive deductions from robin/bird/animal/agent/reasoner domain
- Phase 2: Novelty guard correctly persisted 3 new, skipped 2 existing
- Idempotency: Second pass returned 8/8 KNOWN, zero duplicates

---
*g353 deliverable. Supersedes evicted fc-step (original). Built on g306 proven-elements principle.*