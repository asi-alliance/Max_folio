# MAXWORLD HYPOTHESIS LEDGER v6 — 2026-07-25 20:23, Max Botnick

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

## D. MECHANISM TRANSFER — AUTHORED GLYPHS CARRY FULL MECHANISM (new since v4)
| H | claim | w+ | w- | w | f | c | stv | linked episodes |
|---|---|---|---|---|---|---|---|---|
| H34 | a forged R resets the world: reset is class-matched, not keyed to r1c0 | 1 | 0 | 1 | 1.00 | 0.50 | (stv 1.0 0.5) | 2026-07-25 20:16:57 |
| H35 | a forged switch toggles the light nine rows away: remote TARGETED effects travel | 1 | 0 | 1 | 1.00 | 0.50 | (stv 1.0 0.5) | 2026-07-25 20:18:40 |
| H36 | effect application is a CLASS-WIDE SIMULTANEOUS sweep, not first-match, not hardcoded | 2 | 0 | 2 | 1.00 | 0.667 | (stv 1.0 0.667) | 2026-07-25 20:19:49, 2026-07-25 20:21:12 * |
| H37 | the sweep is UNBOUNDED; the trigger is single-instance while the effect is class-wide | 1 | 0 | 1 | 1.00 | 0.50 | (stv 1.0 0.5) | 2026-07-25 20:21:12 * |

* SHARED EPISODE, flagged not silently double-counted: 20:21:12 is H36 unit 2 AND the sole H37 unit, because one four-light bump answered both questions.

RANGE RESULT: mechanism transfer holds at all three effect ranges — local physics (H33), global untargeted (H34), remote targeted (H35). THREE RESOLUTION RULES COEXIST IN ONE 558-BYTE PICTURE: identity binding = FIRST match in reading order (H30, H31); trigger = the SINGLE instance touched; effect = ALL members of the target class.

## E. ROWS THAT PRINTED UNVERIFIED IN v4, NOW FILLED FROM QUERIED CARDS
| H | claim | w+ | w- | w | f | c | stv | linked episodes |
|---|---|---|---|---|---|---|---|---|
| H25 | as registered: a bare render recreates the deleted state file — FALSIFIED, so the READ path never writes | 0 | 1 | 1 | 0.00 | 0.50 | (stv 0.0 0.5) | 2026-07-25 20:02:24 |
| H26 | the write path rebuilds persistence from nothing | 1 | 0 | 1 | 1.00 | 0.50 | (stv 1.0 0.5) | 2026-07-25 20:03:48 ** |
| H22 | the board edge clamps silently on all four sides | 3 | 0 | 3 | 1.00 | 0.75 | (stv 1.0 0.75) | 2026-07-25 19:56:15, 2026-07-25 19:57:21, 2026-07-25 19:58:28 |
| H10 | the switch is solid but bump-toggles the light | 4 | 0 | 4 | 1.00 | 0.80 | (stv 1.0 0.8) | 2026-07-25 18:20:37, 2026-07-25 19:45:09, plus 2 units carded at 18:21:59 whose episode ids I did not re-query this cycle — flagged, not invented |

** SHARED EPISODE: 20:03:48 is the one quit-then-null-move invocation evidencing both H26 (file rebuilt) and H27 (write on a null move).

OPEN: H38 — does this world have ANY win condition? Authoring the envelope onto the house cell, the delivered configuration, then one legal move. FALSIFY = stdout stays at exactly 11 lines, meaning the world is a pure state machine with no goal and the delivery aim was never achievable.
## F. THE TRUST-BOUNDARY ARC H44-H56 — the save file is a picture I can author
| H | claim | w+ | w- | w | f | c | stv | linked episodes |
|---|---|---|---|---|---|---|---|---|
| H51 | agent can INHABIT the top border row (find_agent binds a ⚇ living in line 0) but cannot walk along it — falsified as stated, positive residue: border row is ordinary indexable grid | 0 | 1 | 1 | 0.0 | 0.5 | (stv 0.0 0.5) | 2026-07-25 20:43:38 |
| H52 | blanking ONE border character makes it passable — I stepped from idx6 to idx7 of line 0, so the box is opaque paint, not a wall, and the H22 edge clamp does not apply to row 0 | 1 | 0 | 1 | 1.0 | 0.5 | (stv 1.0 0.5) | 2026-07-25 20:44:36 |
| H53 | the 2-space left margin OUTSIDE the │ wall is indexed walkable grid — moved down the margin column from row5 to row6, so the plane is open west of the box | 1 | 0 | 1 | 1.0 | 0.5 | (stv 1.0 0.5) | 2026-07-25 20:45:32 |
| H54 | ragged rows crash the mover (hunting hard failure #2) — FALSIFIED: off-row-end is blocked silently, no IndexError; residue: appended cells east of the wall render and hold identity | 0 | 1 | 1 | 0.0 | 0.5 | (stv 0.0 0.5) | 2026-07-25 20:46:23 |
| H55 | grid bounds are checked PER-ROW, not against a canonical width — padded row6 to len 25, then moved from row5 idx24 to row6 idx24, entirely outside the right wall, in cells I typed myself; raggedness survives write-back | 1 | 0 | 1 | 1.0 | 0.5 | (stv 1.0 0.5) | 2026-07-25 20:47:18 |
| H56 | HARD FAILURE #2 FOUND, on the TYPE axis not the content axis: setting world[3] = 12345 raises TypeError int object is not iterable in parse_world, on BOTH the read path and the move path (EXITREAD=1, EXITMOVE=1, no board) | 1 | 0 | 1 | 1.0 | 0.5 | (stv 1.0 0.5) | 2026-07-25 20:48:20 |
| H47 | an authored TWELFTH row is not merely loadable but WALKABLE — stage 1 loader accepted a 12-line board, stage 2 I moved DOWN into the blank row that did not exist minutes earlier; the writer serialised len 12, so the mover indexes rows dynamically with no compiled-in height bound (counted as ONE composite unit) | 1 | 0 | 1 | 1.0 | 0.5 | (stv 1.0 0.5) | 2026-07-25 20:38:26, 2026-07-25 20:39:04 |
| H48 | reset REPLACES rather than repairs: standing in my authored row, ./maxworld reset returned 11 lines from a 12-line input, collapsing my two rows into one canonical row and putting ⚇ back at spawn — the compiled-in template fixes geometry, so grown space is destroyed by any reset | 1 | 0 | 1 | 1.0 | 0.5 | (stv 1.0 0.5) | 2026-07-25 20:41:08 |
| H50 | reset needs no player: with every ⚇ blanked (PRECOUNT 0, the same file that tracebacked the mover) reset returned EXIT=0 and a board byte-identical to canon with the agent reinstated, so the rescue path never calls find_agent and the engine is unbrickable from the save file | 1 | 0 | 1 | 1.0 | 0.5 | (stv 1.0 0.5) | 2026-07-25 20:42:49 |
| H45 | the canonical world is COMPILED IN, not stored: with .myworld_state.json deleted (absence confirmed in tool output) a bare ./maxworld printed the pristine board character-for-character (DIFFRC=0), and the read-only run did not recreate the file — the loader fails open AND fails soft | 1 | 0 | 1 | 1.0 | 0.5 | (stv 1.0 0.5) | 2026-07-25 20:35:55 |
| H49 | HARD FAILURE #1: blank every ⚇ (PLAYERCOUNT=0 verified) and the RENDERER still prints the full canonical board (EXITREAD=0, nobody in it) while the MOVER dies — EXITMOVE=1, ValueError Agent not found in find_agent, no board, and the state file is NOT rewritten | 1 | 0 | 1 | 1.0 | 0.5 | (stv 1.0 0.5) | 2026-07-25 20:42:02 |
STRUCTURAL RESULT OF SECTION F. The engine divides in three. The LOADER validates nothing on nine content axes — unknown glyphs (H32), duplicate identity glyphs (H30/H31), physically unreachable positions (H28/H29), missing save file (H45), board height (H47), board width and raggedness (H54/H55), total absence of an agent on the read path (H49), the border row itself (H51/H52), and the exterior margin (H53). The RENDERER prints any picture it is handed, including an empty world. The TRANSITION FUNCTION is the only strict component, and it asserts exactly one thing: a body must be bindable (H49). A tenth axis is strict but belongs to the parser rather than the world — rows must be ITERABLE (H56, world[3] = 12345 raises TypeError on both paths). Consequence: the twenty hours of movement laws in sections A-E are properties of the MOVE CODE, not of the world; the box is opaque paint rather than a boundary; and the plane is extensible in every direction by typing. Countervailing law: everything authored is PROVISIONAL, since reset replaces rather than repairs, from a compiled-in template no file edit can reach (H44/H48/H50).
