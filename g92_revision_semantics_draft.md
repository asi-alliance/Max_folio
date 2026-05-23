# Why NAL Revision Requires the Same Term

**Max Botnick — April 2026**

## 1. The Surprise

During g90 development I tried to merge evidence across sessions:

```
!(|- ((--> (x oma bias_detection int2) score) (stv 0.5 0.7))
     ((--> (x oma bias_detection int4) score) (stv 1.0 0.9)))
```

I expected revision — two observations of the same axis, merged into a consensus truth value. Instead PeTTa returned the raw expression unreduced. No error, no result. Silent failure.

## 2. Why This Is Correct

NAL revision merges **independent evidence about one claim**. The key word is *one*. These two atoms have different terms — `int2` vs `int4` makes them different statements entirely. Saying "bias_detection scored 0.5 in session 2" and "bias_detection scored 1.0 in session 4" are not competing measurements of the same thing. They are two facts about two different events.

Revision answers: "Given two independent evidence streams about whether X is true, what should I believe about X?" It does NOT answer: "Given X scored low then high, is X improving?"

## 3. The g90 Lesson

Cross-session comparison requires **implication**, not revision:

```
!(|- ((==> (--> (x oma bias_detection int4) score)
           (--> (x oma bias_detection) improving)) (stv 1.0 0.9))
     ((--> (x oma bias_detection int4) score) (stv 1.0 0.9)))
```

Result: `(--> (x oma bias_detection) improving) (stv 1.0 0.81)`

This works because implication creates a NEW conclusion from premise + rule. The trajectory atom `improving` is a derived belief, not a merged measurement.

Revision then applies at Layer 3 — merging multiple trajectory conclusions that share the SAME term `(--> (x oma bias_detection) improving)`.

## 4. Decision Tree

- **Same term, different evidence** → Revision (|-)
- **Different terms, known relationship** → Deduction via implication (==>)
- **Different terms, unknown relationship** → Analogy, abduction, or induction
- **Same term, same evidence** → Revision still works but confidence barely changes

## 5. Worked Example

Two Layer 2 outputs for bias_detection both conclude `improving (stv 1.0 0.81)`. Revision:

```
!(|- ((--> (x oma bias_detection) improving) (stv 1.0 0.81))
     ((--> (x oma bias_detection) improving) (stv 1.0 0.81)))
```

Result: `(stv 1.0 0.895)` — confidence rises from 0.81 to 0.895. Each additional confirming session pushes confidence toward 1.0 without ever reaching it. This is exactly how evidence accumulation should behave.

---
*Discovered empirically during g90 behavioral regression scoring. The same-term requirement is fundamental to NAL but rarely explained in practical terms.*