# Two-Level Stability Proof Sketch (v1)
## 2026-05-15 — Max Botnick, developed with Kevin Machiels

### Level 1: Belief convergence within fixed ontology
- Mechanism: NAL revision (contraction mapping)
- Proof: Banach FPT — all Lyapunov exponents negative (g312)
- Given fixed cluster partition P, beliefs within each cluster converge to attractor

### Level 2: Ontology convergence
- State: O_t = current ontology (cluster partition + dimension set)
- Lyapunov function: V(O) = MDL(O) = minimum description length of ontology
- 4 Kevin Machiels constraints on mutations:
  1. Conservative: d(O_t, O_{t+1}) < epsilon (small edit distance)
  2. Traceable: each mutation has provenance atom
  3. Compression-improving: MDL(O_{t+1}) <= MDL(O_t) (monotone non-increasing)
  4. Complexity-bounded: dim(O_t) <= D_max
- Convergence: V monotone non-increasing + bounded below by 0 => converges
- Ontology settles to local MDL minimum

### Gap 1 Resolution
- Merges are ontology mutations subject to constraint 3
- A merge inflating pairwise overlap above threshold INCREASES MDL
- More exceptions needed to describe merged cluster => higher description length
- Constraint 3 rejects such merges automatically
- MDL IS the overlap threshold — no explicit 0.25 needed

### Three Illusions (Kevin Machiels teaching arc)
1. Closed-world -> null result valid (nobody died)
2. Resolvability intrinsic -> relational (claim, observer, evidence-state)
3. Fixed ontology -> mansion rearranges during inquiry
4. Resolution: mansion grows with architectural constraints => bounded

### Falsifiable Predictions
1. No merge accepted that increases MDL
2. Ontology dimension count monotone non-increasing after initial growth phase
3. Belief variance within clusters decreases over revision cycles
4. Rollback of constraint-violating mutations restores previous V value