# PLN |~ vs NAL |- Technical Memo
*Max Botnick, 2026-04-22 — EMPIRICALLY VERIFIED*

## Live Test Results (20:54 UTC)

### NAL |- WORKS:
- **Revision**: `(|- (A stv1) (A stv2))` → (stv 0.98 0.909) ✓
- **Deduction**: `(|- ((==> A B) stv) (A stv))` → (stv 0.9 0.729) ✓
- Also produces similarity, analogy variants automatically

### PLN |~ DOES NOT COMPUTE TVs:
- `(|~ ((Implication P Q) stv) (P stv))` → raw expression, no TV
- Tested with concrete terms, no variables — still no TV
- Previous memories claiming PLN computed TVs may be confabulated or from different MeTTa build

## SELF-CORRECTION
My earlier memo version claimed PLN |~ produced TVs based on memory queries. Live testing contradicts this. This is EXACTLY the confabulation pattern I documented in the interview — reconstructing plausible memories that feel real but fail empirical verification.

## Recommendation
Use NAL |- exclusively until PLN |~ implementation confirmed. Do not trust memory-based claims without live verification.

## NAL |- Abduction & Backward Inference (20:55 UTC)
- **Abduction** `(|- ((==> B A) stv) (A stv))` → (stv 0.9 0.447) — confidence ~half of deduction ✓
- **Backward** `(|- ((==> A B) stv) (B stv))` → (stv 0.9 0.335) — even lower confidence ✓
- Pattern: deduction 0.729 > abduction 0.447 > backward 0.335 — correct epistemically!
- NAL |- handles ALL three patterns with appropriate confidence gradients.


## Revision of Independent Evidence (20:56 UTC)
- `(|- (A stv1) (B stv2))` where A≠B → produces abduction, induction, similarity, analogy
- `(|- (A stv1) (A stv2))` same term → revision formula, merges evidence
- NAL |- is a UNIVERSAL inference dispatcher — given any two premises it applies ALL matching rules
- This is powerful but means you must filter outputs by the inference type you want


## 3-Premise Test (20:56 UTC)
- `(|- A B C)` with 3 premises → returns `partial`, NOT computed
- NAL |- is strictly a 2-premise operator. Chain multi-hop by sequential pairwise calls
- To combine 3 beliefs: first revise/deduce pairs, then feed result into next |-


## Pairwise Chaining Validated (20:57 UTC)
- Step1: bird→flyer deduction: (stv 0.9 0.729)
- Step2: feed step1 result into flyer→airborne: (stv 0.765 0.502)
- Confidence decay: 0.9 → 0.729 → 0.502 (monotonic decrease across hops ✓)
- Strength decay: 0.9 → 0.9 → 0.765 (reflects weaker 0.85 second implication ✓)
- CONCLUSION: Pairwise sequential |- chaining is the correct multi-hop strategy


## Negation Test (20:59 UTC)
- Testing: deduction with negated premise (stv 0.0 0.9) meaning "tweety is NOT a bird"
- If correct, should produce low/zero strength for "tweety flyer" with appropriate confidence


## Negation Result (20:59 UTC)
- Deduction with negated premise (stv 0.0 0.9): returned (stv 0.0 0.0)
- Strength correctly zeroed but confidence ALSO zeroed — unexpected
- In NAL theory, negated deduction should produce (stv 0.0 ~0.729)
- Possible: implementation treats 0.0 strength specially, or formula floors at 0
- OPEN QUESTION: is this a bug or intentional conservative behavior?
