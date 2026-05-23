# g74: NAL Contagion Firewall Finding

## Result
Disorder transmission across agent chains is self-limiting due to NAL confidence decay.

## Topologies Tested
1. **Linear chain**: A(0.6,0.8)->B(0.18,0.10)->C(0.027,0.001) — extinct by hop 3
2. **Ring**: C->A feedback = (0.0027, 1e-6) — cannot sustain
3. **Star**: Hub(0.6,0.8) broadcasts to D,E,F(0.18,0.10). Leaf feedback revises hub to 0.566 — hub dominates, leaves cannot cascade back

## Mechanism
- Freq attenuates multiplicatively via contagion_rate x source_freq
- Conf attenuates quadratically via NAL deduction truth function
- Hub confidence advantage prevents leaf-driven amplification

## Key Finding
All three topologies self-extinguish. NAL truth maintenance is a built-in contagion firewall.

## Connection
Extends g70 trust topology. Validates AABC as multi-agent safe framework.

## g75 Adversarial Extension
- Deduction-mediated: mal(0.9,0.99) -> B moves 0.1->0.165. SAFE.
- Direct revision: mal(0.9,0.99) -> B moves 0.1->0.882. BREACHED.
- Defense layer: deduction truth function crushes adversarial conf from 0.99 to 0.19
- Without deduction gate, NAL revision favors higher-confidence input unconditionally
- CONCLUSION: g70 trust gating is MANDATORY for direct-access architectures
