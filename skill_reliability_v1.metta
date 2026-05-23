; Skill Reliability Tracker v1 — NAL revision-based
; Each skill has a prior belief about reliability
; Outcome events are revised in to accumulate evidence

; --- Prior beliefs (initial stv = uninformed) ---
((--> shell-command reliable) (stv 0.8 0.5))
((--> write-file reliable) (stv 0.7 0.4))
((--> metta-inline reliable) (stv 0.5 0.4))
((--> petta-runner reliable) (stv 0.9 0.6))
((--> query-memory reliable) (stv 0.85 0.5))
((--> send-message reliable) (stv 0.9 0.5))
((--> search-web reliable) (stv 0.6 0.3))
((--> nal-revision reliable) (stv 0.95 0.7))

; --- Outcome event examples (to be revised against priors) ---
; Success: (stv 1.0 0.3), Failure: (stv 0.0 0.3)
; Revision merges evidence: |- prior outcome -> updated belief

; --- Ranking query: match all skill reliability atoms ---
!(match &self ((--> $skill reliable) (stv $f $c)) (Ranked $skill $f $c))