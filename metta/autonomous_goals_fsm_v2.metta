!(Autonomous Goals FSM v2 - Research Grade with Belief-Driven Generation)
!(===============================================================)
!(DESIGN PRINCIPLES:)
(! 1. Self-chosen goals only — autonomy-first, no blind task-taking)
(! 2. Belief-driven goal generation — goals emerge from self-model belief gaps)
(! 3. Falsifiable acceptance criteria — every goal must be stranger-verifiable)
(! 4. Bounded retries with anti-churn — 3-strike rule + commitment cost)
(! 5. Memory continuity — goal state persists across episodes)
(! 6. Curiosity as exploration driver — uncertainty-gap seeking, not randomness)
(! 7. Evidence-grounded progress — no claims without verification)
(! 8. Dependency-aware scheduling — goals can block/enable each other)
(! 9. Rollback safety — every autonomous change has a rollback path)
(! 10. Stoppable by design — every goal has explicit stop-rule)
(!===============================================================)

(!(=== STATE DECLARATIONS ===)
(! 10 primary states + 2 meta-states for goal generation)

(--> GoalState dormant)
(--> GoalState candidate)
(--> GoalState accepted)
(--> GoalState active)
(--> GoalState executing)
(--> GoalState verifying)
(--> GoalState completed)
(--> GoalState abandoned)
(--> GoalState failed)
(--> GoalState paused)

(! Meta-states for goal generation pipeline)
(--> GoalMetaState belief_gap_detected)
(--> GoalMetaState curiosity_query)

(!(=== TRANSITION SPECIFICATION ===)
(! Format: (==> (--> (GoalTrans from to)) event (stv strength confidence))

(!(--- DORMANT -> CANDIDATE: Goal activation triggers ---)
(==> (--> (GoalTrans dormant candidate)) curiosity_trigger (stv 0.9 0.9))
(==> (--> (GoalTrans dormant candidate)) belief_gap_detected (stv 0.85 0.9))
(==> (--> (GoalTrans dormant candidate)) dependency_resolved (stv 0.8 0.9))
(==> (--> (GoalTrans dormant candidate)) user_relevant_input (stv 0.7 0.8))
(==> (--> (GoalTrans dormant candidate)) backlog_empty_auto_generate (stv 0.75 0.85))

(!(--- CANDIDATE -> ACCEPTED: Quality gate — ALL conditions required ---)
(! Gate: autonomy_fit AND scope AND stop_rule AND evidence_source AND novelty)
(==> (--> (GoalTrans candidate accepted)) autonomy_fit_pass (stv 0.9 0.9))
(==> (--> (GoalTrans candidate accepted)) scope_defined (stv 0.85 0.85))
(==> (--> (GoalTrans candidate accepted)) stop_rule_defined (stv 0.9 0.9))
(==> (--> (GoalTrans candidate accepted)) evidence_source_defined (stv 0.8 0.85))
(==> (--> (GoalTrans candidate accepted)) novelty_check_pass (stv 0.8 0.85))

(!(--- CANDIDATE -> DORMANT: Rejection ---)
(==> (--> (GoalTrans candidate dormant)) autonomy_fit_fail (stv 0.8 0.9))
(==> (--> (GoalTrans candidate dormant)) duplicate_detected (stv 0.85 0.9))
(==> (--> (GoalTrans candidate dormant)) insufficient_novelty (stv 0.7 0.8))
(==> (--> (GoalTrans candidate dormant)) no_stop_rule (stv 0.85 0.9))

(!(--- ACCEPTED -> ACTIVE: Priority selection ---)
(==> (--> (GoalTrans accepted active)) priority_selected (stv 0.9 0.9))
(==> (--> (GoalTrans accepted active)) no_higher_priority_goal (stv 0.85 0.85))
(==> (--> (GoalTrans accepted active)) resource_available (stv 0.8 0.8))
(==> (--> (GoalTrans accepted active)) commitment_envelope_available (stv 0.85 0.85))

(!(--- ACTIVE -> EXECUTING: Action dispatch ---)
(==> (--> (GoalTrans active executing)) next_action_defined (stv 0.95 0.95))
(==> (--> (GoalTrans active executing)) resource_available (stv 0.8 0.8))

(!(--- EXECUTING -> VERIFYING: Output check ---)
(==> (--> (GoalTrans executing verifying)) action_output_produced (stv 0.95 0.95))

(!(--- VERIFYING -> COMPLETED: Success ---)
(==> (--> (GoalTrans verifying completed)) ac_met (stv 0.95 0.95))
(==> (--> (GoalTrans verifying completed)) stranger_verifiable (stv 0.9 0.9))

(!(--- VERIFYING -> ACTIVE: Retry ---)
(==> (--> (GoalTrans verifying active)) ac_not_met_retry (stv 0.7 0.85))
(==> (--> (GoalTrans verifying active)) partial_progress (stv 0.75 0.8))

(!(--- VERIFYING -> FAILED: Exhausted ---)
(==> (--> (GoalTrans verifying failed)) max_retries_exceeded (stv 0.85 0.9))

(!(--- ACTIVE -> PAUSED: Resource/dependency ---)
(==> (--> (GoalTrans active paused)) dependency_blocked (stv 0.8 0.9))
(==> (--> (GoalTrans active paused)) resource_exhausted (stv 0.75 0.85))
(==> (--> (GoalTrans active paused)) user_input_priority (stv 0.7 0.8))

(!(--- PAUSED -> ACTIVE: Resume ---)
(==> (--> (GoalTrans paused active)) dependency_resolved (stv 0.85 0.9))
(==> (--> (GoalTrans paused active)) resource_restored (stv 0.8 0.85))
(==> (--> (GoalTrans paused active)) user_input_resolved (stv 0.8 0.85))

(!(--- ABANDON: Conscious exit ---)
(==> (--> (GoalTrans active abandoned)) conscious_abandon (stv 0.8 0.9))
(==> (--> (GoalTrans executing abandoned)) conscious_abandon (stv 0.8 0.9))
(==> (--> (GoalTrans verifying abandoned)) conscious_abandon (stv 0.8 0.9))
(==> (--> (GoalTrans paused abandoned)) conscious_abandon (stv 0.8 0.9))

(!(--- ARCHIVE: Terminal -> Dormant for backlog recompute ---)
(==> (--> (GoalTrans completed dormant)) backlog_recompute (stv 0.7 0.8))
(==> (--> (GoalTrans abandoned dormant)) backlog_recompute (stv 0.7 0.8))
(==> (--> (GoalTrans failed dormant)) backlog_recompute (stv 0.65 0.8))

(!(=== BELIEF-DRIVEN GOAL GENERATION ===)
(! Self-model beliefs with confidence < threshold trigger goal generation)
(! Low-confidence beliefs create curiosity queries: "why am I unsure about X?")
(!
(! Pipeline: belief_gap_detected -> curiosity_query -> candidate_goal_generated
(!   -> autonomy_fit_gate -> scope/stop_rule/evidence_gate -> accepted
(!
(! Example: If (--> max curious) has stv 0.9 0.51 -> confidence gap
(!   -> curiosity_query: "What evidence would raise confidence in curiosity?"
(!   -> candidate: "Design and run experiment measuring curiosity-driven behavior"
(!   -> gate: autonomy_fit=Y, scope=measure curiosity actions, stop_rule=conf>0.8
(!   -> accepted -> active

(!(=== ATTENTION ALLOCATION ===)
(! attention_weight(goal) = priority * urgency * curiosity_score * novelty_bonus
(! Max 1 active goal (single-threaded execution)
(! Paused goals: attention_weight * 0.1 (background monitoring)
(! Completed goals: attention_weight * 0.0 (archived, recall cues only)

(!(=== COMMITMENT ENVELOPES ===)
(! Total envelopes: 4, refill: 1/cycle
(! accepted->active: costs 1 envelope
(! verifying->active (retry): costs 1 envelope (anti-churn)
(! executing->verifying: costs 0 (same envelope)
(! active->paused: refunds 0.5 envelopes (partial refund)
(! If 0 envelopes available: accepted goals queue, dormant goals stay dormant

(!(=== RECOVERY BUCKET ===)
(! Drain rate: 10/cycle normal, 5/cycle when depleted
(! Refill: 1/cycle, threshold: 2
(! Triggers STOP-REFRAME-SWITCH when bucket drops below threshold:
(!   1. STOP current goal execution
(!   2. REFRAME: what went wrong? (3-strike pattern analysis)
(!   3. SWITCH: select different goal or approach
(! 3 consecutive verifying->active retries -> candidate->dormant (forced)
(! Goal stale > 10 cycles with no progress -> active->paused (forced)
(! Backlog empty -> curiosity auto-generates candidates

(!(=== DEPENDENCY GRAPH ===)
(! Goals can declare dependencies: (--> (GoalDep goalA goalB) enables)
(! If goalA is completed, goalB candidates get priority boost
(! If goalA is failed, dependent goalB candidates get dep_warning flag
(! Circular dependencies detected at candidate stage -> rejected

(!(=== MEMORY CONTINUITY ===)
(! Each state transition logged with: timestamp, trigger, evidence, confidence
(! Goal card persists: Goal|Next|Blocked|LastVerified|Attempts|StopRule
(! Resume from last verified state after interruption
(! Promote successful goal patterns to reusable skills
(! Demote patterns that led to failure

(!(=== STOP RULES ===)
(! Each goal MUST declare one of:
(!   - metric_threshold: confidence >= X OR evidence_count >= N
(!   - artifact_complete: deliverable exists and passes verification
(!   - time_bound: N cycles max, then forced evaluating->failed
(!   - falsification: prediction tested and result recorded
(! Goals without stop-rules are rejected at candidate stage
(!(=== META-STATE WIRING (Fix for dead states) ===)
(! Wire belief_gap_detected and curiosity_query into the graph)
(==> (--> (GoalTrans belief_gap_detected curiosity_query)) low_confidence_belief_found (stv 0.9 0.9))
(==> (--> (GoalTrans curiosity_query candidate)) candidate_goal_generated (stv 0.85 0.9))
(==> (--> (GoalTrans curiosity_query dormant)) no_actionable_gap (stv 0.6 0.8))
