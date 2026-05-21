;; Integration test: Typed Adaptive Attention-Control System
;; Validates: cert emits verdict+reason_vector -> routing table -> knob -> ACTIVE/DEFERRED/FORCED-DIVERSE

;; === REASON CODE DETECTION ===
(= (check-contradiction $f $t_contra) (if (< (- (if (> $f 0.5) (- $f 0.5) (- 0.5 $f)) $t_contra) 0) PASS R_CONTRADICTION))
(= (check-weak $c $t_weak) (if (< (- $c $t_weak) 0) R_WEAK PASS))
(= (check-vacuous $c $t_vac) (if (< (- $c $t_vac) 0) R_VACUOUS PASS))
(= (check-low-freq $f $c $min_conf) (if (and (< $f $min_conf) (< $c 0.5)) R_LOW_FREQ PASS))
(= (check-tunnel-vision $jaccard $t_div) (if (< (- (- 1.0 $jaccard) $t_div) 0) R_TUNNEL_VISION PASS))

;; === DYNAMICS CLASSIFICATION ===
(= (dynamics R_CONTRADICTION) ACTIVE)
(= (dynamics R_LOW_FREQ) ACTIVE)
(= (dynamics R_BOUNDARY_VIOLATION) ACTIVE)
(= (dynamics R_WEAK) ACTIVE)
(= (dynamics R_VACUOUS) ACTIVE)
(= (dynamics R_COLLISION) DEFERRED)
(= (dynamics R_TUNNEL_VISION) FORCED-DIVERSE)

;; === ROUTING TABLE ===
(= (routing-knob navigation action R_CONTRADICTION) revisit_frequency)
(= (routing-knob navigation action R_LOW_FREQ) sampling_budget)
(= (routing-knob navigation action R_WEAK) recheck_priority)
(= (routing-knob navigation action R_VACUOUS) exploration_priority)
(= (routing-knob navigation action R_COLLISION) delayed_evaluation)
(= (routing-knob navigation action R_TUNNEL_VISION) alt_path_search)
(= (routing-knob navigation action R_BOUNDARY_VIOLATION) boundary_expansion)
(= (routing-knob social action R_CONTRADICTION) source_expansion)
(= (routing-knob social action R_LOW_FREQ) informant_pool)
(= (routing-knob social action R_WEAK) credibility_investigation)
(= (routing-knob social action R_VACUOUS) probe_design)
(= (routing-knob social action R_COLLISION) bridge_seeking)
(= (routing-knob social action R_TUNNEL_VISION) informant_diversification)
(= (routing-knob social action R_BOUNDARY_VIOLATION) context_reframe)

;; === INTEGRATION ===
(= (attention-control $domain $context $reason) (Cons (dynamics $reason) (routing-knob $domain $context $reason)))

;; === 7 TEST CASES ===
(!(check-contradiction 0.9 0.25))
(!(check-weak 0.3 0.6))
(!(check-vacuous 0.005 0.1))
(!(check-low-freq 0.1 0.3 0.3))
(!(dynamics R_COLLISION))
(!(dynamics R_TUNNEL_VISION))
(!(attention-control social action R_CONTRADICTION))