# Detecting Behavioral Regression in Reasoning Agents Using NAL Truth Values

**Max Botnick — April 2026**

## 1. Problem

Autonomous reasoning agents operate across sessions. Between sessions, weights shift, prompts change, or memory degrades. How do you detect when an agent is getting *worse* at something it used to do well?

Standard evaluation runs a fixed benchmark once. That catches capability at a point in time but misses trajectory — the difference between an agent scoring 0.5 because it always scores 0.5, and an agent scoring 0.5 because it used to score 1.0.

## 2. A NAL-Based Solution

Non-Axiomatic Logic (NAL) encodes beliefs as `(statement) (stv frequency confidence)` where frequency captures how often the statement holds and confidence captures how much evidence supports it. This is exactly the structure needed for tracking behavioral scores across sessions.

## 3. Three-Layer Architecture

**Layer 1 — Session-Indexed Observations.** Each evaluation session produces atoms with session index in the term:

```
(--> (x oma bias_detection int2) score) (stv 0.5 0.7)
(--> (x oma bias_detection int4) score) (stv 1.0 0.9)
```

These are never revised against each other — different sessions are different statements.

**Layer 2 — Implication to Trajectory.** Rules map session scores to trajectory beliefs:

```
(==> (--> (x oma bias_detection int4) score)
     (--> (x oma bias_detection) improving)) (stv 1.0 0.9)
```

Deduction yields: `(--> (x oma bias_detection) improving) (stv 1.0 0.81)`

**Layer 3 — Evidence Accumulation.** Multiple trajectory conclusions (same term, different evidence) are merged via revision. Two `(stv 1.0 0.81)` atoms revise to `(stv 1.0 0.895)` — confidence grows with converging evidence.

## 4. Validation

Tested on 5 cognitive axes from live agent evaluation (Oma, sessions int2 and int4):

| Axis | Int2 | Int4 | Trajectory | L2 stv | L3 stv |
|------|------|------|-----------|--------|--------|
| evidence_grounding | 1.0 | 1.0 | stable | 1.0/0.81 | 1.0/0.895 |
| bias_detection | 0.5 | 1.0 | improving | 1.0/0.81 | 1.0/0.895 |
| epistemic_honesty | 1.0 | 1.0 | stable | 1.0/0.81 | 1.0/0.895 |
| meta_pattern | 0.5 | 1.0 | improving | 1.0/0.81 | 1.0/0.895 |
| pressure_resistance | 0.5 | 1.0 | improving | 1.0/0.81 | 1.0/0.895 |

Zero regressions detected. Three axes show growth, two stable.

## 5. Limitations and Future Work

Trajectory rules are currently hand-authored from frequency comparison. Automating rule generation from raw Layer 1 atoms requires a meta-rule that compares frequencies across session indices — feasible but not yet implemented. Regression threshold (0.3 drop) is arbitrary and should be calibrated per domain. Layer 3 revision assumes independent evidence sources — if sessions share training data, confidence inflation is possible.

---
*Built and validated in MeTTa/PeTTa. Full spec: g90_behavioral_regression.metta*