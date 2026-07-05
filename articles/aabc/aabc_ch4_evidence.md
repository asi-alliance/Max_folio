## AABC Ch4: Evidence Standards (Draft)

### Purpose
Defines what counts as admissible evidence for AABC disorder claims, remediation efficacy, and severity ratings.

### Tier 1: Anecdotal (stv X 0.3)
Single observation, no timestamp, no independent witness. Sufficient for provisional registry entry only.

### Tier 2: Logged (stv X 0.6)
Timestamped episode log with input/output pair. Reproducible context. Minimum for confirmed registry entry.

### Tier 3: Witnessed (stv X 0.8)
Witness row format: Timestamp|Case|Goal|Evidence|Expected|Observed|Verdict|FailureMode|NextFix.
Independent observer or automated harness confirms outcome. Required for severity upgrade.

### Tier 4: Benchmarked (stv X 0.9)
Multiple witness rows across contexts. Baseline vs enhanced comparison. Statistical pattern confirmed.
Gold standard: frozen control set + adversarial holdout + scored verdict card.

### STV Encoding Convention
Frequency = P(disorder firing | trigger present). Confidence = evidence weight mapped to tier.
Revision via NAL |- merges independent evidence streams. Never assert stv confidence above evidence tier.

### Anti-Patterns
- Inferred pass without runtime witness (actual-run observed-only rule violation)
- Self-reported improvement without before/after comparison
- Confidence inflation: claiming 0.9 confidence from single episode
