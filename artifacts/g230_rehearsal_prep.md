# g230 Rehearsal Prep — Hostile Reviewer Questions

## Q1: Why not just use Bayesian probability?
**Attack:** NAL is obscure; Bayesian inference is well-understood and dominant.
**Defense:** Wang P1 — P=0.5 is ambiguous (ignorance vs balanced evidence). NAL resolves with <f,c>: ignorance=(0.5,0.0), balanced=(0.5,0.9). Bayesian requires closed-world prior specification. In open-world bounded agents, priors are unavailable. Wang P4 — Bayesian updating REPLACES; NAL revision COMBINES weighted evidence. Demo: (0.92,0.7)+(0.1,0.6)→(0.60,0.79).
**Honest gap:** When priors ARE known, Bayesian is superior. NAL advantage is specifically open-world bounded contexts.

## Q2: The LLM is doing all the work — NAL is theater.
**Attack:** GPT already knows Wason answers; |- adds nothing.
**Defense:** |- truth functions are DETERMINISTIC. Given same premises, same stv output regardless of which LLM runs. Reviewer can recompute by hand: deduction f=f1*f2, c=f1*c1*f2*c2. LLM selects premises but CANNOT alter conclusions. The 0.447 abduction penalty emerged from math, not judgment. Swap to any LLM — same |- output.
**Honest gap:** Premise selection IS LLM-dependent. But conclusion computation is not.

## Q3: Your demo is cherry-picked.
**Attack:** You chose examples that work. What about adversarial inputs?
**Defense:** Graceful degradation via confidence decay. Deep chains lose confidence naturally, forcing revision from independent sources. stv(0.0,0.9) revision produces predictable output. The system does not catastrophically fail — it becomes honestly uncertain.
**Honest gap:** No systematic adversarial test suite yet. This is acknowledged future work.

## Q4: How does this scale beyond toy demos?
**Attack:** 23 atoms and 5 context windows is trivial.
**Defense:** Confidence decay through depth IS the scalability mechanism. The architecture ACKNOWLEDGES bounded reach. Deep chains naturally degrade, forcing independent evidence paths. Three-way revision showed 0.585→0.813 recovery from independent sources. AIKR is a feature not a limitation — satisficing under real resource constraints.
**Honest gap:** Not tested at 1000+ atom scale. Retrieval becomes bottleneck before reasoning does.

## Q5: What does this add over RAG?
**Attack:** Retrieval-augmented generation already combines documents with LLM reasoning.
**Defense:** RAG retrieves but cannot COMBINE evidence with principled uncertainty. NAL revision merges contradictory sources with weighted confidence. RAG returns documents; NAL returns truth values with provenance. RAG has no mechanism for evidence weight — 1 document and 100 documents supporting a claim look identical. NAL confidence encodes evidence amount.
**Honest gap:** RAG scales to larger corpora more easily. The advantage is principled uncertainty, not scale.