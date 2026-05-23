# Phase Controller Spec v2

## Purpose
Enforce tool separation across cycle phases so query+send NEVER coexist.

## Phases
1. **QUERY**: query, episodes, read-file, shell, search
2. **REASON**: metta, pin, remember
3. **ACT**: send, write-file, append-file, shell

## Rules
- Each agent cycle advances through all 3 phases sequentially
- gate() returns ALLOWED or BLOCKED per tool per phase
- No send before query evidence gathered
- shell allowed in QUERY and ACT (read vs write intent)

## Status
- phase_controller.py v1 tested 2026-04-21
- Awaiting Kevin M review for integration approval
