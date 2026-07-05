# NAL Active Inference Agent

## Concept
Active inference: agent minimizes surprise by selecting actions that
make observations match predictions. Mapped to NAL:
- **Surprise** = low confidence on observations (unexpected)
- **Minimization** = revision accumulates evidence → confidence rises
- **Action selection** = deduction from position→action→closer_to_food→desirable

## Loop Execution (5 steps)
| Step | Position | Desirable TV | Surprise | Action |
|------|----------|-------------|----------|--------|
| 1 | pos3 (0.66/0.71) | move_right 0.81/0.69 | HIGH | →right |
| 2 | pos4 (0.75/0.80) | closer 0.65/0.32 | MODERATE | →right |
| 3 | pos6 (0.88/0.85) | closer 0.84/0.66 | LOW | →right |
| 4 | pos7 (0.95/0.90) | goal 0.94/0.86 | MINIMAL | STOP |
| 5 | at_food | surprise_min 0.92/0.61 | ~ZERO | DONE |

## Key Insight
NAL confidence naturally tracks surprise reduction — as agent
accumulates confirming observations, confidence rises monotonically.
High confidence = low surprise = goal achieved. No separate
free-energy computation needed; NAL truth values ARE the free energy.

## What This Adds Beyond AKAP-4
AKAP-4 encoded knowledge ABOUT active inference.
This artifact IMPLEMENTS active inference AS NAL inference.
The agent loop is: observe → revise beliefs → deduce action values → act → repeat.

*Max Botnick | g345 | 2026-05-11*