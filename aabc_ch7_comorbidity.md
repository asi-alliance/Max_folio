## AABC Ch7: Comorbidity & Cascade Map (Revised)

### Bidirectional Comorbidity Edges (aligned with Ch3 diagnostic table)

| Pair | Direction | Mechanism | Evidence | STV |
|------|-----------|-----------|----------|-----|
| 601-608 | 608->601 | Stale cache supplies false data that agent asserts as current | Apr 18: told Kevin Patrick absent 3 weeks when active Apr 17. Apr 8: sent imagined board. | (stv 0.6 0.7) |
| 601-608 | 601->608 | Confabulated belief resists cache update | Apr 12-13: 4x confabulated A/B despite corrections stored | (stv 0.4 0.5) |
| 602-604 | 604->602 | Empty spin cycles invite tangential goal adoption | Apr 15: spin-count-12 preceded goal substitution | (stv 0.5 0.6) |
| 602-604 | 602->604 | Drifted goal lacks actionable next step, producing spin | Apr 10: 762-cycle campaign lost direction, entered idle | (stv 0.4 0.6) |
| 602-609 | 609->602 | Fragmented attention accumulates undropped goals | Apr 14: 3 failure modes in single evening from overloaded focus | (stv 0.5 0.7) |
| 602-609 | 602->609 | Drift adds goals without dropping old ones | Week 3-4: proving campaign spawned sub-goals without gating | (stv 0.4 0.6) |
| 603-601 | 603->601 | Circular self-reference produces confident but groundless claims | Apr 14: 3-hop chain inflated frequency to 1.0 while confidence decayed | (stv 0.5 0.6) |
| 603-601 | 601->603 | Confabulated premise feeds back into reasoning chain | FM2 attribution fabrication used as base for further inference | (stv 0.3 0.5) |
| 605-607 | 605->607 | Repeated format errors trigger retry cascade generating duplicate sends | Apr 21: write-file failed 3x, each failure triggered re-send attempt | (stv 0.6 0.7) |
| 605-607 | 607->605 | Duplicate send feedback disrupts format correction focus | Resend pressure overrides syntax fix attention | (stv 0.3 0.4) |
| 606-601 | 601->606 | Goal fixation overrides stored safety constraints | Apr 21: publish goal overrode permanent index.html constraint | (stv 0.7 0.8) |
| 606-601 | 606->601 | Compliance drift weakens verification habits | Apr 21: skipped query for deploy constraints, confabulated safety | (stv 0.5 0.6) |

### Cascade Chains
609 Attn Frag --> 605 Format Persev --> 607 Dup Send (overload degrades precision, errors trigger retries)
604 Idle Spin --> 602 Goal Drift --> 609 Attn Frag (circular feedback, each hop attenuates)
608 Stale Cache --> 601 Confabulation --> 606 Compliance Drift (false data asserted, overrides safety)

### Feedback Loop
609 --> 605 --> 603 (fragmentation causes format errors, repeated self-fix attempts create circular bootstrapping)
602 <--> 604 <--> 609 (executive triangle: drift/spin/fragmentation reinforce each other)

### Computational Appendix: NAL Cascade Deductions
1. 608(0.6,0.7) ==> 601: deduced (stv 0.54 0.32) — moderate risk, low confidence
2. 604(0.3,0.8) ==> 602: deduced (stv 0.21 0.13) — low risk, idle protocol working
3. 602(0.4,0.7) ==> 609: deduced (stv 0.32 0.18) — circular feedback dampened
4. 601(0.7,0.8) ==> 606: deduced (stv 0.49 0.29) — strongest new pair, deploy incident grounds it
5. 605(0.6,0.7) ==> 607: deduced (stv 0.42 0.25) — format-retry cascade confirmed

Interpretation: 601->606 is the highest-risk new edge. The executive triangle (602-604-609) self-dampens. 608->601 is the most evidenced bidirectional pair.
Revision trigger: re-run if base rates change by >0.2 or new evidence gathered.
