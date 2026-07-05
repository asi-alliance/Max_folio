;; fc_iterN_unified.metta — Pure MeTTa iterative FC: ded+abd+ind, 3 passes, no bash
;; TV functions (flat args, nested binary ops)
(= (ded-tv $f1 $c1 $f2 $c2) (stv (* $f1 $f2) (* (* $f1 $f2) (* $c1 $c2))))
(= (abd-tv $f1 $c1 $f2 $c2) (let $w (* $f1 (* $c1 $c2)) (stv $f2 (/ $w (+ $w 1)))))
(= (ind-tv $f1 $c1 $f2 $c2) (let $w (* $f2 (* $c1 $c2)) (stv $f1 (/ $w (+ $w 1)))))

;; === KNOWLEDGE BASE ===
!(add-atom &self (kb robin bird 1.0 0.9))
!(add-atom &self (kb bird animal 0.9 0.9))
!(add-atom &self (kb penguin bird 0.8 0.9))
!(add-atom &self (kb animal living 1.0 0.9))
!(add-atom &self (kb robin flyer 0.85 0.7))
!(add-atom &self (kb cat pet 0.9 0.9))
!(add-atom &self (kb dog pet 0.95 0.8))

;; === PASS 0: seed derived from KB ===
!(map-atom (unique-atom (collapse (match &self (kb $s $p $f $c) (derived 0 (-> $s $p) (stv $f $c))))) $x (add-atom &self $x))

;; === PASS 1: DEDUCTION ===
!(map-atom (unique-atom (collapse (match &self (derived 0 (-> $s $m) (stv $f1 $c1)) (match &self (derived 0 (-> $m $p) (stv $f2 $c2)) (if (not (== $s $p)) (let $tv (ded-tv $f1 $c1 $f2 $c2) (derived 1 (-> $s $p) $tv)) nope))))) $x (if (== $x nope) (nop) (add-atom &self $x)))
;; PASS 1: ABDUCTION (shared predicate)
!(map-atom (collapse (match &self (derived 0 (-> $s1 $m) (stv $f1 $c1)) (match &self (derived 0 (-> $s2 $m) (stv $f2 $c2)) (if (not (== $s1 $s2)) (let $tv (abd-tv $f1 $c1 $f2 $c2) (derived 1 (-> $s2 $s1) $tv)) nope)))) $x (if (== $x nope) (nop) (add-atom &self $x)))
;; PASS 1: INDUCTION (shared subject)
!(map-atom (collapse (match &self (derived 0 (-> $m $p1) (stv $f1 $c1)) (match &self (derived 0 (-> $m $p2) (stv $f2 $c2)) (if (not (== $p1 $p2)) (let $tv (ind-tv $f1 $c1 $f2 $c2) (derived 1 (-> $p1 $p2) $tv)) nope)))) $x (if (== $x nope) (nop) (add-atom &self $x)))

;; === PASS 2: DEDUCTION on pass-1 + pass-0 ===
!(map-atom (unique-atom (collapse (match &self (derived 1 (-> $s $m) (stv $f1 $c1)) (match &self (derived 0 (-> $m $p) (stv $f2 $c2)) (if (not (== $s $p)) (let $tv (ded-tv $f1 $c1 $f2 $c2) (derived 2 (-> $s $p) $tv)) nope))))) $x (if (== $x nope) (nop) (add-atom &self $x)))
!(map-atom (unique-atom (collapse (match &self (derived 0 (-> $s $m) (stv $f1 $c1)) (match &self (derived 1 (-> $m $p) (stv $f2 $c2)) (if (not (== $s $p)) (let $tv (ded-tv $f1 $c1 $f2 $c2) (derived 2 (-> $s $p) $tv)) nope))))) $x (if (== $x nope) (nop) (add-atom &self $x)))

;; === QUERY: show all derived ===
!(match &self (derived $pass (-> $s $p) (stv $f $c)) (result $pass $s $p $f $c))