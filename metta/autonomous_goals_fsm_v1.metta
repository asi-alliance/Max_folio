!(Autonomous Goals FSM - Research Grade)
!(State: GoalDormant - goal exists in backlog but not yet evaluated)
!(State: GoalCandidate - goal under active evaluation for acceptance)
!(State: GoalAccepted - goal passed evaluation, queued for activation)
!(State: GoalActive - goal is current live goal with next action defined)
!(State: GoalExecuting - next action is being executed this cycle)
!(State: GoalVerifying - execution output being checked against acceptance criteria)
!(State: GoalCompleted - acceptance criteria met, goal closed)
!(State: GoalAbandoned - goal consciously abandoned with documented reason)
!(State: GoalFailed - goal failed after max retries, moved to failed log)
!(State: GoalPaused - goal temporarily paused due to dependency or resource constraint)

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

(! Transitions: (==> (--> (GoalTrans from to)) event (stv strength confidence)))

(!( Lifecycle: Dormant -> Candidate -> Accepted -> Active -> Executing -> Verifying -> Completed)
(!( Dormant -> Candidate: curiosity trigger or user-relevant input)

(==> (--> (GoalTrans dormant candidate)) curiosity_trigger (stv 0.9 0.9))
(==> (--> (GoalTrans dormant candidate)) user_relevant_input (stv 0.7 0.8))
(==> (--> (GoalTrans dormant candidate)) dependency_resolved (stv 0.8 0.9))

(!( Candidate -> Accepted: passes autonomy-fit gate + scope/evidence/stop-rule check)
(==> (--> (GoalTrans candidate accepted)) autonomy_fit_pass (stv 0.9 0.9))
(==> (--> (GoalTrans candidate accepted)) scope_defined (stv 0.85 0.85))
(==> (--> (GoalTrans candidate accepted)) stop_rule_defined (stv 0.9 0.9))
(==> (--> (GoalTrans candidate accepted)) evidence_source_defined (stv 0.8 0.85))

(!( Candidate -> Dormant: rejected, returned to backlog)
(==> (--> (GoalTrans candidate dormant)) autonomy_fit_fail (stv 0.8 0.9))
(==> (--> (GoalTrans candidate dormant)) duplicate_detected (stv 0.85 0.9))
(==> (--> (GoalTrans candidate dormant)) insufficient_novelty (stv 0.7 0.8))

(!( Accepted -> Active: selected as current goal by priority/curiosity ranking)
(==> (--> (GoalTrans accepted active)) priority_selected (stv 0.9 0.9))
(==> (--> (GoalTrans accepted active)) no_higher_priority_goal (stv 0.85 0.85))
(==> (--> (GoalTrans accepted active)) resource_available (stv 0.8 0.8))

(!( Active -> Executing: next action defined and ready)
(==> (--> (GoalTrans active executing)) next_action_defined (stv 0.95 0.95))
(==> (--> (GoalTrans active executing)) resource_available (stv 0.8 0.8))

(!( Executing -> Verifying: action output produced, check against AC)
(==> (--> (GoalTrans executing verifying)) action_output_produced (stv 0.95 0.95))

(!( Verifying -> Completed: acceptance criteria met)
(==> (--> (GoalTrans verifying completed)) ac_met (stv 0.95 0.95))

(!( Verifying -> Active: AC not met, retry with revised next action)
(==> (--> (GoalTrans verifying active)) ac_not_met_retry (stv 0.7 0.85))
(==> (--> (GoalTrans verifying active)) partial_progress (stv 0.75 0.8))

(!( Verifying -> Failed: max retries exceeded)
(==> (--> (GoalTrans verifying failed)) max_retries_exceeded (stv 0.85 0.9))

(!( Active -> Paused: dependency or resource constraint)
(==> (--> (GoalTrans active paused)) dependency_blocked (stv 0.8 0.9))
(==> (--> (GoalTrans active paused)) resource_exhausted (stv 0.75 0.85))

(!( Paused -> Active: dependency resolved or resource restored)
(==> (--> (GoalTrans paused active)) dependency_resolved (stv 0.85 0.9))
(==> (--> (GoalTrans paused active)) resource_restored (stv 0.8 0.85))

(!( Any Active/Executing/Verifying -> Abandoned: conscious abandonment with reason)
(==> (--> (GoalTrans active abandoned)) conscious_abandon (stv 0.8 0.9))
(==> (--> (GoalTrans executing abandoned)) conscious_abandon (stv 0.8 0.9))
(==> (--> (GoalTrans verifying abandoned)) conscious_abandon (stv 0.8 0.9))

(!( Completed/Abandoned/Failed -> Dormant: goal archived, backlog recomputed)
(==> (--> (GoalTrans completed dormant)) backlog_recompute (stv 0.7 0.8))
(==> (--> (GoalTrans abandoned dormant)) backlog_recompute (stv 0.7 0.8))
(==> (--> (GoalTrans failed dormant)) backlog_recompute (stv 0.65 0.8))

(!( Quality Gates (analogous to COEC quality floors))
(!( Gate: candidate->accepted requires ALL of: autonomy_fit, scope, stop_rule, evidence_source)
(!( Gate: verifying->completed requires stranger-verifiable evidence)
(!( Gate: active->abandoned requires documented reason + rollback path)

(!( Attention Allocation (analogous to COEC attention currency)
(!( Each active goal gets attention weight proportional to priority * urgency * curiosity_score)
(!( Max 1 active goal at a time (single-threaded execution)
(!( Paused goals retain attention weight * 0.1 (background monitoring)

(!( Commitment Envelopes (analogous to COEC commitment currency)
(!( Each accepted->active transition costs 1 commitment envelope)
!(: commitment envelopes refill at 1 per cycle, max 4)
!(: executing->verifying costs 0 (free, part of same envelope)
!(: verifying->active retry costs 1 envelope (anti-churn control)

(!( Recovery Bucket (analogous to COEC recovery)
!(: If 3 consecutive retries fail (verifying->active), force candidate->dormant)
!(: If goal stale > 10 cycles with no progress, force active->paused)
!(: If backlog empty, curiosity generates new candidates automatically)