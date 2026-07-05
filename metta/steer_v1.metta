;; steer-v1: Metacognitive Self-Steering Engine (g248)
;; Autonomously identifies weakest belief and generates evidence-gathering plan
;; Composes: find-weakest (foldl-atom) + cdr1-4 accessors + campaign-planner
;; 15th major artifact - 2026-05-02 Cy4401

;; MARGIN tuple accessors via pattern matching
(= (cdr1 (MARGIN $n $f $c $m)) $n)
(= (cdr2 (MARGIN $n $f $c $m)) $f)
(= (cdr3 (MARGIN $n $f $c $m)) $c)
(= (cdr4 (MARGIN $n $f $c $m)) $m)

;; find-weakest: selects MARGIN tuple with smallest margin value via foldl-atom
(= (find-weakest $margins) (foldl-atom $margins (MARGIN none 0.0 0.0 1.0) $acc $x (if (< (cdr4 $x) (cdr4 $acc)) $x $acc)))

;; steer-v1: orchestration - find weakest, compute target, invoke campaign-planner
(= (steer-v1 $margins) (let* (($w (find-weakest $margins)) ($name (cdr1 $w)) ($f (cdr2 $w)) ($c (cdr3 $w)) ($tgt (if (> (+ $c 0.15) 0.95) 0.95 (+ $c 0.15))) ($plan (campaign-planner $f $c $tgt 0.8 0.7 5))) (steer-recommendation $name $f $c $tgt $plan)))