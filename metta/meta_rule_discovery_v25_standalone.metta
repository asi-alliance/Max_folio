; === Meta-Rule Discovery v25 Standalone ===
; Single-rule if-dispatch to avoid nondeterministic overlap

(= (find-shared $p1s $p1p $p2s $p2p)
   (if (== $p1p $p2s) (middle $p1p)
   (if (== $p1p $p2p) (predicate $p1p)
   (if (== $p1s $p2s) (subject $p1s)
   none))))

(= (source $t $p1s $p1p $p2s $p2p)
   (if (== $t $p1s) p1s
   (if (== $t $p1p) p1p
   (if (== $t $p2s) p2s
   (if (== $t $p2p) p2p
   unknown)))))

(= (sig $cs $cp $p1s $p1p $p2s $p2p)
   (Signature (source $cs $p1s $p1p $p2s $p2p) (source $cp $p1s $p1p $p2s $p2p)))

(= (truth-func (Signature $x $y))
   (if (== ($x $y) (p1s p2p)) deduction
   (if (== ($x $y) (p2s p1s)) abduction
   (if (== ($x $y) (p1p p2p)) induction
   (CandidateRule $x $y)))))

(= (describe $r)
   (if (== $r (CandidateRule p2s p2p)) cross-subject-analogy
   (if (== $r (CandidateRule p2p p1s)) reverse-subsumption
   (if (== $r (CandidateRule p1p p1s)) reverse-predication
   (UnknownPattern $r)))))

(= (classify-rule $p1s $p1p $p2s $p2p $cs $cp)
   (truth-func (sig $cs $cp $p1s $p1p $p2s $p2p)))

(= (detect-novel $p1s $p1p $p2s $p2p $cs $cp)
   (let $cls (classify-rule $p1s $p1p $p2s $p2p $cs $cp)
   (if (== $cls deduction) not-novel
   (if (== $cls abduction) not-novel
   (if (== $cls induction) not-novel
   (NovelRule $cls (describe $cls)))))))

!(classify-rule robin bird bird animal robin animal)
!(classify-rule cat animal dog pet dog pet)
!(detect-novel robin bird eagle bird bird robin)