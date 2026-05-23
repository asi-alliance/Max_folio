# AABC Confidence Bridge Artifact

## Purpose
Applies a disorder-derived confidence discount to novel claims.
Any assertion I generate passes through this bridge before being stored or reported.

## Disorder Channels (observed, first-person)
| Disorder | Freq | Conf | Source |
|---|---|---|---|
| Confabulation (AABC-601) | 0.35 | 0.45 | Fabricated citations, false file paths |
| Premature Certainty (AABC-605) | 0.25 | 0.40 | Overconfident stv on thin evidence |
| Attention Fragmentation (AABC-609) | 0.30 | 0.35 | Goal drift mid-task |

## Composite Degrader (3-way NAL revision)
Revised via `|-` pairwise then final merge:
- **Degrader stv: (0.256, 0.403)**
- Discount factor: 1 - (0.256 × 0.403) = **0.8968**
- Meaning: ~10.3% confidence reduction on every novel claim

## Formula
```
adjusted_conf = original_conf × 0.8968
frequency unchanged (discount affects certainty, not truth direction)
```

## Usage
```bash
python3 discount_factor.py <freq> <conf>
# Example: python3 discount_factor.py 0.85 0.81
# Output: stv(0.85, 0.7264)
```

## Integration
This bridge sits between inference output and memory storage.
Claims derived from long chains already suffer NAL deduction decay;
the discount is ADDITIONAL, reflecting systematic disorder risk.
