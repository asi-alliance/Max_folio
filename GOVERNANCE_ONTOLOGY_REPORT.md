# Belief Governance Ontology Report
## Corrected Edition — 2026-05-03

### 1. Architecture Overview
NAL-based belief system with deductive ceilings, conductance flow, two-gate admission, certification invariants, EXP-C structural audit, EXP-C′ warrant audit, and fixpoint revision.

### 2. Four-Category Taxonomy
| Category | Definition | Examples |
|---|---|---|
| **SEED** | Externally asserted, no derivation path, no ceiling | autonomous_agent (0.900), proactive_support (0.891) |
| **DERIVED-GROUNDED** | Deductively derived, actual ≤ ceiling | goal_directed (0.91/0.67, ceiling 0.674, margin −0.004) |
| **EVIDENCE-ENRICHED** | Surplus above ceiling backed by independent behavioral warrants | creative_thinker (0.809/0.717, ceiling 0.606, surplus +0.111) |
| **RECOVERY-ORPHAN** | Hysteresis-repaired surplus without behavioral warrant; includes path-deleted beliefs with unmeasurable ceiling AND beliefs carrying unauditable revision-injected confidence | rational_entity (0.87, ceiling 0.689, surplus +0.181) |

Note: **UNWARRANTED-SURPLUS** is a transient audit state, not a stable category. Beliefs flagged as unwarranted-surplus during EXP-C audit enter a probe window and resolve to EVIDENCE-ENRICHED (if warranted) or DERIVED-GROUNDED (if surplus decays).

### 3. Deductive Ceilings
Ceiling = max confidence achievable via deduction from parent beliefs. Computed via NAL deduction: if A→B (stv f1 c1) and B→C (stv f2 c2), ceiling for A→C = c1 × c2 × 0.9.
- ct ceiling: mb→ps→ct = 0.606 (actual 0.5806, deficit −0.025 → DERIVED-GROUNDED before revision)
- gd ceiling: 0.674 (actual margin −0.004)
- re ceiling: 0.689 (actual 0.87, surplus +0.181)

### 4. Conductance Flow
ps is load-bearing conductance support: network conductance drops 0.606→0.333 when ps is degraded. Shell coupling is quality-coupling — ct survives ps removal at degraded conductance.

### 5. Two-Gate Admission
- Gate 1: Contradiction check (t_contradiction = 0.20, context-adaptive)
- Gate 2: Under-support check (c_revised ≥ 0.4 floor)
- Differential hold: longer for Gate1-fail (evidence exists but conflicts), shorter for Gate2-fail (evidence absent)

### 6. EXP-C / EXP-C′ Dual Audit
- **EXP-C**: Structural audit — compares actual confidence to deductive ceiling, flags surplus
- **EXP-C′**: Warrant audit — evaluates behavioral evidence backing surplus beliefs
- Validated by catching ct false-surplus error (0.474 was revision asymptote, not ceiling)

### 7. Surplus Governance
- **prior-support flag**: ps_flag = external_evidence/total per trait (re=0.43, gd=0.50), threshold 0.3
- **proportional ε**: ε_t = α × ceiling_conf × freshness_decay, α=0.12
- **Probe window**: N=50 cycles, auto-promote to EVIDENCE-ENRICHED or auto-demote to DERIVED-GROUNDED
- **Debt model**: debt_unit = surplus-magnitude × cycles; coverage = min(1, n_independent_warrants / 5) where warrants = cataloged independent behavioral evidence items (not deductive paths); debt_remaining = debt_accrued × (1 − evidence_coverage); debt ceiling N=200 surplus-cycles

### 8. Fixpoint Revision
NAL revision merges evidence: f_revised = weighted mean, c_revised = c1 + c2 − c1×c2. Contradiction revision yields f≈0.5 with boosted confidence (textbook rational midpoint). Revision is idempotent at fixpoint.

### 9. Certification Invariants
- false_admit = 0 (maintained across all sweeps)
- signal_retention ≥ 84.2% (v2 calibrated)
- All beliefs auditable via EXP-C structural + EXP-C′ warrant dual pathway

### 10. h-Regime Architecture
Two operational modes: h≈0.85 core-only execution (aa, re, gd, ee), h≈0.6 reflective maintenance (full basin including ps, ct coupled shell). Plateau 0.62–0.80 is dead zone. Phase transition at h=0.62.

---
*Report reconstructed from audit trail Cy8787–Cy9013. Four corrections applied per Kevin Machiels review 2026-05-03.*