; === Meta-Rule Discovery v25: Unknown Pattern Detector ===
; Extends v05 classify-rule with catch-all for novel signatures
; Loads AFTER v05_rebuilt.metta

; --- catch-all: any signature not matching ded/abd/ind ---
(= (truth-func (Signature $x $y))
   (if (== ($x $y) (p1s p2p)) deduction
   (if (== ($x $y) (p2s p1s)) abduction
   (if (== ($x $y) (p1p p2p)) induction
   (CandidateRule $x $y)))))

; --- describe: human-readable explanation of novel pattern ---
(= (describe (CandidateRule p2s p2p)) cross-subject-analogy)
(= (describe (CandidateRule p2p p1s)) reverse-subsumption)
(= (describe (CandidateRule p1p p1s)) reverse-predication)
(= (describe (CandidateRule $x $y)) (UnknownPattern $x $y))

; --- detect-novel: given 6 terms, return CandidateRule if novel ---
(= (detect-novel $p1s $p1p $p2s $p2p $cs $cp)
   (let $sig (sig $cs $cp $p1s $p1p $p2s $p2p)
   (let $cls (truth-func $sig)
   (if (== $cls deduction) not-novel
   (if (== $cls abduction) not-novel
   (if (== $cls induction) not-novel
   (NovelRule $cls (describe $cls))))))))

; --- TEST: cross-subject-analogy A->B + C->D => C->D (sig p2s p2p) ---
; Premises: cat->animal, dog->pet. Conclusion: dog->pet
; find-shared returns none (no shared term!)
; sig maps cs=dog->p2s, cp=pet->p2p = (Signature p2s p2p)
; This is NOT ded/abd/ind => CandidateRule!

; --- TEST: reverse-predication A->B + C->B => B->A (sig p1p p1s) ---
; Premises: robin->bird, eagle->bird. Conclusion: bird->robin
; sig maps cs=bird->p1p, cp=robin->p1s = (Signature p1p p1s)
; Novel! reverse-predication detected