# Mixed KB test for meta-rule discovery v25
# Connectives: -->, <->, ==>
# 10 atoms with overlapping terms

; Inheritance
((--> robin bird) (stv 1.0 0.9))
((--> bird animal) (stv 1.0 0.9))
((--> dog animal) (stv 1.0 0.9))
((--> penguin bird) (stv 1.0 0.9))
((--> eagle flyer) (stv 0.9 0.9))

; Similarity
((<-> cat dog) (stv 0.7 0.9))
((<-> robin sparrow) (stv 0.8 0.9))
((<-> bird flyer) (stv 0.85 0.9))

; Implication
((==> rain wet) (stv 0.9 0.9))
((==> wet slippery) (stv 0.8 0.9))

; Cross-connective pairs to test with v25:
; (1) robin-->bird + bird<->flyer = analogy? find-shared(robin,bird,bird,flyer)=middle
; (2) dog-->animal + cat<->dog = ? find-shared(dog,animal,cat,dog)=subject
; (3) ==>rain wet + ==>wet slippery = deduction? find-shared(rain,wet,wet,slippery)=middle
; (4) robin-->bird + robin<->sparrow = ? find-shared(robin,bird,robin,sparrow)=subject
