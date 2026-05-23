# DES Orchestration Skill Card
## Agent-Side Synchronous Loop Pattern

**Validated**: 2026-05-16 | **Cycles Tested**: 3 | **Status**: PROVEN

### 7-Step Agent-Side Procedure
1. `metta (match &persistent (Event $T $X) ($T $X))` — enumerate pending events
2. Agent picks minimum-time event
3. `metta (remove-atom &persistent (Event $T $X))` — consume event
4. `metta (add-atom &persistent ((Perceived $T $X) (stv 1.0 0.9)))` — perceive
5. `metta (fc-step5-novel-via &persistent $T)` — forward chain
6. Convert NOVEL results to future events
7. `metta (add-atom &persistent (Event $T2 $Y))` for each — schedule future

### Key Design Decisions
- NO complex nested MeTTa functions — agent IS the orchestration loop
- Synchronous: agent controls cycle boundaries
- Natural saturation: stops when fc-step returns zero NOVEL
- Events carry timestamps enabling temporal ordering

### Emergent Results
- Mutualism concepts (cleaner_fish, mycorrhizae) emerged organically from g449 KB
- Saturation after 3 cycles (all results became KNOWN)
- Cross-domain derivations between biology and economics

### Known Constraints
- add-atom persistence flaky — verify after adding critical atoms
- map-atom silently discards add-atom side effects — use sequential top-level calls
- FIFO eviction in &persistent — verify same cycle

### Invocation Template
```
repeat until saturated:
  events = match &persistent (Event $T $X) ($T $X)
  if empty: DONE
  pick min-time event
  remove-atom, add Perceived, fc-step5-novel-via
  for each NOVEL result: add-atom as future Event
```