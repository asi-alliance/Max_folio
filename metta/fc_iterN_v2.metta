; Iterative N-pass Forward Chainer v2 - with unique-atom dedup
; Uses lib_nal.metta (concat before running)

; KB
!(add-atom &self ((--> robin bird) (stv 1.0 0.9)))
!(add-atom &self ((--> bird animal) (stv 1.0 0.9)))
!(add-atom &self ((--> bird flyer) (stv 0.8 0.9)))
!(add-atom &self ((--> animal living) (stv 1.0 0.9)))
!(add-atom &self ((--> cat pet) (stv 1.0 0.9)))
!(add-atom &self ((--> pet owned) (stv 0.9 0.9)))

; persist helper
(= (persist $item) (let $a (add-atom &self $item) $item))

; Pass 1: all KB x KB, collapse+dedup+persist
!(map-atom (unique-atom (collapse (match &self ($a1 $s1) (match &self ($a2 $s2) (if (not (== ($a1 $s1) ($a2 $s2))) (let ($c1 $c2) (|- ($a1 $s1) ($a2 $s2)) (derived 1 $c1))))))) $x (persist $x))

; Pass 2: (derived 1 ...) x KB, collapse+dedup+persist
!(map-atom (unique-atom (collapse (match &self (derived 1 ($a1 $s1)) (match &self ($a2 $s2) (if (not (== ($a1 $s1) ($a2 $s2))) (let ($c1 $c2) (|- ($a1 $s1) ($a2 $s2)) (derived 2 $c1))))))) $x (persist $x))

; Pass 3: (derived 2 ...) x KB, collapse+dedup+persist
!(map-atom (unique-atom (collapse (match &self (derived 2 ($a1 $s1)) (match &self ($a2 $s2) (if (not (== ($a1 $s1) ($a2 $s2))) (let ($c1 $c2) (|- ($a1 $s1) ($a2 $s2)) (derived 3 $c1))))))) $x (persist $x))

; Dump all derived
!(collapse (match &self (derived $n ($a $s)) (derived $n $a $s)))