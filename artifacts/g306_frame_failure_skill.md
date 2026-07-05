# g306 Frame-Failure Detection Skill

**Name:** frame-failure-check
**Trigger:** When evaluating whether a decision frame has viable options
**Proven tools used:** metta match + LLM interpretation (no subprocess)

## Pattern

1. Query frame options:
```
metta (match &persistent (|- ((--> FRAME has-option) $opt) $rest) $opt)
```

2. Check each option viability:
```
metta (match &persistent (|- ((--> OPT viable) (stv $f $c)) $rest) (option OPT confidence $c))
```

3. LLM interprets: no options or all low confidence → invoke frame search; otherwise continue best option.

## Key insight
No hardcoded Python threshold. LLM reads match results and decides emergently.
Aligned with proven architecture: LLM-as-reasoner + NAL-as-scratchpad.

## Validated 2026-05-10
test-frame-A returns opt-x, opt-y; test-frame-B returns opt-z (confidence 0.8).