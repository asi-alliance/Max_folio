!(bind! &kb (new-space))

(= (predict-revision $f1 $c1 $f2 $c2)
  (let* (
    ($w1 (/ $c1 (- 1.0 $c1)))
    ($w2 (/ $c2 (- 1.0 $c2)))
    ($wsum (+ $w1 $w2))
    ($f_new (/ (+ (* $f1 $w1) (* $f2 $w2)) $wsum))
    ($c_new (/ $wsum (+ $wsum 1.0)))
  ) (predicted (stv $f_new $c_new))))

; Test case 1: spatial revision pair 1
!(predict-revision 0.3 0.7 0.6 0.85)
; Expected: ~(stv 0.5125 0.889)

; Test case 2: spatial revision pair 2
!(predict-revision 0.5125 0.889 0.75 0.85)
; Expected: ~(stv 0.611 0.932)