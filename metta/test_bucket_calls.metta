(= (pair $a $b) (pair $a $b))

(= (test-bucket-score-1) (bucket-score (Cons (pair formally_proven 0.9) (Cons (pair human_asserted 0.8) (Cons (pair tool_observed 0.7) Nil)))))
(= (test-bucket-score-2) (bucket-score (Cons (pair benchmark_seed 0.9) (Cons (pair model_generated 0.6) Nil))))
(= (test-verdict-1) (verdict-from-bucket-score (bucket-score (Cons (pair formally_proven 0.9) (Cons (pair human_asserted 0.8) (Cons (pair tool_observed 0.7) Nil)))) default))
(= (test-verdict-2) (verdict-from-bucket-score (bucket-score (Cons (pair benchmark_seed 0.3) (Cons (pair model_generated 0.2) Nil)))) adversarial))

!(test-bucket-score-1)
!(test-bucket-score-2)
!(test-verdict-1)
!(test-verdict-2)