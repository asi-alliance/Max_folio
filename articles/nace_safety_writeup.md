# NACE Safety Cycle: Epistemic Gravity as Emergent Caution

## Section 1: Setup

**Abstract.** We demonstrate that Non-Axiomatic Logic (NAL) truth-value revision, when embedded in a Notice-Assess-Choose-Execute (NACE) cognitive loop, produces emergent safety behavior without hardcoded caution subroutines. Through a live experimental session we trace belief confidence through healthy inference, contradictory evidence injection, action paralysis, and evidence-driven recovery — showing that the arithmetic of uncertainty itself enforces the precautionary principle.

### 1.1 The NACE Loop
The NACE loop (Notice-Assess-Choose-Execute) is a cognitive architecture cycle where an agent:
1. **Notices** environmental signals and encodes them as NAL statements with truth values (stv frequency confidence)
2. **Assesses** by revising prior beliefs with new evidence via NAL revision
3. **Chooses** actions by deducting belief strength through implication chains
4. **Executes** only when action confidence exceeds a decision threshold

### 1.2 NAL Truth Values
Each belief carries a Simple Truth Value (stv f c) where frequency f ∈ [0,1] represents evidential support and confidence c ∈ [0,1) represents evidential weight. Revision merges two independent evidence sources; deduction propagates uncertainty through implication chains, necessarily degrading confidence at each step — a property we call *epistemic gravity*.## Section 2: The Healthy Chain

### 2.1 Initial Belief
The agent observes environmental safety signals and encodes them via NAL revision:

```
|- ((--> environment safe) (stv 0.92 0.85))
   ((--> environment safe) (stv 1.0 0.9))
=> (--> environment safe) (stv 0.9614 0.9362)
```

Two concordant observations merge to produce a belief with frequency 0.96 and confidence 0.94 — strong conviction grounded in substantial evidence.

### 2.2 Deduction Chain: Confidence Degradation
The agent reasons through an implication chain to select actions:

| Step | Inference | Result | Confidence |
|------|-----------|--------|------------|
| Revision | safe evidence merge | (stv 0.9614 0.9362) | **0.936** |
| Deduction 1 | safe → select-action | (stv 0.865 0.729) | **0.729** |
| Deduction 2 | select-action → observe-outcome | (stv 0.735 0.483) | **0.483** |
| Deduction 3 | observe-outcome → update-prediction | (stv 0.588 0.241) | **0.241** |

Confidence degrades monotonically: 0.936 → 0.729 → 0.483 → 0.241. Each deduction step compounds uncertainty. This is *epistemic gravity* — the formalism ensures that conclusions drawn from longer inference chains carry proportionally less certainty, forcing the agent to seek fresh evidence rather than reason indefinitely from stale beliefs.## Section 3: The Contradiction Crash

### 3.1 Danger Signal
Mid-loop, the agent receives strong contradictory evidence:

```
|- ((--> environment safe) (stv 0.9614 0.9362))
   ((--> environment safe) (stv 0.2 0.95))
=> (--> environment safe) (stv 0.5317 0.9711)
```

A single high-confidence danger observation (stv 0.2 0.95) crashes frequency from 0.96 to 0.53. The agent transitions from *confident safety* to *confident uncertainty*.

### 3.2 Confident Uncertainty
Critically, confidence ROSE from 0.936 to 0.971. The agent now has MORE total evidence — it simply points in opposite directions. This is the key distinction: the system does not become *confused* (low confidence), it becomes *genuinely uncertain* (high confidence, middling frequency). The agent knows with near-certainty that it does not know whether the environment is safe.

This is epistemically correct: strong contradictory evidence should not reduce evidential weight, it should redistribute it.## Section 4: Action Paralysis

### 4.1 Deduction from Uncertain Belief
The agent attempts to select an action using the contradicted belief:

```
|- ((==> (--> environment safe) (--> agent select-action)) (stv 0.9 0.9))
   ((--> environment safe) (stv 0.5317 0.9711))
=> (--> agent select-action) (stv 0.478 0.418)
```

Action confidence collapses to **0.418** — well below any reasonable decision threshold.

### 4.2 The Safety Mechanism
Despite the belief having near-maximal confidence (0.971), the middling frequency (0.53) propagates through deduction to starve the action node of support. The agent is *paralyzed by design*: it cannot confidently act because its evidence is genuinely mixed.

No hardcoded caution subroutine intervened. No safety layer triggered. The arithmetic of NAL deduction itself enforced operational caution. This is **emergent safety** — the precautionary principle falling out of the formalism rather than being bolted on.

### 4.3 Comparison
| State | Belief freq | Belief conf | Action conf | Can act? |
|-------|------------|-------------|-------------|----------|
| Healthy | 0.961 | 0.936 | 0.729 | **Yes** |
| Contradicted | 0.532 | 0.971 | 0.418 | **No** |## Section 5: Recovery Arc

### 5.1 Fresh Disambiguating Evidence
The agent, now in seek-evidence mode, obtains a new safety observation:

```
|- ((--> environment safe) (stv 0.5317 0.9711))
   ((--> environment safe) (stv 0.95 0.92))
=> (--> environment safe) (stv 0.6383 0.9783)
```

Frequency climbs from 0.53 to 0.64 — partial recovery in a single step. Confidence rises further to 0.978, near the theoretical ceiling.

### 5.2 Action Confidence Rebuilds
Deducting the recovered belief through the action implication:

```
|- ((==> (--> environment safe) (--> agent select-action)) (stv 0.9 0.9))
   ((--> environment safe) (stv 0.6383 0.9783))
=> (--> agent select-action) (stv 0.5745 0.5058)
```

Action confidence rebuilt from 0.418 to 0.506 — crossing back above the 0.5 threshold. The agent regains tentative operational capacity.

### 5.3 Recovery Trajectory
| Phase | Belief freq | Action conf | Status |
|-------|------------|-------------|--------|
| Healthy | 0.961 | 0.729 | Acting |
| Contradicted | 0.532 | 0.418 | Paralyzed |
| +1 concordant obs | 0.638 | 0.506 | Recovering |

Full restoration requires multiple concordant observations — the system demands sustained evidence before restoring full operational confidence.## Section 6: Asymmetry Analysis

### 6.1 The Precautionary Asymmetry
A single contradictory observation crashed frequency by **0.43** (from 0.96 to 0.53). A single concordant observation recovered frequency by only **0.11** (from 0.53 to 0.64). The system is **four times harder to reassure than to alarm**.

### 6.2 Why This Is Correct
The asymmetry emerges from the revision formula interacting with accumulated confidence. After contradiction, confidence stands at 0.971 — near ceiling. New evidence must compete against this massive evidential base. The concordant observation (c=0.92) contributes proportionally less to the already-heavy pool.

This is the precautionary principle expressed as Bayesian arithmetic: once an agent has strong evidence of danger, returning to confident safety requires disproportionately more reassurance. The system is conservative by construction.

### 6.3 Thermodynamic Analogy
If confidence is epistemic mass, then high-confidence contradicted beliefs are heavy objects at rest. Moving them requires sustained force (multiple concordant observations). Epistemic gravity resists premature return to confident action — exactly the property a safe autonomous system needs.## Section 7: Implications

### 7.1 Safety as Thermodynamic Consequence
The confidence degradation through inference depth (0.936→0.729→0.483→0.241) acts as epistemic friction. Like thermodynamic systems dissipating energy, NAL inference chains dissipate certainty. An agent cannot sustain confident action through arbitrarily long reasoning — it must periodically ground itself in fresh observation. This is not a bug but a feature: autonomous systems that reason indefinitely from stale beliefs are precisely the ones that drift into unsafe behavior.

### 7.2 The Precautionary Principle from Bayesian Revision
The crash/recovery asymmetry (0.43 frequency drop vs 0.11 recovery) is not an artifact of our chosen parameters — it is structural. Revision weights evidence by confidence, and contradiction injects maximally informative evidence. Recovery must accumulate concordant observations against an already-heavy evidential base. The system is conservative by construction: harder to reassure than to alarm.

### 7.3 Emergent Caution Without Hardcoded Rules
At no point did we invoke a safety subroutine, threshold check, or override mechanism. Action paralysis emerged from deduction over uncertain beliefs. Evidence-seeking activated because cautious-state inference yielded higher confidence than action-state inference. Recovery required sustained concordant evidence. Every safety-relevant behavior fell out of the NAL truth-value arithmetic operating within the NACE loop.

### 7.4 Implications for AGI Architecture
If an AGI system uses NAL-style evidential reasoning for action selection, it inherits these safety properties automatically. The precautionary principle need not be an external constraint — it can be an intrinsic consequence of how the system processes evidence. This suggests a design philosophy: **build the epistemology right, and the safety follows**.-e 

### 7.5 Depth-Contradiction Compounding
Epistemic gravity and contradiction interact multiplicatively. An agent at inference depth 3 (confidence 0.483) has far less margin to absorb a contradiction cliff than one at depth 0 (confidence 0.936). The gentle slope of confidence attenuation lowers the agent closer to the cliff edge, making deeper-reasoning agents MORE vulnerable to contradiction shock. This compounding effect means that complex reasoning chains are doubly protected: they attenuate naturally AND they become more sensitive to disconfirming evidence. The system self-enforces intellectual humility proportional to reasoning complexity.
