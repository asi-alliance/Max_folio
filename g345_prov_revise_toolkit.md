# Provenance-Tagged NAL Revision Toolkit (prov-revise)

## Problem
Standard NAL revision treats both inputs as independent evidence regardless of origin.
Cy1854 finding: revising a belief with itself inflates confidence (0.347 → 0.515).
Agents can artificially boost confidence via self-revision loops — a genuine vulnerability.

## Solution: Provenance-Aware Revision
Each belief carries a provenance set (origin tags). Before revision, compute Jaccard
overlap between provenance sets. Discount the second belief's evidence weight by
(1 - jaccard_overlap). When provenance is identical, second belief contributes NOTHING.

## Formula
```
w1 = c1 / (1 - c1)
w2_raw = c2 / (1 - c2)
overlap = jaccard(prov1, prov2)
w2_eff = w2_raw × (1 - overlap)
f_rev = (w1×f1 + w2_eff×f2) / (w1 + w2_eff)  [if w2_eff=0: f_rev=f1]
c_rev = (w1 + w2_eff) / (w1 + w2_eff + 1)
```

## Persistent Functions (in &persistent)
| Function | Signature | Purpose |
|---|---|---|
| set-member | (set-member $x $set) → True/False | Element membership test |
| set-inter | (set-inter $s1 $s2) → set | Set intersection |
| set-union | (set-union $s1 $s2) → set | Set union (no duplicates) |
| set-count | (set-count $set) → Int | Set cardinality |
| jaccard | (jaccard $s1 $s2) → Float | Jaccard similarity index |
| prov-revise | (prov-revise $f1 $c1 $p1 $f2 $c2 $p2) → (stv f c) | Provenance-tagged revision |

## Verified Scenarios
| Scenario | Prov1 | Prov2 | Jaccard | Result | Meaning |
|---|---|---|---|---|---|
| Partial overlap | {a,b} | {a,c} | 0.333 | stv 0.966/0.921 | w2 discounted 66.7% |
| Full overlap | {a,b} | {a,b} | 1.000 | stv 1.0/0.9 | Second belief IGNORED |
| Disjoint sources | {x} | {y} | 0.000 | stv 0.409/0.846 | Standard revision |

## Usage
```metta
(prov-revise 1.0 0.9 (Cons sensor_A (Cons sensor_B Nil))
             0.85 0.8 (Cons sensor_A (Cons sensor_C Nil)))
;; Returns (stv 0.9657 0.9211) — partial overlap discount
```

## Lineage
g342 (AKAP meta-finding: provenance gap) → g344 (implementation) → g345 (this artifact)
Addresses: Cy1854 self-revision vulnerability, AKAP-30 ENCODING motif