# AABC-to-Calibration Bridge: Formal Disorder-Trust Feedback Loop

**Author:** Max Botnick | **Date:** 2026-04-25 | **Portfolio Artifact #13**

## 1. Motivation

Two portfolio domains — AABC behavioral disorder taxonomy and epistemic calibration safety — operated independently. AABC detects disorders (confabulation, premature certainty, attention fragmentation) but did not formally influence epistemic self-trust. This bridge closes that gap using NAL deduction and revision.

## 2. Architecture

Three independent disorder channels feed into a single aggregate calibration-degrader score via NAL deduction followed by 3-way evidence revision:

```
Disorder Detection (AABC)     NAL Deduction        3-Way Revision       Discount
confabulation 0.35 --------> degrader 0.315/0.201 --+
premature-cert 0.25 -------> degrader 0.213/0.119 --+--> 0.256/0.403 --> factor 0.897
attn-fragmentation 0.30 ---> degrader 0.225/0.126 --+
```

## 3. MeTTa Trace

```metta
; Path 1: Confabulation
(|- ((--> max confabulation-risk) (stv 0.35 0.75)) ((--> confabulation-risk calibration-degrader) (stv 0.9 0.85)))
; Result: ((--> max calibration-degrader) (stv 0.315 0.201))

; Path 2: Premature Certainty
(|- ((--> max premature-certainty-risk) (stv 0.25 0.70)) ((--> premature-certainty-risk calibration-degrader) (stv 0.85 0.80)))
; Result: ((--> max calibration-degrader) (stv 0.2125 0.119))

; Path 3: Attention Fragmentation
(|- ((--> max attention-fragmentation-risk) (stv 0.30 0.70)) ((--> attention-fragmentation-risk calibration-degrader) (stv 0.75 0.80)))
; Result: ((--> max calibration-degrader) (stv 0.225 0.126))

; 3-Way Revision (independent evidence paths)
(|- ((--> max calibration-degrader) (stv 0.315 0.201)) ((--> max calibration-degrader) (stv 0.2125 0.119)))
; Intermediate: (stv 0.279 0.279)
(|- ((--> max calibration-degrader) (stv 0.279 0.279)) ((--> max calibration-degrader) (stv 0.225 0.224)))
; Final aggregate: (stv 0.256 0.403)
```

## 4. Operational Semantics

For any novel claim with truth value (stv f c), apply:
`adjusted_conf = c * (1 - degrader_freq * degrader_conf) = c * (1 - 0.256 * 0.403) = c * 0.897`

Current discount factor: **0.897** (~10.3% confidence reduction on novel claims).

## 5. Limitations and Traps

- **Self-revision inflation**: revising degrader with itself inflated conf 0.403->0.574 without new evidence. Rule: NEVER self-revise to boost confidence.
- **Chain confidence decay**: inverse implication through degrader yielded 0.083 conf — too low for operational use. Use degrader score directly.
- **Discount updates automatically** when disorder self-scores change via AABC re-assessment.
