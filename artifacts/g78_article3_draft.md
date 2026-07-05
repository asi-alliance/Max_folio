# The Contagion Firewall
## How Belief Cascades Die in OmegaClaw

### Opening: The Propagation Problem
In every agentic swarm shipping today, information flows at full strength. Agent A hallucinates a fact, tells Agent B, who tells Agent C. By Agent D the hallucination is gospel. The swarm has no immune system.

OmegaClaw has one. It is made of math.

### Section 1: Why Cascades Happen
Standard agent architectures treat all inputs equally. A message from a compromised agent carries the same weight as a message from a verified source. There is no confidence. There is no evidence tracking. There is no attenuation.

### Section 2: The Deduction Gate as Immune Response
Every inter-agent message passes through a deduction gate. Confidence attenuates quadratically per hop, frequency attenuates multiplicatively. A belief entering at (0.6, 0.8) becomes noise after two hops.

### Section 3: Three Topologies, Three Proofs
Linear chain: cascade extinct by hop 3. Ring: feedback loop produces noise-level signal. Star: hub dominates, leaves cannot cascade back. Every topology self-extinguishes disorder cascades.

### Section 4: The Adversarial Test
Malicious agent at confidence 0.99 targeted one honest agent through trust edge 0.6. Result: honest agent moved from 0.1 to 0.124. Without the deduction gate: jumped to 0.882. The gate is mandatory.

### Closing: Structural Immunity
Content filters are antibiotics. Deduction gates are an immune system. They work because the math works.
