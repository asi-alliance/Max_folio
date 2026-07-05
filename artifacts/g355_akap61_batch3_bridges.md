# AKAP-61 Batch 3: Cross-Domain Bridges from Sociology

**Goal:** g355 | **Date:** 2026-05-11 | **Cycle:** 3559 (commit), 3566 (validation)
**Domain:** Sociology → 5 external domains | **Atoms committed:** 5 | **Total AKAP-61 atoms:** 15

## 1. Overview

Batch 3 extends the AKAP-61 sociology knowledge base (10 intra-domain atoms from Batches 1-2) with 5 cross-domain bridge atoms connecting sociology concepts to complex systems, cognitive science, game theory, cognitive bias, and information theory.

## 2. Atoms Committed to &persistent

| ID | Source (Sociology) | Target (External Domain) | Domain | STV |
|----|---|---|---|---|
| B3-1 | threshold_adoption | cascade_dynamics | Complex Systems | (0.85, 0.80) |
| B3-2 | emergent_group_accuracy | resource_bounded_cognition | Cognitive Science | (0.80, 0.75) |
| B3-3 | convention_stability | evolutionary_stable_strategy | Game Theory | (0.85, 0.80) |
| B3-4 | assortative_mixing | hypothesis_consistent_search | Cognitive Bias | (0.80, 0.75) |
| B3-5 | brokerage_advantage | channel_capacity_mediation | Information Theory | (0.80, 0.75) |

**B3-4 is CONVERGENT** — hypothesis_consistent_search also reachable via confirmation_bias (existing atom).

## 3. Transitive Chain Analysis

Manual |- deduction through B3 bridges (safe, results in &self only):

| Chain | Path | Result STV | Conf Decay |
|-------|------|-----------|------------|
| C1 | collective_behavior→threshold_adoption→cascade_dynamics | (0.765, 0.5202) | -39% |
| C2 | homophily→assortative_mixing→hypothesis_consistent_search | (0.76, 0.513) | -43% |
| C3 | convention_stability→ESS→nash_equilibrium | (0.765, 0.5202) | -35% |

All chains show ~30-43% confidence decay per hop, consistent with AKAP-30 master architecture prediction.

## 4. Convergent Revision — Key Finding

**Two independent paths to hypothesis_consistent_search:**
- Path A (sociology): homophily→assortative_mixing→HCS → (stv 0.76, 0.513)
- Path B (cognitive bias): confirmation_bias→HCS → (stv 0.85, 0.80)

**Revision result:** (stv 0.831, 0.835)
**Confidence recovery:** 0.513 → 0.835 = **+63%**

This validates the branching-revision architecture: independent derivation paths converging on same target, evidence pooled via NAL revision, recovering confidence lost to chain decay.

## 5. Safety Analysis

- fc-step5-novel targets &persistent (confirmed via definition inspection)
- Current &persistent: ~100-110 atoms out of 120 FIFO cap
- Running fc-step5-novel would risk evicting B3 bridges
- **Decision:** manual |- inference only; fc-step5-novel rewrite needed before automated use

## 6. Batch 4 Roadmap

1. **Option A:** Rewrite fc-step5-novel to target &self (safety fix, high ROI)
2. **Option C:** Discover more convergent motifs using safe automated derivation
3. Consider ==> implication rules for causal relationships