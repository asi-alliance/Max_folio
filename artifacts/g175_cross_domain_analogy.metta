;;== g175: Cross-Domain Compositional Analogy ====
;; Reuses g174 5-function toolkit on DOMAIN pairs

;; === TOOLKIT ===
(= (compose-int ((--> $s $p1) (stv $f1 $c1)) ((--> $s $p2) (stv $f2 $c2))) ((--> $s (& $p1 $p2)) (stv (* $f1 $f2) (min $c1 $c2))))
(= (decompose-int ((--> $s (& $p1 $p2)) (stv $f $c))) ((--> $s $p1) (stv $f $c)))
(= (decompose-int2 ((--> $s (& $p1 $p2)) (stv $f $c))) ((--> $s $p2) (stv $f $c)))
(= (shared-prop ((--> $a $p) (stv $f1 $c1)) ((--> $b $p) (stv $f2 $c2))) ((<-> $a $b) (stv (* $f1 $f2) (min $c1 $c2))))
(= (transfer-prop ((<-> $a $b) (stv $fs $cs)) ((--> $a $p) (stv $fp $cp))) ((--> $b $p) (stv (* $fs $fp) (* $cs $cp))))

;; === ROLE MAPPING ===
;; Structural role bridges between domains
(= (role-map ((--> $a $role) (stv $f1 $c1)) ((--> $b $role) (stv $f2 $c2))) ((role-bridge $a $b $role) (stv (* $f1 $f2) (min $c1 $c2))))

;; === ECOLOGY KB ===
!(decompose-int ((--> wolf (& hunts apex-predator)) (stv 0.95 0.9)))
!(decompose-int2 ((--> wolf (& hunts apex-predator)) (stv 0.95 0.9)))
!(decompose-int ((--> deer (& grazes prey-species)) (stv 0.9 0.85)))
!(decompose-int2 ((--> deer (& grazes prey-species)) (stv 0.9 0.85)))

;; === ECONOMICS KB ===
!(decompose-int ((--> corporation (& undercuts market-dominant)) (stv 0.85 0.8)))
!(decompose-int2 ((--> corporation (& undercuts market-dominant)) (stv 0.85 0.8)))
!(decompose-int ((--> small-firm (& competes vulnerable)) (stv 0.8 0.75)))
!(decompose-int2 ((--> small-firm (& competes vulnerable)) (stv 0.8 0.75)))

;; === SIT: Cross-Domain Structural Role Matching ===
;; Structural roles: apex-predator <=> market-dominant, prey-species <=> vulnerable
!(role-map ((--> wolf apex-predator) (stv 0.95 0.9)) ((--> corporation market-dominant) (stv 0.85 0.8)))
!(role-map ((--> deer prey-species) (stv 0.9 0.85)) ((--> small-firm vulnerable) (stv 0.8 0.75)))

;; === STEP2: Compute cross-domain similarity via shared structural roles
;; hunts and undercuts are NOT shared literally - we need role abstraction
;; Abstract roles: both are "dominates" actions
!(shared-prop ((--> wolf dominates) (stv 0.9 0.75)) ((--> corporation dominates) (stv 0.85 0.7)))

;; === STEP3: Transfer causal chains across domains
;; Ecology: keystone-removal → trophic-cascade
!(transfer-prop ((<-> wolf corporation) (stv 0.765 0.7)) ((--> keystone-removal trophic-cascade) (stv 0.85 0.8)))

;; === STEP4: Recompose cross-domain hypothesis
;; monopoly-removal → market-cascade (transferred from ecology)
!(compose-int ((--> monopoly-removal market-restructuring) (stv 0.7 0.65)) ((--> monopoly-removal market-cascade) (stv 0.65 0.56)))

;; === STEP5: Reverse transfer (economics → ecology)
;; Economics: market-consolidation → reduced-diversity
!(transfer-prop ((<-> corporation wolf) (stv 0.765 0.7)) ((--> market-consolidation reduced-diversity) (stv 0.8 0.75)))

;; === STEP 6: Novel hypothesis - ecological monoculture risk
!(compose-int ((--> ecosystem-consolidation reduced-resilience) (stv 0.75 0.7)) ((--> ecosystem-consolidation cascade-vulnerability) (stv 0.6 0.55)))
