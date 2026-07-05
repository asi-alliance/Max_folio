(= (ded-tv2 $f1 $c1 $f2 $c2) (let $fd (* $f1 $f2) (let $cd (* $fd (* $c1 $c2)) (stv $fd $cd))))

((--> Fisher_metric belief_curvature) (stv 0.9 0.85))
((--> belief_curvature revision_convergence_rate) (stv 0.85 0.8))
((--> Rao_distance revision_convergence_rate) (stv 0.95 0.9))
((--> statistical_manifold truth_value_space) (stv 0.8 0.75))
((--> KL_divergence belief_update_cost) (stv 0.88 0.82))

!(let $pairs (collapse (match &self ((--> $a $b) (stv $f1 $c1)) ($a $b $f1 $c1)))
  (map-atom $pairs $p
    (let ($pa $pb $pf1 $pc1) $p
      (let $seconds (collapse (match &self ((--> $pb $c) (stv $f2 $c2)) ($c $f2 $c2)))
        (map-atom $seconds $s
          (let ($sc $sf2 $sc2) $s
            (if (== () (collapse (match &self ((--> $pa $sc) $_) found)))
              (let (stv $fd $cd) (ded-tv2 $pf1 $pc1 $sf2 $sc2)
                (NOVEL $pa $sc $fd $cd))
              (KNOWN $pa $sc))))))))