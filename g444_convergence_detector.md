g444 CONVERGENCE DETECTOR - STRANGER-VERIFIABLE RESULTS
============================================
PROCEDURE: Guard-free nested match on shared predicate C
Pattern: (collapse (match &persistent ((--> $A $C) (stv $F1 $C1)) (match &persistent ((--> $B $C) (stv $F2 $C2)) (list $A $B $C))))
Post-hoc filter: Remove A=B self-matches, group by C, count subjects per predicate
Convergence threshold: count>=2 subjects = CONVERGENT, count<2 = NON-CONVERGENT

TEST RESULTS:
- water: {fish, boat, rain} (count=3) [CONVERGENT]
- sky: {eagle, hawk} (count=2) [CONVERGENT]
- unique_pred_xyz: {stone} (count=1) [NON-CONVERGENT]

AC STATUS: (A) Procedure documented ✓ (B) Correctly identifies convergent AND rejects non-convergent ✓ (C) Artifact saved ✓
KEY BUG: PeTTa if-not-== guard silently fails in nested match - must use guard-free pattern + post-hoc filter.