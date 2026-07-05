# NAL Revision Forms a Commutative Monoid Over Independent Evidence

**Artifact 41 | g265 Temporal Paradox Probe | 2026-05-03**

## Abstract

We show that NAL/PLN belief revision over same-term judgments with independent evidence sources forms a commutative monoid. The identity element is any STV with zero confidence. Prior findings of non-associativity (April 27) are reframed as duplicate-evidence artifacts, not genuine order-dependence.

## Theorem

Let E be a set of independent evidence sources producing judgments on the same term. Let rev(a,b) denote NAL revision. Then (E, rev, stv(any, 0.0)) is a commutative monoid:

1. **Closure**: rev of two STVs yields an STV
2. **Associativity**: rev(rev(a,b),c) = rev(a,rev(b,c)) in exact arithmetic
3. **Commutativity**: rev(a,b) = rev(b,a)
4. **Identity**: rev(a, stv(f,0.0)) = a for all a

## Proof Sketch

The revision formula maps confidence to evidence weight: w = c/(1-c), mapping [0,1) to [0,inf). Under this transform:
- Frequency merges as weighted average: f_rev = (w1*f1 + w2*f2)/(w1+w2)
- Total weight adds: w_total = w1 + w2
- Confidence recovers: c_rev = w_total/(w_total + 1)

Since (R>=0, +, 0) is a commutative monoid, and the w-transform is a monotone bijection, the structure transfers back to STV space. The identity maps to w=0, which is c=0.

## Failure Mode: Shared Sub-Evidence

When intermediates share sub-evidence, revision DOUBLE-COUNTS:
- t1+t2 = (0.431, 0.906), t2+t3 = (0.175, 0.870)
- Cross-revision (t1+t2) rev (t2+t3) = (0.326, 0.942)
- Correct independent triple = (0.447, 0.914)
- Delta: 0.121 in frequency — t2 weight counted twice

## Architectural Fix: Provenance Tracking

Each derived judgment must carry its evidence ancestry. Before revision, check overlap. If shared ancestors exist, discount or skip. This enforces the independence precondition. See g206v3/g207 dedup chainer.

## Empirical Evidence

| Test | Path A | Path B | Delta | Finding |
|------|--------|--------|-------|---------|
| Same-term triple | (0.447, 0.914) | (0.446, 0.914) | 0.001 | Approx associative |
| Heterogeneous 3-path | (0.732, 0.666) | (0.732, 0.666) | 0.000 | Exact match |
| Zero-conf identity | (0.732, 0.666) | (0.732, 0.666) | 0.000 | Identity confirmed |
| Cross-revision overlap | (0.326, 0.942) | (0.447, 0.914) | 0.121 | Double-count |
| Commutativity | rev(a,b) | rev(b,a) | 0.000 | Symmetric |
| April 27 reframe | order-dependent | duplicate-evidence | - | Reclassified |