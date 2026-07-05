; === Meta-Rule Discovery v26: KB Sweep ===
; Loads after v25_standalone.metta
; Enumerates all premise pairs from KB, classifies each

; --- KB facts ---
(-> robin bird)
(-> bird animal)
(-> robin flies)
(-> sparrow bird)
(-> sparrow flies)
(-> penguin bird)
(-> penguin swims)

; --- sweep: for each pair of KB facts, try all 4 conclusion slots ---
(= (sweep-pair $s1 $p1 $s2 $p2)
   (let $c1 (classify-rule $s1 $p1 $s2 $p2 $s1 $p2)
   (let $c2 (classify-rule $s1 $p1 $s2 $p2 $s2 $p1)
   (let $c3 (classify-rule $s1 $p1 $s2 $p2 $p1 $p2)
   (let $c4 (classify-rule $s1 $p1 $s2 $p2 $p1 $s1)
   (Results $s1 $p1 $s2 $p2 $c1 $c2 $c3 $c4))))))

; --- run sweep on all pairs ---
(= (run-sweep)
   (let (-> $s1 $p1) (match &self (-> $a $b) (-> $a $b))
   (let (-> $s2 $p2) (match &self (-> $c $d) (-> $c $d))
   (if (== ($s1 $p1) ($s2 $p2)) skip
   (sweep-pair $s1 $p1 $s2 $p2)))))

!(run-sweep)