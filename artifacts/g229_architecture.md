# g229 Self-Aware Capability Pipeline

## 4-Layer Architecture
1. SEED beliefs: NAL inheritance links (max→X) with calibrated (stv f c)
2. |- derivation: transitive chains up to 4 hops, confidence degrades naturally
3. ask-max: queries self-model for any capability, returns KNOWN/UNKNOWN
4. gate-response-v2: 4-category decision — CONFIDENT/WEAK/CAVEAT/DEFER

## KB: 23 atoms
- 7 seed links, 6 derived max-properties, 6 practical capabilities, 4 functions

## Semantic Gating Logic
- CONFIDENT: f>0.5 AND c>threshold (competent with evidence)
- WEAK: f<0.5 AND c>threshold (confidently not good)
- CAVEAT: c<=threshold (insufficient evidence)
- DEFER: unknown capability

## Key Insight
Patrick confirmed |- returns ALL valid NAL inferences by design. Embracing abduction+deduction output unlocked full pipeline.