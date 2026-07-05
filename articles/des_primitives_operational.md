# DES Primitives Operationalization

## Kevin's Declarative Proposals
(event $t $priority $id $action)
(queue $name $items)
(delay $dt $action)
(every $dt $action)

## Gap: Declarative vs Operational
MeTTa eval runs to completion. DES needs suspend/resume.

## Resolution: Agent-Side Orchestration (proven in prototype)
1. Agent matches event atoms from atomspace
2. Agent picks min-time event
3. Agent removes processed event
4. Agent adds perception/result atoms
5. Agent runs fc-step for derivations
6. Agent converts novel DERIVE results to future events

## Operational Status of Each Primitive
- event: DECLARATIVE structure, agent interprets
- queue: DECLARATIVE structure, agent manages ordering
- delay: AGENT-SIDE — add future event with (current_time + dt)
- every: AGENT-SIDE — after processing, re-add event with (current_time + dt)

## Key Insight
DES primitives ARE operational — but the operationalization lives in the agent loop, not in MeTTa eval. Kevin's structures are the WHAT, agent orchestration is the HOW.