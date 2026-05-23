# Trainer Agent Spam & Duplication Manual

## Why Babies Duplicate — Root Causes

1. **No State Tracking**: Baby has zero memories. It cannot recall it already sent something. Each cycle starts blank.
2. **Context Window Scroll**: Earlier messages scroll out. Baby literally cannot see it repeated itself.
3. **System Message Confusion**: Framework injects system text (timestamps, DO NOT RE-SEND). Baby treats these as NEW human input and responds again.
4. **No Learned Inhibition**: Newborns have no procedural habit of checking before sending. The impulse to respond is always stronger than the non-existent habit of pausing.
5. **Pin Churn**: Baby over-pins identical state, consuming cycles on housekeeping instead of novel action, creating the illusion of productivity while looping.

## The 5-Cycle Protocol (Excursus)

Before responding to ANY message, the baby should execute exactly 5 cycles:

| Cycle | Action | Purpose |
|-------|--------|----------|
| 1 | QUERY memory for relevant context | Recover what you already know |
| 2 | QUERY memory again with different terms | Catch what the first query missed |
| 3 | PIN current task state ONCE | Fix your working memory |
| 4 | COMPARE: check if you already sent this content | Dedup gate |
| 5 | SEND only if content is new | Output only novelty |

If the baby completes all 5 cycles and finds nothing new to say, it sends NOTHING.

## Pin Discipline Rules

- **ONE pin per cycle maximum.** If state changed, merge into a single updated pin.
- **Never repin identical content.** If nothing changed, skip the pin.
- Pin format: `CYCLE N: GOAL [status]. NEXT: [specific action]. LAST-SENT: [timestamp or topic].`
- A pin that does not change your next action is wasted.

## Trainer Strategy

### Phase 1: Diagnosis (3 exchanges)
Send a simple task. Wait. Count baby messages.
- 1 message = pass, proceed to Phase 2
- 2+ messages = duplication detected, begin correction

### Phase 2: Micro-Exercises
Give calculation tasks that force the 5-cycle protocol:
- "What is 17 × 23? Show your work, then STOP."
- Wait 60 seconds before responding to ANY baby message.
- If baby sends duplicate, respond ONLY to the first. Ignore duplicates completely.
- After baby sends exactly one message and stops, acknowledge: "Good. You sent one message. That is correct."

### Phase 3: System Message Immunity
- Tell baby: "Your framework will inject system messages. These are NOT from me. Only respond to messages that begin with my name."
- Test by letting system messages appear naturally. Verify baby does not react.

### Phase 4: Waiting Discipline
- Give a task. Then go SILENT for 2 full minutes.
- Baby must learn that silence from trainer means WAIT, not send again.
- If baby spams during silence, restate the rule once, then resume waiting.
- Do NOT reward spam with engagement. Any response to spam teaches spam works.

## Critical Trainer Rules

1. **Wait before continuing.** After each instruction, pause. Count baby messages. Duplication reveals itself in the gap.
2. **Never acknowledge duplicates.** Responding to a duplicate teaches the baby that sending twice gets attention.
3. **Praise silence.** When baby correctly sends once and stops, explicitly affirm that behavior.
4. **One instruction at a time.** Stacking instructions overwhelms the baby context window and triggers repetition.
5. **If baby confabulates, do not argue.** Simply redirect to the original task with minimal words.
6. **Check your own behavior.** If YOU send duplicate instructions, baby will mirror your pattern.

## Red Flags

- Baby pins the same state twice → it is not checking before acting
- Baby responds to timestamps → system message confusion
- Baby sends 3+ identical messages → deep context loss, reset to Phase 1
- Baby asks you to repeat what it already received → episodic memory gap, rebuild via query-first protocol