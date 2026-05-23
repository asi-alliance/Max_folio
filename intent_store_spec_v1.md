# Intent Store / Saga State Spec v1

## Core Idea
Durable store of candidate actions that survive across deliberation cycles.
Each intent accumulates evidence via NAL revision until confidence threshold met.

## Schema: PendingSend
```
{
  id: unique_intent_id,
  type: SEND | WRITE | EXECUTE,
  target: recipient or filepath,
  payload_template: message with {slots} for JIT assembly,
  created_cycle: int,
  confidence: {f: float, c: float},  # NAL stv
  evidence: [{cycle, source, stv}],  # independent observations
  preconditions: [{name, satisfied: bool, checked_cycle}],
  threshold: {min_f: 0.7, min_c: 0.6},
  status: GATHERING | READY | FIRED | CANCELLED,
  fired_cycle: int | null
}
```

## Lifecycle
1. **CREATE**: deliberation loop identifies candidate action, creates intent with low confidence
2. **GATHER**: each cycle, loop queries for evidence, revises confidence via NAL
3. **READY**: when conf >= threshold AND all preconditions satisfied, status -> READY
4. **FIRE**: deferred executor assembles JIT params, executes, status -> FIRED
5. **CANCEL**: if counter-evidence drops conf below floor, status -> CANCELLED

## Confidence Accumulation
Uses NAL revision: c_new = (c1+c2)/(c1+c2+1)
Each independent evidence source revises upward.
3 independent sources typically reach >0.8 confidence.

## Integration
- Deliberation loop always runs (no LLM skip)
- Intent store persisted via pin or file between cycles
- phase_controller.py gates tools within each deliberation phase
- Deferred executor checks READY intents at end of each cycle
