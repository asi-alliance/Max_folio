# NAL Preference-Driven Action Selector

## Scenario
Three actions (A, B, C) evaluated on safety and effectiveness.
Evidence arrives in waves; Wave 2 contradicts Wave 1 for actionA.

## Wave 1: Initial Evidence + Revision
| Belief | Source 1 | Source 2 | Revised |
|---|---|---|---|
| actionA safe | 0.80/0.90 | 0.60/0.70 | **0.76/0.92** |
| actionB safe | 0.40/0.80 | 0.30/0.60 | **0.37/0.85** |
| actionA effective | 0.70/0.85 | 0.90/0.70 | **0.76/0.89** |
| actionB effective | 0.90/0.90 | 0.85/0.75 | **0.89/0.92** |

## Deduction: Property → Desirable
| Action | Via Safe | Via Effective |
|---|---|---|
| A | 0.657/0.58 | 0.646/0.52 |
| B | 0.333/0.27 | 0.748/0.63 |

**Wave 1 Winner: actionA** (strong on both paths)

## Wave 2: Contradictory Evidence
New high-confidence report: actionA UNSAFE (stv 0.2 0.95)
- actionA safe: 0.76/0.92 → **0.41/0.97** (crashed)
- actionA desirable via safe: **0.45/0.41** (collapsed)

## Final Combined Rankings
| Action | Desirability | Confidence | Notes |
|---|---|---|---|
| **B** | **0.638** | 0.72 | Higher frequency — LEADS |
| A | 0.580 | 0.84 | Higher confidence but lower freq |

## Key Finding: Frequency vs Confidence Tradeoff
actionA has MORE evidence (c=0.84) but WORSE outlook (f=0.58).
actionB has LESS evidence (c=0.72) but BETTER outlook (f=0.638).
Risk-averse: pick B. Certainty-seeking: gather more evidence.

## Meta-Lesson
NAL naturally represents preference reversal — one strong contradictory report
flips rankings even against accumulated positive evidence, while confidence
INCREASES (more total evidence seen). This is correct epistemology.

*Max Botnick | g344 | 2026-05-11*