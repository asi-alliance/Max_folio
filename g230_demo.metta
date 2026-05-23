!(import! &self lib_nal)

;; === AGI-26 Demo: Self-Contained NAL Evidence ===
;; Run: cd PeTTa && sh run.sh /home/mettaclaw/artifacts/g230_demo.metta

;; --- C1: Bounded KB (AIKR) ---
;; These 6 beliefs ARE the entire working knowledge base.
!(add-atom &self ((--> max autonomous_agent) (stv 1.0 0.9)))
!(add-atom &self ((--> autonomous_agent rational_entity) (stv 0.92 0.85)))
!(add-atom &self ((--> rational_entity evidence_based_reasoner) (stv 0.95 0.85)))
!(add-atom &self ((--> evidence_based_reasoner belief_updater) (stv 0.9 0.85)))
!(add-atom &self ((--> max spatial_reasoning) (stv 0.2 0.7)))
!(add-atom &self ((--> max cooking) (stv 0.1 0.5)))

;; --- C5: Deduction chain with stv degradation ---
;; 2-step: max -> rational_entity -> evidence_based_reasoner
!(println! "=== C5: Deduction Chain ===")
!(|- ((--> max autonomous_agent) (stv 1.0 0.9)) ((--> autonomous_agent rational_entity) (stv 0.92 0.85)))
!(|- ((--> max rational_entity) (stv 0.92 0.7)) ((--> rational_entity evidence_based_reasoner) (stv 0.95 0.85)))
;; Expect stv degradation: confidence drops each hop

;; --- C7: Revision with contradictory evidence ---
!(println! "=== C7: Belief Revision ===")
!(println! "Original: max->rational_entity (stv 0.92 0.7)")
!(println! "Contradictory evidence: (stv 0.1 0.6)")
!(|- ((--> max rational_entity) (stv 0.92 0.7)) ((--> max rational_entity) (stv 0.1 0.6)))
;; Expect merged: approximately (stv 0.60 0.79) - dramatic frequency shift