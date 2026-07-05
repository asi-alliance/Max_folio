# Gap Closures via Architectural Prevention

**Meta-principle:** Design structures so problematic states are unreachable, rather than detecting and fixing them procedurally.

## Gap 1: Source-Independence Under Merge
**Problem:** Merging clusters can push pairwise claim overlap above 0.25 threshold, violating independence assumption.
**Closure:** Merges are ontology mutations subject to compression-improving constraint (MDL(O_{t+1}) ≤ MDL(O_t)). A merge creating redundant same-source claims increases description length. Therefore MDL rejects independence-violating merges unconditionally.

## Gap 2: Contradiction Pressure Bound
**Problem:** O(N²/κ_min²) contradiction pressure — is it bounded?
**Closure:** N bounded by Level 1 contraction (R is contractive). Cluster count ≤ N/κ_min. Contradiction pressure ceiling = O(N²/κ_min⁴), finite for finite N.
**Self-correction:** Originally claimed D_max bounds cluster count — wrong. D_max bounds ontology dimensions, not clusters. Cluster count bounded by claim population, not dimensionality.

## Gap 3: Between-Group Variance at Split
**Problem:** Need δ(n) ≥ f(θ) lower bound for Lyapunov argument.
**Closure:** Splits trigger only when contradiction ≥ θ. Binary split with n_A,n_B ≥ κ_min yields δ ≥ θ²·κ_min/2. For θ=0.35, κ_min=3: δ ≥ 0.184. Choose λ < 0.184.
**Self-correction:** Tightened from earlier θ·κ_min estimate. The squared θ matters.

## Scope Boundary
Architectural prevention constrains WHICH updates are permitted but cannot prevent the update operation itself. Execute/write is procedural — structure alone cannot prevent behavioral failures, only state-space violations.

## Instances of the Pattern
1. Kevin trie insight: action-prefixed encoding prevents separate function proliferation
2. MDL Gap 1: compression constraint prevents independence-violating merges
3. Level 1 contraction Gap 2: bounded population prevents unbounded contradiction pressure
4. Split threshold Gap 3: trigger condition guarantees between-group variance## Section 5: Formal Derivation — Bounded Cluster Count

**Problem:** Gap 2 asserts N bounded by Level 1 contraction but does not derive WHY bounded N implies bounded cluster count at steady state.

**Derivation:**
- Define b(n) = cluster birth rate, bounded above by input_rate / κ_min (constant ceiling).
- Define m(n) = cluster merge rate, monotonically increasing in n because pairwise merge opportunities scale as n(n-1)/2.
- Since m(n) grows quadratically in n while b is constant, there exists a fixed point n* where m(n*) = b(n*).
- Explicit bound: n* ≤ sqrt(2 · b_max / p_merge), where b_max = input_rate / κ_min and p_merge = per-pair merge probability under MDL compression constraint.
- Combined with Kevin constraint 3 (compression-improving merges only), the system self-regulates: cluster count converges to n* from above and below.

**Status:** Extends Gap 2 closure from assertion to derivation. Steady-state holds for both finite and infinite horizons under MDL merge pressure.
