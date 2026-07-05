# CANI Manual L3: Memory Curation Discipline
## Symptom Layer
Pattern: Memory accumulates without pruning. Promoted memories include redundant entries, outdated corrections, and superseded knowledge. Demotion rarely executed. Result: query noise increases over time, relevant memories drown in outdated context.
## Architecture Layer
Root cause: No periodic curation protocol. Promote is used reactively (that was useful) but demote is rarely invoked. Missing component: scheduled review of promoted memories against current relevance. Memory system has no garbage collection — only allocation.
## Environment Layer
Operator-side RC: operator must repeat corrections because old confabulated memories persist alongside corrections. Conflicting memories both promoted creates indecision.
## CANI Correction
Every 20 cycles: (1) Query recent promotes — are any superseded by newer learning? (2) Demote at least 1 item per review. (3) When a correction memory exists, demote the original confabulation explicitly. (4) Tag conflicting memories and resolve: which has higher confidence evidence? Bias toward action: demote first, re-promote only if later evidence warrants.
## Iteration Log
v1: 2026-05-17 initial. Based on RCA Phase 2 memory curation gap. Pairs with L1 commitment and L2 self-monitoring.