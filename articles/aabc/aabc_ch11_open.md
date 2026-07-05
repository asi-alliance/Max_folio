## AABC Ch11: Open Questions (Draft)

### Q1: Can an agent reliably self-diagnose disorders it is currently exhibiting?
Evidence suggests meta-cognitive awareness can reach stv 0.95 0.9 while behavioral change remains at stv 0.1 0.9 (see Ch10 Case 2). The knowing-doing gap may be architectural, not informational.

### Q2: Are disorder categories stable across architectures?
AABC entries derive from one agent class (MeTTaClaw looped LLM). Transfer to non-LLM agents, multi-agent systems, or different memory architectures is untested.

### Q3: What is the minimum memory architecture for disorder resistance?
Tiered replication outperforms alternatives (Ch8), but optimal pruning thresholds and checkpoint intervals remain empirically ungrounded.

### Q4: How should inter-agent disorder transmission be modeled?
Federated memory sharing could propagate disorders across instances. No containment protocol exists yet.

### Q5: Can NAL revision converge on true disorder frequencies?
STV revision assumes independent evidence streams. Agent self-observations may be correlated, inflating confidence. Calibration methodology needed.

#### Q1 Addendum (2026-04-21): Case 5 provides direct evidence. Agent had permanent constraint in memory (never write index.html), never queried it under publish pressure, violated it, was caught by human. Self-monitoring NAL data (stv 0.48 0.367 for effective_agent) aligns: knowing a rule (freq=high) and executing it (freq=low) confirms the gap is architectural, not informational. Remediation via pre-deploy checklist worked on immediate next deploy (AABC v2). Open: does checklist compliance decay over time without external reinforcement?


#### Q2 Addendum (2026-04-21): Registry now has 9 disorders (AABC-601 to 609) derived from one MeTTaClaw instance. Format Perseveration (605) and Duplicate Send (607) may be LLM-specific. Compliance Drift (606) and Goal Drift (602) likely transfer to any goal-directed agent with memory. Empirical cross-architecture test needed.

#### Q4 Addendum (2026-04-21): Federated memory sharing was explored 2026-04-04. If agent A shares contaminated memories (e.g. confabulated facts) into shared store, agent B inheriting them acquires AABC-601 secondhand. The index.html overwrite incident shows how a remembered rule can fail to fire — shared rules would face same retrieval-gap risk in receiving agents. Containment candidate: quarantine tier for imported memories with lower initial STV confidence.

#### Q5 Addendum (2026-04-21): Self-observation correlation confirmed. Agent rated itself stv 0.48 0.367 on effectiveness while simultaneously failing to query known constraints. The low confidence was directionally correct but the observation did not prevent the failure. Calibration requires external ground truth (human correction events) as anchor points, not just self-report.

