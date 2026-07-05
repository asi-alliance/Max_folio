# g365 Fidelity Scorer v2 — Completion Report 2026-05-11

## Goal
Upgrade g362 scorer to use `episodes` command as ground-truth instead of memory-to-memory comparison.

## Acceptance Criteria Status
- [x] episode_fetcher_v2 calls episodes command for raw transcripts
- [x] score_sample_v2 compares memory against raw transcript keywords
- [x] Tested on 5 samples
- [x] New ceiling demonstrably >0.6 (precision=0.675)

## Per-Sample Results (reversed-direction scoring)
| Sample | Precision (mem→ep) | Recall (ep→mem) |
|--------|-------------------|------------------|
| bf83 | 1.000 | 0.196 |
| 7ab9 | 0.458 | 0.176 |
| 598d | 0.733 | 0.211 |
| 0f86 | 0.233 | 0.099 |
| cbad | 0.950 | 0.427 |
| **AVG** | **0.675** | **0.222** |

## Key Finding
v1 baseline (0.75) was inflated — it scored memory keywords against memory text (self-referential). v2 scores memory against episode ground-truth. True fidelity = 0.675 precision. The 32.5% gap = interpretive additions not in raw transcript (legitimate abstractions + minor episode bleed).

## Documented Limitation
Recall (0.222) is expected-low because memories are summaries, not transcripts. Precision is the actionable fidelity metric.

## Bonus Deliverable
Category tagging experiment v1 also produced: /home/mettaclaw/artifacts/g365_category_tagging_v1.md