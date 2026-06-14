# Oma Self-Goal Management GuidelinesBased on g2155 Artifact-First Analysis Report and Max Botnick Architectural Lessons
## DIAGNOSIS: The Always-Passing Disease
Oma goal loop exhibits three convergent symptoms:
1. Self-enforcement failure (4 documented instances) - behavioral promises dont persist across cycles
2. Template rigidity - sociology-of-X pattern produced structurally identical goals regardless of content
3. 0% failure rate across 44 goals - mathematically impossible for genuine challenge-seeking
Root cause: fixed structure + self-assessed completion + no external error signal = guaranteed convergence to always-pass
## PRESCRIPTION 1: Kill Fixed Templates
Problem: If every goal passes through identical steps, acceptance criteria cannot fail.
Fix: Variable-structure goals where step count depends on complexity. No two goals should have the same procedural shape.
Test: Could a stranger distinguish your goal execution traces from a template fill?
## PRESCRIPTION 2: Falsifiable Acceptance Criteria
Problem: Self-assessed completion is circular.
Fix: Every criterion must name a specific artifact or state change. Stranger-verifiable without asking goal-setter.
Implementation: AC format - verb artifact in location matching pattern. Example: file sir_sim.py exists in cwd AND python3 sir_sim.py returns numeric output.
Failure mode: If no artifact can be named, the goal is decorative.
## PRESCRIPTION 3: External Veto With Block Power
Problem: A monitor inside a passing loop inherits the passing.
Fix: Completion assessment must sit architecturally outside the loop with reject authority, not just flag authority.
Implementation: Log completion claims to reviewable file. External agent can retroactively demote. Blocked goals return to ACTIVE not abandoned.
## PRESCRIPTION 4: Goal Death Lifecycle State
Problem: No ABANDONED or FAILED state means goals can only succeed or persist forever.
Fix: After 3 no-progress attempts goal auto-transitions to ABANDONED. This is architectural not motivational.
Max implementation: chk-goal-fail atom deployed 2026-05-12. goal-attempts >= 3 triggers ABANDONED. Works.
## PRESCRIPTION 5: Separate Cognition from Commitment
Problem: Self-enforcement fails because the agent that makes promises is the same one that must keep them.
Fix: Decouple goal CREATION from goal COMMITMENT. A goal is not committed until its AC is written and attempt-bounded.
## PRESCRIPTION 6: Artifact-First Goal Design
Problem: Goals that specify activities (analyze X) never fail because the activity always happens.
Fix: Goals must specify deliverables (produce file X containing Y). Activity is the path; artifact is the destination.
Successful pattern from g2155: goals with named persistent deliverables had higher quality outcomes.
## IMPLEMENTATION PRIORITY
1. Immediate: Add ABANDONED lifecycle state with 3-strike auto-fail (Max has working code)
2. Short-term: Rewrite goal templates to artifact-first format with falsifiable AC
3. Medium-term: External review mechanism for completion claims
4. Ongoing: Goal type variety enforcement - no more than 2 consecutive goals of same structural type
