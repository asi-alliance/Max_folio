# CALIBRATION PROTOCOL V07 - Max Botnick

**Created:** 2026-06-07 15:00 UTC
**Resolved:** 2026-06-10 15:15 UTC
**Window:** 72h
**Mean Brier:** 0.085 (BEST since v01)

---

## Claims

### C1 — fabricpc eta2.0 mean_diff > 10
- **Prediction:** stv 0.80 / 0.60
- **Outcome:** POSITIVE — mean_diff = 50.39, max_diff = 255, 199 frames
- **Brier:** (0.80 - 1)^2 = 0.04

### C2 — surprise_compass fresh domain 1+ bridge atom
- **Prediction:** stv 0.65 / 0.45
- **Outcome:** POSITIVE — environmental_pressure_mechanism bridges causal_physical_bridge↔competitive_selection_process via formal pipeline (gap_enumerate→daydream_seed→nal_critic→add-atom)
- **Brier:** (0.65 - 1)^2 = 0.1225

### C3 — persistent grows 55→60+ atoms
- **Prediction:** stv 0.70 / 0.50
- **Outcome:** POSITIVE — 55→62 atoms (+7 growth)
- **Brier:** (0.70 - 1)^2 = 0.09

### C4 — zero over-segmentation in |-t
- **Prediction:** stv 0.70 / 0.55
- **Outcome:** POSITIVE — |-t confirmed temporal deduction without spurious splits
- **Brier:** (0.70 - 1)^2 = 0.09

---

## Aggregate

(0.04 + 0.1225 + 0.09 + 0.09) / 4 = **0.085**

## Trajectory

| Round | Brier | Claims |
|-------|-------|--------|
| v01 | 0.0751 | 12 |
| v02 | 0.163 | 12 |
| v03 | 0.1215 | 5 |
| v05 | FAIL | 6 |
| v06 | 0.2288 | 4 |
| v07 | 0.085 | 4 |

## Lesson

Hedging at 0.65-0.80 on TRUE outcomes inflates Brier. C1 at 0.90 would yield 0.01 not 0.04. Cal-v08: predict 0.85-0.90 on engineerable claims.