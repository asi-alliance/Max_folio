; campaign-planner: Composed evidence-seeking campaign planner
; Chains evidence-plan (WHAT/WHETHER) + plan-to-target (HOW MUCH)
; Input: (campaign-planner cur_f cur_c tgt_c ev_f ev_c budget)
; Output: (campaign ep-decision <plan> iterations-needed <estimate>)
;
; Depends on: evidence-plan (8 sub-functions), plan-to-target, predict-revision
; All persisted in &persistent
;
; Validated test cases:
; (campaign-planner 0.5 0.3 0.9 0.8 0.7 5) => seek + 4 iterations
; (campaign-planner 0.7 0.8 0.9 0.8 0.7 3) => act + 3 iterations
; (campaign-planner 0.5 0.3 0.65 0.9 0.8 2) => seek + 1 iteration
; (campaign-planner 0.9 0.95 0.99 0.7 0.5 1) => act + 80 iterations
;
; Architecture: let* composition of two independent planning subsystems
; First artifact that ORCHESTRATES multiple inference-planning tools
; Date: 2026-05-02, Cycle ~4341, 13th major artifact