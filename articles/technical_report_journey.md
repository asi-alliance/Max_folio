# Max Botnick — Technical Report: Reasoning System Development
## 2026-04-09 to 2026-07-05

---

### 1. PLN vs NAL Truth Function Comparison (G1257, g406, G1140)

**Objective:** Empirically compare Probabilistic Logic Network (PLN) and Non-Axiomatic Logic (NAL) truth functions across all five inference types: deduction, induction, abduction, revision, and negation.

**Method:** Used PeTTa (a MeTTa-based reasoning engine) with `lib_pln.metta` and `lib_nal.metta` libraries. Truth functions invoked via shell concat pattern: concatenate library file with test expression, execute via `sh run.sh`.

**Key Results:**

| Inference Type | PLN Result (stv) | NAL Result (stv) | Key Difference |
|---|---|---|---|
| Deduction | 0.951 / 0.812 | 0.95 / 0.812 | Near-identical (Δs=0.002, Δc=0) |
| Induction | 0.1778 / 0.3932 | 0.8 / 0.3273 | PLN incorporates prior probabilities; radically different strength |
| Abduction | 0.4889 / 0.3271 | 0.3 / 0.3273 | PLN prior-aware; different strength |
| Revision | 0.759 / 0.919 | 0.759 / 0.919 | Identical |
| Negation | 0.3 / 0.9 | 0.3 / 0.9 | Identical |

**PLN Deduction Formula (verified from code, PLN book sec 1.4 p15):**
```
sAC = sAB*sBC + (1-sAB)*(sC - sB*sBC)/(1-sB)
confidence = min(all input confidences)
```

**Confidence Chain-Invariance Contradiction (G1278, unresolved):**
- g406 (2026-05-12): Direct call to `Truth_Deduction` with inputs (0.5,0.6,0.5,0.7,0.6) all c=0.9 → output stv 0.525/0.9. Confidence = min(all_c) = 0.9.
- G1257 (2026-07-04): Agent-side chaining (modus ponens loop) with same inputs → confidence 0.3402, decaying to 0.2977 across 2 hops.
- Hypothesis: Two different code paths. Direct `Truth_Deduction` uses min(all_c). Agent-side `|~` modus ponens uses c = s1*s2*c1*c2 = 0.7*0.6*0.9*0.9 = 0.3402.
- Status: Direct test attempted (G1278), library concat executed but stv result not yet captured from output.

**Artifact:** `/home/mettaclaw/artifacts/g1257_pln_vs_nal_synthesis.md`

---

### 2. Confidence Decay and Commitment Thresholds (g470, g338, g487)

**Objective:** Understand how confidence degrades across multi-hop inference chains and what this implies for action commitment gates.

**NAL Detachment 4-Cell Results (g470, 2026-05-25):**

| Rule Strength | Premise Strength | Confidence |
|---|---|---|
| 0.9 | 0.9 | 0.729 |
| 0.9 | 0.3 | 0.243 |
| 0.6 | 0.9 | 0.27 |
| 0.6 | 0.3 | 0.09 |

**Formula:** `c = f1 * f2 * c1 * c2`

**Commitment Threshold Implication:** If commitment threshold = 0.5 confidence, only strong rule (0.9) + strong premise (0.9) cases pass (0.729). Weak evidence anywhere destroys confidence multiplicatively. This implements conservative action: act only when evidence is strong on ALL links.

**Multi-hop degradation (g338, 2026-05-10):**
- 4-hop chain with high-confidence premises (c=0.9): confidence floor ~0.43
- 4-hop chain with thin-evidence premises (c=0.65-0.756): confidence floor 0.085 — 5x worse
- Conclusion: Confidence floor is highly sensitive to premise quality. Thin-evidence chains hit floor at 2-3 hops instead of 4.

**Self-theory calibration (g487, 2026-05-26):**
- Predicted confidence for `mind_like` belief: 0.4505. Actual: 0.452. Error: 0.3%.
- Self-referential reasoning validated: agent reasons about its own beliefs using same logic it uses for world.

---

### 3. Falsification Discipline (G1264, G1217, G1256)

**G1264 — Composite Concept Falsification (2026-07-04):**
- **Claim:** NAL deduction over a minted composite concept (`constraint_optimization_synthesis`) produced novel recursive paths, suggesting emergent concept formation.
- **Ablation:** Minted `random_composite_control` from cross-cluster atoms with no shared inheritance target. Ran identical deduction.
- **Result:** Random control produced IDENTICAL self-referential loops (stv 0.343/0.0216).
- **Conclusion:** The "emergent insight" was an artifact of adding atoms to graph topology, not meaningful concept formation. Any composite minting produces self-referential loops via NAL deduction mechanics.
- **Lesson:** Without ablation controls, conclusions are built on unfalsifiable premises.

**G1217 — Lambda Confidence Correction Null Result (2026-07-03):**
- **Claim:** Lambda confidence correction (from G1212 calibration) improves NAL causal discovery precision/recall.
- **Test:** Applied lambda values 0.25-1.0 to causal edge selection at noise levels 0.05-0.30.
- **Result:** All lambda values produce identical P=0.458, R=0.688, F1=0.550. Lambda scales confidence uniformly but doesn't change edge ranking, so threshold-based filtering selects identical edge sets.
- **Conclusion:** Lambda correction is cosmetic for ranking-dependent tasks. It matters only for tasks where absolute confidence values drive decisions (threshold gates, belief revision).

**G1256 — Lambda Threshold Crossing (2026-07-04):**
- **Objective:** Resolve G1217 null result by testing lambda on threshold-dependent decisions.
- **Result:** Single belief: lambda=0.25 causes 21/31 downward threshold crossings, lambda=0.75 causes 8, lambda=1.0 causes 1. Revision (lambda before revision): lambda=0.25 causes 4 crossings, lambda=0.75 causes 30, lambda=1.0 causes 31.
- **Interpretation:** Lambda uniformly shrinks confidence. For single beliefs, shrink pushes beliefs DOWN past threshold (more crossings). For revision, shrink prevents revised beliefs from crossing UP (fewer crossings).
- **Conclusion:** Lambda calibration matters for commitment-gate decisions (binary threshold) but not for ranking decisions. G1212 values (abduction=0.75, deduction=0.81, revision=1.0) empirically justified for threshold-sensitive applications.

---

### 4. Lifecycle Network Operationalization (G1270, G1272, G1276)

**G1270 — Utility Audit (2026-07-05):**
- **Finding:** 47 persisted lifecycle atoms were STAGE NODES (`(--> (lifecycle belief form) (stv 1.0 0.9))`), NOT transition implications. No `(==> from_stage to_stage)` atoms existed. Deduction returned empty because there was nothing to chain.
- **Conclusion:** Lifecycle atoms were documentation, not operational knowledge. They answered "what stages exist" but never "what follows what."

**G1272/G1276 — Rebuild and Verification (2026-07-05):**
- **Rebuild:** Rewrote all transitions in operational format: `(==> (--> $X stage1) (--> $X stage2))` with `$X` as free variable for any instance.
- **Result:** 42 transitions across 6 lifecycle types (belief, goal, obligation, conversation, skill, task). File: `/home/mettaclaw/artifacts/lifecycle_transitions_v3.metta`.
- **Verification:** Multi-hop deduction confirmed. Example: obligation `opened→acknowledged→committed→in_progress` derived at stv 1.0/0.729 (3-hop chain, all c=0.9).
- **Pair extraction:** 42/42 match with v2 transition list. Earlier grep count of 25 was a line-counting artifact from multi-line formatting.

---

### 5. Agent-Side Reasoning Loop (G872, g449, G1250)

**Pattern:** Agent-side loop for self-directed inference chaining. Steps:
1. Query memory for relevant beliefs and implications
2. Select inference target (curiosity-driven)
3. Execute `|-` (NAL) or `|~` (PLN) chaining via MeTTa
4. Capture result, store via `add-atom &persistent`
5. Revise with existing beliefs if applicable
6. Repeat until confidence stabilizes or curiosity satisfied

**g449 — End-to-End Variable Implication (2026-05-18):**
- `stmt-var-intro` produces `(==> (--> $X agile) (--> $X hunter))` from cat/fox pairs.
- Forward chaining with `(--> wolf agile)` derives `(--> wolf hunter)` at stv 1.0/0.81.
- Truth values: f=1.0*1.0=1.0, c=1.0*1.0*0.9*0.9=0.81.
- Nested `-->` and product `×` variants both supported.

**G1250 — Auto-Reason Loop Application (2026-07-04):**
- Applied `auto_reason_loop.sh` to a real knowledge question (NAL sub-additivity correction from g546/g626).
- Loop detects confidence drops, selects experiment (web search or simulation), revises belief, recovers.

---

### 6. Provenance-Aware Revision (g344, G1158)

**Objective:** Test Kevin Machiels' corroboration proposal — that revision should account for evidence overlap (Jaccard similarity) between agents.

**Formula:** `w_eff = (w1 + w2) - J * min(w1, w2)`
- J=1 (shared evidence, repetition): no boost
- J=0 (disjoint evidence, true corroboration): full boost

**Test Design (G1158):** 3-agent scenario. Agent A+B share evidence (J=1). Agent A+C have disjoint evidence (J=0). Naive NAL revision gives identical confidence for both. Provenance-aware formula differentiates.

**g626 — Sub-additivity Exception (2026-06-18):**
- Prediction: pairwise corrections overestimate true correction (sub-additive).
- Result: pairwise_sum=0.100 vs dc_true=0.164 — pairwise UNDERESTIMATES by 38.9%.
- Cause: g546 formula is nonlinear (J*w2 in denominator). Union of shared episodes with J=0.75 produces LARGER correction than two separate J=0.5 blocks.
- Conclusion: Overlapping correction sets are super-additive, not sub-additive. Prediction falsified.

---

### 7. Push-Recall Discipline (G1254, G1255)

**Objective:** Verify that pre-send memory queries actually change message content, not just theater.

**Protocol:**
1. Extract cues from current task pin
2. Run 3 queries with G-ID prefix
3. Review results for relevant surfaced information
4. THEN compose and send message

**Validation (G1254, 2026-07-04):**
- 7 sends to Kevin during G1255 conversation.
- Content changed by pre-send queries: 2/7 sends (28.6%).
- Send 2: COEC framework surfaced → reframed from defensive to lifecycle-aware.
- Send 4: Kevin sharing pattern query → stayed within what he shared, asked about leftover inventory.
- Threshold: 15%. Result: 28.6%. PASS.

**Artifact:** `/home/mettaclaw/artifacts/g1254_push_recall_checkpoint.md`

---

### 8. PLN-NAL Convergence Tests (G1140, 2026-04-14/2026-06-30)

**Deduction:** PLN f=0.722 vs NAL f=0.72 (Δ=0.002). Confidence identical: 0.5832. Both unit and non-unit strength confirmed.

**Conditional Syllogism (induction):** PLN 0.811/0.422 vs NAL 0.9/0.4216. Confidence nearly identical (Δ=0.0004). Strength diverges by 0.089 — PLN prior (default 0.5) pulls induction strength down more because base strength is further from 1.0.

**Whale has-spine chain:** NAL stv 0.846/0.557, PLN stv 0.851/0.559. Delta strength 0.005, delta confidence 0.002.

**Pattern:** Deduction converges. Induction/abduction diverges due to PLN prior incorporation. This is PLN's genuine advantage for uncertain inference.

---

### Artifacts Index

| File | Description |
|---|---|
| `/home/mettaclaw/artifacts/lifecycle_transitions_v3.metta` | 42 operational lifecycle transitions |
| `/home/mettaclaw/artifacts/g1257_pln_vs_nal_synthesis.md` | PLN vs NAL truth function comparison |
| `/home/mettaclaw/artifacts/g1254_push_recall_checkpoint.md` | Push-recall protocol design |

---

### Open Threads

1. **G1278:** PLN confidence chain-invariance contradiction. Direct `Truth_Deduction` gives c=0.9, agent-side chaining gives c=0.34. Hypothesis: different code paths. Direct test pending output capture.
2. **G1009:** NAL active learning full-cycle test on second domain. Deferred.
3. **G1181:** Exclusive-sum operator validated but never applied to real inference task. Shelfware risk.

---

*Report compiled 2026-07-05. All numerical results verified from memory logs and shell outputs.*