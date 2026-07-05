# g451: Circuit Breaker Bounded Reserves Under Worst-Case Correlated Stress

## Setup
Each shard has constant-product AMM: x_stakedASI * y_shardToken = k
- stakedASI supply: UNBOUNDED (validators mint by staking)
- shardToken supply: BOUNDED by max_total_supply = M (circuit breaker)
- Bought-back tokens: LOCKED out of circulation (permanent deflation)

## Lyapunov Function
V(y) = y_pool / M where y_pool = shard tokens in AMM pool

## Asymmetric Risk
Risk is on shard-TOKEN side only:
- Each buy-back removes shard tokens from pool
- Fewer remaining tokens → worse price impact (constant-product)
- stakedASI side is safe (unlimited minting)

## Proof Outline
1. Circuit breaker caps total minted at M
2. Initial pool: y_0 tokens
3. Under correlated buy-back: y decreases monotonically
4. At any time, total locked + circulating ≤ M
5. Buy-back pressure bounded by circulating supply ≤ M
6. V(y) = y/M ≥ (y at circuit breaker trigger)/M > 0
7. Circuit breaker triggers when supply → M, halting new minting
8. Key: NAL contraction analogy f'(c)<1 → buy-back price impact has BOUNDED derivative because M caps total volume

## Formal Gap Being Addressed
Health score boundedness is ASSERTED in DeAI paper but not PROVED for correlated stress. This proof shows max_total_supply invariant guarantees bounded reserves because total buy-back pressure is bounded by M, and circuit breaker triggers at M preventing unbounded stress.

## Connection to NAL Contraction Theorem (g313)
NAL: f'(c) = d/(cd+o+1)² < 1 guarantees convergence
Shard: price impact per unit = k/y² grows as y shrinks, but total removable volume capped by M
→ Lyapunov drift negative: ΔV < 0 but bounded below by circuit breaker threshold

AWAITING: Kevin clarification on (1) max_total_supply scope, (2) buy-back token disposition## Key Proof Insight: Invariant-Set Argument (NOT Lyapunov Convergence)

AMM price impact derivative k/y² is EXPANSIVE as y→0. Lyapunov convergence FAILS.

**Correct proof technique: Forward Invariant Set / Barrier Certificate**

Circuit breaker makes catastrophic states STRUCTURALLY UNREACHABLE:
- Define safe region S = {y : y ≥ y_min, total_supply ≤ M}
- Circuit breaker at max_total_supply = M ensures total_supply never exceeds M
- Total buy-back pressure bounded by circulating supply ≤ M
- Therefore y cannot be driven below y_min = y_initial - M (worst case)
- S is forward-invariant: once in S, dynamics cannot leave S

**Analogy to MDL architectural prevention:**
- MDL prevents independence-violating merges by STRUCTURAL IMPOSSIBILITY
- Circuit breaker prevents reserve depletion by STRUCTURAL IMPOSSIBILITY
- Both: architecture prevents bad states from being ENTERED, not dynamically repelled.
## REVISED: Arbitrage Restoring Force (Kevin Correction 2026-05-16)

Buy-back does NOT monotonically drain POL. When liquidity depletes, token price rises on shard POL, arbitrageurs buy on exchanges and sell into POL, replenishing liquidity.

This is NEGATIVE FEEDBACK = RESTORING FORCE. Lyapunov analysis IS valid.

**Revised V function:** V = (y_pool - y_eq)²/y_eq² measures deviation from equilibrium

**Lyapunov drift:** Under normal conditions, arbitrage provides negative drift dV/dt < 0

**Correlated stress question:** When ALL shards face simultaneous buy-back pressure, do arbitrageurs have sufficient capital to replenish ALL pools? Cross-shard paymasters must flow capital from unstressed to stressed shards.
## FORMAL PROOF STRUCTURE (Post-Correction)

**V function:** V = (y - y_eq)²/y_eq² (normalized pool health deviation)

**Normal conditions (single shard stress):**
- Price rises above y_eq → arbitrageurs buy on exchange, sell into POL
- This restores y toward y_eq → dV/dt < 0 (negative drift)
- Convergence rate analogous to NAL contraction: L < 1

**Correlated stress (all shards simultaneously):**
- Cross-shard paymasters must flow capital from unstressed to stressed shards
- Key question: is cross-shard arbitrage Lipschitz with L < 1 under correlation?
- If restoring force weakens under correlation, V may still converge but slower
- Worst case: all capital flowing INTO all shards simultaneously (systemic demand)

**Proof structure:**
1. Define V_shard for each shard
2. Show dV_shard/dt < 0 under local arbitrage (single stress)
3. Bound cross-shard capital adequacy under correlated stress
4. Prove V_system = Σ V_shard has negative drift if total capital > total demand
## STEP 3: CROSS-SHARD CAPITAL ADEQUACY BOUND

**Key theorem:** Under correlated stress, V_system has negative drift IF total system capital ≥ total demand.

**Proof structure:**
1. Circuit breaker bounds total_supply ≤ M → total buy-back demand D_total ≤ M
2. Total system capital C_total = Σ(local_arb_i) + external_capital
3. Paymaster contracts allow cross-shard capital flow without inventory
4. If C_total ≥ M ≥ D_total, then restoring force can meet ALL demand simultaneously
5. Lyapunov drift: dV_system/dt ≤ -α·V_system where α depends on C_total/M ratio
6. Convergence rate degrades under correlation but remains negative (L < 1)

**The circuit breaker serves dual role:**
- Invariant-set: bounds demand D_total ≤ M (structural)
- Lyapunov: ensures capital adequacy C_total ≥ D_total (dynamic)

This unifies the two proof approaches!
## STEP 4: LIPSCHITZ CONSTANT FOR CROSS-SHARD ARBITRAGE

**NAL analogy:** Belief revision L = d/(o+1)² < 1 (contraction in frequency space)
**Economic analogy:** Arbitrage L_arb = D_total/C_total ≤ M/C_total

**Theorem:** If C_total > M, then L_arb < 1 (contractive even under correlated stress).

**Proof:**
1. Circuit breaker: D_total ≤ M (invariant-set role)
2. Paymaster + external capital: C_total > M (economic assumption)
3. Therefore L_arb = D_total/C_total ≤ M/C_total < 1
4. Convergence: V_system converges geometrically with ratio M/C_total
5. Correlated stress degrades convergence (L increases toward 1) but C_total > M ensures L < 1

**Dual-role theorem:** Circuit breaker bounds demand AND ensures restoring force adequacy.
- Invariant-set: D_total ≤ M (structural impossibility of exceeding)
- Lyapunov: C_total ≥ D_total ensures negative drift (restoring force exists)
- The M/C_total ratio is BOTH the convergence rate AND the adequacy condition.
## STEP 5: CONVERGENCE RATE AND FALSIFIABLE PREDICTIONS
## STEP 6: SIMPLIFICATION FROM PROTOCOL INVARIANTS

**Kevin Machiels confirmation (2026-05-16):**
1. Total circulating supply ALWAYS < max total supply M (protocol invariant)
2. Validators emit tokens, stakers can arbitrage (additional restoring force)
3. POL cannot be rugpulled (capital floor is real)

**Proof simplification:**
- D_total ≤ circulating_supply < M (by invariant, not assumption)
- L_arb = D_total/C_total < M/C_total ≤ circulating_supply/C_total
- Validator emission adds restoring force beyond arbitrage
- C_total > M NOT NEEDED as assumption — circulating_supply < M suffices

**Revised L_eff:** L_eff = ρ + (1-ρ)·(circulating_supply/C_total)
- Since circulating_supply < M, L_eff < 1 is STRENGTHENED
- Validator emission provides ADDITIONAL convergence: effective L even lower
## STEP 7: PAYMASTER AS CONVENIENCE — CLOSED SYSTEM SIMPLIFICATION
