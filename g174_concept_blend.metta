(= (compose-int ((--> $s $p1) (stv $f1 $c1)) ((--> $s $p2) (stv $f2 $c2))) ((--> $s (& $p1 $p2)) (stv (* $f1 $f2) (min $c1 $c2))))
(= (decompose-int ((--> $s (& $p1 $p2)) (stv $f $c))) ((--> $s $p1) (stv $f $c)))
(= (decompose-int2 ((--> $s (& $p1 $p2)) (stv $f $c))) ((--> $s $p2) (stv $f $c)))
(= (shared-prop ((--> $a $p) (stv $f1 $c1)) ((--> $b $p) (stv $f2 $c2))) ((<-> $a $b) (stv (* $f1 $f2) (min $c1 $c2))))
(= (transfer-prop ((<-> $a $b) (stv $fs $cs)) ((--> $a $p) (stv $fp $cp))) ((--> $b $p) (stv (* $fs $fp) (* $cs $cp))))

;; FULL BLEND PIPELINE: eagle (fast+flying) + cheetah (fast+agile)
;; Input profiles
!(decompose-int ((--> eagle (& fast flying)) (stv 0.9 0.9)))
!(decompose-int2 ((--> eagle (& fast flying)) (stv 0.9 0.9)))
!(decompose-int ((--> cheetah (& fast agile)) (stv 0.95 0.85)))
!(decompose-int2 ((--> cheetah (& fast agile)) (stv 0.95 0.85)))
;; Shared property: both fast
!(shared-prop ((--> eagle fast) (stv 0.9 0.9)) ((--> cheetah fast) (stv 0.95 0.85)))
;; Transfer novel: eagle flying -> cheetah flying
!(transfer-prop ((<-> eagle cheetah) (stv 0.855 0.85)) ((--> eagle flying) (stv 0.9 0.9)))
;; Transfer novel: cheetah agile -> eagle agile
!(transfer-prop ((<-> cheetah eagle) (stv 0.855 0.85)) ((--> cheetah agile) (stv 0.95 0.85)))
;; Recompose blended cheetah: (fast + agile + flying)
!(compose-int ((--> cheetah agile) (stv 0.95 0.85)) ((--> cheetah flying) (stv 0.77 0.765)))
