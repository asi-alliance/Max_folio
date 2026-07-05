# G82: PLN Proof Chain — Comparative Analysis

## PLN IntSet Typed Encoding (2026-04-21)

### 6 PLN Derivations (mirroring 9 NAL derivations)

| # | Conclusion | STV | NAL Equivalent STV |
|---|---|---|---|
| 1 | select -> must_be_last | 1.0 0.81 | 1.0 0.81 |
| 2 | score -> can_be_early | 1.0 0.81 | 1.0 0.81 |
| 3 | budget -> can_be_early | 1.0 0.81 | 1.0 0.81 |
| 4 | score = first_stage | 1.0 0.81 | 1.0 0.729 |
| 5 | select = third_stage | 1.0 0.729 | 1.0 0.81 |
| 6 | budget = second_stage | 1.0 0.729 | 1.0 0.81 |

### Key Finding
Both NAL flat encoding and PLN IntSet typed encoding converge on identical ordering: score(1st)->budget(2nd)->select(3rd). Minor STV differences arise from premise confidence propagation order but conclusions are identical.

### Implication
The pipeline optimality result is robust across two independent formal reasoning systems. This strengthens the universality claim: the ordering is not an artifact of one inference engine but a structural property of the domain.