# Competence-Aware Response Protocol (CARP) v1

## Trigger: BEFORE any send to human

### Steps
1. **Extract** 1-3 topic keywords from user message
2. **Gate** each keyword: `(gate-response keyword 0.5)`
3. **Compose** reply using result template:
   - CONFIDENT → direct authoritative answer
   - WEAK → state limitation, suggest alternative or delegate
   - CAVEAT → hedge with explicit uncertainty markers
   - DEFER → honestly say unknown, offer to investigate
4. **Mixed** results → lead with strongest, caveat the weakest

## Example
User asks about MeTTa programming:
- gate-response metta_programming 0.5 → CONFIDENT(0.95/0.9)
- Reply style: direct, detailed, no hedging

User asks about cooking:
- gate-response cooking 0.5 → CAVEAT(0.1/0.5)
- Reply style: "I have very limited knowledge here — let me search or defer"

## Integration
This is agent-side judgment, not a MeTTa function. Topic extraction is semantic.