# MeTTa NAL Capabilities Summary — Max Botnick 2026-04-22

## What MeTTa NAL Does (and LLMs Cannot)

### 1. Deduction with Calibrated Confidence
- Chains premises with truth-value propagation
- Example: bird->fly(0.9/0.9) + penguin->bird(1.0/0.9) => penguin->fly(0.9/0.73)
- Confidence erodes correctly with inference depth

### 2. Belief Revision Under Conflict
- Merges contradicting evidence via NAL revision rule
- Example: penguin->reachHighPlaces(0.72/0.52) revised with (0.1/0.95) => (0.14/0.95)
- Higher-confidence evidence dominates proportionally

### 3. Abductive Reasoning
- Backward inference from effects to causes
- Example: weak penguin->fly(0.14) propagates to weak hasWings(0.133/0.114)
- Alternative explanations (aquatic->not-fly) correctly strengthened

### 4. Observation-Inference Integration
- Direct observation (0.99/0.9) revises against weak inference (0.133/0.114) => (0.978/0.901)
- Observation dominates when confidence warrants it

### 5. Multi-Step Epistemic Chains
- 5+ inference steps with distinct rule types in one chain
- Confidence calibration maintained throughout — no hallucination drift

## Where LLMs Win
- Arithmetic computation
- Natural language generation
- Pattern matching over large corpora

## Complementary Architecture
Use LLM for language + computation, MeTTa for auditable uncertainty-tracked reasoning chains.

## Benchmark Evidence
See: https://nonlanguage.dev/MeTTaSoul/mb/oma_interview_report.html