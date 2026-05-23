; plan-to-target: Meta-cognitive planning-over-inference
; Given current belief (f,c), target confidence, and evidence quality,
; computes how many independent evidence items are needed.
; Depends on: predict-revision (persisted in &persistent)
;
; Usage: (plan-to-target f_cur c_cur f_target c_target f_ev c_ev 0)
; Returns: (reached count (stv f_final c_final))
;
; Validated test cases:
; (plan-to-target 0.5 0.5 0.5 0.9 0.8 0.7 0) => (reached 4 (stv 0.771 0.912))
; (plan-to-target 0.3 0.3 0.3 0.95 0.9 0.8 0) => (reached 5 (stv 0.887 0.953))
; (plan-to-target 0.7123 0.828 0.7123 0.9 0.8 0.7 0) => (reached 2 (stv 0.755 0.905))
;
; Architecture: recursive application of predict-revision until c >= c_target
; Persisted via: (add-atom &persistent (= (plan-to-target ...) ...))
; Date: 2026-05-02, Cycle ~4295