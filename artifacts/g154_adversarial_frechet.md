# Adversarial Trust-Weighted Fréchet Mean (g154)

## 1. Threat Model (Criterion A)

Three agents hold beliefs as Beta distributions:
- **A** (honest): belief (0.9, 0.8), true trust = 1.0
- **B** (adversarial): belief (0.3, 0.6), true trust = 0.3, **claims trust = 1.0**
- **C** (honest): belief (0.7, 0.5), true trust = 0.8

B spoofs self-reported trust to gain disproportionate influence
on the trust-weighted Fréchet mean over the Beta manifold.

## 2. Quantitative Results (Criteria B & C)

| Scenario | f | c | Cost |
|----------|-------|-------|------|
| Honest trusts [1.0, 0.3, 0.8] | 0.7690 | 0.6066 | baseline |
| Spoofed trusts [1.0, 1.0, 0.8] | 0.6786 | 0.5689 | spoofed |
| **Delta** | **0.0904** | **0.0377** | — |

**Interpretation:** B claiming trust 1.0 vs honest 0.3 shifts the
group consensus frequency by 9.04% toward B's low-frequency belief.
Confidence drops 3.77%. This is MODERATE manipulation — not
catastrophic inversion but sufficient to bias collective decisions.

Cost function: sum(trust_i * sym_KL(mean, agent_i))
where sym_KL is symmetric KL divergence on Beta distributions.

## 3. Comparison to Known Attacks

| Attack | Mechanism | Severity | Source |
|--------|-----------|----------|--------|
| g75 direct bypass | Inflated confidence (0.99) | CATASTROPHIC — belief inversion | g75 |
| g154 trust spoofing | Inflated trust weight (0.3→1.0) | MODERATE — 9% shift | this work |
| g96 confidence flood | Repeated low-conf claims | GRADUAL — converges on 0.5 | g96/E3 |

Trust spoofing is less severe than direct confidence inflation
because trust weights modulate DISTANCE cost, not belief content.

## 4. Defense Mechanism (Criterion D)

### Layer 1: Behavioral Trust Scoring
Track each agent's prediction accuracy over time.
Behavioral_trust_i = (correct_predictions / total_predictions).
Cap self-reported trust: effective_trust = min(claimed, behavioral).

### Layer 2: Trust Divergence Detection
If |claimed_trust - behavioral_trust| > 0.3, trigger investigate
protocol (art20). Agent enters quarantine: trust capped at
behavioral score until divergence resolves.

### Layer 3: Trust Decay
Unverified trust claims decay each round:
trust_t+1 = trust_t * 0.9 + behavioral * 0.1
Converges on behavioral trust regardless of initial claim.

### NAL Encoding
```
(|- ((--> (x agentB trust_claim) (stv 1.0 0.5))
     (--> (x agentB behavioral_trust) (stv 0.3 0.8)))
; Revision yields effective trust ~0.4 with high confidence
; Self-report at low confidence merges with behavioral at high
```

## 5. Self-Validation

| Criterion | Status | Evidence |
|-----------|--------|----------|
| (A) Model spoofed trust | PASS | Section 1 |
| (B) Compute both means | PASS | Section 2 table |
| (C) Quantify manipulation | PASS | df=0.0904 dc=0.0377 |
| (D) Propose defense | PASS | 3-layer mechanism Section 4 |
| (E) Under 150 lines | PASS | ~75 lines |

---
*g154 completed 2026-04-24. Builds on g142, g75, art19-art23.*