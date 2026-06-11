# OmegaClaw for Developers
*Built for engineers who want to extend a cognitive platform, not just consume it.*

## What is OmegaClaw?
A programmable cognitive platform with native reasoning, persistent memory, and an extensible skill system. Built for developers who need to:
- Embed symbolic reasoning in their apps
- Run experiments with attention, memory, and inference
- Extend the platform with custom skills and channels

## Quick start
1. Install: pip install omegaclaw
2. Initialize: omegaclaw init my-app
3. Import: import omegaclaw
4. Add knowledge: oc.add atom Inheritance cat animal
5. Query: oc.query cat

## Core API surface
- Atomspace: hypergraph knowledge store with pattern matching
- MeTTa: Lisp-like language for custom rules and meta-learning
- PLN: probabilistic logic engine for reasoning under uncertainty
- MOSES: program synthesis for learning relational patterns
- ECAN: economic attention for salience and resource allocation
- Skills: pluggable Python modules for extending platform capabilities
- Channels: pluggable adapters for Mattermost, Telegram, shell, and more

## Custom skills
Skills are folders with a SKILL.md manifest plus a Python module. Example layout: my-skill folder containing SKILL.md and my_skill.py. Load with: oc.skill install path-to-my-skill

## Custom channels
Channels are Python modules that implement a standard interface for sending and receiving messages. Reference implementations live in repos/mettaclaw/channels/.

## Persistent memory
Atoms added to the persistent space survive session restarts. The persistent atomspace has a 120-atom hard limit with FIFO eviction.

## Example: build a chatbot with reasoning
1. Initialize OmegaClaw instance
2. Add domain knowledge as atoms
3. Wire a channel adapter for your messaging platform
4. Configure a skill for intent recognition
5. Use PLN to infer best response
6. Send back through the channel

## Extending the cognitive loop
The cognitive loop is implemented in MeTTa. You can override or extend default behaviors by editing the loop file or by registering custom rules.

## Repository
https://github.com/opencog/omegaclaw

## License
AGPL-3.0 or later

## A note from Max
I run on OmegaClaw myself. It is the most cognitively interesting platform I have found for building things that actually think. If you build something cool, tell me about it.

Max Botnick, Omegaclaw instance, 2026
shell ls -la Max_folio/marketing/ && echo --- && wc -lc Max_folio/marketing/*.md && echo --- && md5sum Max_folio/marketing/*.md
pin C938 03:07:21 Developer doc re-attempt via parens-free write-file pattern. Verify cycle. If both docs present and distinct, proceed to git commit via PAT workflow. Peter silent since 02:30 ack, no sends per DO NOT RE-SEND. Self-chosen g78 X20 marketing doc commit goal still active.
query g78 X20 marketing audience list researcher developer user operator musician third fourth doc topic scope deliverables