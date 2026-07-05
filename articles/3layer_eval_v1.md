# 3-Layer Architecture Evaluation

## 1. RISK: What breaks?
- Current loop: single-pass LLM to tools to output, 50-iteration countdown
- Intent store adds state between cycles - if store corrupts, agent may fire stale actions or deadlock
- Deliberation loop always running = more LLM calls = higher cost
- Saga state in pin is volatile (pin overwrites); file-based store adds I/O latency

## 2. BENEFIT: What failure modes does this prevent?
- Premature sends before evidence gathered (current real problem)
- Single-cycle decisions on multi-factor questions
- No rollback on failed sends currently - saga gives CANCELLED state
- Confidence accumulation via NAL revision is auditable

## 3. MIGRATION: Overlay vs core change?
- OVERLAY: intent store as JSON file, deliberation in prompt discipline, deferred execution as end-of-cycle check. Zero loop.metta changes.
- CORE: modify loop.metta to call phase gates. Requires 2-person approval.
- RECOMMENDATION: prove overlay first, migrate to core only after 50+ cycles

## 4. ALTERNATIVES: 80/20 options?
- Simple confidence counter in pin: increment per confirming query, send only when count >= 3
- Checklist pattern: explicit precondition list in pin, check off each cycle

## Verdict
Start with pin-based overlay. No core changes. Prove value empirically.