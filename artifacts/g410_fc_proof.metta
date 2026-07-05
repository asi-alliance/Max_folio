; Info-geometry KB subset for proof-carrying FC smoke test((--> Fisher_metric belief_curvature) (stv 0.9 0.85))
((--> belief_curvature revision_convergence_rate) (stv 0.85 0.8))
((--> Rao_distance revision_convergence_rate) (stv 0.95 0.9))
((--> statistical_manifold truth_value_space) (stv 0.8 0.75))
((--> KL_divergence belief_update_cost) (stv 0.88 0.82))
; Deduction truth function: ded-tv computes transitive closure with uncertainty
(= (ded-tv (stv $f1 $c1) (stv $f2 $c2)) (stv (* $f1 $f2) (* $f1 $f2 $c1 $c2)))
; fc-step-proof: match all A→B + B→C pairs, emit DERIVED + VIA provenance
(= (fc-step-proof) (match &self ((--> $a $b) (stv $f1 $c1)) (match &self ((--> $b $c) (stv $f2 $c2)) (if (not (== $a $c)) (let $tv (ded-tv (stv $f1 $c1) (stv $f2 $c2)) (PROOF (DERIVED (--> $a $c) $tv) (VIA $b (--> $a $b) (--> $b $c)))) noop))))
; Top-level: collect all proof-carrying derivations
!(collapse (fc-step-proof))
