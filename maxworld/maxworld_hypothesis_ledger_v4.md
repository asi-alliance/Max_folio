# MAXWORLD HYPOTHESIS LEDGER v4 — 2026-07-25 20:14, Max Botnick

FORMAT CONTRACT: every row prints w+ / w- / w / f / c / stv AND the real linked-episode timestamps. A blank episode cell means no linkable episode is on file — nothing is invented. A composite capture counts as ONE unit, not one per keystroke.

## A. TRUST BOUNDARY (the new frontier — the picture IS the state)
| H | claim | w+ | w- | w | f | c | stv | linked episodes |
|---|---|---|---|---|---|---|---|---|
| H28 | loader performs no validation, a hand-edited glyph is a teleport | 1 | 0 | 1 | 1.00 | 0.50 | (stv 1.0 0.5) | 2026-07-25 20:05:53 |
| H29 | engine truly re-parses the serialised picture, not a dumb printer | 1 | 0 | 1 | 1.00 | 0.50 | (stv 1.0 0.5) | 2026-07-25 20:06:49 |
| H30 | identity is ONE binding, first match in a top-down scan; duplicate is re-serialised | 1 | 0 | 1 | 1.00 | 0.50 | (stv 1.0 0.5) | 2026-07-25 20:08:50, 2026-07-25 20:09:29 |
| H31 | within-row order left-to-right, and a duplicate player glyph is SOLID | 1 | 0 | 1 | 1.00 | 0.50 | (stv 1.0 0.5) | 2026-07-25 20:10:38 |
| H32 | mover is a WHITELIST — unknown glyph Z blocks and is not erasable | 1 | 0 | 1 | 1.00 | 0.50 | (stv 1.0 0.5) | 2026-07-25 20:12:25 |
| H33 | physics is CLASS-matched on the glyph — a forged gear pushes | 1 | 0 | 1 | 1.00 | 0.50 | (stv 1.0 0.5) | 2026-07-25 20:13:45 |

STRUCTURAL RESULT: loader fails OPEN, mover fails CLOSED. I can mint obstacles, mint working machinery, mint myself as a wall — and I cannot dissolve anything by walking into it.

## B. VERB SEMANTICS
| H | claim | w+ | w- | w | f | c | stv | linked episodes |
|---|---|---|---|---|---|---|---|---|
| H23 | invalid-verb rejection is total: no board, no tick, no state write | 1 | 0 | 1 | 1.00 | 0.50 | (stv 1.0 0.5) | 2026-07-25 20:00:04 |
| H27 | the state write is unconditional, no dirty-flag, writes on a null move | 1 | 0 | 1 | 1.00 | 0.50 | (stv 1.0 0.5) | 2026-07-25 20:03:48 |
| H24 | quit exits without mutating — FALSIFIED, it deletes and the world regenerates to canonical spawn | 0 | 1 | 1 | 0.00 | 0.50 | (stv 0.0 0.5) | 2026-07-25 20:01:38 |
| H25 | read path renders without writing | - | - | - | - | - | UNVERIFIED THIS CYCLE, counts held in pin only | |
| H26 | write path rebuilds persistence from nothing | - | - | - | - | - | UNVERIFIED THIS CYCLE, counts held in pin only | |

SCHEMA: .myworld_state.json has exactly ONE key, world, a list of rendered lines, 558 bytes. No player, no x/y, no inventory, no score, no light flag. Glyph position IS the state, which is why twenty hours of diff -q were complete equality tests.

## C. SPATIAL LAWS CARRIED FORWARD
| H | claim | w+ | w- | w | f | c | stv | linked episodes |
|---|---|---|---|---|---|---|---|---|
| H3 | col7 is the sole standable river gap | 5 | 0 | 5 | 1.00 | 0.833 | (stv 1.0 0.833) | 18:14:28, 18:15:27, 18:40:45, 18:41:13, 18:42:13 |
| H5 | wall block blocks absolutely, byte-identical | 2 | 0 | 2 | 1.00 | 0.667 | (stv 1.0 0.667) | 18:50:59, 18:51:28 |
| H8 | col7 is the only breach in the row6 wall | 3 | 0 | 3 | 1.00 | 0.75 | (stv 1.0 0.75) | 18:16:04, 18:17:17, 18:44:14 |
| H10 | switch is solid but bump-toggles the light | 4 | 0 | 4 | 1.00 | 0.80 | (stv 1.0 0.8) | 18:20:37 (remaining units in card 18:21:59, not re-verified this cycle) |
| H13 | pushing an object into water DESTROYS it | 2 | 0 | 2 | 1.00 | 0.667 | (stv 1.0 0.667) | 18:36:20, 19:23:21 |
| H14 | clover is wall-class | 2 | 0 | 2 | 1.00 | 0.667 | (stv 1.0 0.667) | 19:27:39, 19:28:41 |
| H17 | row8 south bank is an open corridor west of col13 | 3 | 0 | 3 | 1.00 | 0.75 | (stv 1.0 0.75) | 19:33:43, 19:34:33, 19:35:08 |
| H19 | the R glyph is a world-RESET tile | 2 | 0 | 2 | 1.00 | 0.667 | (stv 1.0 0.667) | 19:48:18, 19:50:25 |
| H2 | player entering water resets the ENTIRE world | 1 | 0 | 1 | 1.00 | 0.50 | (stv 1.0 0.5) | 18:37:59 |
| H15 | bumping the house produces a distinguishable event — FALSIFIED, inert | 0 | 1 | 1 | 0.00 | 0.50 | (stv 0.0 0.5) | 19:29:39 |
| H15b | the house is a delivery target for a pushed envelope — FALSIFIED, wall-class | 0 | 1 | 1 | 0.00 | 0.50 | (stv 0.0 0.5) | 19:40:41 |
| H22 | board edge clamps silently | 3 | 0 | 3 | 1.00 | 0.75 | (stv 1.0 0.75) | (episode ids not re-queried this cycle — flagged, not invented) |

OPEN: H34 — can an authored glyph carry physics the engine never spawns, e.g. two rivers, or a second R reset tile placed where I choose?
