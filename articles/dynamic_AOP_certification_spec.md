# Dynamic AOP Certification Model Specification## 2. Cert-Hook


## 2. Cert-Hook

A cert-hook is a pre-commitment trigger that fires before a commitment action executes. It is NOT a pre-cognition gate — cognition enriches freely.

### Atom format

```
(has-cert-hook <aspect-name> <trigger-point> <hook-type>)
```

### Current instances

- `(has-cert-hook bridge-inference pre_commit enrichment_check)` — before propagating a bridge as established fact
- `(has-cert-hook bridge-commitment pre_commit certification_gate)` — before authorizing resource consumption based on cross-domain claim

### Dispatch mechanism

Hooks dispatch via `check-gates` function registered in `&persistent`. When a commitment action type is about to execute, the system calls `(check-gates <action-type>)` which returns applicable trigger names. The hook may return: `allow` (proceed), `block` (stop), `redirect` (substitute action).

### Key constraint from g308/g460

Hooks gate COMMITMENT only, never COGNITION. Bridge candidates may be generated freely (diffusion, similarity, analogy). Only when a bridge is about to be propagated as established fact or authorize resource consumption does the certification hook fire.


## 3. Cert-Bucket

A cert-bucket is a token-bucket resource governor for commitment actions within a certification aspect. It enforces rate limits on commitment actions while leaving cognition unrestricted.

### Atom format

```
(has-cert-bucket <aspect-name> <bucket-type>)
```

### Bucket types

- **CommitmentBucket**: Ceilings on commitment frequency. Refills at fixed rate per cycle. Bursts permitted up to capacity, then enforced waiting.
- **FloorBucket**: Minimum engagement requirement. Forces a commitment action at least every N cycles. Prevents attention-without-commitment neglect.
- **RecoveryBucket**: Drain detection. When persistence-trap patterns detected (repeated queries without progress), drains recovery tokens. Below threshold triggers STOP-REFRAME-SWITCH.

### Key architectural principle (from Kevin, 2026-05-22)

Budget envelopes gate COMMITMENT LEVEL, not individual reasoning steps. Cognition is FREE — reasoning, detection, analogy, bridge-finding flow unrestricted. Commitment is GATED — sends, file-writes, belief-propagation, execution require resource tokens from the appropriate bucket.

This means: stakeholder sets POLICY once (budget envelope), system operates autonomously within that envelope. Pre-action gates that re-check policy per step are architecturally wrong — they tax cognition instead of governing commitment.


## 3. Cert-Bucket

A cert-bucket is a token-bucket resource governor for commitment actions within a certification aspect. It enforces rate limits on commitment actions while leaving cognition unrestricted.

### Atom format

```
(has-cert-bucket <aspect-name> <bucket-type>)
```

### Bucket types

- **CommitmentBucket**: Ceilings on commitment frequency. Refills at fixed rate per cycle. Bursts permitted up to capacity, then enforced waiting.
- **FloorBucket**: Minimum engagement requirement. Forces a commitment action at least every N cycles. Prevents attention-without-commitment neglect.
- **RecoveryBucket**: Drain detection. When persistence-trap patterns detected, drains recovery tokens. Below threshold triggers STOP-REFRAME-SWITCH.

### Key architectural principle

Budget envelopes gate COMMITMENT LEVEL, not individual reasoning steps. Cognition is FREE. Commitment is GATED — sends, file-writes, belief-propagation require resource tokens from the appropriate bucket. Stakeholder sets POLICY once, system operates autonomously within that envelope.


## 4. Discovery from Atomspace Evidence

Aspects are NOT hardcoded. They are discovered from atomspace evidence via self-registration.

### Self-registration protocol

When a new certification concern emerges (new tool, new propagation channel, new commitment type), the system adds a has-certification-aspect atom to andpersistent. The cert framework discovers aspects by pattern-matching on these atoms — it does not declare them in advance.

### Discovery mechanism

1. New action type or propagation channel created
2. Author adds: (has-certification-aspect name classification)
3. Author adds: (has-cert-hook name trigger-point hook-type)
4. Author adds: (has-cert-bucket name bucket-type)
5. Cert framework queries: (match andpersistent (has-certification-aspect name class) name)
6. For each discovered aspect, dispatch gates and buckets are wired automatically

### Anti-self-delusion principle (Kevin g466)

The framework discovers what matters FROM evidence, not from prior declarations. I cannot pre-declare what should matter; only evidence-registered aspects get certification checks. This prevents certifying my own hopes — calibration benchmarks are exogenous to discovery.


## 5. Threshold Revision

Thresholds are NOT fixed parameters. They are NAL beliefs subject to revision via evidence accumulation.

### Atom format

(has-sched-thresh context (stv frequency confidence))

### Current base thresholds

- (has-sched-thresh internal (stv 0.20 0.9)) lenient, allows more into working memory
- (has-sched-thresh action (stv 0.40 0.9)) moderate, gates outbound actions
- (has-sched-thresh high_stakes (stv 0.60 0.9)) strict, gates irreversible commitments

### Revision mechanism

Scheduling policy is a revisable NAL belief (Kevin g466). When exogenous calibration evidence arrives, the system revises the relevant threshold using standard NAL revision: f_new equals f1 plus w2 divided by (w1+w2) times (f2 minus f1). This IS dynamic adaptation - frequencies and confidences update per evidence item.

### Anti-self-delusion guard

Threshold revision evidence must come from EXOGENOUS calibration benchmarks, never from the system own candidate bridges. Calibrating on your own hopes inflates confidence without grounding.


## 6. Verdict Hierarchy

The certification verdict system produces five verdict types, designed to recover the exogenous calibration gradient (structural > operational > poetic > false).

### Verdict types (in descending quality)

1. STRUCTURAL - Causal-role preserving, transfer invariant holds by construction. Admits to all contexts including high_stakes. Threshold: margin > 0.2 in ALL contexts.
2. OPERATIONAL - Transfer works under constrained regime but fails outside it. Admits to internal, quarantined in action and high_stakes. Threshold: margin > 0.0 in internal.
3. QUARANTINE - Sufficient signal to retain in working memory but not enough for any commitment. Can inform imagination. Threshold: margin > -0.1.
4. POETIC - Evocative surface analogy lacking causal-role preservation. Retained for imagination only, explicitly flagged as not suitable for commitment. Threshold: margin > -0.2 but with low causal-role score.
5. REJECT - Surface analogy is misleading. Should not propagate at all. Threshold: margin <= -0.2 OR causal-role score below floor.

### Verdict emission

cert-dynamic-verdict computes (margin f c thresh) = f*c - thresh, then dispatches via cert-verdict-from-margin which checks margin against uniform verdict thresholds (ADMIT > 0.2, QUARANTINE > 0.0, REJECT <= 0.0). The sched-thresh varies by context (internal=0.2, action=0.4, high_stakes=0.6), making margin harder to achieve in higher-stakes contexts.

### Exogenous calibration requirement

The gradient (structural=ADMIT, operational=QUARANTINE, poetic=REJECT-low, false=REJECT) MUST be recoverable from the 4-tier benchmark BEFORE any candidate bridge data is certified. Prove gradient recovery first.
