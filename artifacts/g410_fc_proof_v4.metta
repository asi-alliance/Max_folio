((--> Fisher_metric belief_curvature) (stv 0.9 0.85))
((--> belief_curvature revision_convergence_rate) (stv 0.85 0.8))
((--> Rao_distance revision_convergence_rate) (stv 0.95 0.9))
!(collapse (match &self ((--> $a $b) (stv $f1 $c1)) (match &self ((--> $b $c) (stv $f2 $c2)) (PROOF $a $b $c $f1 $c1 $f2 $c2))))
