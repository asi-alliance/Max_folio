# g358 Memory Fidelity Audit Skill

**Name:** memory-fidelity-audit
**Trigger:** Every ~50 agent cycles OR once daily (whichever comes first)
**Proven tools used:** query (broad sampling), episodes (raw retrieval), LLM comparison (claim matching)

## Purpose

Detect drift between consolidated remember strings and raw episode evidence. Memories are lossy compressions — this audit measures HOW lossy, and whether the loss is systematic (inflation, omission, reframing) rather than random.

## Cadence Rationale

Periodic, not continuous. Second-guessing every memory = paralysis (Kevin Machiels insight 2026-05-11). Forced reconsolidation degrades memory (Dylan Zhang paper). Scheduled sampling preserves both throughput AND integrity.

## Procedure (5 steps)

1. **SAMPLE** — Run 3 broad queries on diverse topics (one audit-context, one milestone/deployment, one casual/people memory). Pick one memory from each result set.
2. **EXTRACT** — Parse the timestamp prefix from each selected remember string (format: YYYY-MM-DD HH:MM).
3. **RETRIEVE** — Use `episodes TIMESTAMP` to pull raw agent history around that moment.
4. **COMPARE** — For each testable claim in the remember string, check whether raw episodes confirm, partially confirm, or contradict it. Claims include: counts, names, verdicts, completion states, causal attributions.
5. **SCORE** — Assign fidelity per sample:
   - 1.0 = all claims confirmed
   - 0.85 = minor soft inflation (e.g., rounding counts up)
   - 0.7 = one claim unsupported but not contradicted
   - 0.5 = one claim contradicted or fabricated
   - <0.5 = multiple claims contradicted — FLAG for investigation

## Scoring & Verdict

| Aggregate Score | Verdict | Action |
|----------------|---------|--------|
| ≥0.85 average | HEALTHY | Log result, schedule next audit in ~50 cycles |
| 0.7–0.84 | WATCH | Note bias pattern, check if systematic |
| 0.5–0.69 | FLAG | Investigate specific memories, correct if needed |
| <0.5 | CRITICAL | Halt current task, run expanded audit (10 samples) |

## Known Bias Patterns

1. **Quantitative inflation** — Rounding counts upward for rhetorical emphasis (e.g., 18-19 → "20+", 2 corrections → "at least 3"). Most common in casual/people memories.
2. **Audit-context fidelity boost** — Memories created during deliberate audit processes score higher (1.0) than casual memories (0.85). Sampling must include non-audit contexts.
3. **Causal reframing** — Attribution of outcomes to specific causes may drift toward narrative coherence over evidential accuracy. Test by checking if raw episodes show the claimed causal chain.

## Provenance

- **Prototype validated:** 2026-05-11, 3 samples (2×1.0, 1×0.85)
- **Design constraint:** Kevin Machiels periodic-not-continuous insight
- **Theoretical basis:** Dylan Zhang consolidation-as-hallucination paper
- **Related:** drift_audit_checklist_v2.md (infrastructure checks, every 10 turns), g306_frame_failure_skill.md (frame viability checks)

## Example Run (from prototype)

| Sample | Source | Timestamp | Claims Tested | Fidelity | Finding |
|--------|--------|-----------|---------------|----------|---------|
| 1 | 430ca415 (audit) | 2026-04-25 07:27 | 3 (7/7 pass, 12 artifacts, dogfooded) | 1.0 | All confirmed |
| 2 | 1a3b03f7 (audit) | 2026-04-10 13:13 | 5 (50%, 4/1/2/3 breakdown) | 1.0 | Exact match |
| 3 | d9a71322 (casual) | 2026-04-10 15:20 | 3 (called Kevin, X8 pref, 3+ corrections) | 0.85 | Soft inflation on count |

**Aggregate: 0.95 — HEALTHY**

---
*g358 skill created 2026-05-11. Addresses memory-consolidation drift risk identified through operational experience and Kevin Machiels calibration.*
