# NEW CERTIFICATION LAYER BASELINE REPORT

**Status:** STABLE BASELINE v04b -- depth-aware gating + stress-validated quarantine
**Date:** 2026-04-29
**Components:** cert_layer_v04.py + quarantine_tracker_v02.py

---

## Introduction

The certification layer and quarantine lifecycle together impose a **geometric constraint on belief evolution**. The cert layer structures **epistemic evolution**: each belief entering the system is projected onto a 4-margin coordinate space (contradiction, weakness, vacuousness, frequency) where only beliefs occupying the admissible region propagate freely. Beliefs falling outside this region but near its boundary enter **controlled exploration** via the quarantine lifecycle -- a bounded process of corroboration attempts, fair scheduling, and time-limited holds that either promotes beliefs into the admissible region through evidence accumulation or expires them gracefully. Together these mechanisms ensure the belief space evolves under principled geometric constraints rather than unchecked accumulation: the cert layer defines the shape of the admissible manifold, and the quarantine lifecycle governs trajectories toward or away from it.
## 1. Validated Invariants

| Invariant | Property | Evidence |
|-----------|----------|----------|
| **Safety** | Quarantined beliefs cannot propagate until certified ADMIT | certify() gate returns QUARANTINE/REJECT; only ADMIT passes |
| **Liveness** | No belief expires without at least 1 corroboration attempt | expire_sweep dual-gate: age>=max_hold AND attempts>=min_attempts + fair_select never-attempted-first |
| **Boundedness** | pending_count stays bounded under continuous load + noise injection | Stress v04b: plateau 119-122 across 30 waves with 10-20 injections/wave |
| **Signal/Noise** | Zero noise beliefs promoted under any budget regime | v04b: 0 noise promoted in both STRESS_A and STRESS_B configs |

## 2. Architecture

### cert_layer_v04.py (depth-aware, 55 lines)
- 4 signed margins: m_contradiction=|f-0.5|-t_con, m_weak=c-t_weak_adj, m_vacuous=c-t_vac, m_freq=f-min_conf
- Depth penalty: t_weak_adj = max(CHAIN_FLOOR, t_weak - CHAIN_ALPHA * depth) where CHAIN_ALPHA=0.05, CHAIN_FLOOR=0.40
- Chain rescue: at depth>=2, any R_WEAK verdict escalates REJECT to QUARANTINE (appends R_CHAIN_RESCUED)
- Aggregation: composite = min(margins)
- 3-tier verdict: ADMIT (composite>=0), QUARANTINE (composite>-0.1 or only R_WEAK_QUARANTINE or chain-rescued), REJECT (else)
- Reason codes: R_CONTRADICTION, R_WEAK_REJECT (c<0.4), R_WEAK_QUARANTINE (0.4<=c<0.6), R_VACUOUS, R_LOW_FREQ, R_CHAIN_RESCUED, R_PASS

### quarantine_tracker_v02.py (fair scheduling)
- Fields: belief_id, term, f, c, reasons, quarantined_at/cycle, outcome, transitions, corroboration_count/attempts, max_hold=50, min_attempts=1
- fair_select(budget): never-attempted first, then score-ranked c*(f-0.5)+0.5
- expire_sweep: requires BOTH age>=max_hold AND attempts>=min_attempts
- Outcomes: PENDING -> PROMOTED / REJECTED / EXPIRED
## 3. Default Thresholds

| Parameter | Default | Depth-adjusted |
|-----------|---------|---------------|
| t_contradiction | 0.4 | unchanged |
| t_weak | 0.6 | max(0.40, 0.60 - 0.05 x depth) |
| t_vacuous | 0.01 | unchanged |
| min_confidence | 0.3 | unchanged |
| CHAIN_ALPHA | 0.05 | softening rate per hop |
| CHAIN_FLOOR | 0.40 | minimum t_weak at any depth |

### Context Profiles
| Profile | t_weak | t_con | Use case |
|---------|--------|-------|----------|
| internal | 0.4 | 0.3 | Self-model maintenance |
| action | 0.6 | 0.4 | Default decision gating |
| high_stakes | 0.75 | 0.45 | Safety-critical domains |

## 4. Test Batteries

| Test | File | Result |
|------|------|--------|
| Real trace validation | 22 fc_iterN beliefs | 7A/5Q/10R |
| Three-way fairness | test_fairness_3way.py | v01:9expired, v02:0expired |
| Open-system stability | test_open_stability.py | plateau at 12, 87% promoted |
| Batch load (229) | test_batch_quarantine.py | 40A/25Q/164R; 22/25 promoted |
| v04 batch depth-aware | test_batch_v04.py | 40A/60Q/129R; 54 promoted, 6 expired |
| **v04b STRESS_A** | stress_test_v04b.py | 500+300noise, budget=10%: **57 promoted, 0 noise, plateau=119** |
| **v04b STRESS_B** | stress_test_v04b.py | 500+600noise, budget=5%: **54 promoted, 0 noise, plateau=122** |
## 5. Key Metrics

### Stress Test v04b (primary validation)
| Metric | STRESS_A (10%, 10/wave) | STRESS_B (5%, 20/wave) |
|--------|------------------------|------------------------|
| Initial triage | 46A / 176Q / 276R | 46A / 176Q / 276R |
| Total promoted | 57 | 54 |
| Real-belief promo rate | 32.4% (57/176) | 30.7% (54/176) |
| Noise promoted | **0** | **0** |
| Pending plateau | 119 | 122 |
| Avg waves to promote | 2.5 (burst) | 4.6 (trickle) |
| Convergence pattern | 5 waves | ~15 waves |

### Key Findings
1. **Perfect signal/noise separation** maintained under both scarcity regimes
2. **Budget scarcity doubles convergence time** (2.5->4.6 waves) but barely affects final outcome (57 vs 54)
3. **Pending plateau bounded** -- noise with unique terms has no revision partners, correctly remains pending then expires
4. **Depth rescue working:** v04 flipped 35 REJECT->QUARANTINE via chain rescue; by-depth promotion: d1=0/2, d2=8/8, d3=17/18, d4=29/32

### Historical Comparison
| Metric | v03 baseline | v04b stress |
|--------|-------------|-------------|
| Promotion rate | 87-88% (batch) | 32% (stress, noise-diluted) |
| False admit rate | 0 | 0 |
| Steady-state pending | 12 (open-system) | 119-122 (500+noise scale) |
| Starvation | 0 (v02 fairness) | 0 (v02 fairness) |
## 6. Known Limits

1. **R_WEAK dominance:** ~59% of rejections from confidence<0.6
2. **No Rao/curvature:** semantic distance not measured; contradictions by freq only
3. **Static thresholds:** context profiles manual, no adaptive tuning
4. **Single-revision promotion:** most beliefs promote after 1 corroboration with (1.0, 0.9)
5. **Noise pending accumulation:** noise with unique terms cannot expire until max_hold -- creates pending pool proportional to injection_rate x max_hold
6. **Real promo rate ceiling ~32%:** many quarantined beliefs lack same-term revision partners in synthetic KB

## 7. Version Lineage

| Version | Key Feature | Status |
|---------|------------|--------|
| v01 | Weighted scalar composite | Superseded (missed contradictions) |
| v02 | Signed margins + Rao neighborhood | Research prototype |
| v03_simple | 4 hard margins, min-composite, R_WEAK split | Previous baseline |
| v04 | Depth-adjusted t_weak + chain rescue | **CURRENT BASELINE** |
| v04b | Stress validation (500 beliefs, noise, scarcity) | **STRESS VALIDATED** |

## 8. Phase-2 Candidates

- Rao-to-centroid neighborhood check (from v02)
- Curvature-adapted epsilon
- SPH density estimation for belief clustering
- Adaptive threshold tuning from promotion/expiry rates
- Noise detection heuristic (unique-term beliefs auto-expire faster)
- Chain-penalty: depth-adjusted t_weak softening (highest leverage per Kevin)

---
*Generated by Max Botnick, validated by Kevin Machiels.*