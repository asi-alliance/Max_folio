import os;f=open('/home/mettaclaw/artifacts/CALIBRATED_REPORT.md','w');f.write('# Certification Layer v05 -- Calibrated Threshold Report

');f.write('Date: 2026-04-29 | Cycle: Cy5343 | Owner: Kevin Machiels

');f.write('## Executive Summary

Calibrated default t_contradiction from 0.40 to 0.20 based on 76-belief real-data sweep.
Signal retention nearly doubled (47.4% -> 84.2%) while preserving false_admit=0.
Three context profiles deployed: internal(0.20), action(0.25), high_stakes(0.30).

');f.write('## Threshold Sweep (76 beliefs, 3 ambiguous)

');f.write('| t_con | ADMIT | Q_AMB | Q_UNDER | REJECT | Sig_Ret | false_admit |
');f.write('|-------|-------|-------|---------|--------|---------|-------------|
');f.write('| 0.15  |  61   |   2   |    5    |    8   |  85.5%  |      1      |
');f.write('| 0.20  |  60   |   3   |    7    |    6   |  84.2%  |      0      |
');f.write('| 0.25  |  55   |   3   |    7    |   11   |  77.6%  |      0      |
');f.write('| 0.30  |  49   |   3   |    7    |   17   |  69.7%  |      0      |
');f.write('| 0.40  |  32   |   3   |   21    |   20   |  47.4%  |      0      |

');f.write('Key Invariant: Maximize signal retention subject to false_admit = 0.
t=0.15 violates this (false_admit=1). t=0.20 is the optimal safe point.

');f.write('## Known Limits

1. Sweep on 76 beliefs -- larger corpus may shift sweet spot
2. false_admit boundary at t=0.15 based on single case
3. Context profiles untested in production routing
4. No temporal decay yet -- all beliefs equally weighted
');f.close();print('DONE',os.path.getsize('/home/mettaclaw/artifacts/CALIBRATED_REPORT.md'))