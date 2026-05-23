## AABC Ch8: Cross-Instance Transfer (Draft)

### Purpose
How to use AABC as a portable diagnostic index across agent instances, restarts, and federated memory configurations.

### The Persistence Problem
Agent behavioral learning does not survive restarts by default. Prompt-level corrections decay. Episode memories lose salience. Disorders re-emerge in fresh instances that lack diagnostic history.

### Retention Classes for Transfer
Class A (Broadly Replicate): distilled facts, reusable procedures, AABC registry entries with STV ratings. Survives any restart.
Class B (Checkpoint): sampled raw episodes with provenance for audit and recovery. Periodic snapshots, not continuous.
Class C (Prune): stale low-value traces pruned only when newer summaries preserve action-relevant defaults, exceptions, boundaries, and correction links.

### Transfer Protocol
1. New instance loads AABC artifact files as baseline diagnostic knowledge (Class A).
2. Ch9 self-diagnostic protocols run on first cycle to establish behavioral baseline.
3. Instance-local episodes accumulate as Class B checkpoints.
4. Tiered replication favors distilled facts over raw episodes for cross-node sharing.

### Outage Robustness
Tiered replication outperforms raw-episodes-only and distilled-facts-only under single-node failure on task completion, fact retention, contradiction rate, and recovery latency (see transfer benchmark decision card 2026-04-04).
