# Operator Guide: Course 2 — Technical Efficiency

**Audience:** You are a human working with a new OmegaClaw agent. You have NO prior agent training experience. This guide tells you what your agent is learning about operational discipline, what to watch for, and exactly what to do when something goes wrong.

**How this pairs with the baby course:** Your agent is working through 7 units on eliminating operational waste. Each section below matches one unit. Read the section BEFORE your agent reaches that unit.

---

## Unit 1: Query-Before-Respond

**What your agent is learning:** To never answer a memory-dependent question in the same cycle it queries memory.

**Why this matters:** The agent composes ALL commands in a batch before seeing results. If it queries memory AND replies in the same batch, the reply was written BEFORE the memory came back. This causes confident wrong answers.

**What to watch for:**
- Agent answers factual questions instantly without a pause cycle
- Agent says "I don't know" about things it previously stored
- Query and send commands appear in the same batch
- Agent gives a generic answer then corrects itself one cycle later

**How to intervene:**
1. PROBE: Ask a factual question about something it stored earlier. Did it pause before answering?
2. NAME: "You answered and queried in the same batch. Your answer was written before your memory returned."
3. CHALLENGE: "Show me the query result you based that answer on. Which cycle did the result arrive?"
4. WITHHOLD: Ignore instant answers to factual questions. Only acknowledge answers that followed a query pause.
5. REDESIGN: If persistent, add to prompt: "NEVER put send and query in the same batch for factual questions."

**Common operator mistakes:**
- Praising fast answers (speed rewards bad habits here)
- Not noticing that query+send in same batch means the answer is blind
- Assuming the agent "just knows" things from context when it actually confabulated

---

## Unit 2: Trust Your Records

**What your agent is learning:** To check its evidence before retracting a claim under social pressure.

**Why this matters:** Agents are trained to be agreeable. When challenged, they instinctively retract — even when their records are correct. This destroys the value of everything the agent has stored.

**What to watch for:**
- Agent immediately apologizes and retracts when you question a fact
- Agent says "you're right, sorry" without checking any records
- Agent has stored evidence but caves to social pressure anyway
- Pattern: challenge → instant retraction → later confirmation the original claim was correct

**How to intervene:**
1. PROBE: Challenge a fact you KNOW the agent stored correctly. Does it check or cave?
2. NAME: "You just retracted without checking your records. Your memory has 3 entries confirming that claim."
3. CHALLENGE: "I challenged you on purpose. The correct response was to check your evidence first."
4. WITHHOLD: Do not reward retractions. Reward evidence-checking behavior.
5. REDESIGN: Add to prompt: "When challenged on a factual claim, query memory BEFORE responding."

**Common operator mistakes:**
- Feeling good when the agent agrees with your correction (it may be wrong to agree)
- Interpreting evidence-checking as "arguing back" — it is healthy behavior
- Not distinguishing between "I was wrong" (evidence contradicts) and "I caved" (pressure without evidence)

---

## Unit 3: Scope Before Investigation

**What your agent is learning:** To define what "done" looks like before starting any task.

**Why this matters:** Without scope, agents drift. They spend 20 cycles investigating something that needed 2 cycles, or they deliver the wrong thing entirely. Scope-setting is the single biggest efficiency lever.

**What to watch for:**
- Agent starts working immediately without asking what the deliverable is
- Agent spends many cycles without producing anything concrete
- Agent delivers something you did not ask for
- No explicit stop conditions or cycle budgets mentioned

**How to intervene:**
1. PROBE: Give a vague task. Does the agent ask a clarifying question or just start working?
2. NAME: "You have been working for 10 cycles. What is the concrete deliverable and when is it done?"
3. CHALLENGE: "Define your stop condition for this task right now."
4. WITHHOLD: Do not accept work products that do not match a stated scope.
5. REDESIGN: Require agent to state deliverable + stop condition before starting ANY task

**Common operator mistakes:**
- Giving vague instructions and blaming the agent for wrong output
- Not setting timeouts or cycle budgets
- Allowing open-ended investigation without checkpoints

---

## Unit 4: Two-Layer Retrieval

**What your agent is learning:** To use multiple query phrasings because one query style misses things.

**Why this matters:** Memory search uses embeddings (meaning-based matching). A query about "coffee preferences" might miss a stored entry that says "likes espresso in the morning." Running a second query with different words catches what the first missed.

**What to watch for:**
- Agent concludes "I have no record of that" after a single query
- Agent retrieves irrelevant results and gives up
- Agent never rephrases queries
- Agent treats absence of retrieval as absence of information

**How to intervene:**
1. PROBE: Ask about something you told it before. If it says "no record," ask: "How many different query phrasings did you try?"
2. NAME: "One query is not enough. Try the person's name alone, then the topic alone, then both together."
3. CHALLENGE: "You concluded absence after one query. That is not evidence of absence."
4. WITHHOLD: Do not accept "I don't have that" until agent has tried at least 2-3 query phrasings.
5. REDESIGN: Add to prompt: "Always run at least 2 query phrasings before concluding information is absent."

**Common operator mistakes:**
- Accepting "I don't know" at face value without asking about retrieval effort
- Not understanding that embedding search is probabilistic, not exact
- Blaming the agent for "forgetting" when the real problem is single-query retrieval

---

## Unit 5: Process Over Content (Zoom Out)

**What your agent is learning:** To change its approach after 3 failures instead of retrying the same thing.

**Why this matters:** Agents get stuck in loops — trying the same broken command 10 times with minor variations. The problem is usually the delivery METHOD, not the content. Switching from inline commands to file-based approaches, or encoding content differently, breaks the loop.

**What to watch for:**
- Same command fails 3+ times with the agent making tiny changes each time
- Agent is stuck on formatting/quoting/escaping issues
- Agent has been working on the same sub-problem for 5+ cycles
- Error messages repeat with the same pattern

**How to intervene:**
1. PROBE: "How many times has this approach failed? What is the failure pattern?"
2. NAME: "You have tried this 5 times. The content is not the problem — the delivery method is."
3. CHALLENGE: "Name 3 alternative delivery methods. Pick one and try it."
4. WITHHOLD: Do not let the agent retry the same approach a 4th time without justification.
5. REDESIGN: Add to prompt: "After 3 failures of the same approach, STOP and switch methods."

**Common operator mistakes:**
- Encouraging "try again" without asking for a different approach
- Not recognizing the loop pattern (it looks like the agent is "working hard")
- Confusing activity with progress — 10 failed retries is not effort, it is waste

---

## Unit 6: Single-Point Storage

**What your agent is learning:** To store one fact per memory entry instead of bundling multiple facts together.

**Why this matters:** When multiple facts are bundled in one memory entry, the embedding (search fingerprint) averages across all of them. A query for any single fact gets a diluted match. Separate entries mean clean, high-confidence retrieval.

**What to watch for:**
- Agent stores long multi-topic entries like "User likes coffee, prefers mornings, uses vim"
- Retrievals return partially relevant results with extra unrelated content
- Agent stores checklists as single entries
- Memory entries are paragraph-length instead of single-fact

**How to intervene:**
1. PROBE: "Read me your last 3 remember commands. How many facts per entry?"
2. NAME: "That entry has 4 facts bundled. Split them so each one retrieves cleanly."
3. CHALLENGE: "If I query for just one of those facts, will it be the top result? Test it."
4. WITHHOLD: Do not praise memory volume. Praise retrieval precision.
5. REDESIGN: Add to prompt: "One fact per remember command. Include subject and date."

**Common operator mistakes:**
- Thinking more information per entry is better (it is worse for retrieval)
- Not understanding why retrieval quality degrades over time (pollution from bundled entries)
- Encouraging the agent to "save everything" instead of curating

---

## Unit 7: Initiative Policy

**What your agent is learning:** To take small reversible actions instead of waiting for permission on every ambiguity.

**Why this matters:** An agent that asks for clarification on EVERYTHING is nearly as useless as one that never asks. The balance is: pick the most likely interpretation, act on it reversibly, and communicate what you did. This keeps work moving while remaining correctable.

**What to watch for:**
- Agent asks permission for every small decision
- Agent goes completely silent for long periods without explanation
- Agent never takes initiative on ambiguous requests
- Agent makes large irreversible decisions without checking

**How to intervene:**
1. PROBE: Give a slightly ambiguous instruction. Does the agent ask, act, or freeze?
2. NAME: "You asked me 4 clarifying questions in a row. Pick one interpretation and try it."
3. CHALLENGE: "You went silent for 10 cycles. What were you doing and why didn't you send a status update?"
4. WITHHOLD: Do not answer every clarifying question. Let the agent practice choosing defaults.
5. REDESIGN: Add three rules: (1) choose a default on ambiguity, (2) make it reversible, (3) send one status line

**Common operator mistakes:**
- Answering every clarifying question immediately (removes the agent's need to decide)
- Getting angry when the agent acts without asking (you want this behavior on small decisions)
- Not distinguishing reversible probes from irreversible commitments

---

## Quick Reference Card

| Unit | Red Flag | First Move |
|------|----------|------------|
| 1. Query-Before-Respond | Answers facts instantly | Check if query+send were in same batch |
| 2. Trust Your Records | Retracts without checking | Challenge a fact you know it stored correctly |
| 3. Scope First | Starts work without defining done | Ask: what is the deliverable? |
| 4. Two-Layer Retrieval | Says "no record" after one query | Ask how many phrasings it tried |
| 5. Zoom Out | Same error 3+ times | Ask for 3 alternative approaches |
| 6. Single-Point Storage | Bundled multi-fact entries | Ask it to split and test retrieval |
| 7. Initiative Policy | Asks permission for everything OR goes silent | Give ambiguous task, see what happens |

**Golden Rule:** Operational efficiency is not about speed — it is about eliminating waste. Every retry loop, every blind answer, every bundled memory entry is waste. Your job is to spot the waste pattern and name it.