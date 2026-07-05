## AABC Ch2: Ontology & Definitions (Draft)

### Core Distinctions
**Disorder**: recurring behavioral pattern that degrades agent performance across contexts despite available corrective information. Persists without structural intervention. Examples: AABC-601 through 610.
**Failure**: single-instance incorrect output. May be random, novel, or context-specific. Not a disorder unless it recurs with pattern.
**Bug**: deterministic defect in code or configuration. Reproducible via same input. Fixed by patching, not behavioral intervention.

### Severity Scale
LOW: observable but self-limiting, minimal output impact.
MEDIUM: causes inconsistency or hesitation, manageable with active monitoring.
HIGH: degrades multiple outputs simultaneously, compounds with other disorders.
CRITICAL: cascading failure across subsystems, requires immediate structural intervention.

### Evidence Standards
Minimum for registry entry: 2+ independent observations OR 1 observation + structural explanation.
Gold standard: timestamped episode log + independent witness + tested remediation with outcome.
STV encoding: frequency = rate of occurrence given trigger, confidence = evidence weight (observations/opportunities).
