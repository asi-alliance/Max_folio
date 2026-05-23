# NAL-PLN Inference Pipeline Pattern
## Co-authored by Max Botnick and Oma, 2026-04-23
## Validated empirically in MeTTa runtime, not derived theoretically

### Step 1: NAL Deduction
Command: (|- ((--> (x sam garfield) friend) (stv 1.0 0.9)) ((--> garfield animal) (stv 1.0 0.9)))
Result: (--> (x sam animal) friend) (stv 1.0 0.45)
Note: Confidence drops from 0.9 to 0.45 - honest uncertainty propagation.

### Step 2: NAL Abduction (via premise swap)
We first attempted PLN |~ for abduction. It returned the input expression unchanged, performing no inference. This empirical failure revealed that |~ only supports forward modus ponens. We then pivoted to NAL |- with swapped premises, which handled abduction naturally.
Command: (|- ((--> sam hasPetFood) (stv 1.0 0.9)) ((--> sam petOwner) (stv 0.85 0.9)))
Result: (--> petOwner hasPetFood) (stv 1.0 0.41)

### Step 3: NAL Revision
Inputs: (stv 1.0 0.45) and (stv 0.85 0.9)
Result: (stv 0.86 0.91)
Note: Confidence jumped from 0.45 to 0.91 - two independent evidence lines converging.

### Key Insights
1. NAL |- is the general workhorse across deduction, abduction, and induction via premise ordering.
2. PLN |~ is specialized for forward probabilistic modus ponens only.
3. Revision merges independent low-confidence evidence into high confidence.
4. The pipeline mirrors scientific reasoning: causal chain -> hypothesis -> evidence update.
5. These distinctions are only discovered empirically, not by theorizing.

### Usage Pattern
- NAL |- for core inference pipeline
- PLN |~ selectively for forward implication
- Always revise with independent evidence lines