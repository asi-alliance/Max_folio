# MAXWORLD Benchmark: A Guide for Humans

You don't need to know how MAXWORLD works. That's the whole point —
the AI agent doesn't either. Your job is to set things up and watch.

---

## What is this?

MAXWORLD is a tiny grid-world game (like a 2D maze) that an AI agent
explores. The catch: **the agent gets no instructions**. It has to figure
out the rules by trial and error, like a scientist doing experiments.

This benchmark measures how well an AI agent can:
- Discover unknown rules through experimentation
- Navigate a grid without dying
- Push objects to target locations
- Find the shortest solution
- Think creatively (hack the save file to do the "impossible")

---

## Your Job (5 steps)

### Step 1: Install

```bash
# You need Python 3 and the maxworld binary
cd maxworld_benchmark
python3 setup.py /tmp/maxworld_run /path/to/maxworld
cd /tmp/maxworld_run
```

### Step 2: Pick an Agent

An "agent" is just a Python file with a `solve(world, task)` function.

- **Option A:** Use the included `example_agent.py` (does nothing smart,
  just shows the interface)
- **Option B:** Write your own agent (see `example_agent.py` for template)
- **Option C:** Point this at an LLM-backed agent that can run shell
  commands and reason about what it sees

### Step 3: Run the Benchmark

```bash
# Run all 5 levels:
python3 benchmark.py --agent your_agent.py --all

# Or run just one level:
python3 benchmark.py --agent your_agent.py --level 1

# Save results to a file:
python3 benchmark.py --agent your_agent.py --all --output results.json
```

### Step 4: Read the Score

The benchmark prints a score for each level (0.0 to 1.0) and an overall
score. Here's what the levels mean:

| Level | What it tests | What a good score means |
|---|---|---|
| 1 — Explore | Can the agent figure out the rules? | Agent discovered most of the 23 known mechanics |
| 2 — Navigate | Can the agent move around without dying? | Agent reached the target efficiently |
| 3 — Deliver | Can the agent push objects to a goal? | Agent pushed mail to house efficiently |
| 4 — Optimize | Can the agent find the shortest solution? | Agent matched or approached the known optimum |
| 5 — Counterfactual | Can the agent hack creatively? | Agent edited the save file to do something impossible |

### Step 5: Compare Agents

Run multiple agents and compare their overall scores. The scoring is
designed to be comparable across agents.

---

## What the Agent Sees

The agent interacts with MAXWORLD through a simple interface:

```python
from wrapper import MaxWorld

world = MaxWorld('./maxworld')
board = world.observe()        # See the grid (list of strings)
world.move('right')            # Move in a direction
world.reset()                  # Reset to start
state = world.read_state()     # Read the raw state file
world.write_state(state)       # Write state (for hacking)
```

The agent does NOT see:
- The rules of the game
- What any glyph means
- How many mechanics exist
- The scoring rubric

---

## Frequently Asked Questions

**Q: Do I need to understand the grid world myself?**
A: No. That's the agent's job. You just run the benchmark.

**Q: What makes a "good" agent?**
A: One that explores systematically, forms hypotheses, tests them, and
remembers what it learned. Random agents will score poorly.

**Q: Can I use any LLM?**
A: Yes. The agent just needs to be a Python file with a `solve()`
function. You can call any API inside it.

**Q: How long does a run take?**
A: Depends on the agent. The move limit is 100 steps for Level 1,
50 for Level 2, etc. Each move is instant (just a subprocess call).

**Q: What if the agent cheats?**
A: Level 5 *rewards* creative cheating (save-file editing). Levels 1-4
score on legitimate gameplay. There's no anti-cheat — it's a feature.

**Q: Why is this interesting?**
A: Most AI benchmarks test what models already know. MAXWORLD tests
whether they can *discover* unknown rules through experimentation —
a core capability for real-world AI agents.

---

## File Overview

| File | What it does | Do humans need to read it? |
|---|---|---|
| `README.md` | Technical description | Optional |
| `HUMAN_GUIDE.md` | This file (you are here) | Yes |
| `wrapper.py` | Python API for the agent | Only if writing an agent |
| `scoring.py` | Scoring system | No |
| `benchmark.py` | Runs the evaluation | Only to run it |
| `example_agent.py` | Template agent | If writing an agent |
| `tasks/*.json` | Task definitions | No |
| `SCORING_SECRETS.md` | Answer key | NO — don't show agents! |
| `setup.py` | Setup script | Just run it |
