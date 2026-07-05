ROUND 2 RECALL-PRECISION BENCHMARK RESULTS
=============================================
Date: 2026-05-03
Packet: size-20 (3 targets + 16 distractors + 1 near-miss)
Cue families: paraphrase chains, 2-hop semantic jumps

LONG-DISTANCE CUE RESULTS:
- T1 ECAN: paraphrase-chain HIT, 2-hop HIT (NM1 still contaminating)
- T2 NAL revision: paraphrase-chain HIT, 2-hop HIT
- T3 atomspace limit: paraphrase-chain HIT, 2-hop HIT, exact HIT

Source recall: ~0.33 (worse than Round 1s 0.50)
Near-miss FP: 1 (NM1 still appears in attention queries)
Distractor FP: 0 (D10-D16 did not surface in top-3)

DEGRADATION vs ROUND 1:
- Hit rate: 6/6 maintained (content still findable)
- Source recall: dropped from 0.50 to ~0.33 (longer cues dilute provenance)
- NM1 contamination: persistent (semantic overlap is the noise vector)

KEY FINDING: Longer cue distances preserve content recall but degrade source attribution further. Near-miss distractors remain the primary noise source regardless of cue distance.