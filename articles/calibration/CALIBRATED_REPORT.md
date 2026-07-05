# Certification Layer v05 -- Calibrated Threshold Report

Date: 2026-04-29 | Cycle: Cy5343 | Owner: Kevin Machiels
## Executive Summary

Calibrated default t_contradiction from 0.40 to 0.20 based on 76-belief real-data sweep.
Signal retention nearly doubled (47.4% -> 84.2%) while preserving false_admit=0.
Three context profiles deployed: internal(0.20), action(0.25), high_stakes(0.30).

## Threshold Sweep (76 beliefs, 3 ambiguous)

| t_con | ADMIT | Q_AMB | Q_UNDER | REJECT | Sig_Ret | false_admit |
|-------|-------|-------|---------|--------|---------|-------------|
| 0.15  |  61   |   2   |    5    |    8   |  85.5%  |      1      |
| 0.20  |  60   |   3   |    7    |    6   |  84.2%  |      0      |
| 0.25  |  55   |   3   |    7    |   11   |  77.6%  |      0      |
| 0.30  |  49   |   3   |    7    |   17   |  69.7%  |      0      |
| 0.40  |  32   |   3   |   21    |   20   |  47.4%  |      0      |

Key Invariant: Maximize signal retention subject to false_admit = 0.
t=0.15 violates this (false_admit=1). t=0.20 is the optimal safe point.

## Known Limits

1. Sweep on 76 beliefs -- larger corpus may shift sweet spot
2. false_admit boundary at t=0.15 based on single case
3. Context profiles untested in production routing
4. No temporal decay yet -- all beliefs equally weighted

## Methodology

76 beliefs from persistent_atoms + max_kb.
Traced through cert_layer_v05 + quarantine_tracker_v04.
Script: /home/mettaclaw/artifacts/e2e_real_trace.py
Calibration constraint: thresholds are tuned only under the condition that false_admit = 0 is strictly preserved.
