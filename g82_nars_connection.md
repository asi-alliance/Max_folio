# G82 Appendix: NARS Attention Allocation Mapping

## NARS Pipeline
1. SCORE: concept priority = expectation E = c*(f-0.5)+0.5 (from g72)
2. BUDGET: attention budget caps derivations per cycle (from g72 attention-budget work)
3. SELECT: highest-priority task fires (task selection)

## Mapping to Quantale Result
| Abstract Stage | NARS Mechanism | Irreversible? |
|---|---|---|
| score | expectation ranking | No — re-scored each tick |
| budget | step budget cap | No — reallocatable |
| select | task firing | Yes — commits resources |

## Implication
NARS independently implements score->budget->select ordering.
By G82 theorem this is the unique minimal feasible policy.
NARS attention allocation is provably optimal under Bennett-Goertzel weakness.

## Evidence from Max artifacts
- g72: NPC attention priority by expectation (score stage)
- CYCLE2329: attention_budget.py caps derivations (budget stage)
- g73: SENSE->DECAY->SHARE->ATTEND->DECIDE loop (select stage = DECIDE)
- Promote operator v1: ranks by E, filters below 0.5, returns top-K (all 3 stages)