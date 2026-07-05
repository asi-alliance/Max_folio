; === g159 Trust Decay NAL Atoms v3 ===
; REQUIRES: cat lib_nal.metta + this file > combined.metta

; --- C1: 7 Source Trust Atoms (g69) ---
!(add-atom &self ((--> (source alice) reliable) (stv 0.855 0.654)))
!(add-atom &self ((--> (source bob) unreliable) (stv 0.72 0.454)))
!(add-atom &self ((--> (source carol) reliable) (stv 0.81 0.365)))
!(add-atom &self ((--> (source dave) reliable) (stv 0.81 0.365)))
!(add-atom &self ((--> (source eve) reliable) (stv 0.765 0.365)))
!(add-atom &self ((--> (source jon) reliable) (stv 0.747 0.365)))
!(add-atom &self ((--> (source kevin) reliable) (stv 0.702 0.365)))

; --- C2: 5 Temporal Decay Buckets (g101) ---
!(add-atom &self ((==> (--> alice_belief stale_1d) (--> alice_belief discounted_1d)) (stv 0.96 0.9)))
!(add-atom &self ((==> (--> alice_belief stale_3d) (--> alice_belief discounted_3d)) (stv 0.885 0.9)))
!(add-atom &self ((==> (--> alice_belief stale_7d) (--> alice_belief discounted_7d)) (stv 0.751 0.9)))
!(add-atom &self ((==> (--> alice_belief stale_14d) (--> alice_belief discounted_14d)) (stv 0.565 0.9)))
!(add-atom &self ((==> (--> alice_belief stale_30d) (--> alice_belief discounted_30d)) (stv 0.294 0.9)))

; --- C3: Adversarial Gate (g154) ---
!(add-atom &self ((==> (--> claim_X boost_above_0.15) (--> claim_X unsafe_horizon)) (stv 1.0 0.929)))
!(add-atom &self ((==> (--> claim_X boost_above_0.20) (--> claim_X catastrophic_horizon)) (stv 1.0 0.81)))

; --- TEST 1: Decay Modus Ponens ---
!(|- ((==> (--> alice_belief stale_7d) (--> alice_belief discounted_7d)) (stv 0.751 0.9)) ((--> alice_belief stale_7d) (stv 0.9 0.9)))

; --- TEST 2: Adversarial Chain ---
!(|- ((==> (--> claim_X boost_above_0.15) (--> claim_X unsafe_horizon)) (stv 1.0 0.929)) ((--> claim_X boost_above_0.15) (stv 0.9 0.9)))

; --- TEST 3: Revision of two sources ---
!(|- ((--> (source alice) reliable) (stv 0.855 0.654)) ((--> (source alice) reliable) (stv 0.81 0.365)))