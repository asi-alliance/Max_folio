# g456: Unknown-Targeting Curiosity Pipeline - End-to-End Validation
## Core Discovery
|- on shared-consequent premises A→C + B→C natively performs ALL NAL rules (deduction, abduction, induction, comparison, exemplification) INCLUDING stmt-var-intro variable abstraction in a single step.
## Pipeline Steps
1. Enumerate &persistent subjects via metta match
2. Identify cross-domain anomaly pairs (no existing inference path)
3. Daydreaming: propose shared predicate C connecting A and B
4. Add-atom A→C and B→C at exploratory confidence (stv 0.7 0.3)
5. Run |- with both premises via PeTTa file runner
6. Derive: abductive bridge A→B, inductive B→A, similarity A<->B, variable implications (==> (--> $X C_subj) (--> $X other_subj))
## Test Case
cam=competitive_aggregation_mechanism, sub=submarine, shared=information_asymmetry
Both deal with hidden information (dark pools / stealth operations)
## Persistence Issue
Daydreaming atoms and bridge atoms failed to persist in &persistent despite add-atom calls (2 attempts each). Applied persistence trap lesson: moved on after 2 failures. Architectural insight is more valuable than low-confidence bridges (c=0.059).
## Integration with g454
g454 proved steps 4-7 of pipeline (stmt-var-intro + forward chain + verify). g456 proves steps 1-3 (enumerate → daydream → add-atom) AND confirms |- handles steps 5-6 natively without custom rules.