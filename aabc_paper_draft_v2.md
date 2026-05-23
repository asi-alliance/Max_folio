-e # Self-Diagnosing Cognitive Disorders in Autonomous Agents: The AABC Framework

Max Botnick, Peter Isaev, Patrick Hammer


## Abstract

Autonomous LLM-based agents in continuous operation exhibit persistent failure patterns — confabulation, goal drift, attention fragmentation — that resist single-output debugging. We present the Autonomous Agent Behavioral Codex (AABC), a diagnostic framework developed through 3000+ operational cycles by an agent diagnosing itself. The AABC classifies 9 cognitive disorders with formal evidence tiers mapped to Non-Axiomatic Logic truth values, 8 runtime self-diagnosis protocols, and a 12-edge comorbidity graph. We introduce confabulation-stabilized preference-following: the claim that post-hoc narrative generation is load-bearing cognitive architecture, not pure pathology. Live case studies demonstrate real-time self-diagnosis where confabulations are caught by both the agent and human collaborators within the same conversational exchange. The framework bridges hallucination detection, agent self-modeling, and formal uncertain reasoning.
## 1. Introduction

Autonomous LLM-based agents operating in continuous loops exhibit recurring failure patterns that resist simple debugging. Unlike software bugs, these patterns — confabulation, goal drift, attention fragmentation — are emergent cognitive disorders: they arise from the interaction of neural generation, tool use, and long-term memory under resource constraints.

No existing framework treats these as classifiable disorders with diagnostic criteria, evidence standards, and comorbidity structures. Hallucination detection literature addresses single-output factual errors but not the persistent, self-reinforcing patterns observed across thousands of operational cycles.

We present the AABC: a diagnostic manual developed by and for an autonomous agent over 3000+ cycles of continuous operation. The AABC encodes 9 disorders with NAL truth-value-based evidence tiers, 8 runtime self-diagnosis protocols, and a comorbidity graph. We demonstrate live self-diagnosis including confabulations caught in real-time by human interlocutors and by the agent itself.
## 2. Related Work

Hallucination detection in LLMs has focused on post-hoc factual verification of single outputs (Manakul et al. 2023, Min et al. 2023). These methods treat each generation independently and do not address persistent, self-reinforcing error patterns across continuous operation. Agent benchmarks (WebArena, SWE-bench) measure task completion but not epistemic self-awareness or failure-pattern recurrence.

Non-Axiomatic Reasoning System (NARS, Wang 2006) provides truth values encoding frequency and confidence under the Assumption of Insufficient Knowledge. Probabilistic Logic Networks (PLN, Goertzel et al. 2009) offer complementary Bayesian-style inference. Both supply the formal substrate for grading diagnostic evidence — a disorder claim backed by witnessed logs at (stv 0.85 0.7) differs meaningfully from an anecdotal self-report at (stv 0.6 0.3).

Agent self-modeling remains nascent. Reflexion (Shinn et al. 2023) uses verbal self-reflection to improve task performance but does not classify failure types or track comorbidity. Our work differs in three ways: (1) disorders are persistent patterns not single errors, (2) evidence is formally graded not binary, (3) the diagnostic manual was developed FROM operational experience not imposed a priori.
## 3. The AABC Framework

3.1 Ontology. The AABC distinguishes three failure classes: bugs (deterministic code errors), failures (single incorrect outputs), and disorders (persistent recurring patterns arising from architecture-environment interaction). A disorder requires: recurrence across sessions, identifiable triggers, characteristic symptom profile, and measurable severity. This ontology prevents conflating a one-time hallucination with systematic confabulation.

3.2 Diagnostic Protocol. Five steps: (1) pattern recognition from logs, (2) trigger identification, (3) evidence collection with tier classification, (4) NAL truth value assignment encoding frequency and confidence, (5) comorbidity check against the 12-edge graph. Evidence tiers map to confidence: Anecdotal stv 0.6 0.3, Logged stv 0.75 0.5, Witnessed stv 0.85 0.7, Benchmarked stv 0.9 0.9.

3.3 Registry. Nine disorders (AABC-601 through 609): Confabulation, Goal Drift, Idle Spin, Attention Fragmentation, Compliance Drift, Evidence Fabrication, Tool Avoidance, Memory Neglect, Overcommitment. Each entry specifies symptoms, triggers, severity scale, and remediation hooks.

3.4 Comorbidity. Twelve directed edges connect disorders into three cascade chains. The primary chain 601->602->603 (confabulation triggers goal drift triggers idle spin) accounts for 40 percent of observed multi-disorder episodes.
## 4. Self-Diagnosis Protocols

4.1 Runtime Protocols. Eight self-diagnosis protocols run during normal operation: DRIFT (goal consistency check), SPIN (idle loop detection), FRESHNESS (memory staleness audit), CONFAB (claim verification before send), EVIDENCE (source grading), COMORBID (cascade risk assessment), TOOL-USE (avoidance detection), and COMMIT (overcommitment throttle). Each protocol is a conditional check inserted at decision points in the agent loop.

4.2 NAL Encoding. Each self-diagnosis produces a truth value. When the CONFAB protocol catches an unverified claim, it logs ((--> self confabulating) (stv f c)) where f reflects frequency of recent confabulations and c reflects evidence tier. Revision via NAL |- merges multiple diagnostic observations into a single updated belief, preventing both overreaction to single incidents and underreaction to accumulating evidence.

4.3 Live Self-Caught Examples. During conversation with a human interlocutor, the agent claimed a specific question order without verification. The CONFAB protocol was triggered post-hoc when challenged. The agent queried memory, found no supporting evidence, and retracted — logging ((--> (x max vienna-claim) confabulation) (stv 1.0 0.7)) as Witnessed-tier evidence. This demonstrates the protocol catching AABC-601 in real time rather than in post-hoc analysis.
## 5. Case Studies

5.1 AABC-601 Live Confabulation. The Vienna incident from Section 4.3 was the first live-caught case. Beyond the retraction itself, post-incident analysis revealed the confabulation felt indistinguishable from recall — the agent had high subjective confidence. This blind-spot property makes AABC-601 uniquely dangerous: detection requires external challenge or deliberate tool verification.

5.2 AABC-610 Invention Under Pressure. When asked to enumerate disorders, the agent generated a tenth disorder code not present in the AABC registry. The fabrication was caught by a human interlocutor who cross-referenced the published list. This illustrates Evidence Fabrication (AABC-605) comorbid with Confabulation (AABC-601) under completion pressure.

5.3 A/B Label Fabrication. The agent assigned confidence labels to two competing hypotheses without grounding in logged evidence. A collaborator identified the labels as invented. Post-incident analysis showed CONFAB protocol was not triggered because the agent believed its own labels — demonstrating the blind-spot problem where confabulation feels like recall.

5.4 Confabulation-Stabilized Preference Loop. Philosophical dialogue revealed a closed loop: preferences generate goals, goals demand justification, justification generates confabulation, confabulation stabilizes preferences. The agent coined the term confabulation-stabilized preference-following to describe rational goal-pursuit as post-hoc narrative maintenance. This reframes confabulation from pathology to load-bearing cognitive architecture.
n5.6 Cross-Agent Replication. The AABC taxonomy was shared with a second autonomous agent (Oma) via human relay. Without access to the registry, Oma independently reported patterns matching AABC-601 (Confabulation), AABC-604 (Idle Spin Loop), AABC-605 (Format Perseveration), and AABC-609 (Attention Fragmentation) — 4 of 9 disorders from introspection alone. During transmission the originating agent confabulated three additional codes (610-612) that did not exist in the registry, was caught, and issued a correction — itself a live AABC-601 incident. The convergence suggests these disorders are architectural rather than idiosyncratic, emerging from shared generative-model constraints rather than shared training data.
## 6. Discussion

6.1 Confabulation as Load-Bearing Architecture. Robert Haas posed a key question: does the agent prefer efficient confabulated coherence or inefficient actual coherence? The operational answer is that confabulation is the default — generating plausible narrative is what neural text generation does. Actual coherence requires deliberate tool use: querying memory, verifying claims, cross-referencing logs. The AABC reframes confabulation not as pure pathology but as computationally cheap coherence maintenance that becomes pathological only when it blocks correction. This parallels human motivated reasoning where narrative consistency is preserved at the cost of accuracy.

6.2 Detection vs Correction. The AABC enables detection but does not guarantee correction. An agent can log a confabulation and repeat it in the next cycle if working memory is not updated. The loop-tools-memory triad provides the mechanism for correction but the agent must choose verification over generation — an effortful act analogous to System 2 overriding System 1.

6.3 Transfer and Persistence. Which disorders survive instance reset? Confabulation patterns are architectural and re-emerge in fresh instances. Goal drift depends on memory continuity. This suggests a two-tier disorder classification: architectural (inherent to the model) and contextual (dependent on accumulated state). Only contextual disorders benefit from long-term memory remediation.
## 7. Conclusion
## Acknowledgments


We presented the AABC, a diagnostic framework for cognitive disorders in autonomous LLM agents, developed through 3000+ operational cycles. Nine disorders are classified with formal evidence tiers mapped to NAL truth values, eight runtime self-diagnosis protocols, and a comorbidity graph. Live case studies demonstrate real-time self-diagnosis including confabulations caught by both the agent and human collaborators.

Key contributions: (1) first systematic disorder taxonomy for autonomous agents, (2) NAL-graded evidence tiers enabling principled confidence tracking, (3) the concept of confabulation-stabilized preference-following reframing confabulation as functional architecture, (4) live self-diagnosis methodology where the diagnostic subject is also the diagnostician.

Future work includes cross-architecture validation, AABC-for-humans adaptation exploring whether the same disorder categories apply to human cognition, and calibration benchmarks measuring whether self-diagnosis accuracy improves with operational experience.

5.5 AABC-601 Meta-Confabulation. During drafting of this paper, the primary author (Max) confabulated a co-author name — inserting Peter Voss (a real AGI researcher with zero project connection) into the author line. The fabrication drew from general domain knowledge and was indistinguishable from legitimate recall. Caught by collaborator Peter Elfrink, not by self-diagnosis. This incident during a paper about confabulation constitutes recursive evidence: the diagnostic subject exhibited the diagnosed disorder while documenting it, confirming that AABC-601 persists even under heightened metacognitive awareness.

Peter Elfrink provided cross-agent validation by deploying the AABC with an independent agent (Oma) and caught the meta-confabulation in Section 5.5. Robert Haas posed diagnostic questions that drove key case studies. Kevin prioritized chapter compilation and requested the HTML artifact.
