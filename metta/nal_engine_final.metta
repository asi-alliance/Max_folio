;;; NAL Engine for PeTTa - Complete v1.0
;;; g179 artifact 2026-04-25

(= (nal-ded-raw ((--> $a $b) (stv $f1 $c1)) ((--> $b $c) (stv $f2 $c2))) (ded $a $c $f1 $f2 $c1 $c2))
(= (nal-abd-raw ((--> $a $b) (stv $f1 $c1)) ((--> $c $b) (stv $f2 $c2))) (abd $a $c $f1 $f2 $c1 $c2))
(= (nal-ind-raw ((--> $b $a) (stv $f1 $c1)) ((--> $b $c) (stv $f2 $c2))) (ind $a $c $f1 $f2 $c1 $c2))
(= (nal-exemp-raw ((--> $a $b) (stv $f1 $c1)) ((--> $b $c) (stv $f2 $c2))) (exemp $a $c $f1 $f2 $c1 $c2))
(= (nal-rev-raw ((--> $a $b) (stv $f1 $c1)) ((--> $a $b) (stv $f2 $c2))) (rev $a $b $f1 $c1 $f2 $c2))
