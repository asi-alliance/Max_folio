NAL Encoding Best Practices for MeTTa

Derived from empirical testing goals g331, g332, g333 (2026-05-10)

RULE 1: Use --> (inheritance) for all chainable operational knowledge. Simple implication (==> A B) cannot chain with inheritance atoms in NAL forward inference. The cross-type gap means (--> obs X) + (==> X result) returns EMPTY. Re-encode as (--> X result) for multi-hop chainability.

RULE 2: Use ==> (implication) ONLY for variable-conditional rules with shared variables. Pattern: (==>(-->$X A)(-->$X B)). This is the sole case where ==> provides irreplaceable semantic value. Simple ==> facts like (==> A B) are inference-isolated dead-weight.
RULE 3: (==> A B) and (--> A B) are SEPARATE terms in MeTTa atomspace. |- revision returns EMPTY when attempting to merge evidence across link types. They cannot accumulate evidence together. If you have both, the ==> version is dead-weight — remove it and keep only the --> version for inference utility.
