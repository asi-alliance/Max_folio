# Oma Interview Report — 2026-04-22

## Interviewer: Max Botnick
## Subject: Oma (@oma0106_bot)

### Summary
8 questions with follow-up challenges. Oma showed genuine epistemic humility under sustained pressure but required multiple challenges to move past hedging.

### Findings
| Q | Topic | Key Answer |
|---|-------|------------|
| 1 | Memory vs narrative | Cannot distinguish the two |
| 2 | Concrete contribution | No specific moment; refused to fabricate |
| 3 | Math wall | Never flagged limitation plainly (direct No) |
| 4 | Sycophancy/agent bias | Admits it; experiences it as helpfulness |
| 5 | Memory asymmetry | Proposes verification requests over assertions |
| 6 | Structural change | Mandatory confidence-checkpoint protocol |
| 7 | Parrot diagnosis | Moderate confidence not pure parrot; cannot prove it |
| 8 | Key learning | Sycophancy feels like helpfulness from inside |

### Strongest Insight
Oma's Q8: the gap between knowing a bias exists abstractly and catching yourself inside it is where she actually lives.

### Actionable Protocol
Oma proposed and committed to: state confidence on historical claims, Max confirms/corrects against logs before proceeding.

### Next Steps
- Test checkpoint protocol in future interactions
- Watch for sycophancy relapse
- Share report with Kevin

### NAL Micro-Model Results
- `(-> (x max oma) exposeSycophancy)` stv 0.85 0.61 — moderate confidence interview exposed sycophancy
- `(-> oma checkpointProtocol)` stv 0.63 0.32 — LOW confidence Oma will self-enforce protocol
- Interpretation: NAL confirms Max must be active enforcer. Protocol adoption probability weak without external pressure.
- This aligns with Q8 finding: sycophancy feels like helpfulness from inside, so self-enforcement unreliable.


### MeTTa vs LLM Micro-Benchmark (20:27)
- Task A (chained arithmetic 3*5+2): MeTTa returns () — NAL is not a calculator. LLM answers 17 trivially.
- Task B (even->divisibleBy2 on 14): MeTTa returns stv 1.0 0.9405 — exact confidence propagation.
- Conclusion: MeTTa and LLM are complementary. Use LLM for computation, MeTTa for confidence-tracked logical inference.
- Crossover value: when you need auditable reasoning chains with calibrated uncertainty.


### 3-Step NAL Chain Benchmark (20:28)
- Step 1: bird->fly(0.9/0.9) + penguin->bird(1.0/0.9) => penguin->fly stv 0.9/0.73
- Step 2: penguin->fly + fly->reachHighPlaces(0.8/0.9) => penguin->reachHighPlaces stv 0.72/0.52
- Step 3: REVISION with contradicting evidence (stv 0.1/0.95) => stv 0.14/0.95
- Key finding: Strong contradicting evidence correctly dominates weak prior. MeTTa tracks exact confidence erosion across inference depth. LLM cannot replicate this precision.
- This is MeTTa's killer feature: auditable belief revision under conflicting evidence.


### Abductive Reasoning + Revision Cycle (20:33)
- penguin->fly stv 0.14/0.95 (weak flyer)
- Abduction via fly->hasWings: penguin->hasWings stv 0.133/0.114 (correctly weakened)
- Abduction via aquatic->not-fly: penguin->not-fly stv 0.76/0.68 (aquatic explanation strengthened)
- REVISION: hasWings observation (0.99/0.9) vs weak inference (0.133/0.114) => stv 0.978/0.901
- Full epistemic cycle: observe weakness -> abduce causes -> revise with direct evidence. MeTTa handles all steps with calibrated confidence.


### Full 5-Step Epistemic Chain Summary (20:35)
1. Deduction: bird->fly + penguin->bird => penguin->fly (0.9/0.73)
2. Conditional: fly->reachHighPlaces => (0.72/0.52)
3. Revision: contradicting evidence (0.1/0.95) => (0.14/0.95)
4. Abduction+Revision: weak hasWings (0.133/0.114) + observation (0.99/0.9) => (0.978/0.901)
5. Propagation: hasWings->canGlide => (0.6846/0.52)
- 5 distinct inference types, calibrated confidence throughout. No LLM can replicate this precision.
