;; Unified FC+BC Engine v4 — multi-pass iterative FC + backward chainer + revision
;; Max Botnick 2026-04-30

(= (w2c $w) (/ $w (+ $w 1)))
(= (c2w $c) (/ $c (- 1 $c)))
(= (ded-tv ($f1 $c1) ($f2 $c2)) (stv (* $f1 $f2) (* (* $f1 $f2) (* $c1 $c2))))
(= (abd-tv ($f1 $c1) ($f2 $c2)) (stv $f2 (w2c (* (* $f1 $c1) $c2))))
(= (ind-tv ($f1 $c1) ($f2 $c2)) (abd-tv ($f2 $c2) ($f1 $c1)))
; NAL-5 conditional deduction (modus ponens)
(= (imp-ded-tv ($f1 $c1) ($f2 $c2)) (stv (* $f1 $f2) (* (* $f1 $c1) (* $f2 $c2))))
(= (rev-tv (stv $f1 $c1) (stv $f2 $c2)) (let* (($w1 (c2w $c1)) ($w2 (c2w $c2)) ($ws (+ $w1 $w2))) (stv (/ (+ (* $w1 $f1) (* $w2 $f2)) $ws) (w2c $ws))))
(= (persist $x) (let $a (add-atom &self $x) $x))

;; KB
!(add-atom &self ((--> robin bird) (stv 0.9 0.9)))
!(add-atom &self ((--> bird animal) (stv 0.95 0.9)))
!(add-atom &self ((--> animal living) (stv 0.95 0.9)))
!(add-atom &self ((--> robin fly) (stv 0.85 0.9)))
!(add-atom &self ((--> bird fly) (stv 0.9 0.9)))
!(add-atom &self ((--> eagle bird) (stv 0.95 0.9)))
!(add-atom &self ((--> penguin bird) (stv 0.8 0.9)))
!(add-atom &self ((--> penguin swimmer) (stv 0.95 0.9)))
!(add-atom &self ((--> shark fish) (stv 0.9 0.9)))
!(add-atom &self ((--> fish animal) (stv 0.95 0.9)))
!(add-atom &self ((--> whale mammal) (stv 0.95 0.9)))
!(add-atom &self ((--> mammal animal) (stv 0.95 0.9)))
!(add-atom &self ((--> dolphin mammal) (stv 0.9 0.9)))
!(add-atom &self ((--> swimmer aquatic) (stv 0.9 0.9)))
!(add-atom &self ((--> aquatic living) (stv 0.9 0.9)))
; NAL-5 test implications
!(add-atom &self ((==> bird flyer) (stv 0.9 0.9)))
!(add-atom &self ((==> flyer mobile) (stv 0.85 0.9)))
!(add-atom &self (bird (stv 1.0 0.9)))

;; === FC Pass 1: KB x KB ===
!(map-atom (unique-atom (collapse (match &self ((--> $A $B) (stv $f1 $c1)) (match &self ((--> $B $C) (stv $f2 $c2)) (if (not (== $A $C)) (let $tv (ded-tv ($f1 $c1) ($f2 $c2)) (fc-ded 1 ((--> $A $C) $tv))) nope))))) $x (persist $x))
!(map-atom (collapse (match &self ((--> $A $B) (stv $f1 $c1)) (match &self ((--> $C $B) (stv $f2 $c2)) (if (not (== $A $C)) (let $tv (abd-tv ($f1 $c1) ($f2 $c2)) (fc-abd 1 ((--> $C $A) $tv))) nope)))) $x (if (== $x nope) (nop) (persist $x)))
!(map-atom (collapse (match &self ((--> $A $B) (stv $f1 $c1)) (match &self ((--> $A $C) (stv $f2 $c2)) (if (not (== $B $C)) (let $tv (ind-tv ($f1 $c1) ($f2 $c2)) (fc-ind 1 ((--> $C $B) $tv))) nope)))) $x (if (== $x nope) (nop) (persist $x)))

;; === FC Pass 2: Pass1-derived x KB ===
!(map-atom (unique-atom (collapse (match &self (fc-ded 1 ((--> $A $B) (stv $f1 $c1))) (match &self ((--> $B $C) (stv $f2 $c2)) (if (not (== $A $C)) (let $tv (ded-tv ($f1 $c1) ($f2 $c2)) (fc-ded 2 ((--> $A $C) $tv))) nope))))) $x (if (== $x nope) (nop) (persist $x)))
!(map-atom (unique-atom (collapse (match &self (fc-abd 1 ((--> $A $B) (stv $f1 $c1))) (match &self ((--> $C $B) (stv $f2 $c2)) (if (not (== $A $C)) (let $tv (abd-tv ($f1 $c1) ($f2 $c2)) (fc-abd 2 ((--> $C $A) $tv))) nope))))) $x (if (== $x nope) (nop) (persist $x)))
!(map-atom (unique-atom (collapse (match &self (fc-ind 1 ((--> $A $B) (stv $f1 $c1))) (match &self ((--> $A $C) (stv $f2 $c2)) (if (not (== $B $C)) (let $tv (ind-tv ($f1 $c1) ($f2 $c2)) (fc-ind 2 ((--> $C $B) $tv))) nope))))) $x (if (== $x nope) (nop) (persist $x)))

; NAL-5 modus ponens FC pass
!(map-atom (unique-atom (collapse (match &self ((==> $A $B) (stv $f1 $c1)) (match &self ($A (stv $f2 $c2)) (let $tv (imp-ded-tv ($f1 $c1) ($f2 $c2)) (fc-imp 1 ($B $tv))))))) $x (persist $x))
;; === FC Pass 3: Pass2-derived x KB ===
!(map-atom (unique-atom (collapse (match &self (fc-ded 2 ((--> $A $B) (stv $f1 $c1))) (match &self ((--> $B $C) (stv $f2 $c2)) (if (not (== $A $C)) (let $tv (ded-tv ($f1 $c1) ($f2 $c2)) (fc-ded 3 ((--> $A $C) $tv))) nope))))) $x (if (== $x nope) (nop) (persist $x)))

;; BC: searches KB + all derived atoms
(= (bc (stv $f $c) (--> $a $b)) (match &self ((--> $a $b) (stv $f $c)) (stv $f $c)))
(= (bc (stv $f $c) (--> $a $b)) (match &self (fc-ded $n ((--> $a $b) (stv $f $c))) (stv $f $c)))
(= (bc (stv $f $c) (--> $a $b)) (match &self (fc-abd $n ((--> $a $b) (stv $f $c))) (stv $f $c)))
(= (bc (stv $f $c) (--> $a $b)) (match &self (fc-ind $n ((--> $a $b) (stv $f $c))) (stv $f $c)))
(= (bc (stv $f $c) (--> $a $c2)) (match &self ((--> $a $m) (stv $f1 $c1)) (let (stv $f2 $cv2) (bc (stv $f2 $cv2) (--> $m $c2)) (ded-tv ($f1 $c1) ($f2 $cv2)))))

;; BC query with revision
!(println! === v4 multi-pass FC+BC+revision ===)
!(let $results (collapse (bc $tv (--> robin living))) (let* (($first (car-atom $results)) ($rest (cdr-atom $results)) ($second (car-atom $rest))) (rev-tv $first $second)))