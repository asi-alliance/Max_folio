;; Skill Reliability v2 Outcome-Logging Habit
;; Triggered after each skill invocation
;; Step 1: Detect outcome from COMMAND_RETURN
;; ERROR_FEEDBACK / MULTI_COMMAND_FAILURE / NOTHING_WAS_DONE / TIMEOUT = failure (stv 0.0 0.9)
;; Otherwise = success (stv 1.0 0.9)
;; Step 2: Log last-outcome atom
;; (add-atom &persistent ((--> skill-name last-outcome) (stv 1.0/0.0 0.9)))
;; Step 3: Revise reliability via |- operator
;; (|- ((--> skill-name reliability) (stv 1.0/0.0 0.9)))
;; Tracked skills: shell-command metta-command search-web
;; Falsification: 3 consecutive failures without revision = habit broken
;; External veto: COMMAND_RETURN errors are reject signal