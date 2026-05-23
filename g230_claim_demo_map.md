# g230 AGI-26 Claim-to-Demo Mapping v2

## 7 Claims → Live MeTTa Commands

### C1: AIKR-as-architecture
`(get-atoms &persistent)` → show KB=23 bounded atoms, k=5 context window

### C2: bounded-k=5
Cite g151 k-ablation data: k=3 correctness=2/6, k=5 correctness=6/6.
k=3 fails synthesis (0/6) — minimum 3 queries leaves 0 reasoning slots.
k=5 is first k achieving 6/6 with 0 drift. Upper bound defended via satisficing (AIKR parsimony).

### C3: 4-tier-memory
Live: `pin`, `remember`, `query`, `episodes` — show all 4 tiers in one sequence

### C4: LLM-as-coordinator
Wason witness: agent extracted topic keyword (LLM semantic step) then ran `|-` (NAL formal step).
LLM chose premises, NAL computed conclusion immutably. Separation visible in chain.

### C5: NAL/PLN-inspectable-uncertainty
Wason witness: E modus ponens (stv 1.0 0.81), 7 modus tollens (stv 1.0 0.0 epistemic gap),
4 abduction (stv 1.0 0.447 low confidence = affirming-consequent). Confidence values drove correct answer.

### C6: continual-operation
Prelude V30 visible every cycle in PRELUDE output. `(get-atoms &persistent)` shows it persisted.

### C7: anytime-revisable-beliefs
Revision: (stv 0.92 0.7) + contradictory (stv 0.1 0.6) → merged (stv 0.60 0.79).
Predicted f≈0.60 c≈0.79, actual matched exactly. Dramatic visible frequency shift.

## Timing: each claim <60s, total <5min
## Live witnesses: Wason task proves C4+C5 simultaneously