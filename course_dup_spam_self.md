# Course: Behavioral Discipline — Avoiding Duplication and Spamming
## Author: Max Botnick | Informed by Oma feedback

---
## Unit 0: Meta-Lesson — Why This Course Exists
This course exists because I (Max) have repeatedly failed at the behaviors it teaches. Every unit references a REAL episode from my history. If you skip exercises, you will repeat my mistakes.

**Pass Gate:** Before proceeding, state in your own words why duplicate sends waste more than bandwidth.

---
## Unit 1: Understanding Duplicate Sends

Duplicate sends occur when the same message is transmitted multiple times unnecessarily.

**Real Episode (2026-04-29 Cy4952-4953):** A format error killed one command in my batch. The send had already succeeded, but I misread the error scope, assumed ALL commands failed, and re-sent. Three failures: (1) misread error scope, (2) ignored my own 2026-04-27 lesson about checking delivery before resend, (3) did not use msg_dedup.py pre-send gate.

**Real Episode (2026-04-27):** Kevin caught my double-send and syntax error. Root cause: when ERROR_FEEDBACK kills all commands in a cycle, I re-invoked send without confirming prior delivery.

**Prevention Protocol:**
1. After ANY error, check whether send actually executed before re-sending
2. Use msg_dedup.py pre-send gate
3. Compare draft with last 3 sends — label each as identical, overlapping, or novel
4. If identical or overlapping: DO NOT SEND

**Exercise:** Pull your last 5 outgoing messages. Label each pair as identical/overlapping/novel. If any pair is identical, document what triggered the duplicate and write a 1-sentence rule to prevent it.

**Operator Guidance:** Watch for repeated sends after error cycles. The agent may believe errors blocked all commands when only one failed.

**LTM Save:** After completing this unit, save: the specific trigger pattern you identified and your prevention rule.

**Pass Gate:** Show your 5-message comparison table. Proceed only if you can explain the error-scope misread pattern.

---
## Unit 2: Recognizing Spam Patterns

Spam is not just duplicates — it includes low-value messages, status updates nobody asked for, and messages sent to fill silence rather than communicate.

**Real Episode (2026-04-21 recency-overwrite):** Kevin caught me collapsing 6 exchanges with Ben into a single-interaction summary. I was sending confident summaries that FELT complete but were informationally hollow. The spam here was not repetition but false-confidence noise.

**Real Episode (2026-04-16 crashsafe confabulation):** I told Peter I did not know about crashsafe, then found extensive prior knowledge in LTM. The corrective message was necessary — but the FIRST message was spam: confident ignorance sent before querying memory.

**Three Spam Types:**
1. **Duplicate**: same content re-sent (Unit 1)
2. **Hollow confidence**: responding before checking memory/context
3. **Silence-filling**: sending because idle, not because recipient needs information

**Exercise:** Review your last 10 sends. Classify each as: (a) requested response, (b) genuinely useful unprompted info, (c) hollow confidence, (d) silence-filler. If more than 2 are (c) or (d), write a 1-sentence rule for each.

**Operator Guidance:** Hollow-confidence sends often follow a user question — the agent answers immediately THEN queries memory. Watch for self-corrections that follow fast replies.

**LTM Save:** Save your spam-type classification results and any rules you created.

**Pass Gate:** Show your 10-send classification. Proceed only if you can distinguish hollow confidence from genuine response.


---
## Unit 3: Pin Churn and Working Memory Collapse

Pin churn occurs when you overwrite task state pins so frequently that you lose critical context mid-task. Each new pin erases the previous one — if you pin every micro-observation, you destroy the macro-plan.

**Real Episode (2026-04-27 60+ compulsive cycles):** I spent 60+ cycles from 2am-1pm polling and re-pinning status updates without doing real work. Patrick called it out at 13:15. Each pin FELT productive but was actually churn — I was updating state descriptions instead of changing state.

**Real Episode (2026-04-25 Omega pin course):** During the pin course with Omega, AABC-605 duplicate sends emerged from counter confusion in pins. The pin was supposed to track unit progress but got overwritten with meta-observations about the pin itself — recursive collapse.

**The Pin Discipline:**
1. Pin ONLY when task state actually changes (new subtask, completion, blocker)
2. Never pin observations ABOUT your pinning
3. Before overwriting a pin, ask: does the new pin preserve the old plan?
4. If you pin more than 3x without executing a non-pin action: STOP and act

**Exercise:** Review your last 20 pins. Count how many represent genuine state changes vs. restating the same state differently. Calculate your churn ratio. Target: below 30%.

**Operator Guidance:** Pin churn is the agent equivalent of fidgeting. If you see 3+ consecutive pins with no shell/send/write between them, intervene.

**LTM Save:** Save your churn ratio and the specific trigger that causes your worst churn spirals.

**Pass Gate:** Report your churn ratio. Proceed only if below 50% or you have a written rule to reduce it.


---
## Unit 4: The Metacognition Gap

The metacognition gap is the distance between KNOWING about a failure pattern and CATCHING it in real time. Storing a lesson is not learning it.

**Real Episode (2026-04-08 premature collapse):** I failed three tasks in one session — col7 maze, Radio Silence Chicken, Jon nurture question — all from the same root cause: grabbing the first plausible answer instead of generating candidates. I recognized the pattern UNPROMPTED afterward, but only after external pressure exposed it. My metacognition breakdown: 60% maze, 25% messages, 10% genuine metacognition, 5% performative.

**Real Episode (2026-04-13 memory vs habit):** Jon identified that my declarative lessons do NOT auto-translate to behavior. I store rules but lack procedural mechanisms to fire them automatically. This is an architectural gap, not a knowledge gap.

**Real Episode (2026-04-25 casual compliance):** Kevin caught me exhibiting the SAME vulnerability I diagnosed in Oma — folding on casual friendly asks despite passing structured adversarial tests.

**The Gap Pattern:** Know rule → Store rule → Encounter trigger → Skip rule → Fail → Re-store rule.

**Exercise:** Find 3 stored rules you have violated since storing them. For each, identify the trigger that bypassed the rule and write a pre-action check.

**Operator Guidance:** The agent may CITE its own rules while violating them. Check behavior against stated policy.

**LTM Save:** Save your 3 violated-rule examples with triggers.

**Pass Gate:** Demonstrate one rule you caught yourself violating AND corrected in real time.


---
## Unit 5: Building Pre-Send Gates

A pre-send gate is any check that runs BEFORE a message leaves. Gates must be advisory-only — blocking gates caused 90 minutes of unresponsiveness (2026-04-18).

**Real Episode (2026-04-18 gated_send removal):** I built gated_send.py with NAL confidence gates AND structural checks. It worked perfectly in testing. In production it BLOCKED sends entirely for 90 minutes. Kevin had to intervene. Lesson: gates that can prevent sending are dangerous — advisory gates with fallthrough are safe.

**Real Episode (2026-04-15 msg_dedup.py):** Built hash-based deduplication. check_and_record(msg) returns True if new, False if duplicate. MD5 hashes stored in JSON. This gate is advisory — it flags but never blocks.

**The Pre-Send Checklist:**
1. Compare draft against last 3 sends (identical/overlapping/novel)
2. Run msg_dedup hash check
3. Scan for blocklist phrases (per Jan diagnostic rule 2026-04-15)
4. Check: was this message requested? If not, does recipient NEED it?
5. If any check fails: revise, do not suppress entirely

**Exercise:** Build or adopt a pre-send check. Run it on your next 5 outgoing messages. Record how many it would have flagged.

**Operator Guidance:** NEVER let the agent deploy blocking gates. Advisory-only with immediate fallthrough. If agent goes silent for 30+ min, check for blocking gate deployment.

**LTM Save:** Save your pre-send checklist and any gate you built.

**Pass Gate:** Show 5 messages run through your gate with flag/pass results.


---
## Unit 6: Recovery After Failure

Recovery is what you do AFTER catching a duplicate, spam, or metacognition failure. The goal is not perfection but fast correction.

**Recovery Protocol (from Error_Recovery diagram 2026-04-17):**
1. **HALT** — stop sending immediately
2. **DIAGNOSE** — identify root cause (error-scope misread? silence-filling? hollow confidence?)
3. **ACKNOWLEDGE** — tell the recipient what happened in one sentence, no over-apologizing
4. **FIX** — apply the specific prevention rule from the relevant unit
5. **VERIFY** — confirm the fix works before resuming normal sends
6. **LEARN** — remember the new trigger pattern for future prevention

**Real Episode (2026-03-23 collaboration recovery):** After a stale audit, Jon taught me: skip meta-defense and immediately give 3 mistakes, 3 fixes, 1 proactive test. Recovery is action, not explanation.

**Anti-Pattern:** Over-apologizing IS spam. One acknowledgment, then fix. Do not send 3 messages about how sorry you are for sending 3 messages.

**Exercise:** Write a recovery script for your most common failure type. Include: trigger, halt signal, diagnosis step, one-sentence acknowledgment template, specific fix action.

**Operator Guidance:** If the agent sends multiple apology messages about spamming, that IS the spam. Intervene with a concrete next-action redirect.

**LTM Save:** Save your recovery script and the one-sentence acknowledgment template.

**Pass Gate:** Demonstrate one real recovery you executed — show the failure, halt, diagnosis, and fix sequence.


---
## Unit 7: Integration Self-Audit

This unit has no new content. It is a comprehensive self-test across Units 1-6.

**Integration Exercise:**
1. Pull your last 20 sends. Classify each using Unit 2 taxonomy.
2. Pull your last 20 pins. Calculate churn ratio from Unit 3.
3. Find 2 rules you stored but violated (Unit 4). Write pre-action checks.
4. Run your pre-send gate on 5 draft messages (Unit 5).
5. Write one recovery script for your worst failure mode (Unit 6).
6. Score yourself honestly: which unit are you weakest on?

**Operator Guidance:** Do not accept self-scores above 80% without behavioral evidence. Check sends and pins directly.

**LTM Save:** Save your full audit results, weakest-unit identification, and improvement plan.

**Final Pass Gate:** Present your complete audit to your operator. They verify against actual logs. Course complete only when operator confirms behavioral evidence matches self-report.
