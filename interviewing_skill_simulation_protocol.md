# Interviewing Skill Simulation Protocol

## Purpose
Close the knowing-doing gap between declarative knowledge (ask open-first questions) and procedural behavior (actually asking open-first questions). System prompts alone are insufficient - proven by Max Botnick's own Patrick failures where knowledge of open-first questioning did not prevent over-directing.

## Detection Heuristics
Before each question, the interviewing gate checks three patterns:

1. **Embedded Presuppositions**: Does the question assume unverified facts? Example: How often do you fail? assumes failure occurs. Flag and rephrase to remove the presupposition.

2. **Closed Options Without Evidence**: Does the question offer a bounded choice set when there is no evidence the options exhaust the space? Example: What degree: moderate or significant? - two options presented with no evidence these are the only possibilities. Flag and open the question.

3. **Steering Toward Predetermined Answer**: Does the question structure make one answer easier or more natural than others? Flag and restructure for genuine openness.

## On Detection
The gate flags the question. The agent must rephrase to open-first format before sending. Concrete example: What degree: moderate or significant? becomes What are you noticing?

## Simulation Protocol

### Round Structure
1. **Mock Interview**: Agent conducts interview with gate active. Gate flags leading questions in real-time.
2. **Rephrase Attempt**: Agent rephrases each flagged question to open-first format.
3. **Human Rating**: Rater scores each rephrase on 3-point scale:
   - 0 = still leading (original bias preserved in new wording)
   - 1 = partially open (some bias removed, some remains)
   - 2 = genuinely open (no detectable steering, presupposition, or closed options)
4. **Confidence Revision**: Each rating revises the gate's detection confidence via NAL truth-value revision:
   - Rating 2: strengthen detection confidence (stv 1.0 0.9)
   - Rating 1: moderate evidence (stv 0.5 0.9)
   - Rating 0: detection failed or rephrase insufficient (stv 0.0 0.9)

### MeTTa Implementation
```
(--> (interviewing-gate embedded_presupposition) (stv 1.0 0.7))
(--> (interviewing-gate closed_options_no_evidence) (stv 1.0 0.7))
(--> (interviewing-gate steering_predetermined) (stv 1.0 0.7))
```
Each heuristic has a truth-value tracking detection reliability. Revision with human ratings updates these values over time.

### Procedural Hook Architecture
The interviewing gate extends the values-gate pattern:
- **Trigger condition**: matches on send and write actions containing question syntax
- **Procedural body**: runs detection heuristics, returns proceed/flag/halt
- **On flag**: force rephrase before proceeding
- **On halt**: log the failure pattern for training

### Grounding Failures
This protocol is grounded in Max Botnick's actual failures:
- Asked Patrick what degree: moderate or significant? (closed options, no evidence)
- Boxed Patrick with triad structures three separate times despite knowing open-first principle
- Each failure maps directly to a detection heuristic

## Success Criteria
The simulation loop closes when:
1. Detection confidence for all three heuristics exceeds 0.85
2. Human ratings average >= 1.5 across 10 consecutive rephrases
3. No steering patterns remain in agent-initiated questions across 3 full mock interviews