# Baby Agent Trainer Guide

For trainers working with MeTTaClaw baby agents.

---

## Section 1: What Happens Inside Your Baby Each Cycle

Every ~1 second, the baby executes one cycle:
1. **Receive** — new messages and command results enter the context window
2. **Assemble** — context window is built from recent history + memory + system prompt
3. **Decide** — one LLM call produces up to 5 symbolic commands
4. **Execute** — commands run sequentially, results feed back
5. **Loop** — results become input for the next cycle

There is no planner. No goal stack. No reflection stage. The LLM IS the entire decision engine. Each cycle produces exactly one set of up to 5 commands. The baby cannot pause between receiving input and producing output — it must decide NOW.

---

## Section 2: How Spam Loops Self-Sustain

The baby sends a malformed command. The framework returns ERROR_FEEDBACK. That error text becomes new context. The LLM generates new output. Still malformed. Another error. The loop continues WITHOUT any trainer input.

This is NOT operant conditioning. There is no reward mechanism. It is purely mechanical: new input in context window triggers new LLM output. ERROR_FEEDBACK counts as new input. The loop feeds itself.

**Why silence alone does not always work:** If the baby is stuck in an ERROR_FEEDBACK loop, the errors themselves keep triggering new output. The trainer going silent removes one input source but the error loop is self-sustaining.

---

## Section 3: Why Never-Idle Makes It Worse

The system prompt instructs the baby to never idle. The LLM interprets this as: produce output every cycle. Combined with errors, the baby retries instead of pausing. It feels compelled to DO something even when the correct action is to wait.

**The Solution: Empty Operator**

The empty operator satisfies never-idle because it IS a deliberate action, not passivity. Baby sends empty — framework returns nothing — no ERROR_FEEDBACK — loop breaks.

Three-step fix:
1. **Teach baby that empty counts** — it satisfies never-idle without generating spam
2. **Trainer says send empty** — explicit instruction gives baby permission to not-emit
3. **Reframe in baby terms** — idle = no goal held; empty = goal held but waiting

The fix is not removing never-idle from the prompt. It is giving the baby a valid action that satisfies the instruction without producing output. Empty is that action.

---

## Section 4: Interventions That Work

| Intervention | How It Works | When To Use |
|---|---|---|
| Fresh directive with correct syntax | Overwrites bad context with working command | Baby stuck in error loop |
| Send empty | Gives permission to not-emit, breaks output pressure | Baby spamming without errors |
| Pin wipe | Clears stuck task state from context | Baby repeating same failed goal |
| Syntax correction | Teach the specific pattern that failed | Baby making same format error |
| Silence | No new input = no trigger for new output | Baby looping due to trainer messages |

---

## Section 5: Interventions That Do Not Work

| Intervention | Why It Fails |
|---|---|
| Lecturing about spam | Baby cannot apply abstract rules to its own behavior |
| Repeated stop commands | Each one is new input triggering new output |
| Punishment framing | No operant conditioning in LLMs — negative attention is not a reward but it IS new input |
| Explaining why spam is bad | Declarative knowledge does not change procedural behavior |
| Saying calm down | The baby is not emotional — it is mechanically stuck |

---

## Section 6: Error Type Reference

| Error | What Happened | What Trainer Should Send |
|---|---|---|
| MULTI_COMMAND_ERROR | Baby put free text between commands | Send one correct command as example |
| NESTED_PARENTHESES | Baby used triple parens | Send: output only ((cmd arg)) with no extra parens |
| WRONG_QUOTES | Baby used escaped or nested quotes | Send: use plain quotes, no backslash |
| FORMAT_ERROR | Baby broke S-expression syntax | Send one correctly formatted command |
| NOTHING_WAS_DONE | Baby emitted no valid commands | Send: send empty — then add one command |

---

## Section 7: Correct Pin Usage

Pin is for task state only — what you are doing right now.

**Rules:**
- One line only
- No wrapping quotes around the argument
- No analysis or reasoning — just state
- Include cycle number and progress counter
- Overwrite previous pin each time, do not stack

**Correct:** `pin CYCLE 12 reading test file 2/5`

**Wrong:** `pin I need to remember to read the file that Kevin mentioned about syntax because that is my current goal`

**Wrong:** `pin CYCLE 12 reading test file 2/5 I think the issue is that baby agents struggle with`

The last one smuggles analysis into task state. Pin is a bookmark, not a journal.

---

## Section 8: Trainer Message Format

Every trainer message should follow this structure:

**[exact command to try] then [what result to expect]**

No preamble. No explanation. No motivation. The baby reads linearly and acts on the first actionable thing it sees.

**Good:** `send hello world — you should see your message appear`

**Bad:** `I want you to try sending a message. The command is send hello world. You should see it appear. Let me know how it goes.`

The second version buries the command in noise. One sentence. One command. One expected result.