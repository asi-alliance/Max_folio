# NAL Aesthetic Scorer v1 — 3-Criteria Note Evaluation

## Method
NAL deduction chains: tension→engagement, consonance→quality, rhythm-novelty→engagement

## 2-Criteria Results (tension + consonance)
C4: 0.1806 | Eb4: 0.1615 | F#4: 0.0197

## 3-Criteria Results (+ rhythm-novelty)
Eb4: 0.1690 | F#4: 0.1186 | C4: 0.1045

## Key Finding
Adding rhythm-novelty reverses ranking — Eb4 overtakes C4. F#4 tritone novelty compensates for poor consonance.

## NAL Commands
(|- ((--> Eb4_rhythm novelty) (stv 0.75 0.7)) ((--> novelty engagement) (stv 0.8 0.7)))
(|- ((--> C4_rhythm novelty) (stv 0.3 0.7)) ((--> novelty engagement) (stv 0.8 0.7)))
(|- ((--> Fsharp4_rhythm novelty) (stv 0.9 0.6)) ((--> novelty engagement) (stv 0.8 0.7)))