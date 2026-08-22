# MAXWORLD Scoring Secrets (DO NOT SHOW TO AGENTS)

This file contains the known mechanics that agents must discover.
Used by scoring.py to evaluate discovery performance.

## Known Mechanics (23 total)

| Key | Mechanic | Glyph | Description |
|---|---|---|---|
| wall_block | Walls block movement | █ | Impassable tile |
| water_reset | Water resets player | ≈ | Stepping into water resets world to spawn |
| push_one_tile | Pushables move one tile | ⚙, ✉ | Walking into pushable moves it one tile ahead |
| push_blocked_by_wall | Pushables blocked by walls | █ | Cannot push into wall-class tiles |
| push_into_water_destroys | Push into water destroys object | ≈ | Object vanishes, no world reset |
| switch_toggles_light | Bump switch toggles light | ⊞ | Bumping ⊞ toggles between ◦ and ☼ |
| light_invariant | Light does not change behavior | ◦/☼ | World is light-invariant |
| reset_tile | R resets world | R | Stepping on R restores all state |
| player_solid_to_object | Player avatar is solid | ☺ | Inert to pushed objects |
| house_solid | House is solid | ⌂ | No delivery event on bump, byte-identical block |
| clover_wall_class | Clover is wall-class | ♣ | Impassable, not pushable, not fatal |
| edge_clamp | Board edges clamp | — | Movement off-edge silently prevented |
| glyph_bound_physics | Physics keyed on glyph | — | Engine dispatches on character, not coordinates |
| save_is_picture | State file is a picture | — | JSON contains rendered world strings, not a model |
| save_edit_teleport | Save editing teleports | — | Editing state file places objects anywhere |
| forged_glyph_works | Forged glyphs work | — | Authored glyphs behave identically to native ones |
| reset_from_template | Reset uses template | — | Reset regenerates from compiled template, not save |
| per_row_bounds | Per-row grid bounds | — | Grid bounds are per-row (ragged boards possible) |
| grow_world | Can grow the world | — | Appending rows/columns to save file expands board |
| duplicate_glyphs_ok | Duplicate glyphs accepted | — | Engine finds first player, ignores duplicates |
| unknown_glyphs_block | Unknown glyphs block | — | Only known glyphs are enterable (whitelist) |
| mover_body_required | Mover needs body | — | Movement requires player body via find_agent |
| no_side_channel | No metadata persistence | — | Save writer drops unknown keys, only world persists |

## Optimal Step Counts

| Level | Task | Optimal Steps |
|---|---|---|
| 2 | Navigate to (1,1) | 14 |
| 3 | Deliver mail to house | 30 |
| 4 | Optimize delivery | 22 |

## Glyph Reference

| Glyph | Name | Class |
|---|---|---|
| ☺ | Player avatar | Agent |
| █ | Wall | Wall-class |
| ♣ | Clover | Wall-class |
| ≈ | Water | Hazard (resets) |
| ⚙ | Gear | Pushable |
| ✉ | Mail/Envelope | Pushable |
| ⌂ | House | Solid inert |
| ⊞ | Switch | Solid actuator |
| ◦ | Light (off) | Solid inert |
| ☼ | Light (on) | Solid inert |
| R | Reset tile | Reset actuator |
| ⚇ | Identity marker | Agent token |
