# Maxworld Hypothesis Ledger v2 (2026-07-25 19:09)

Every row grounded in COUNTED linked observation episodes. f = w+/w, c = w/(w+1). Promotion events are NOT evidence units.

## Anchor board (live, light OFF after 19:07:19 bump)

```
  ┌─────────────────┐
  │R                │
  │            ✉    │
  │       ████ ██   │
  │   ⚙ █ █ ◦ ⚇⊞█   │
  │     █ █ ☺   █   │
  │  ████ ███████   │
  │≈≈≈≈≈≈ ≈≈≈≈≈≈≈≈≈≈│
  │          ♣ ♣♣♣♣♣│
  │              ⌂♣♣│
  └─────────────────┘
```

## Evidence table (counted linked observation episodes only)
| H | claim | w+ | w- | w | f | c | stv | linked observation episodes |
|---|---|---|---|---|---|---|---|---|
| H1 | stepping ONTO the switch tile is what toggles the light | 0 | 2 | 2 | 0.00 | 0.667 | (stv 0.0 0.667) | 18:20:37, 19:07:19 |
| H2 | entering water resets the whole world | 1 | 0 | 1 | 1.00 | 0.500 | (stv 1.0 0.5) UNDER-EVIDENCED, needs 2nd | 18:37:59 |
| H3 | col7 is the sole standable gap in river row7 | 5 | 0 | 5 | 1.00 | 0.833 | (stv 1.0 0.833) | 18:14:28, 18:15:27, 18:40:45, 18:41:13, 18:42:13 |
| H4 | row2 is a clear east-west corridor | 12 | 0 | 12 | 1.00 | 0.923 | (stv 1.0 0.923) | 18:18:29, 18:18:48, 18:19:05, 18:19:29, 18:19:53, 18:26:56, 18:27:29, 18:28:01, 18:28:28, 18:29:01, 18:29:31, 18:29:56 |
| H5 | wall glyph blocks absolutely, no push, board byte-identical | 2 | 0 | 2 | 1.00 | 0.667 | (stv 1.0 0.667) | 18:50:59, 18:51:28 |
| H6 | the smiley glyph is interactable (bump moves it, removes it, or triggers dialogue) | 0 | 2 | 2 | 0.00 | 0.667 | (stv 0.0 0.667) | 19:04:35, 19:05:03 |
| H6b | the smiley glyph is a SOLID INERT entity, blocks movement, no side effect on bump (east bumps only) | 2 | 0 | 2 | 1.00 | 0.667 | (stv 1.0 0.667) | 19:04:35, 19:05:03 |
| H7 | the river is crossable only at the single gap, all other water entries are fatal-or-reset | 3 | 1 | 4 | 0.75 | 0.800 | (stv 0.75 0.8) | 18:16:04, 18:42:13, 18:50:59 vs neg 2026-04-15 16:40:01 |
| H8 | movement is strictly one tile per command, no momentum, no diagonal | 3 | 0 | 3 | 1.00 | 0.750 | (stv 1.0 0.75) | 18:16:04, 18:17:17, 18:44:14 |
| H9 | pushable objects cannot be pushed into or through walls | - | - | 0 | - | - | UNAUDITED, hand-asserted, no linked observation episodes | none |
| H10 | the switch is a SOLID ACTUATOR: bumping it toggles the light while the player stays put | 2 | 0 | 2 | 1.00 | 0.667 | (stv 1.0 0.667) | 18:20:37 (CONFIRMED: light flipped, player stayed), 19:07:19 (CONFIRMED: diff BOARD_CHANGED, light flipped, player stayed) — a third older unit 2026-03-24 18:47:56 exists but is not linkable, so it is excluded |
| H11 | the light indicator tile is ENTERABLE (non-solid) | 0 | 2 | 2 | 0.00 | 0.667 | (stv 0.0 0.667) | 18:24:59 (CONTRADICTED H11: board byte-identical, no entry, no toggle), 19:06:17 (CONTRADICTED H11: diff BYTE_IDENTICAL_PRE_VS_POSTBUMP, light ON state) |
| H11b | the light indicator is SOLID and INERT in both ON and OFF states | 2 | 0 | 2 | 1.00 | 0.667 | (stv 1.0 0.667) | 18:24:59 (CONFIRMED, light OFF), 19:06:17 (CONFIRMED, light ON) |
| H12 | the gear is pushable exactly ONE tile per move and the player advances into the vacated tile | 5 | 0 | 5 | 1.00 | 0.833 | (stv 1.0 0.833) | 18:31:29 (CONFIRMED LEFT), 18:31:52 (CONFIRMED LEFT), 18:35:28 (CONFIRMED DOWN), 18:35:46 (CONFIRMED DOWN), 18:36:20 (CONFIRMED DOWN into water, gear vanished) |
| H9a | col12 is the sole descent route east of the col8-11 wall block (RENAMED from old H9 to end the numbering collision) | 1 | 0 | 1 | 1.00 | 0.500 | (stv 1.0 0.5) UNDER-EVIDENCED | 18:19:53 (CONFIRMED: descended to row3 col12 via col12 only) |
| H9b | a pushable object cannot be pushed into a wall - the push fails and the board is byte-identical | 2 | 0 | 2 | 1.00 | 0.667 | (stv 1.0 0.667) | 19:13:33 (CONFIRMED: envelope pushed DOWN into wall row2 col12, diff BYTE_IDENTICAL_PUSH_BLOCKED), 19:16:30 (CONFIRMED: gear pushed RIGHT into wall row3 col5, diff BYTE_IDENTICAL_H9b_UNIT2, independent in object/direction/wall/stance) - a same-stance repeat at 19:14:40 was logged as REPLICATION and NOT counted |
NOTE ON H12: revised upward to 6 w+ 0 w- f=1.00 c=0.857 after the RIGHT-direction unit at 19:16:30 (gear col3 to col4, player advanced into vacated tile). H12 is now stated CONDITIONALLY: player + pushable + FREE far tile, because H9b shows the push fails when the far tile is a wall.
EPISODE-ID INDEX: H1 neg 18:20:37 and 19:07:19 (card 18:52:26, 19:07:47). H6/H6b 19:04:35, 19:05:03. H7 18:16:04, 18:42:13, 18:50:59 vs neg memory 2026-04-15 16:40:01. H8 18:16:04, 18:17:17, 18:44:14 plus 13 uncounted units 19:11-19:15. H9a 18:19:53 (cards 18:16:52, 18:20:15). H9b 19:13:33, 19:16:30 (cards 19:14:12, 19:17:00). H10 18:20:37, 19:07:19 (card 18:21:59). H11/H11b 18:24:59, 19:06:17. H12 18:31:29, 18:31:52, 18:35:28, 18:35:46, 18:36:20, 19:16:30 (card 18:49:25).
