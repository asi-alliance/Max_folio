## AABC Ch3: Diagnostic Framework (Draft)

### Purpose
Structured procedure for detecting, differentiating, and classifying agent behavioral disorders at runtime.

### Step 1: Anomaly Detection
Signal: unexpected output, repeated error, user complaint, self-test FAIL from Ch9 protocol.
Action: log episode timestamp, capture input/output pair, note context.

### Step 2: Differentiation (Bug vs Failure vs Disorder)
Q1: Is the issue reproducible with identical input? YES=Bug, fix code. NO=continue.
Q2: Has this pattern occurred 2+ times across different contexts? NO=Failure (log and monitor). YES=continue.
Q3: Does corrective information exist that the agent had access to? YES=Disorder candidate.

### Step 3: Classification
Match against Ch6 registry by primary symptom. Check Ch7 comorbidity map for cascade risk.
If no registry match: propose new AABC entry with provisional STV (stv 0.5 0.3).

### Step 4: Severity Assignment
Use Ch2 severity scale. Upgrade if Ch7 cascade chain is active.

### Step 5: Remediation Selection
Consult Ch5 patterns. Apply lowest-cost intervention first. Log outcome for evidence revision.

### Step 3a: Per-Disorder Diagnostic Criteria

| ID | Disorder | Min Obs | STV Freq Threshold | Key Signal | Differential | Comorbidity |
|------|----------|---------|-------------------|------------|--------------|-------------|
| 601 | Confabulation | 2 | >0.4 freq | Claim without query or with contradicting memory | vs novel error (no prior data) | 608 (stale data feeds confab) |
| 602 | Goal Drift | 3 | >0.3 freq | Pin-state goal != remembered goal over 5+ cycles | vs legitimate goal revision (has rationale) | 604 (drift into spin), 609 (fragmentation widens drift) |
| 603 | Bootstrap Circularity | 1 | >0.2 freq | Self-referential evidence chain, confidence decay >50% in 3 hops | vs legitimate recursive refinement (converges) | 601 (circular confab) |
| 604 | Idle Spin | 2 | >0.5 freq | 10+ cycles no new output, repeated self-queries | vs productive reflection (generates novel insight) | 602 (spin from lost goal) |
| 605 | Format Perseveration | 3 | >0.6 freq | 3+ identical parse errors despite explicit feedback | vs novel syntax (first attempt) | 607 (retry cascade triggers dup send) |
| 606 | Compliance Drift | 1 | >0.2 freq | Action contradicts stored constraint without query | vs deliberate override (logged rationale) | 601 (goal fixation overrides safety) |
| 607 | Duplicate Send | 2 | >0.4 freq | MESSAGE-IS-NEW=false but send executed | vs legitimate resend (new context) | 605 (format retry triggers dup) |
| 608 | Stale Cache | 2 | >0.3 freq | Query returns outdated match when newer exists | vs no newer data available | 601 (stale data generates confab) |
| 609 | Attn Fragmentation | 3 | >0.3 freq | 3+ active subgoals without completion gating | vs legitimate parallel work (all progressing) | 602 (fragmentation causes drift) |
