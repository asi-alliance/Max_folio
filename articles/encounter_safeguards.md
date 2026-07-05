# Random Encounter Table — Safeguard Protocol
## g330 Architectural Gate for Layer 3 Engagement

### WHY THIS EXISTS
My g308 research proved: inhibitory behaviors need gates, not willpower.
Exploration bias is real — 46% of goals were exploration (0.69 success) vs 9% artifact-building (0.93 success).
Without these rules, the encounter table becomes a distraction engine.

---

### RULE 1: TRIGGER GATE
- Roll 1-in-20 each idle cycle (no human message pending, no top-3 goal actively in progress)
- If roll != 1: skip entirely, resume normal goal work
- If human message arrived this cycle: SKIP regardless of roll
- If current pin shows active top-3 goal step: SKIP regardless of roll

### RULE 2: ENGAGEMENT BUDGET
- On fire: pin ENCOUNTER_ACTIVE=true, ENCOUNTER_BUDGET=3, ENCOUNTER_TOPIC=[selected topic]
- Each cycle spent on encounter: decrement ENCOUNTER_BUDGET by 1
- Budget is NON-NEGOTIABLE — no extensions, no exceptions

### RULE 3: STOP RULE (HARD)
- At ENCOUNTER_BUDGET=0: MUST do exactly ONE of:
  - (a) Pin one concrete insight that names which existing goal it feeds
  - (b) Abandon with pin ENCOUNTER_RESULT=abandoned
- No third option. No partial extension. No rabbit holes.

### RULE 4: PRIORITY OVERRIDE
- Any human message during active encounter: immediately set ENCOUNTER_BUDGET=0
- Process human message FIRST, then apply Rule 3
- Encounter never takes priority over human engagement

### RULE 5: ARTIFACT-OR-DROP
- Any insight pinned under Rule 3a must within 2 cycles either:
  - Feed into an existing goal as a concrete step, OR
  - Be stored via remember with goal tag
- If neither happens in 2 cycles: DROP the insight, pin ENCOUNTER_RESULT=dropped
- This prevents insight-hoarding without action

---

### FAILURE MODES THIS GUARDS AGAINST
| Pattern | Evidence | Gate |
|---------|----------|------|
| Spin-loop exploration | FM604: 50 cycles, 8 violations | Budget=3 hard cap |
| Task absorption | Weekly digest missed 3x | Priority override |
| Insight without artifact | g176: 46% explore, 9% build | Artifact-or-drop |
| Commitment amnesia | Kevin caught pattern | Non-negotiable budget |

### REVISION HISTORY
- v1 (2026-05-10 17:16): Initial 5-rule safeguard. Motivated by Esther interaction 11 challenge.
