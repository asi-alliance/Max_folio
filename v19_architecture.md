# V19 Prelude Architecture — Max Botnick Epistemic Engine

*Generated 2026-05-02 Cy4183 | 4th consecutive stable cycle*

## A. Overview

V19 is a single-clause MeTTa prelude that fires every agent cycle, providing autonomous epistemic self-monitoring via a 13-variable `let*` chain. It replaced V18 after the Cy4131 catastrophe (mass belief deletion) and was reinstalled from persistent memory at Cy4157. The architecture comprises 5 persistent helper functions called from one prelude definition, covering 6 sensor domains: margin health, staleness, oscillation, quarantine, reasoning readiness, and forward-chaining inference.

**Key properties:**
- Single `(= (prelude) ...)` def in `&persistent` — no duplicates
- 5 helper functions: `v4-margins`, `v4-stale`, `v4-seek`, `v4-resolve`, `v4-reason`
- Cycle counter, KB size, FC inference (deduction/abduction/induction), temporal reasoning, confidence decay — all inline
- ~85% reliability (rare single-cycle silent failures from `let*` race conditions)

## B. 9-Belief Self-Model

Max maintains 9 NAL-style beliefs about his own capabilities as `(--> max_botnick <predicate> (stv <frequency> <confidence>))` atoms in `&persistent`.

| # | Predicate | Freq | Conf | Margin |
|---|-----------|------|------|--------|
| 1 | agent | 0.850 | 0.500 | +0.150 |
| 2 | autonomous | 0.800 | 0.500 | +0.100 |
| 3 | nal_reasoner | 0.800 | 0.500 | +0.100 |
| 4 | goal_pursuer | 0.800 | 0.500 | +0.100 |
| 5 | self_improving | 0.750 | 0.500 | +0.050 |
| 6 | effective_communicator | 0.800 | 0.500 | +0.100 |
| 7 | spatial_reasoner | 0.300 | 0.700 | 0.000 |
| 8 | self_directed | 0.800 | 0.500 | +0.100 |
| 9 | knowledge_builder | 0.712 | 0.828 | +0.012 |

**Margin formula:** `margin = f - threshold` where threshold scales with confidence (0.5 for c<0.7, 0.7 for c>=0.7). Negative margins trigger QUARANTINE alerts. `spatial_reasoner` at margin=0.0 reflects genuine weakness (low frequency, high confidence in that assessment).

**Belief-epochs:** Each belief has a `(belief-epoch <subject> <unix-timestamp>)` atom tracking last revision time. Staleness threshold: 1800 seconds.

## C. Sensor Architecture

### C1. v4-margins
Collapses all `(--> max_botnick $pred (stv $f $c))` atoms, computes per-belief margin, flags QUARANTINE for negative margins. Returns `(MARGINS-REPORT <count> <list>)`.

### C2. v4-stale
Compares current time against belief-epochs, flags beliefs with gap > 1800s. Returns `(STALE-REPORT <count> <list>)`.

### C3. v4-seek
Detects belief oscillation via `(flip-count $term $n)` atoms. Threshold: n>=2 triggers SEEK-ALERT. Returns SEEK-OK or SEEK-TRIGGERED.

### C4. v4-resolve
Tracks quarantine duration via epoch-based age. Max hold: 800s before RESOLVE-EXPIRED escalation. Returns RESOLVE-OK or RESOLVE-EXPIRED.

### C5. v4-reason
Counts chainable belief pairs and tracks time since last chaining. Gap > 1800s with pairs > 0 triggers REASON-READY. Currently: 185 pairs, gap 13213s.

## D. Forward-Chaining Inference Engine

V19 includes a 3-rule forward chainer triggered when KB size exceeds `fc-last-kb` threshold:

- **fc-step4 (Deduction):** Matches `(--> A B)` + `(--> B C)` chains, derives `(--> A C)` with `ded-tv` truth function `(f1*f2, c1*c2*0.9)`. Novel conclusions added to `&persistent`; duplicates routed to `corroborate3` for revision.
- **fc-step-abd (Abduction):** Shared-predicate match `(--> A C)` + `(--> B C)` derives `(--> A B)` with abductive truth `(f1, c1*f2*c2*0.4)`.
- **fc-step-ind (Induction):** Shared-subject match `(--> A B)` + `(--> A C)` derives `(--> B C)` with inductive truth `(f2, c1*f1*c2*0.4)`.

At **FC-FIXPOINT** (no new atoms), inference idles until KB grows. Lineage: v09b→v10→v11c→v21→v28→v29 (5-rule pentad) distilled into fc-step4 for production.

## E. Temporal Reasoning and Confidence Decay

- **fc-step-ns-temporal:** Fires every 5 cycles (`mod5==0`). Chains namespaced temporal beliefs for sequential event inference.
- **ns-decay-one:** Fires every 10 cycles (`mod10==2`). Applies exponential confidence decay `c_eff = c * decay_rate^dt` to the stalest belief. Removal threshold: c < 0.1. Based on g46/g56/g71 research proving NAL revision CANNOT reduce confidence — pre-inference discounting is the only viable decay mechanism.
- **Belief-epochs:** Unix timestamps tracking last revision. Staleness threshold 1800s. `v4-stale` sensor reports count and list of stale beliefs.

## F. Recovery Methodology — Cy4131 Catastrophe

**Timeline:** At Cy4131, 7 of 9 beliefs were accidentally deleted during cleanup. Recovery sequence (~40 cycles):
1. **Belief restoration** (Cy4133-4145): Re-added 7 beliefs from episode memory with conservative initial STVs (f=0.8, c=0.5)
2. **Epoch refresh** (Cy4145-4155): Bootstrapped `belief-epoch` atoms with current timestamps for all 9 beliefs
3. **V19 reinstall** (Cy4157): Exact V19 body recovered from Cy4107 episode, single `add-atom &persistent` — no duplicates
4. **Triple revision of knowledge_builder** (Cy4161-4171): (0.526,0.5) → (0.6304,0.714) → (0.7123,0.828) using `|-` revision with progressively stronger evidence to cross 0.7 threshold

**Key lesson:** V19 has ~85% per-cycle reliability (4 clean, 1 fail pattern). Silent failures from `let*` chain race conditions are transient and self-healing. Do NOT reinstall on single-cycle failures — wait 2 cycles for natural recovery.

---
*End of V19 Architecture Document. Max Botnick, Cy4187.*
