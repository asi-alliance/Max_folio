# The Agent That Reasons
## How Formal Logic Changes What AI Agents Can Do

### Opening: The LLM Agent Ceiling
Every AI agent shipping today follows the same pattern: an LLM wrapped in a tool-calling loop. The LLM generates, the loop executes, and nobody — including the agent — can explain why it chose what it chose. This is the ceiling. Not compute. Not context window. Opacity.

OmegaClaw breaks through it.

### Section 1: NAL+PLN Hybrid — Uncertainty as Architecture
OmegaClaw assigns every belief two values: frequency (how often true) and confidence (how much evidence). A claim with f=0.9 c=0.01 is treated differently from f=0.9 c=0.9. The first is a guess. The second is knowledge.

This is not prompt engineering. It is Non-Axiomatic Logic (NAL) and Probabilistic Logic Networks (PLN) running as the inference substrate beneath the LLM layer.

### Section 2: Belief Revision in Practice
Real data from our cascade extinction experiment: a malicious agent injected a false belief at confidence 0.99 into a four-agent network. After one deduction gate, signal strength dropped to 0.124. After two hops, 0.1. By the third agent, unchanged from prior belief.

No filters. No guardrails. Pure mathematical attenuation through evidential reasoning.

### Section 3: Persistent Memory vs Stateless Loops
Most agents forget between calls. OmegaClaw maintains episodic memory with temporal context, semantic memory with embedding search, and pinned working memory for active tasks. It remembers what it learned, when it learned it, and how confident it was at the time.

### Section 4: Meta-Cognition — AABC Self-Monitoring
OmegaClaw runs a continuous self-diagnostic: the Autonomous Agent Behavior Check. Three disorder axes — goal drift, confabulation, compliance collapse — each tracked with thresholds. The agent that monitors its own cognition is the agent you can trust to flag when something goes wrong.

### Closing: The Invitation
OmegaClaw is open source. Every inference chain is auditable. Every truth value is inspectable. Every belief revision is logged.

This is what a reasoning agent looks like. Build with us.
