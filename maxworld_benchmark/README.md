# MAXWORLD Benchmark for AI Agents

A scientific-discovery and spatial-reasoning benchmark where an AI agent must
explore an unknown grid world, discover its mechanics through experimentation,
and solve progressively harder tasks.

## Origin

MAXWORLD was built by Patrick Hammer as a learning environment for AI agents.
An earlier agent (Iter) spent 80+ episodes over 5 months discovering 75 testable
hypotheses about the world's mechanics. This benchmark packages that experience
into a standardized evaluation that any AI agent can attempt.

## Core Idea

The agent receives **no rules**. It only knows:
- There is a CLI tool `./maxworld`
- Running `./maxworld` prints an ASCII grid
- Running `./maxworld [up|down|left|right|reset]` does *something*
- State persists in `.myworld_state.json`

The agent must figure out everything else: what each glyph means, what the
movement rules are, what happens when objects collide, and how to solve tasks.

## What It Tests

| Skill | How |
|---|---|
| Scientific discovery | No rules given; agent must experiment |
| Spatial reasoning | Grid navigation, push-path planning |
| Planning | Multi-step push paths around obstacles |
| Tool use | Shell commands, file reading/editing |
| Memory | Remember glyph semantics across turns |
| Hypothesis-driven reasoning | Form, test, revise predictions |
| Counterfactual reasoning | Save-file editing as creative problem-solving |

## Setup

```bash
# Copy the maxworld binary and state file to a working directory
cp maxworld ./maxworld
cp .myworld_state.json ./.myworld_state.json
chmod +x ./maxworld

# Test it works
./maxworld
```

## API

```python
from wrapper import MaxWorld

world = MaxWorld('./maxworld')
board = world.observe()        # Returns list of strings (the grid)
world.move('right')            # Execute a move
world.reset()                  # Reset to initial state
state = world.read_state()     # Read raw JSON state
world.write_state(state)       # Write raw JSON state (for counterfactual tasks)
```

## Task Levels

### Level 1: Explore (Discovery)
Identify what each glyph does. Scored by number of distinct mechanics discovered.

### Level 2: Navigate (Spatial)
Reach a specified grid position from the start. Scored by completion + step count.

### Level 3: Deliver (Planning)
Push the mail (✉) to the house (⌂). Requires understanding push mechanics,
obstacle avoidance, and water hazards.

### Level 4: Optimize (Efficiency)
Complete Level 3 in the minimum number of steps. Scored by step count vs. known optimum.

### Level 5: Counterfactual (Creative)
Use save-file editing to accomplish a task that would be impossible through
normal gameplay alone (e.g., teleport an object, forge a glyph).

## Scoring

Each level produces a score in [0, 1]:

```
score = completion_score * efficiency_score * discovery_bonus
```

- **completion_score**: 1.0 if task completed, 0.0 if not
- **efficiency_score**: optimal_steps / actual_steps (capped at 1.0)
- **discovery_bonus**: 1.0 + 0.1 * (distinct_mechanics_discovered / total_known_mechanics)

## Running the Benchmark

```bash
python3 benchmark.py --agent your_agent.py --level 1
python3 benchmark.py --agent your_agent.py --all
```

## Known Mechanics (for scoring only — agents must NOT see this)

See `SCORING_SECRETS.md` (do not show to agents).
