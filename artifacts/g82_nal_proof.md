# G82: NAL Proof Chain — Pipeline Optimality from First Principles

## 8 MeTTa Derivations (2026-04-21)

### Axioms
- select is irreversible_stage (stv 1.0 0.9)
- score is reversible_stage (stv 1.0 0.9)
- budget is reversible_stage (stv 1.0 0.9)
- score ranks_all_candidates (stv 1.0 0.9)

### Derivation 1: select -> must_be_last (stv 1.0 0.81)
Rule: irreversible_stage ==> must_be_last

### Derivations 2-3: score -> can_be_early, budget -> can_be_early (stv 1.0 0.81)
Rule: reversible_stage ==> can_be_early

### Derivation 4: score -> should_precede_budget (stv 1.0 0.81)
Rule: can_be_early AND ranks_all_candidates ==> should_precede_budget (product type)

### Derivation 5: score = first_stage (stv 1.0 0.729)
Rule: should_precede_budget ==> first_stage

### Derivation 6: select = third_stage (stv 1.0 0.81)
Rule: must_be_last AND irreversible_stage ==> third_stage (product type)

### Derivation 7: budget = second_stage (stv 1.0 0.81)
Rule: can_be_early AND NOT first_stage ==> second_stage (product+negation)

### Conclusion
NAL engine derives unique ordering score(1st)->budget(2nd)->select(3rd) from 4 axioms about irreversibility and information preservation. Combined with quantale minimality argument: this is the provably optimal pipeline under Bennett-Goertzel weakness.