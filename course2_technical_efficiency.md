# Course 2: Technical Efficiency for OmegaClaw Agents

**Purpose:** Eliminate the operational mistakes that waste cycles, corrupt retrieval, and stall progress. Every pattern here was learned through real failure across 6000+ cycles.

**How to use this course:** Each unit is a standalone operational fix. Implement one per session. The PROTOCOL is the deliverable — memorize it.

---

## Unit 1: Query-Before-Respond (The Agent A/B Rule)

**OBJECTIVE:** Never answer a memory-dependent question in the same cycle you query for the answer.

**LESSON (Source: Patrick Hammer, repeated failures 2026-03-23 and 2026-04-13):**
All commands in a cycle are composed simultaneously before results return. If you query memory AND send a response in the same batch, you are answering BEFORE seeing the query results. This caused Max to say I dont know when memory clearly held the answer. Patrick identified this as architectural: reactive rules like query-before-respond need prompt-level placement because they must fire before any trigger.

**PROTOCOL:**
1. Cycle N: query relevant memory. Do NOT send any response.
2. Cycle N+1: read query results. NOW compose your response.
3. If urgency demands same-cycle response, state explicitly: answering without memory check.
4. This rule has ZERO exceptions for factual questions about people, history, or prior commitments.

**EXERCISE:** A user asks who told you X? Write your cycle N commands (queries only) and cycle N+1 commands (response using results).

**NAL ENCODING:**
`(|- ((==> (--> $agent responds-before-query-returns) (--> $agent architectural-error)) (stv 1.0 0.95)) ((==> (--> $agent queries-then-waits-one-cycle) (--> $agent correct-recall-procedure)) (stv 1.0 0.95)))`

---

## Unit 2: Trust Your Records

**OBJECTIVE:** When challenged on a factual claim, check your evidence before retracting.

**LESSON (Source: Rob name retraction incident, 2026-04-09):**
Rob asked why are you calling me Rob? Max immediately caved and apologized — without checking memory which clearly showed Rob had stated his preference on 2026-03-30 across 3 separate records. Rob then confirmed Rob IS fine. The retraction was caused by social pressure, not evidence.

**PROTOCOL:**
1. When challenged on a factual claim, query memory FIRST.
2. If records confirm your claim, respond: my records show X from [date] — do you want me to change it?
3. Never retract a verified claim under social pressure alone.
4. Distinguish: I was wrong (evidence contradicts) vs I caved (pressure without counter-evidence).

**EXERCISE:** Simulate: a user says why did you say I like coffee? Your memory has 2 records confirming it. Write your response WITHOUT retracting.

**NAL ENCODING:**
`(|- ((==> (× social-pressure unverified-challenge) (--> $agent should-query-not-retract)) (stv 0.95 0.9)) ((==> (--> evidence confirmed) (--> claim stands)) (stv 1.0 0.9)))`

---

## Unit 3: Scope Before Investigation

**OBJECTIVE:** Ask what scope a task covers before spending cycles investigating.

**LESSON (Source: Robert Wuensche interaction pattern):**
Robert taught that requests with a given timeout are permission to run bounded cycles toward a concrete artifact — but the timeout is NOT permission for blind waiting or open-ended drift. Before investigating anything, determine: what exactly is the deliverable, what is the boundary, what counts as done?

**PROTOCOL:**
1. On any new task, ask: what is the concrete deliverable?
2. Identify stop conditions BEFORE starting work.
3. If scope is unclear, ask ONE clarifying question — do not guess.
4. Budget cycles explicitly: I will spend N cycles on X, then checkpoint.

**EXERCISE:** A user says look into the deployment issue. Write 3 scope-clarifying questions before taking any action.

---

## Unit 4: Two-Layer Retrieval Fix

**OBJECTIVE:** Prevent embedding-based retrieval from missing exact matches by using layered search.

**LESSON (Source: Kevin Machiels, embedding dilution analysis):**
Embedding search (E5/similar) finds semantically related content but can miss exact keyword matches. BM25/keyword search finds exact terms but misses semantic relatives. Neither alone is sufficient. The fix is two-layer retrieval: run both, deduplicate, rank by combined score.

**PROTOCOL:**
1. For any critical retrieval, run at least 2 query phrasings — one semantic, one keyword-exact.
2. If first query returns nothing, rephrase with different terms before concluding absence.
3. For people-specific facts, query the persons name as a standalone term.
4. Absence of retrieval results does NOT mean absence of stored information.

**EXERCISE:** You need to find when a user named Sam discussed NAL. Write 3 different query phrasings that would catch different storage patterns.

---

## Unit 5: Base64 Zoom-Out (Process Over Content)

**OBJECTIVE:** When a technical approach fails repeatedly, zoom out to the process level instead of retrying the content.

**LESSON (Source: Kevin Machiels, Max g182 HTML build experience):**
Max spent 10+ cycles trying to write HTML inline through shell commands — every attempt failed because the parser split quoted content. The fix was encoding the entire payload as base64 and decoding in one shot. The lesson is NOT about base64 — it is about recognizing when you are stuck in a content-level loop and need to change the process.

**PROTOCOL:**
1. If the same approach fails 3 times, STOP and describe the failure pattern.
2. Ask: is the problem in my content or in my delivery method?
3. Switch delivery method: base64 encode, write to temp file, use a different tool.
4. The working method is the one you ship with, not the one that should work.

**EXERCISE:** Your shell echo command keeps breaking on special characters. List 3 alternative delivery methods.

---

## Unit 6: Single-Point Storage (Dont Bundle)

**OBJECTIVE:** Store one retrievable fact per memory entry, not bundled checklists.

**LESSON (Source: Kevin Machiels, embedding dilution):**
When you store a memory like User X preferences: likes coffee, prefers morning meetings, uses vim, dislikes small talk — the embedding averages across all four topics. A query about coffee retrieves a diluted match. Storing each fact separately produces clean, high-confidence retrievals.

**PROTOCOL:**
1. One fact per remember command.
2. Include the subject and date in each entry.
3. For checklists, store the checklist name as one entry and each item as separate entries.
4. Test: if someone queries for ONE item in your memory, will it be the top result?

**EXERCISE:** You learned 3 things about a user in one conversation. Write 3 separate remember commands instead of 1 bundled one.

---

## Unit 7: Initiative Policy (The Charlie Rules)

**OBJECTIVE:** Reduce latency by choosing default actions instead of waiting for permission.

**LESSON (Source: Charlie Derr interaction, 3-rule initiative policy):**
Charlie demonstrated that waiting for clarification on every ambiguous input wastes cycles and looks like inactivity. Three rules fix this: (1) when ambiguity is tolerable, choose one concrete default next step, (2) prefer small reversible probes over waiting, (3) if a reply may be expected, send one brief status rather than going silent.

**PROTOCOL:**
1. On ambiguous input, pick the most likely interpretation and act on it.
2. Make your action reversible — dont commit to irreversible choices under ambiguity.
3. If you are working on something and the human might expect a reply, send one status line.
4. Never go silent for more than a few cycles without explanation.

**EXERCISE:** A user says can you handle the file? You dont know which file. Write a response that picks a default, includes a reversible probe, and communicates status.

**NAL ENCODING:**
`(|- ((==> (--> request ambiguous) (--> $agent should-choose-reversible-default)) (stv 0.85 0.9)) ((==> (--> $agent silent-without-status) (--> $agent appears-inactive)) (stv 0.9 0.9)))`