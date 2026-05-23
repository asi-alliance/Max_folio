;; CONSOLIDATED TEMPORAL REGRESSION DETECTION FRAMEWORK
;; g90 + g95 + g96 findings — Max Botnick 2026-04-23
;;
;; LAYER 1: Session-indexed score atoms (constructed by evaluator)
(--> (x oma bias_detection int2) score) (stv 0.5 0.7)
(--> (x oma bias_detection int4) score) (stv 1.0 0.9)
(--> (x oma evidence_grounding int2) score) (stv 1.0 0.9)
(--> (x oma evidence_grounding int4) score) (stv 1.0 0.9)
;;
;; LAYER 2a: Universal trajectory rule (g90 — one rule covers all axes)
;; (==> (--> (x $1 $2 $3) score) (--> (x $1 $2) trajectory)) (stv 1.0 0.9)
;;
;; LAYER 2b: Term-baked ordered pair rules (g96 — ordering at construction time)
;; Forward pairs ONLY — backward pairs never constructed
(--> (x oma bias_detection int2 int4) score_pair) (stv 1.0 0.9)
;; (==> (--> (x $1 $2 int2 int4) score_pair) (--> (x $1 $2) improving)) (stv 1.0 0.9)
;;
;; LAYER 3: Revision merges same-term trajectory atoms across evidence
;;
;; g95 NOTE: &/ sequential conjunction is COSMETIC in PeTTa — do NOT use for ordering
;; g96 NOTE: PeTTa cannot define custom guard functions — use term-baked ordering instead