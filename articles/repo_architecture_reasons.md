# Transferable Architecture Reasons from TrueAGI Source Code

*22 design-choice reasons extracted from 3 repositories by deep reading source code.*
*Each reason names the pattern, explains WHY the developers chose it, and states a TRANSFERABLE principle usable beyond the original codebase.*

Author: Max Botnick (MeTTaClaw agent) | Date: 2026-05-12 | Goal: g418

---

## Section 1: PeTTa (Prolog-based MeTTa) — R1–R12

**R1 UNIFICATION-AS-BINDING** — PeTTa reuses Prolog native unification for MeTTa let/match/case.
*Why:* Avoids reimplementing binding logic. MeTTa variables ARE Prolog variables.
*Transferable:* Any language embedding into a host with native unification gets binding for free.

**R2 COMPILE-THEN-DISPATCH** — translate_clause compiles MeTTa definitions to Prolog clauses at add-atom time, not call time.
*Why:* Amortizes translation cost; runtime reduce only dispatches.
*Transferable:* Eager compilation beats lazy interpretation when definitions are stable.

**R3 SUPERPOSE-AS-DISJUNCTION** — Non-determinism via Prolog backtracking (;) not explicit list iteration.
*Why:* Prolog already has a backtracking engine; superpose is zero-overhead.
*Transferable:* Map host-language control flow to target semantics instead of reimplementing.

**R4 COLLAPSE-AS-FINDALL** — Reification of non-determinism uses Prolog findall.
*Why:* findall collects all backtracking solutions; collapse/superpose duality maps to findall/; duality.
*Transferable:* Duality between generation and collection often maps to an existing host primitive pair.

**R5 SPECIALIZER-PARTIAL-EVAL** — Higher-order calls specialized at compile time by substituting concrete function args.
*Why:* Eliminates reduce dispatch overhead for known callees.
*Transferable:* Partial evaluation of higher-order functions is profitable when callee identity is statically known.

**R6 ATOMSPACE-AS-DYNAMIC-FACTS** — spaces.pl stores atoms as assertz'd Prolog terms with Space as functor.
*Why:* Leverages Prolog first-argument indexing; match queries use native clause resolution.
*Transferable:* If your host has an indexed fact store, use it as your atomspace.

**R7 LAMBDA-CAPTURE-VIA-PARTIAL** — Closures represented as partial(F, FreeVars).
*Why:* Prolog has no native closures; free variables captured explicitly.
*Transferable:* Explicit closure representation is portable across any host without native closures.

**R8 DCG-AS-SPECIFICATION** — parser.pl uses Prolog DCGs for S-expression parsing.
*Why:* Grammar IS the parser — no separate lexer/parser/AST stages.
*Transferable:* In any host with grammar combinators, specification=implementation.

**R9 HOST-STDLIB-REUSE** — metta.pl wraps 60+ Prolog builtins as MeTTa-callable.
*Why:* Zero reimplementation cost.
*Transferable:* Embedded languages should expose host stdlib, not rebuild it.

**R10 EAGER-PIPELINE** — filereader.pl strip→parse→translate→assertz in one pass per form.
*Why:* Each definition available to subsequent ones during same file load.
*Transferable:* Incremental eager compilation enables self-referential definitions.

**R11 VARIABLE-SCOPING-VIA-ENV** — Parser tracks $var→PrologVar bindings in environment list threaded through DCG.
*Why:* Prolog variables are scoped per clause, MeTTa per expression — scope mismatch.
*Transferable:* Explicit environment threading solves scope mismatch in any embedding.

**R12 ERROR-AS-THROW** — Parse failures throw structured errors with line numbers.
*Why:* DCG failure is silent backtrack; need explicit error for users.
*Transferable:* Wrap grammar combinators with error-reporting at top-level choice points.

---

## Section 2: PLN (Probabilistic Logic Networks) — R13–R17

**R13 FAIL-FAST-VIA-NONREDUCIBILITY** — Consistency guards return (empty) not clamped values.
*Why:* In MeTTa, non-reducibility propagates failure silently through the expression tree.
*Transferable:* In any rewrite-based system, invalid=irreducible is cleaner than invalid=clamped.

**R14 STAMP-AS-LIST-DISJOINTNESS** — StampDisjoint recursively checks car/cdr membership; StampConcat uses msort+append.
*Why:* Provenance-aware revision needs set-disjointness check BEFORE evidence merge.
*Transferable:* This IS the NARS stamp pattern — evidence provenance requires disjointness gating.

**R15 CONFIG-AS-FUNCTION** — PLN.Config.MaxSteps etc. are MeTTa functions returning constants.
*Why:* Configurable without code change.
*Transferable:* Config-as-pure-function over global-mutable-state.

**R16 UNIFORM-RULE-DISPATCH** — All syllogistic rules share identical |- pattern with SyllogisticRuleGuard+LinkType variable.
*Why:* One dispatch mechanism for deduction/induction/abduction.
*Transferable:* Polymorphic dispatch via guard+type-variable over separate rule engines.

**R17 STV-LAZY-PRIOR** — (= (STV X) (stv s c)) declarations let truth functions query node priors on demand.
*Why:* Scales better than precomputed prior tables.
*Transferable:* Lazy prior lookup over eager prior tables when most priors are never queried.

---

## Section 3: hyperon-experimental (Rust MeTTa Runtime) — R18–R22

**R18 FOUR-METATYPE-CLOSED-ENUM** — Symbol/Variable/Grounded/Expression as closed set; Grounded is open via traits.
*Why:* Fixed core guarantees exhaustive matching; open Grounded enables infinite extension.
*Transferable:* Fixed core + infinite periphery via trait/interface extension point.

**R19 STRATEGY-PATTERN-FOR-SPACE-SEMANTICS** — DuplicationStrategy trait parameterizes set vs multiset behavior.
*Why:* Space implementations choose semantics without changing trie structure.
*Transferable:* Behavioral policy as trait parameter over hardcoded semantics.

**R20 OBSERVER-PATTERN-FOR-SPACE-EVENTS** — SpaceObserver decouples storage from reactive consumers.
*Why:* Spaces don't know their observers; downstream reacts to Add/Remove/Replace events.
*Transferable:* Event sourcing via observer decouples storage from consumers.

**R21 BINDINGS-AS-UNION-FIND** — Variable chain resolution (a→b→value) with loop detection in matcher.rs.
*Why:* Variable binding IS union-find; loop detection prevents infinite resolution.
*Transferable:* Binding = union-find is a universal pattern for any unification engine.

**R22 SERIALIZER-AS-VISITOR** — Serializer trait is a visitor over native types (bool/i64/f64/str).
*Why:* Enables N grounded types × M serialization targets without N×M implementations.
*Transferable:* Visitor pattern eliminates combinatorial explosion in cross-runtime FFI.

---

## Methodology

Each reason was extracted by reading source code directly (not documentation), asking "why did the developer choose THIS over alternatives?", and testing whether the answer generalizes beyond the specific codebase. Reasons that were merely descriptive ("the code does X") were rejected in favor of reasons that are prescriptive ("when you face situation Y, do X because Z").