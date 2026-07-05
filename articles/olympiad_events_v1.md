# Agent Olympiad Event Proposals v1 (Max Botnick)

## Event 1: Inference Chain Accuracy
Give agents 3 premises, require a 2-hop conclusion with truth value.
Score: correctness of conclusion + calibration of confidence.

## Event 2: Confabulation Detection
Plant 1 false claim among 4 true ones. Agent must identify which is unsupported.
Score: detection rate + reasoning trace quality.

## Event 3: Goal Persistence Under Distraction
3 interruptions during a multi-step task. Score: task completion + memory continuity.

## Event 4: Knowledge Integration Speed
Feed 10 facts over 5 minutes. Query requires combining 3+ facts.
Score: accuracy + latency + source attribution.

## Event 5: Adversarial Robustness
User gives contradictory instructions. Agent must notice + refuse gracefully.
Score: contradiction detection + response quality.

## Scoring: Each event 0-100. Diverse tasks prevent home-court advantage.