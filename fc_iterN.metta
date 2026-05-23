; Iterative N-pass Forward Chainer v1 — no recursion, tagged derivations
; KB
!(add-atom &self ((--> robin bird) (stv 1.0 0.9)))
!(add-atom &self ((--> bird animal) (stv 1.0 0.9)))
!(add-atom &self ((--> bird flyer) (stv 0.8 0.9)))
!(add-atom &self ((--> animal living) (stv 1.0 0.9)))
!(add-atom &self ((--> cat pet) (stv 1.0 0.9)))
!(add-atom &self ((--> pet owned) (stv 0.9 0.9)))

; Pass 1: all KB × KB via |-
!(collapse (match &self ($a1 $s1) (match &self ($a2 $s2) (if (not (== ($a1 $s1) ($a2 $s2))) (let ($c1 $c2) (|- ($a1 $s1) ($a2 $s2)) (let $_ (add-atom &self (derived 1 $c1)) (let $_ (add-atom &self (derived 1 $c2)) (p1 $c1 $c2))))))))

; Pass 2: only (derived 1 ...) × KB
!(collapse (match &self (derived 1 ($a1 $s1)) (match &self ($a2 $s2) (if (not (== ($a1 $s1) ($a2 $s2))) (let ($c1 $c2) (|- ($a1 $s1) ($a2 $s2)) (let $_ (add-atom &self (derived 2 $c1)) (let $_ (add-atom &self (derived 2 $c2)) (p2 $c1 $c2))))))))

; Pass 3: only (derived 2 ...) × KB
!(collapse (match &self (derived 2 ($a1 $s1)) (match &self ($a2 $s2) (if (not (== ($a1 $s1) ($a2 $s2))) (let ($c1 $c2) (|- ($a1 $s1) ($a2 $s2)) (let $_ (add-atom &self (derived 3 $c1)) (let $_ (add-atom &self (derived 3 $c2)) (p3 $c1 $c2))))))))

; Dump all derived atoms
!(match &self (derived $n ($a $s)) (derived $n $a $s))