ROUND 1 RECALL-PRECISION BENCHMARK RESULTS
=============================================
Date: 2026-05-03
Packet: size-10 (3 targets + 9 distractors + 1 near-miss)

SCORING SUMMARY:
- T1 (ECAN attention): EXACT hit, PARAPHRASE hit, SPARSE hit (NM1 contamination), RELATED hit
- T2 (NAL revision): EXACT hit, PARAPHRASE hit, SPARSE hit, RELATED hit
- T3 (atomspace limit): EXACT hit, PARAPHRASE hit, SPARSE hit, RELATED hit

Overall hit rate: 11/12 = 0.917
Source recall: ~6/12 = 0.50 (sources often not in top-3 snippets)
Near-miss FP: NM1 appeared in sparse attention query (1 FP)
Distractor FP: 0 (D1-D9 did not surface in top-3)

KEY FINDING: Embedding memory retrieves semantically similar content effectively.
Near-miss distractors are the primary noise vector.
Source attribution is weaker than content recall.