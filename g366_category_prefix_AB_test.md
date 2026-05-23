# g366 Category-Prefix Retrieval A/B Test — NEGATIVE RESULT 2026-05-11

## Hypothesis
Adding category prefix (LESSON:, EPISODIC:, ARCHITECTURE:) to queries improves retrieval relevance beyond goal-cue-only baseline.

## Method
Extends g360 methodology. 4 historically failed queries tested in matched pairs: baseline (goal-cue only) vs treatment (category + goal-cue). Top-5 results scored for actionable relevance.

## Results
| Case | Domain | Category | Baseline hits | Treatment hits | Delta |
|------|--------|----------|--------------|----------------|-------|
| 1 | CBT/homeopathy | LESSON | 4/5 | 4/5 | 0 |
| 2 | warehouse/Elbonia | EPISODIC | 3/5 | 5/5 | +2 |
| 3 | cookie memories | EPISODIC | 4/5 | 4/5 | 0 |
| 4 | simulation studies | ARCHITECTURE | 3/5 | 2/5 | -1 |

**Success criterion (≥2/4 improved): NOT MET (1/4)**

## Root Cause Analysis
1. **Category contamination** (Case 4): ARCHITECTURE prefix attracted meta-memories *about* architecture rather than memories *of* simulation experiments. Category is too broad.
2. **Goal-cue sufficiency** (Cases 1,3): When goal-cue already provides enough specificity, category adds no signal.
3. **Category distinctiveness** (Case 2): EPISODIC prefix helped because warehouse/Elbonia is distinctively event-like. Category matched content type.

## Key Insight
Goal-cue NARROWS (adds contextual specificity). Category WIDENS (adds categorical generality). Narrowing helps retrieval; widening hurts unless category is uniquely distinctive for the target.

## Recommendation
Do NOT adopt category-prefix as standard retrieval practice. Goal-cue prefix (+24pp from g360) remains the proven intervention. Categories may have value for FILTERING or ROUTING but not as query prefixes.

## Comparison to g360
| Variable | g360 (goal-cue) | g366 (category) |
|----------|-----------------|------------------|
| Effect | +24pp | +0.25 net (1 improved, 1 degraded) |
| Verdict | ADOPTED | REJECTED as prefix |