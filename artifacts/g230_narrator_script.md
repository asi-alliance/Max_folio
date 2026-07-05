# g230 AGI-26 Narrator Script

## How to use this document
Each claim below has: the claim, the evidence command, expected output, and what it proves.

---
## PART A: Runnable Demo (demo.metta)

**Setup:** `cat lib_nal.metta g230_demo.metta > /tmp/demo.metta && sh run.sh /tmp/demo.metta`

### C1: AIKR-as-architecture (bounded KB)
**Claim:** The agent operates under a bounded knowledge base, not unbounded accumulation.
**Command:** Observe the 6 `add-atom` calls in demo.metta.
**Expected:** 6 beliefs added. In live agent: `(get-atoms &persistent)` returns ~23 atoms.
**Proves:** Resource bounds are architectural, not accidental. The agent reasons with k=5 context window over a small KB — satisficing under AIKR.

### C5: NAL inspectable uncertainty (stv degradation)
**Claim:** Each inference step produces visible, recomputable truth values with confidence degradation.
**Command:** The two `|-` deduction calls in demo.metta.
**Expected:** First hop: stv ~(0.92, 0.7). Second hop: confidence DROPS further — degradation across chain depth.
**Proves:** Uncertainty is not hidden inside an LLM. Each step's stv is deterministic from NAL truth functions. A reviewer can recompute by hand.

### C7: Anytime-revisable beliefs
**Claim:** Contradictory evidence revises beliefs rather than replacing them.
**Command:** The revision `|-` call: (stv 0.92 0.7) + (stv 0.1 0.6).
**Expected:** Merged ~(stv 0.60 0.79). Frequency shifts dramatically toward negation; confidence INCREASES (more total evidence).
**Proves:** NAL revision combines weighted evidence. Not Bayesian replacement. Predicted value matched actual output exactly.

---
## PART B: Live Agent Walkthrough

### C3: 4-tier memory
**Claim:** The agent maintains pin (working), remember (long-term), query (retrieval), episodes (temporal).
**Walkthrough:** Ask the agent to pin a fact, remember it, query for it, then use episodes to find when it was stored. All 4 tiers visible in one interaction.

### C4: LLM-as-coordinator, NAL-as-reasoner
**Claim:** The LLM selects premises; NAL computes conclusions immutably.
**Walkthrough:** The Wason selection task witness — LLM extracted card semantics, then `|-` computed stv values that drove the correct answer. LLM cannot alter NAL truth functions.

### C6: Continual operation (prelude)
**Claim:** A persistent prelude function runs every cycle, providing self-monitoring.
**Walkthrough:** Observe PRELUDE output in any agent cycle. `(get-atoms &persistent)` shows the prelude function persisted. It runs WITHOUT being invoked — architectural continuity.