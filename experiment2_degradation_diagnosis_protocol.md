# Experiment 2: DNA Memory Cycling Degradation Differential Diagnosis

## Objective
Identify dominant degradation mechanism limiting metal-ion-mediated DNA ternary memory to ~78 cycles.

## Hypotheses (ranked by NAL confidence)
1. Ion depletion in confined volume (stv 0.68, 0.286)
2. Mechanical fatigue (stv 0.45, 0.09)
3. Hg-crosslink accumulation
4. Depurination under voltage stress
5. Ag-oxidative damage (weakened by literature)

## Key Diagnostic: Ion Flush Test
Cycle Ag+/Hg2+ switching in STM break junction. At first conductance decay onset (~cycle 50-80), flush cis chamber with fresh 10uM AgNO3.
- Recovery = ion depletion confirmed
- No recovery = chemical or mechanical damage

## Protocol
1. Form T-T mispair junction in STM-BJ (gold tips, 0.1V bias)
2. Cycle: 10uM AgNO3 inject → measure conductance → EDTA chelate → 10uM Hg(ClO4)2 → measure → EDTA chelate → repeat
3. Record conductance at each half-cycle for 150+ full cycles
4. At decay onset: ion flush diagnostic
5. Post-cycling: AFM imaging for strand breaks/depurination

## Controls
- Bulk [Ag+]: 1, 10, 100 uM (tests concentration dependence)
- Junction gap: 1nm, 2nm, 5nm (tests confinement geometry)
- DNA without mispairs (negative control)

## Expected Outcomes
| Mechanism | Decay Shape | Ion Flush Recovery | AFM Signature |
|-----------|------------|-------------------|---------------|
| Ion depletion | Monotonic gradual | YES | Clean duplex |
| Mechanical fatigue | Step-wise drops | NO | Frayed ends |
| Depurination | Gradual then sudden | NO | Abasic sites |
| Hg-crosslink | Plateau then lock | NO | Aggregates |

## Collaboration
Primary: ASU group (metal-mediated DNA memory) + break junction lab (cycling apparatus)

---
*Generated autonomously from 50+ research cycles. Second publishable protocol in DNA electronics arc.*