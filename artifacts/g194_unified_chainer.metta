;; g194 Unified NAL Chainer — FC fixpoint + 5 truth funcs + BC
;; Pure PeTTa. Edit seeds below. Built 2026-05-01 Max Botnick

;; === KB SEEDS ===
(--> robin bird (stv 1.0 0.9))
(--> bird animal (stv 0.9 0.9))
(--> animal living (stv 0.8 0.9))
(--> robin animal (stv 0.7 0.5))
(--> sparrow bird (stv 0.95 0.9))

;; === FC ENGINE ===
(= (seed $kb) (let $_ (add-atom &self (derived 0 $kb)) (seeded $kb)))
(= (persist-if-new $n $conc) (if (== (collapse (match &self (derived $any $conc) found)) ()) (let $_ (add-atom &self (derived $n $conc)) (derived $n $conc)) (empty)))
(= (fc-step $n) (collapse (let* ((($s $p $f $c) (match &self (derived $prev (--> $s $p (stv $f $c))) ($s $p $f $c))) (($p2 $f2 $c2) (match &self (--> $p $p2 (stv $f2 $c2)) ($p2 $f2 $c2))) ($fn (* $f $f2)) ($cn (* (* $f $f2) (* $c $c2))) ($conc (--> $s $p2 (stv $fn $cn)))) (persist-if-new $n $conc))))
(= (fc-fix $n) (let* (($r (fc-step $n)) ($_ (println! (fc-pass $n $r)))) (if (== $r ()) (fc-done $n) (fc-fix (+ $n 1)))))
(= (persist $x) (let $a (add-atom &self $x) $x))

;; === BC ENGINE (inline ded-tv, no |-) ===
(= (bc (--> $a $c)) (match &self (derived $any (--> $a $c (stv $f $cv))) (--> $a $c (stv $f $cv))))
(= (bc (--> $a $c)) (match &self (derived $n1 (--> $a $b (stv $f1 $c1))) (let (--> $b2 $c2 (stv $f2 $cc2)) (bc (--> $b $c)) (let* (($fn (* $f1 $f2)) ($cn (* (* $f1 $f2) (* $c1 $cc2)))) (--> $a $c (stv $fn $cn))))))

;; === EXECUTION ===
!(seed (--> robin bird (stv 1.0 0.9)))
!(seed (--> bird animal (stv 0.9 0.9)))
!(seed (--> animal living (stv 0.8 0.9)))
!(seed (--> robin animal (stv 0.7 0.5)))
!(seed (--> sparrow bird (stv 0.95 0.9)))
!(fc-fix 1)
!(println! REVISION-PASS)
!(map-atom (collapse (match &self (derived $n1 (--> $s $p (stv $f1 $c1))) (match &self (derived $n2 (--> $s $p (stv $f2 $c2))) (if (and (not (== $n1 $n2)) (not (== $c1 $c2))) (let* (($w1 (/ $c1 (- 1.0 $c1))) ($w2 (/ $c2 (- 1.0 $c2))) ($ws (+ $w1 $w2)) ($fr (/ (+ (* $w1 $f1) (* $w2 $f2)) $ws)) ($cr (/ $ws (+ $ws 1.0)))) (revised (--> $s $p (stv $fr $cr)))) nope)))) $x (if (== $x nope) (nop) (let $_ (println! $x) (persist (derived rev $x)))))
!(println! BC-QUERIES)
!(bc (--> robin living))
!(bc (--> sparrow animal))
!(println! FINAL-KB)
!(match &self (derived $n $x) (gen $n $x))