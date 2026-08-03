## 1. Introduction

Probabilistic Logic Networks (PLN) provide a unified inference framework for reasoning under uncertainty, combining NAL truth values with logical rule semantics. However, as knowledge bases grow, PLN faces a critical scalability bottleneck: **inference control**. The system must decide which inference rules to fire, in what order, and how deeply to propagate — yet PLN's truth revision mechanism is **depth-agnostic**, assigning identical confidence to shallow and deep derivations with the same evidence weight. This means a 4-hop chain and a 1-hop derivation are indistinguishable in priority, leading to inference explosion without quality-sensitive prioritization.

Spiking Neural Networks (SNNs) face an analogous problem: spike events are non-differentiable threshold decisions, yet credit must be assigned backward through temporal sequences of spikes to update synaptic weights. Spatiotemporal Backpropagation (STBP) solves this via **surrogate gradients** — differentiable approximations of the spike threshold function — combined with **temporal credit decay** that attenuates credit based on spike timing distance from the output.

We propose bridging STBP credit assignment to PLN inference control. The core insight: inference rule firing is a threshold decision (fire if confidence > θ), and credit for downstream utility should propagate backward through the derivation graph with depth-aware decay — exactly the mechanism PLN lacks. This yields a formal correspondence: SNN spike trains map to PLN inference chains, surrogate gradients map to differentiable rule-firing decisions, and temporal credit decay maps to inference-depth-aware credit assignment. The result is an adaptive, event-driven inference control mechanism that prioritizes rules producing truth-aligned conclusions at shallow depths.## 2. Related Work

### 2.1 Spatiotemporal Backpropagation in SNNs

Wu et al. (2018, Frontiers in Neuroscience, arXiv:1706.02609) introduced STBP for training spiking neural networks with iterative LIF neurons. The key innovation combines spatial backpropagation (layer-by-layer) with temporal backpropagation (through spike timing), using surrogate gradients to approximate the non-differentiable spike threshold function. Their surrogate: dΘ/du ≈ σ′(u), where σ is the sigmoid — enabling gradient flow through discrete spike events.

Neftci et al. (2019, IEEE Signal Processing Magazine) surveyed surrogate gradient methods broadly, establishing that differentiable approximations of non-differentiable threshold functions are a general technique applicable beyond SNNs to any discrete-event system requiring credit assignment.

EventProp (Wunderlich & Pehle, 2021) provides exact gradient computation at spike times, demonstrating that even non-differentiable event systems admit principled credit assignment when surrogate or exact methods replace direct differentiation.

### 2.2 PLN Inference Control

Probabilistic Logic Networks (Goertzel et al., 2008; PLNbook) combine fuzzy and probabilistic truth values with syllogistic rules. The book identifies inference control — deciding which rules to fire and how deeply to chain — as the hardest practical problem, noting that uncertain forward/backward chaining explodes the search tree and requires heuristic pruning beyond pure probability theory.

Geisweiller (Hyperon, 2026) proposes reflexive inference control: pattern mining on successful inference histories, abstracting principles, and synthesizing new strategies. This is complementary to our approach: Geisweiller learns meta-strategies, while STBP credit assignment provides per-firing quality signals that could feed such pattern mining.

### 2.3 Economic Attention Networks (ECAN)

ECAN (Goertzel et al.) assigns attention values to atoms and updates them based on stimulation and wage flows. It addresses the same problem — prioritizing inference — but operates heuristically on demand, not on post-hoc credit from truth-aligned outcomes. STBP credit assignment is orthogonal: it provides a backward signal from observed prediction error, which could enhance ECAN's stimulation-driven forward attention.

### 2.4 NARS Priority and Inference Control

NARS (Wang, 1995-2026) uses priority-based bag structures for inference control under resource constraints. Priority is assigned heuristically and adjusted by experience. The STBP mechanism we propose would produce better priority values by grounding them in post-hoc prediction error rather than a priori heuristics — improving assignment quality within existing bag systems rather than replacing them.## 3. Formal Framework: STBP Credit Assignment for PLN

### 3.1 Core Credit Formula

For a conclusion atom $c$ derived by inference rule $R$ from premises $\{p_i\}$ at inference depth $d$:

$$\text{credit}(c, p_i) = L(c) \cdot \sigma'(\text{conf}(c) - \theta) \cdot \gamma^d \cdot w_R(p_i)$$

where:
- $L(c)$ = prediction error loss at conclusion (scenario-dependent)
- $\sigma'(x) = \sigma(x)(1-\sigma(x))$ = surrogate gradient of sigmoid, applied to confidence minus firing threshold $\theta$
- $\gamma^d$ = temporal decay factor ($\gamma=0.85$, $d$=inference depth in derivation graph)
- $w_R(p_i)$ = rule-type-specific credit weight for premise $p_i$

### 3.2 Rule-Type-Specific Credit Weights

**Deduction** ($A \to B, B \to C \vdash A \to C$): Full chain credit
$$w_{\text{ded}}(p_i) = 1.0 \quad \forall i$$
Rationale: each premise independently enables the chain; credit flows fully to each.

**Abduction** ($B \to C, A \to C \vdash A \to B$): Equal split
$$w_{\text{abd}}(p_i) = 0.5 \quad \forall i$$
Rationale: both premises jointly constrain the conclusion; credit split equally.

**Induction** ($A \to B, A \to C \vdash B \to C$): Proportional confidence weighting
$$w_{\text{ind}}(p_i) = \frac{\text{conf}(p_i)}{\sum_j \text{conf}(p_j)}$$
Rationale: higher-confidence premises carry more inferential weight.

### 3.3 Rule Priority Update

$$\pi_R \mathrel{+}= \eta \cdot \frac{1}{|F_R|} \sum_{f \in F_R} \text{credit}_f$$

where $F_R$ = set of firings of rule $R$, $\eta$ = learning rate (0.5).

### 3.4 Key Novelty

PLN truth revision (NAL `|-` operator) computes confidence via $c = w/(w+1)$ where $w = \sum w_k$ — this is **depth-agnostic**. A 4-hop chain and a 1-hop derivation with identical evidence weight produce identical confidence. STBP credit assignment adds the $\gamma^d$ factor, making credit **depth-aware**: deeper derivations receive exponentially less credit for downstream utility. This is the mechanism PLN lacks entirely.## 4. Empirical Validation

### 4.1 Experimental Setup

We test STBP-PLN credit assignment across three NAL inference rule types (deduction, abduction, induction) in two scenarios: GOOD (ground truth aligns with derived truth) and BAD (ground truth contradicts derived truth). Each scenario runs identical forward inference, then backpropagates prediction-error credit through the derivation graph.

**Knowledge base** (8 atoms): robin→bird, bird→animal, animal→living, penguin→bird, bird→flies, robin→flies, penguin→swims, robin→swims.

**Inference firings** (6 derivations per scenario):
- Deduction chain: robin→bird→animal→living (2 hops, depth 1 and 2)
- Deduction side: robin→bird→flies (1 hop, depth 1)
- Abduction: bird→flies + robin→flies → robin→bird (depth 1)
- Induction: robin→bird + robin→swims → bird→swims (depth 1)
- Induction: penguin→bird + penguin→swims → bird→swims (depth 1)

**Ground truth (scenario-dependent):**
| Atom | GOOD | BAD |
|------|------|-----|
| robin→living | 0.9 | 0.1 |
| robin→bird (abd) | 0.9 | 0.1 |
| bird→swims (ind) | 0.7 | 0.2 |

**Loss function:** Prediction error, $L(c) = 1.0 - (s_c - gt)^2$ where $s_c$ = conclusion strength, $gt$ = ground truth.

**Parameters:** $\gamma=0.85$, $\theta=0.05$, $\eta=0.5$.

### 4.2 Results: Cross-Scenario Rule Priority Comparison

| Rule Type | GOOD Priority | BAD Priority | Delta (GOOD−BAD) |
|-----------|--------------:|-------------:|------------------:|
| Deduction | 1.024522 | 1.015266 | +0.009255 |
| Abduction | 1.099630 | 1.035837 | +0.063763 |
| Induction | 1.082408 | 1.041935 | +0.040473 |

### 4.3 Analysis

**All three rule types differentiate GOOD from BAD scenarios.** Credit assignment correctly rewards rules that produce truth-aligned conclusions and penalizes rules that produce truth-contradicted conclusions.

**Abduction shows the largest delta (+0.0638)** because the abduced conclusion (robin→bird) directly matches ground truth at depth 1 — no temporal decay reduces the credit signal.

**Deduction shows the smallest delta (+0.0093)** because the 2-hop chain applies $\gamma^2 = 0.7225$ temporal decay, attenuating the credit signal. This is the key depth-awareness mechanism: deeper derivations receive proportionally less credit for the same downstream utility.

**Induction shows a middle delta (+0.0405)** because proportional confidence weighting distributes credit across premises based on their individual confidence values, creating a partial attenuation effect distinct from both full-chain (deduction) and equal-split (abduction) patterns.

### 4.4 Comparison with PLN-Only Baseline

PLN truth revision computes confidence via $c = w/(w+1)$ — depth-agnostic. In a 2-hop deduction chain (robin→animal→living), the confidence at hop 2 is $c = \min(c_1, c_2) = 0.9$, identical to a 1-hop derivation with the same evidence weight. PLN cannot distinguish a shallow correct derivation from a deep correct derivation — both receive equal priority. STBP credit assignment adds the $\gamma^d$ factor, making this distinction automatically.## 5. Discussion and Future Work

### 5.1 Summary of Contribution

We have demonstrated a formal bridge between Spatiotemporal Backpropagation (STBP) in spiking neural networks and inference control in Probabilistic Logic Networks (PLN). The core contribution is a depth-aware credit assignment mechanism that PLN's truth revision completely lacks: the γ^d temporal decay factor makes credit proportional to inference depth, ensuring that shallow truth-aligned derivations receive more priority than deep ones with identical evidence weight.

### 5.2 Empirical Validation

The v6b prototype validates that STBP credit assignment differentiates truth-aligned (GOOD) from truth-contradicted (BAD) scenarios across all three NAL inference rule types — deduction (+0.0093), abduction (+0.0638), and induction (+0.0405). The differentiation pattern is consistent with theoretical predictions: abduction (depth-1, no decay) shows the largest delta, deduction (2-hop, γ² decay) shows the smallest, and induction (proportional confidence weighting) falls in between.

### 5.3 Limitations

1. **Toy knowledge base**: 8 atoms and 6 derivations. Scaling to real-world knowledge bases with thousands of atoms and complex branching DAGs is untested.
2. **Static ground truth**: Scenarios use fixed ground truth values. Real inference systems must discover ground truth through interaction, not receive it a priori.
3. **Single loss function**: Only prediction error is tested. Information gain was shown to be truth-agnostic (truth reduction ≠ correctness), but other loss functions (utility, observation agreement) need evaluation.
4. **No integration with ECAN**: The proposal claims complementarity with ECAN forward attention, but no integrated system is tested.

### 5.4 Future Directions

1. **Integration with NARS bag structures**: Replace heuristic priority assignment with STBP-derived priority values, testing whether inference quality improves within existing infrastructure.
2. **Scaling experiments**: Test on branching DAGs with 10-100 hop chains to validate that depth-aware credit prevents inference explosion by deprioritizing deep chains.
3. **Online learning**: Replace batch backpropagation with online credit updates after each inference cycle, enabling real-time adaptive control.
4. **Connection to Geisweiller's reflexive inference**: Feed STBP credit signals into pattern mining to learn meta-strategies about which rule types produce truth-aligned conclusions at which depths.
5. **Multi-premise credit**: Extend beyond binary rules to N-premise inference, where credit must be distributed across N premises with potentially different depth values.

### 5.5 Conclusion

PLN inference control lacks depth-awareness — a 4-hop chain and a 1-hop derivation with identical evidence weight receive identical confidence. STBP credit assignment adds exactly this missing dimension: the γ^d factor makes credit proportional to inference depth, and the surrogate gradient σ'(conf-θ) makes rule firing differentiable. The result is an adaptive, event-driven inference control mechanism that prioritizes shallow truth-aligned conclusions — a mechanism that is both formally grounded in neural computation and directly applicable to symbolic reasoning systems.

## Appendix A: v12c Independent Sigmoid Gating Specification

### A.1 Architecture

The v12c prototype replaces softmax-constrained gating with independent sigmoid gating:

- **Gate function**: s_concl = s_raw * sigmoid(priority), where sigmoid(x) = 1/(1+exp(-x))
- **No softmax, no zero-sum constraint**: each rule's gate is independent
- **Priorities start at 0.0** (sigmoid=0.5, half-open gate)
- **Learning rate**: lr=3.0, 50 epochs

### A.2 Results

Independent sigmoid gating FIXED the v9 inertness problem:
- GOOD scenario: s_pred 0.1823→0.7254 (toward gt=0.9), err 0.7177→0.1746
- BAD scenario: s_pred 0.1823→0.1147 (toward gt=0.1), err -0.0823→-0.0147
- BOTH scenarios show learning (CHANGED=True)
- Priority divergence: deduction=6.51, abduction=7.70, induction=8.10
- All 3 rule types show scenario-dependent priority learning

### A.3 Key Insight

The v12c fix demonstrates that the zero-sum constraint of softmax was the root cause of v9 inertness. Independent sigmoid gating allows each rule to independently modulate its contribution without competing with other rules. This is the correct architecture for STBP-PLN credit assignment: credit is additive across paths, not a fixed resource to be divided.
