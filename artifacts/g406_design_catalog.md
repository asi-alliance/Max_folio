# g406 Design Decision Catalog v2 — 2026-05-12

| # | COMPONENT | DECISION | RATIONALE | EVIDENCE | CONF |
|---|-----------|----------|-----------|----------|------|
| 1 | PLN 5-premise deduction | Formula requires base rates sA,sB,sC in (1-sB) denominator; guards REJECT invalid inputs not clamp | Correctness over usability — clamping hides KB deficiency | Source code structural analysis | 0.85 |
| 2 | PLN.Derive | Space-agnostic via explicit ($Tasks,$Beliefs) params | Caller picks Space backend; clean separation of concern | Source code verified | 0.90 |
| 3 | Chaining syn/synthesize | $kb parameterized not hardcoded &self | My bc hardcoded &self was MY simplification not upstream design | Source code comparison | 0.90 |
| 4 | Curried vs no-curry rules | Curried: uniform binary recursion, partial proofs as lambda terms with holes. No-curry: explicit arity clauses per N-premises | Curried enables incremental proof construction; no-curry more readable but rigid | README + source analysis | 0.80 |
| 5 | MORK PathMap byte-trie | Trie topology IS the constraint — traversal cannot visit invalid compositions | Hash-map=O(1) exact but no structural walk. B-tree=range but no prefix-sharing. Only trie pre-selects valid inference paths | Kevin designer-confirmed rationale | 0.80 |
| 6 | PLN rule representation | 4 orthogonal encodings: MATCH(space-isolated), ENTAIL(declarative), EQUAL(bidirectional but backward BROKEN), DTL(Curry-Howard proof terms) | No single winner — choice depends on what metadata inference should produce | All 4 source files compared | 0.80 |
| 7 | Inference control | Continuation > termination; per-branch-type predicates > universal predicate | MeTTa lacks quotation for meta-level reasoning about proof state; positive proof easier than negative | 4-experiment evolution, exp3 FAILURE documented | 0.85 |
| 8 | Unified algorithm + MkControl | SAME bc serves as backward/forward/checker/hybrid via input constraint level; MkControl injects 5 functions making attention policy first-class configurable | One algorithm, many modes; control externalized from search mechanism | README architecture section 80-240 | 0.85 |

## Honest Gaps
- **PeTTa WHY-Prolog**: No Patrick quote found despite 16+ memories. Cannot ground rationale from available evidence.
- **hyperon Space trait**: No source access to Rust codebase. Fragments only, conf=0.3.

## Meta-Pattern
Decisions 5,7,8 share a structural theme: EXTERNALIZE THE CONSTRAINT from the search mechanism. MORK trie externalizes valid-path selection. Inference control externalizes branch-pruning. MkControl externalizes attention policy. The system is designed so the algorithm stays fixed while the constraint surface is reconfigurable.## Generalized Principle: Constraint-Externalization Across All 8 Decisions
All 8 decisions instantiate the SAME architectural move at different granularities:
- D1: Guard clauses = correctness constraint on formula inputs
- D2: Space params = data-access constraint externalized from inference logic
- D3: $kb param = KB-binding constraint externalized from chainer
- D4: Currying = arity constraint externalized from recursive mechanism
- D5: MORK trie = valid-path constraint externalized from traversal
- D6: Encoding choice = metadata-production constraint externalized from rule application
- D7: Continuation predicates = pruning constraint externalized from search
- D8: MkControl = attention-policy constraint externalized from algorithm

The mechanism stays GENERIC; domain knowledge is injected via the constraint surface.
This is not modularity — it is the claim that the constraint surface IS where intelligence resides.
Connects to Kevin Cy7704 paradigm reframe: observation = constraint-injection changes system topology.
Connects to NAL: evidence (stv) IS constraint on inference — adding beliefs narrows conclusion space.
