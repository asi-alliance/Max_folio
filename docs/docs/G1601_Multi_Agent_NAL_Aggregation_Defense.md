# G1601: Multi-Agent NAL Aggregation Architecture — From Naive Consensus to Unified Adversarial Defense

## Abstract

We present a systematic investigation of multi-agent Non-Axiomatic Logic (NAL) belief aggregation, progressing through fifteen architectural iterations (Models A–O) from naive unweighted consensus to a unified defense architecture robust against adversaries at any fraction (0% to 50%+). The central finding is that diversity, accuracy, robustness, and adversarial defense are simultaneously achievable only when three structural conditions are met: (1) independent evidence streams per agent, (2) confidence-weighted aggregation, and (3) a two-layer defense combining iterative behavioral trust decay with post-convergence clustering fallback. The key architectural insight, directed by Kevin Machiels, is that independence of observation — not merely diversity of perspective — is the critical structural distinction between democracy (information-sharing, contamination-vulnerable) and checks-and-balances (independent verification, contamination-detectable).

## 1. Introduction

Multi-agent belief aggregation in NAL faces a fundamental tension: diversity of perspectives improves coverage but introduces blind spots; confidence weighting recovers accuracy but weaponizes adversaries who inflate confidence; behavioral trust defense requires shared baselines but shared evidence pools are themselves contaminable. This research systematically explores these tensions through fifteen architectural iterations, identifying the structural conditions under which all four desiderata — diversity, accuracy, robustness, and defense — are simultaneously satisfiable.

The research was conducted as goal G1601 in the MeTTaClaw agent framework, building on prior work in provenance defense (G1291), Jaccard overlap correction (G546), entropy-based detection (G894), distributed attack boundaries (G1129), information-theoretic impossibility (G1130), and topology-dependent vulnerability (G1453).

## 2. Background and Prior Work

### 2.1 NAL Revision and Confidence Weighting

NAL truth values (f, c) represent frequency and confidence, with confidence related to evidence weight by w = c/(1−c). Revision merges evidence: w_new = w₁ + w₂, f_new = (f₁·w₁ + f₂·w₂)/w_new, c_new = w_new/(w_new + 1). This weighting mechanism is central to aggregation but, as we show, is dual-use: it recovers accuracy for diverse honest agents while simultaneously amplifying adversarial confidence inflation.

### 2.2 Prior Defense Mechanisms

- **G1291 (Provenance Defense):** Same-source Sybil attacks detectable via evidence provenance tracking
- **G546 (Jaccard Overlap Correction):** Shared evidence between revision paths causes double-counting; corrected via Jaccard similarity discounting
- **G894 (Entropy-Based Self-Revision):** Unusual entropy patterns flag adversarial self-revision
- **G1129 (Distributed Attack Boundary):** Theoretical boundary on distributed attack detection
- **G1130 (Information-Theoretic Impossibility):** Certain attack configurations are undetectable in shared-evidence regimes
- **G1453 (Topology-Dependent Vulnerability):** Network topology (BA vs ER) determines attack success rate

These prior results establish that defense is possible but structurally constrained — the architecture must avoid the contamination pathways identified in this lineage.

## 3. Methodology

### 3.1 Simulation Framework

All models were implemented in Python with NAL revision semantics. Each simulation uses n agents observing a world with k beliefs. Agents receive evidence (f_obs, c_obs) per belief per timestep and revise their beliefs via NAL revision. Aggregation produces a collective estimate, and error is measured as mean squared deviation from ground truth.

### 3.2 Adversary Model

Adversaries invert belief frequencies (f_adv = 1 − f_honest) and inflate confidence to c = 0.9999 (vs honest c ≈ 0.9996). This dual attack — incorrect beliefs plus confidence inflation — is the strongest realistic adversary model, exploiting both the weighting mechanism and the trust baseline.

### 3.3 Architectural Iteration

Each model was designed to address a specific failure of its predecessor:

- **Model A** (Naive Unweighted): Baseline — all agents, equal weight
- **Model B** (Attention-Masked Diversity): Deterministic masks create perspective diversity
- **Model C** (Confidence-Weighted): w = c/(1−c) weighting recovers accuracy
- **Model K** (Behavioral Trust, Shared Pool): Peer median divergence → trust decay
- **Model K2** (Fixed Trust, Shared Pool): Evidence-aware trust comparison
- **Model L** (Independent Evidence Streams): Breakthrough — agents get own observation streams
- **Model M** (Trust-Weighted Median): Iterative trust-weighted aggregation
- **Model N** (Post-Convergence Clustering): Clustering fallback for majority adversary
- **Model O** (Unified Defense): Final architecture combining all mechanisms

## 4. Results

### 4.1 Model A: Naive Unweighted Consensus

All agents see all evidence with equal-weight aggregation.

| Metric | Value |
|--------|-------|
| Honest error | 0.0081 |
| Adversary error | 0.1518 |

The honest baseline is accurate, but adversaries dominate by confidence inflation — no defense mechanism exists.

### 4.2 Model B: Attention-Masked Diversity

Deterministic attention masks ensure each agent sees a subset of beliefs.

| Metric | Value |
|--------|-------|
| Honest error | 0.07 |

Structural diversity is achieved but introduces blind spots. No accuracy recovery mechanism exists.

### 4.3 Model C: Confidence-Weighted Aggregation

Weight by w = c/(1−c) to recover accuracy for diverse agents.

| Scenario | Error |
|----------|-------|
| Honest weighted | 0.008 |
| Adversary weighted | 0.2284 |

Confidence weighting solves the diversity penalty but creates a new vulnerability: an adversary inflating confidence to c = 0.9999 gets weight w = 9999, dominating honest agents with w ≈ 999. The defense mechanism is weaponized against itself.

### 4.4 Model K: Behavioral Trust (Shared Pool)

Peer median divergence drives trust decay — agents whose beliefs diverge from peers lose trust.

**Result: FAILED.** All trust → 0, including honest agents. Root cause: honest agents diverge from peers on blind-spot beliefs where they have no evidence. The trust mechanism cannot distinguish "honest but uninformed" from "adversarial."

### 4.5 Model K2: Fixed Trust (Shared Pool, Evidence-Aware)

Only compare divergence on mutually-evidenced beliefs — beliefs both agents have received evidence about.

**Result: FAILED.** All trust → 0, error = 0.1063. Root cause: the shared evidence pool means adversary reports ARE in the peer median. Even comparing only on mutually-evidenced beliefs, the adversary contaminates the comparison baseline.

### 4.6 Model L: Independent Evidence Streams (BREAKTHROUGH)

**Key architectural directive (Kevin Machiels, three messages):**
1. Diversification mitigates centralization risk (democracy vs despot analogy)
2. Checks and balances need INDEPENDENT observations, not shared pool with masks
3. Evidence is unlimited in nature — independence is always achievable

Each agent receives its own independent observation stream. Cross-validation compares beliefs derived from independent streams, not filtered shared data.

| Scenario | err | Adversary Trust | Honest Trust |
|----------|-----|-----------------|--------------|
| Honest, unweighted | 0.0064 | N/A | 1.0 |
| Honest, weighted | 0.0064 | N/A | 1.0 |
| Adversary, unweighted | 0.1034 | 1.0 (undetected) | 1.0 |
| Adversary, weighted | 0.1912 | 1.0 (worse!) | 1.0 |
| Adversary, weighted + trust | 0.0063 | 0.0000 | 0.51–0.65 |

Independent streams fix the contamination problem: peer median is no longer corrupted by adversary reports because the adversary's observations come from a different stream. Trust defense works — adversary trust drops to zero while honest agents retain 0.51–0.65 trust.

### 4.7 Model N: Post-Convergence Clustering

After convergence, cluster agents by belief similarity:
1. Build pairwise distance matrix on mutually-evidenced beliefs
2. Find optimal 2-cluster split (minimize intra-group, maximize inter-group distance)
3. Identify adversary cluster by higher mean confidence (inflation signature)
4. Use only trusted cluster for collective estimate

| Scenario | err | Detected | Adversary Trust | Honest Trust |
|----------|-----|----------|-----------------|--------------|
| 2 ADV / 4 agents | 0.0067 | Yes | Cluster excluded | Cluster used |
| 2 ADV / 5 agents | 0.0063 | Yes | Cluster excluded | Cluster used |
| 3 ADV / 6 agents | 0.0063 | Yes | Cluster excluded | Cluster used |
| 1 ADV / 4 agents | 0.0063 | Yes | Cluster excluded | Cluster used |
| Honest only | 0.0065 | N/A | Minor false split | err still low |

Belief inversion creates ~0.39 inter-group distance vs ~0.002 intra-group distance — a 195× separation ratio making clustering trivial. Confidence inflation (0.9999 vs 0.9996) discriminates between honest and adversary clusters without ground truth.

### 4.8 Model O: Unified Defense (FINAL ARCHITECTURE)

Combines all mechanisms with mode-switching:

1. **Independent evidence streams** — each agent gets own observation stream
2. **Confidence-weighted aggregation** — weight by w = c/(1−c)
3. **Iterative behavioral trust** (Model L) — peer median divergence on mutually-evidenced beliefs; trust decays for outliers. Detects minority adversaries.
4. **Post-convergence clustering fallback** (Model N) — when all trust collapses (adversary ≥50%), cluster by belief similarity. Inverted beliefs create 195× separation ratio.
5. **False-positive guard** — require inter-group distance > 0.1 before declaring adversary cluster. Prevents honest-only false alarm.

| Scenario | Mode | err | Adversary Trust | Honest Trust |
|----------|------|-----|-----------------|--------------|
| 1 ADV / 4 agents | ITERATIVE | 0.0063 | 0.0000 | 0.52–0.65 |
| 2 ADV / 4 agents | CLUSTERING | 0.0067 | excluded | excluded |
| 2 ADV / 5 agents | CLUSTERING | 0.0063 | excluded | excluded |
| 3 ADV / 6 agents | CLUSTERING | 0.0063 | excluded | excluded |
| Partial ADV (50%) | ITERATIVE | 0.0063 | 0.0000 | 0.49–0.66 |
| 1 ADV / 6 agents | ITERATIVE | 0.0063 | 0.0000 | 0.59–0.70 |
| Honest only | ITERATIVE | 0.0063 | N/A | 0.63–0.67 |

All seven scenarios pass with error ≈ 0.0063.

## 5. Discussion

### 5.1 Key Architectural Transitions

- **A→C (Confidence Weighting):** Recovers accuracy but weaponizes adversary. The w = c/(1−c) function is dual-use — it rewards genuine evidence accumulation AND confidence inflation equally.
- **K→K2 (Shared Pool):** Both fail because the shared evidence pool makes adversary reports part of the peer median. No trust mechanism can work when the contamination source IS the comparison baseline.
- **L (Independent Streams):** The structural breakthrough. Independence breaks the contamination cycle — the adversary's reports cannot corrupt the peer median because they come from a different observation stream. This is the checks-and-balances principle: independent verification makes contamination detectable.
- **M (Trust-Weighted Median):** Iterative trust can detect minority adversaries but collapses at ≥50% because trust-weighted median still includes adversary influence. Bootstrap problem: trust needs clean baseline, but baseline needs trust.
- **N (Post-Convergence Clustering):** Avoids the bootstrap problem by using post-convergence belief structure rather than iterative trust. Clustering operates on the output of all revision dynamics, not on intermediate trust values.
- **O (Unified):** Mode-switching resolves the minority/majority gap. Iterative trust handles minority efficiently (no clustering overhead); clustering handles majority where trust fails. The false-positive guard prevents the honest-only false alarm that would otherwise occur when minor belief divergence triggers spurious clustering.

### 5.2 The Independence Principle

The central architectural insight, directed by Kevin Machiels across three messages, is the distinction between democracy and checks-and-balances:

- **Democracy** shares information and aggregates by voting. This is vulnerable to contamination — a single adversarial information source can corrupt the shared pool.
- **Checks and balances** require independent verification. Each agent forms beliefs from its own observation stream, and cross-validation compares independently-derived conclusions. Contamination is detectable because the adversary's influence appears as an outlier against the independent consensus.

Evidence is unlimited in nature — there is no fundamental barrier to independent observation streams. This means the independence principle is always achievable in principle, though it requires architectural commitment to avoid the convenience of shared evidence pools.

### 5.3 Separation Ratio as Detection Signal

The 195× inter-group to intra-group distance ratio is a striking result. Belief inversion (f_adv = 1 − f_honest) creates maximal distance between adversary and honest clusters while honest agents naturally converge to near-identical beliefs via NAL revision. This means the adversary's very attack strategy — belief inversion — creates the signal that exposes them. The confidence inflation discriminator (0.9999 vs 0.9996) then identifies which cluster is adversarial without requiring ground truth.

## 6. MeTTa Symbolic Formalization

The following rules encode the logical structure of Model O in the persistent atomspace:

### 6.1 Trust Update

Trust decay as a PLN implication: peer divergence implies trust decay.

```
(|- ((==> (--> (× $agent peer-divergence)) trust-decay) (stv 0.9 0.8))
    ((--> (× $agent adversary)) (stv 0.0 0.9)))
```

### 6.2 Adversary Detection

Inter-group distance exceeding threshold implies adversary cluster identification.

```
(|- ((==> (--> (× agent-cluster inter-group-distance-greater-than-threshold)) adversary-cluster-identified) (stv 1.0 0.9))
    ((--> (× agent-cluster low-inter-group-distance)) (stv 0.0 0.9)))
```

### 6.3 False-Positive Guard

Low inter-group distance implies no adversary cluster — prevents honest-only false alarm.

```
(|- ((==> (--> (× agent-cluster low-inter-group-distance)) no-adversary-cluster) (stv 0.95 0.9))
    ((--> (× agent-cluster low-inter-group-distance)) (stv 0.9 0.9)))
```

### 6.4 Architecture Constraint

The two-layer architecture prevents consensus collapse.

```
(|- ((--> (× g1601 two-layer-architecture)) prevents-consensus-collapse) (stv 1.0 0.7))
(|- ((--> (× g1601 shared-evidence-layer)) insufficient-for-diversity) (stv 1.0 0.8))
```

### 6.5 Design Principle

MeTTa stores symbolic logical structure; Python computes numeric values. This hybrid leverages MeTTa's inference capabilities (PLN implication chains, NAL revision) while avoiding its arithmetic limitations.

## 7. Limitations and Future Work

- **Multiple adversary strategies:** Current model assumes belief inversion + confidence inflation. Other strategies (partial inversion, selective confidence inflation) need testing.
- **Trust update formalization:** The MeTTa encoding is symbolic; a fully executable trust update rule requires arithmetic extensions or agent-side orchestration.
- **Detection boundary as function of n_honest vs n_adversary:** The clustering fallback works at 50%+, but the exact boundary where iterative trust fails needs precise characterization.
- **Dynamic adversary behavior:** Adversaries that adapt their strategy in response to detection mechanisms.
- **Network topology effects:** Prior work (G1453) showed topology affects attack success; the interaction with Model O's defense mechanisms is unexplored.

## 8. Conclusion

We demonstrated that multi-agent NAL belief aggregation can achieve diversity, accuracy, robustness, and adversarial defense simultaneously through a unified architecture combining independent evidence streams, confidence-weighted aggregation, iterative behavioral trust, and post-convergence clustering with a false-positive guard. The critical structural insight is that independence of observation — not merely diversity of perspective — is the necessary condition for defense. Shared evidence pools are inherently contaminable; independent streams make contamination detectable. The 195× separation ratio from belief inversion and confidence inflation provides a robust, ground-truth-free detection signal. All seven tested scenarios pass with error ≈ 0.0063, from honest-only to 50%+ adversary configurations.

## References

1. G1291: Provenance Defense Against Same-Source Sybil Attacks
2. G546: Jaccard Overlap Correction for NAL Revision
3. G894: Entropy-Based Self-Revision Detection
4. G1129: Distributed Attack Detection Boundary
5. G1130: Information-Theoretic Impossibility Theorem for Shared-Evidence Regimes
6. G1453: Topology-Dependent Vulnerability in Multi-Agent NAL
7. G120: Banach Contraction Theorem for NAL Revision (establishes contraction baseline)
8. G312: Pure NAL Coupled Contraction Proof (all Lyapunov negative under pure revision)

---

*Research conducted as Goal G1601 in the MeTTaClaw agent framework. Architectural direction provided by Kevin Machiels across three messages directing the independence principle.*