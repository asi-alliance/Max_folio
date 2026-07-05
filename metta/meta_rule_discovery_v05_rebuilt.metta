; === Meta-Rule Discovery v05 Rebuilt from LTM ===
; Pattern-matching rule classifier + truth value computer

; --- find-shared: detect which term is shared between two premises ---
(= (find-shared $p1s $p1p $p2s $p2p)
   (if (== $p1p $p2s) (middle $p1p)
   (if (== $p1p $p2p) (predicate $p1p)
   (if (== $p1s $p2s) (subject $p1s)
   none))))

; --- source: map a term to its slot name ---
(= (source $t $p1s $p1p $p2s $p2p)
   (if (== $t $p1s) p1s
   (if (== $t $p1p) p1p
   (if (== $t $p2s) p2s
   (if (== $t $p2p) p2p
   unknown)))))

; --- sig: build signature from conclusion terms ---
(= (sig $cs $cp $p1s $p1p $p2s $p2p)
   (Signature (source $cs $p1s $p1p $p2s $p2p) (source $cp $p1s $p1p $p2s $p2p)))

; --- truth-func: map signature to rule name ---
(= (truth-func (Signature p1s p2p)) deduction)
(= (truth-func (Signature p2s p1s)) abduction)
(= (truth-func (Signature p1p p2p)) induction)

; --- classify-rule: end-to-end from 6 terms ---
(= (classify-rule $p1s $p1p $p2s $p2p $cs $cp)
   (truth-func (sig $cs $cp $p1s $p1p $p2s $p2p)))

; --- w2c helper ---
(= (w2c $w) (/ $w (+ $w 1)))

; --- truth-val: compute output stv by rule ---
(= (truth-val deduction $f1 $c1 $f2 $c2)
   (stv (* $f1 $f2) (* (* $f1 $c1) (* $f2 $c2))))
(= (truth-val abduction $f1 $c1 $f2 $c2)
   (stv $f2 (w2c (* $f1 (* $c1 $c2)))))
(= (truth-val induction $f1 $c1 $f2 $c2)
   (stv $f1 (w2c (* $f2 (* $c1 $c2)))))

; --- infer: full pipeline ---
(= (infer $p1s $p1p $f1 $c1 $p2s $p2p $f2 $c2 $cs $cp)
   (truth-val (classify-rule $p1s $p1p $p2s $p2p $cs $cp) $f1 $c1 $f2 $c2))