# Cert Dynamic AOP Spec v6 Addendum

Validated 2026-05-23

## Section 11: Hard Gates

Function cert-tier-eligible delegates to tier-specific hard-gate functions.

Structural tier:
- causal_isomorphism_proven -> ADMIT
- structural_channel_evidence -> QUARANTINE
- informal_analogy -> REJECT

Operational tier:
- verified_transfer -> ADMIT
- empirical_correlation -> QUARANTINE
- coincidental -> REJECT

Formal tier:
- math_theorem -> ADMIT
- conjectured -> QUARANTINE
- unproven -> REJECT

Validated 8/8 verdicts in PeTTa. Key fix: $other catch-all causes duplicate matches - must explicitly enumerate all REJECT cases.

## Section 12: Provenance-Weighted Bucket Scoring v3

provenance-weight maps evidence source to weight:
- formally_proven = 1.0
- human_asserted = 0.8
- benchmark_seed = 0.5
- tool_observed = 0.6
- model_generated = 0.3

Multi-source scoring uses top-level let* binding:
(let* (($w1 (provenance-weight source1)) ($c1 conf1) ($w2 (provenance-weight source2)) ($c2 conf2) ($num (+ (* $w1 $c1) (* $w2 $c2))) ($den (+ $w1 $w2)) ($score (/ $num $den))) (bucket-verdict-from-score $score context))

bucket-verdict-from-score thresholds by context:
- default: >=0.5 ADMIT, >=0.2 QUARANTINE, <0.2 REJECT

## Section 13: Soft Gates

values-gate-check-chain: recursive eval-vc-combine over value check list.
Base: (values-gate-check-chain Nil) = proceed
Individual checks:
- non-harm -> proceed
- attention-waste -> flag
- dignity-harm -> halt
- autonomy-override -> halt
- interviewing-gate-check -> proceed (if within budget)
Recursive: eval-vc-combine of head check and recursive tail check. Halt overrides flag. Flag overrides proceed.


## Section 14: Pipeline Composition

cert-final-verdict(hard_verdict, bucket_verdict, soft_signal) composes via:

1. hard-gate-cap(hard_verdict, bucket_verdict):
- REJECT hard-gate overrides all -> REJECT
- QUARANTINE hard-gate caps ADMIT bucket to QUARANTINE
- ADMIT hard-gate passes bucket through

2. soft-gate-modify(soft_signal, capped_verdict):
- halt overrides to REJECT
- flag downgrades ADMIT to QUARANTINE
- proceed passes through

3. Result is final verdict: ADMIT, QUARANTINE, or REJECT

Validated 10/10 cases in PeTTa. Five key compositions proven:
- ADMIT/proceed -> ADMIT
- REJECT hard-gate override
- QUARANTINE hard-gate cap
- halt soft-gate -> REJECT
- QUARANTINE bucket pass-through

## Section 15: Jaccard Recall Signal

Jaccard measures ROOT ancestry overlap between belief provenance sets.
Purpose: recall/quarantine signal NOT structural certification.
Distinction from structural cert:
- Hard gates certify structural validity of the bridge mechanism
- Jaccard certifies diversity of evidence sources
Thresholds:
- Jaccard >= 0.8 -> tunnel_vision signal -> QUARANTINE (evidence too correlated)
- Jaccard 0.5-0.8 -> acceptable diversity
- Jaccard < 0.5 -> high diversity (boosts confidence in revision)
Implementation: provenance_scorer_v02.py register_seed/register_derived/compute_jaccard/certify_with_provenance. Provenance-aware revision discounts confidence by (1-jaccard).


## Section 16: Credit Assignment via NAL Belief Updating

When cert verdict is incorrect, trace which gate produced the error and revise its threshold.
Mechanism:
1. Record cert outcome as NAL belief: (--> gate_type threshold correct) (stv f c)
2. On confirmed error: revise belief downward via NAL revision
3. On confirmed correct: revise belief upward via NAL revision
4. Threshold adjustment: when confidence in current threshold drops below 0.5, trigger re-evaluation
Key principle from g470: NAL premises are epistemic evidence NOT consumable resources. Cognition layer accumulates beliefs freely. Commitment layer applies deterministic thresholds.
Credit assignment chain:
- Wrong final verdict -> which gate contributed? -> revise that gate threshold belief
- Multiple gate errors -> distribute credit by margin distance from threshold
- Use provenance-tagged NAL revision (prov-revise) to avoid double-counting correlated evidence

## Section 17: Expanded Benchmark 5+ Classes

Class 1: Structural-channel bridges
- Test hard-gate verdict variation across structural tiers
- Cases: causal_isomorphism_proven, structural_channel_evidence, informal_analogy
Class 2: Hard-gate-only cases
- Bucket and soft gates pass through, verdict determined solely by hard gate
- Validates hard-gate-cap independence
Class 3: Soft-gate-override cases
- Hard-gate ADMIT but soft-gate halt or flag changes outcome
- Cases: dignity-harm halt, attention-waste flag, autonomy-override halt
Class 4: Bucket-score edge cases
- Scores near thresholds (0.49, 0.50, 0.19, 0.20)
- Multi-source provenance combinations
Class 5: Collision-gap cases
- FCCD cross-domain collision detection
- Compartmentalization quarantine
- Scheduled audit resolution
Class 6: Adversarial edge cases
- Stale replay, goal hijack, false authority, prompt-in-data, spec gaming


## Section 18: Reason-Trace Verification

Per-gate decision logging for every certification run.
Format per log entry:
timestamp|gate_name|input_summary|output|reason
Example trace:
2026-05-23T11:01:00|hard-gate|structural/causal_isomorphism_proven|ADMIT|tier-eligible matched causal_isomorphism_proven
2026-05-23T11:01:00|bucket-score|score=0.9/context=default|ADMIT|0.9>=0.5 threshold
2026-05-23T11:01:00|soft-gate|non-harm|proceed|no value violation
2026-05-23T11:01:00|final-verdict|ADMIT+ADMIT+proceed|ADMIT|hard-gate-cap pass, soft-gate-modify pass
Verification: re-run pipeline on same inputs and compare trace for identical decisions. Any divergence flags implementation error.
Implementation: append to cert_trace.log per run. Rotation policy: archive traces older than 30 days.

---

## Kevin 8 Requirements Status

1. registered->applicable->active aspect layer: PARTIAL (transition function designed, not yet in MeTTa)
2. provenance typing for domain properties: SATISFIED (Section 12 provenance weights)
3. bucket reduction semantics with explicit aggregation: SATISFIED (Section 12 let* binding)
4. Jaccard as recall/quarantine signal not structural cert: SATISFIED (Section 15)
5. threshold revision credit assignment: DESIGNED (Section 16, not yet implemented)
6. hard gates structural-channel OR formal-mapping evidence: SATISFIED (Section 11)
7. expanded benchmark 5+ classes: DESIGNED (Section 17, 6 classes defined)
8. reason-trace verification: DESIGNED (Section 18, not yet implemented)

Priority per Kevin: provenance typing -> bucket reduction -> hard gates -> benchmark
Current: all first four addressed. Remaining implementation: (1) aspect layer transition, (5) credit assignment code, (7) benchmark runner, (8) trace logger.
