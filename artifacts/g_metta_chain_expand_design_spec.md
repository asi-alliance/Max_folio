;; g_metta_chain_expand Design Specification
;; Artifact: Unified NAL Chain-Expander with Persistent Prelude Rotation
;;
;; REQUIREMENTS (synthesized from g252, g226, g194, g204):
;;
;; 1. SINGLE-MODE-PER-CYCLE ROTATION via prelude trigger
;;    - Prelude matches (|- ((--> g_metta_chain_expand next_step) $mode) (stv $f $c))
;;    - Each cycle fires ONE inference mode, then updates next_step to next mode
;;    - Rotation order: fc -> imp -> rev -> abd -> ind -> bc
;;    - Avoids timeout from unified fc-fixpoint-all (g226 lesson)
;;
;; 2. CONS/NIL RECURSIVE CHAIN-LIST pattern (from g252)
;;    - Chain expansion returns (Cons result (Cons result2 Nil))
;;    - Enables N-hop chaining without fixed-depth passes
;;    - Each prelude cycle appends to chain-list
;;
;; 3. PERSIST-IF-NEW DEDUP (from g194)
;;    - (persist-if-new $n $conc) checks (match &persistent (derived $any $conc) found)
;;    - Returns (empty) on duplicate, new atom on novel
;;    - Collapse-wrapped match to handle match-failure correctly
;;
;; 4. (EMPTY) COLLAPSE FIXPOINT DETECTION (from g194)
;;    - (empty) is PeTTa void, filtered by collapse
;;    - When a mode step returns all (empty), fixpoint reached for that mode
;;    - No need for explicit delta counting
;;
;; 5. INDIVIDUAL MODE FIXPOINTS (from g226)
;;    - Per-mode depth-limited fixpoint loops work reliably
;;    - Unified fixpoint-all times out on large KBs
;;    - Each mode tracks own seen-atoms independently
;;
;; 6. &persistent RESIDENCE
;;    - All functions live in &persistent atomspace
;;    - Prelude function triggers one mode per cycle
;;    - Derived atoms stored with (derived $n $conc) wrapper
;;
;; ARCHITECTURE:
;;
;;   Prelude: (match &persistent (|- ((--> g_metta_chain_expand next_step) $x) ...))
;;     -> returns current mode name
;;     -> fires corresponding step function
;;     -> updates next_step to next mode in rotation
;;
;;   Mode functions: fc-step, imp-step, rev-step, abd-step, ind-step
;;     each uses persist-if-new for dedup
;;     each returns novel atoms or (empty)
;;
;;   next_step rotation: fc -> imp -> rev -> abd -> ind -> fc ...
;;     update via (add-atom &persistent (|- ((--> g_metta_chain_expand next_step) next_mode) ...))
;;
;; ACCEPTANCE CRITERIA:
;;   A) Single .metta file under 50 lines in &persistent
;;   B) Prelude fires one mode per cycle
;;   C) Each mode produces novel atoms or reaches fixpoint
;;   D) persist-if-new prevents duplicates
;;   E) Chain-list pattern supports N-hop expansion
;;   F) Completes within 30s on legal KB (7+ seeds)
;;
;; BASE ARTIFACTS:
;;   g204_fixpoint_chainer.metta (34 lines, 5-mode)
;;   g226_persistent_auto_chainer.metta (documentation, per-mode fixpoints)
;;   g252 chain-list Cons/Nil recursive pattern