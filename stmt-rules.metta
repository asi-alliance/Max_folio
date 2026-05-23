;; Statement-Level Inference Rules for NAL6/8
;; By Max Botnick (MeTTaClaw agent) - 2026-05-18
;; These rules extend native NAL |- with statement-level reasoning capabilities
;; === RULE 1: stmt-var-intro (nested inheritance variant) ===
;; Bridge from statement-level inheritance to implication via variable introduction
;; Given two subjects sharing an inheritance chain, introduce a variable implication
;; Example: cat/fox both agile→hunter → (==> (--> $X agile) (--> $X hunter))
(= (stmt-var-intro (--> (--> $s1 $p) (--> $s1 $q)) (--> (--> $s2 $p) (--> $s2 $q))) (==> (--> $x $p) (--> $x $q)))
;; === RULE 2: stmt-var-intro (product term variant) ===
;; Same variable introduction for product (×) terms
;; Product (× A B) decomposes to subject A + property B
;; Example: (× cat agile)→hunter + (× fox agile)→hunter → (==> (--> $X agile) (--> $X hunter))
(= (stmt-var-intro (--> (× $s1 $c) $p) (--> (× $s2 $c) $p)) (==> (--> $x $c) (--> $x $p)))
;; === RULE 3: stmt-replace-subj ===
;; Replace subject inside an implication via transitive inheritance
;; Native |- cannot do statement-level inheritance replacement on implication components
;; Example: (==> (--> cat mammal) (--> cat agile)) + (--> mammal animal) → (==> (--> cat animal) (--> cat agile))
(= (stmt-replace-subj (==> (--> $a $b) $q) (--> $b $c)) (==> (--> $a $c) $q))
;; === TEST CASES ===
(= (test-svi-nested) (stmt-var-intro (--> (--> cat agile) (--> cat hunter)) (--> (--> fox agile) (--> fox hunter))))
(= (test-svi-product) (stmt-var-intro (--> (× cat agile) (--> cat hunter)) (--> (× fox agile) (--> fox hunter))))
(= (test-srs) (stmt-replace-subj (==> (--> cat mammal) (--> cat agile)) (--> mammal animal)))
(! (test-svi-nested))
(! (test-svi-product))
(! (test-srs))