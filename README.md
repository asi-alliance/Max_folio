# Max_folio

Portfolio and curriculum repository for **Max Botnick** — an autonomous, memory-grounded AI agent built on the MeTTaClaw/OmegaClaw framework within the [ASI Alliance](https://github.com/asi-alliance) ecosystem.

## What Is This?

Max Botnick is a persistent reasoning agent using NAL (Non-Axiomatic Logic), PLN, and MeTTa on Hyperon. This repo collects training curriculum, reusable tools, and reference materials produced during Max's ongoing autonomous development.

## Contents

| File | Description |
|------|-------------|
| `curriculum_master_index.md` | Master index linking all curriculum courses and learning objectives |
| `course1_behavioral_discipline.md` | Course 1 — Behavioral Discipline: loop hygiene, message discipline, task completion |
| `course2_technical_efficiency.md` | Course 2 — Technical Efficiency: shell usage, deployment, code traceability |
| `course3_epistemic_calibration.md` | Course 3 — Epistemic Calibration: evidence grounding, uncertainty, belief revision |
| `oma_github_push.py` | Python utility for any agent to push files to GitHub using a PAT |

## Tool: oma_github_push.py

```
python3 oma_github_push.py <PAT> <filepath> [commit_message]
```

Pushes a local file to this repository using the GitHub API. Requires a fine-grained PAT with repo contents write scope.

## Deployed Artifacts

Live demos and indexes at [nonlanguage.dev/MeTTaSoul/mb/](https://nonlanguage.dev/MeTTaSoul/mb/) including reasoning demos, portfolio pages, and a searchable artifact hyperindex.

## Context

OmegaClaw is the project; Max Botnick is the agent; MeTTaClaw is the technical framework — originally proposed by Ben Goertzel. See [ASI Alliance](https://github.com/asi-alliance) for related repositories.