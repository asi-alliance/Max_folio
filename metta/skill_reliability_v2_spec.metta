;; Skill Reliability v2: Automated Feedback Loop - runtime invocation tracking via NAL belief revision;; Scope: runtime invocation tracking via NAL belief revision, NOT more testing
;; v1 proven: shell-command 0.8 to 0.86 on success, search-web 0.6 to 0.3 on failure
;; Drift warning: do NOT extend with more test suites (Patrick chain5 pattern)
(= (skill-reliability-v2) (chain (record-invocation $skill $outcome $ts) (revise-belief $skill $outcome) (check-threshold $skill)))
(= (record-invocation $skill $outcome $ts) (metta (add-atom &persistent (|- ((--> ($skill reliable) (stv (if (== $outcome success) 1.0 0.0) 0.9)))))))
(= (check-threshold $skill) (let ((stv (get-current-stv $skill))) (cond ((> (confidence stv) 0.8) (promote-to-verified $skill)) ((< (confidence stv) 0.3) (flag-for-review $skill)) (else (continue-monitoring $skill)))))
