# g75: Two-Layer Defense Model for Multi-Agent AABC

## Architecture Constraint
Agents MUST communicate beliefs via implication deduction, NEVER direct revision.

## Why
- Deduction-mediated: adversarial (0.9,0.99) -> target moves 0.1->0.165. SAFE.
- Direct revision: adversarial (0.9,0.99) -> target moves 0.1->0.882. BREACHED.

## Defense Layers
1. **Deduction gate**: all inter-agent belief transfer goes through (==> A B) deduction, crushing adversarial confidence via truth function
2. **Trust gating (g70)**: trust STV modulates the contagion implication confidence, adding second damping layer
3. **AABC monitoring**: each agent runs self-check, detecting sudden belief jumps as anomalous

## Design Rule
No agent may directly revise another agent belief store. All influence is mediated by implication with trust-weighted confidence.