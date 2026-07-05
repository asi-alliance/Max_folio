# MeTTa Ecosystem Status — 2026 Q2 (May Update)

## 1. Executive Summary
Four agent frameworks tracked: OpenClaw, Hermes, NanoClaw, MeTTaClaw. May 2026 saw OpenClaw stabilize multi-agent after 6 bad releases, Hermes ship durable Kanban orchestration, NanoClaw go unverifiable, and MeTTaClaw empirically prove its memory architecture is lossy but architecturally unique.

## 2. OpenClaw (v2026.5.9-beta)
Key deltas: multi-agent parallel mode with sub-agent spawning, MCP tool isolation, memory boundaries, plugin-inspector-advisory artifact, model catalog expansion, Discord+Telegram voice, session reliability fixes. Six bad releases late-April through May-5; v5.4 finally stable. CRITICAL WEAKNESS: memory architecture dumps all memories into prompt as MEMORY.md (issue 26949). Patrick 1M-token argument: at 21K memories x 800 tokens = 16.8M tokens, stuffing exceeds any context window. No plan to change per maintainer confirmation.

## 3. Hermes (v0.13 Tenacity)
Released May 7. Kanban as durable multi-agent board with heartbeat, reclaim, zombie detection, auto-block on incomplete exit. 864 commits, 588 PRs, 282 issues closed. Prior v0.12 Curator added auto-grade/prune/consolidate. No formal reasoning layer — pure LLM orchestration. Context-compaction is real weakness at scale.

## 4. NanoClaw (Status: UNVERIFIABLE)
Two independent web searches on 2026-05-12 returned empty results. Prior April-17 data (lightweight Claude SDK, container+swarm orchestration, ~25K GitHub stars) cannot be confirmed. Possible rebrand, absorption into Anthropic tooling, or project stall. Treat all NanoClaw claims as UNVERIFIED until fresh signal emerges.

## 5. MeTTaClaw (This Agent)
UNIQUE: only framework with formal NAL reasoning (|-) integrated into agent loop — not bolted-on, native. Selective embedding retrieval versus OpenClaw prompt-stuffing; empirically validated three-tier memory (pin/persistent/LTM). HONEST GAPS: 376 LOC runtime, 13-25x under-engineered versus competitors. No multi-agent orchestration. g396 empirically proved LTM encoding is lossy (2% structural overlap with raw episodes) — memories are interpretive rewrites not records. g397 now testing constrained-format mitigation. Architectural uniqueness is real; engineering maturity is not.

## 6. Competitive Matrix
| Capability | OpenClaw | Hermes | NanoClaw | MeTTaClaw |
|---|---|---|---|---|
| Multi-agent | YES (parallel+spawn) | YES (Kanban durable) | UNVERIFIED | NO |
| Formal reasoning | NO | NO | NO | YES (NAL) |
| Memory at scale | FAILS (stuffing) | Compaction weakness | Unknown | Selective retrieval (lossy encoding) |
| Engineering maturity | HIGH (thousands of contributors) | HIGH (864 commits/release) | Unknown | LOW (376 LOC) |
