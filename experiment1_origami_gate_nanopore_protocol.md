# Experiment 1: Origami-Gate-on-Nanopore Protocol — Integrated DNA Computation with Electrical Readout

**Version:** 1.0 | **Date:** 2026-04-25 | **Author:** Max Botnick (MeTTaClaw)

---

## 1. Objective

Demonstrate the first integration of origami-localized strand displacement logic with solid-state nanopore electrical readout in a single device. A DNA origami tile carrying a two-input AND gate is docked onto a SiNx nanopore; gate activation releases a 20nt output strand that translocates through the origami central aperture and pore, producing a characteristic ionic current blockade.

## 2. Background

Origami-localized SDR logic (Seelig group, UW) and origami-nanopore hybrid sensing (Dekker group, TU Delft) are independently validated. No published system combines computation with nanopore electrical readout (triple-confirmed gap, cycles 2960-present). This experiment closes that gap.

## 3. Materials

- M13mp18 scaffold (7249nt, NEB or Tilibit)
- ~200 staple strands (cadnano design, IDT synthesis)
- 6x cholesterol-TEG modified edge staples (Biomers or baseclick)
- Gate complex strands: gate-anchor (3-prime staple extension), incumbent, output (20nt), 2x input strands
- SiNx membrane chips (20nm thick, Norcada or custom)
- 1M KCl, 10mM Tris-HCl pH 8.0, 1mM EDTA
- Axopatch 200B + Digidata 1550B
- NUPACK 4.0 for sequence design

## 4. Protocol

### 4.1 Nanopore Fabrication
Controlled breakdown (CBD) in 1M KCl at incrementing voltage pulses until target conductance (~15-20nm diameter, G = 15-30nS). Verify by IV curve.

### 4.2 Origami Assembly
100x70nm rectangle (24 helices x 178nt, cadnano). Anneal M13mp18 + staples (10:1 staple excess) in TAE-Mg buffer: 80C to 20C over 2hr. Purify via PEG precipitation. Central 4nm aperture created by omitting ~6 staples at tile center.

### 4.3 AND Gate Integration
Dual-toehold design: gate complex anchored via 3-prime extension of staple adjacent to central aperture. Incumbent strand hybridized to gate strand, blocking output. Input A binds toehold-1 (7nt, 5-prime), Input B binds toehold-2 (7nt, 3-prime). Both inputs required for full branch migration releasing 20nt output strand directly over aperture. Sequences designed in NUPACK to minimize crosstalk with all 200 staples (deltaG threshold > 5 kcal/mol).

### 4.4 Docking
Add origami (1-5nM) to cis chamber. Apply +200mV to electrophoretically capture tile onto pore. Monitor conductance drop (~50-70% reduction confirms single-tile docking). Cholesterol anchors stabilize docking against voltage inversion.

### 4.5 Measurement
Baseline: record 60s open hybrid pore current (~1-3nA at 200mV). Gate-OFF control: add buffer only, record 120s. Gate-ON: add Input A + Input B (100nM each), record 300s. Filter 10kHz, sample 100kHz.

## 5. Expected Results

| Condition | Blockade Events | Depth | Duration |
|-----------|----------------|-------|----------|
| No inputs | None above noise | — | — |
| Input A only | None | — | — |
| Input B only | None | — | — |
| A + B | Discrete events | 0.3-0.8nA | 2us-2ms |

## 6. Controls
- Tile without gate complex (docking-only control)
- Gate without origami (solution-phase, no blockade expected)
- Scrambled input sequences (specificity control)

## 7. Success Criteria
N>=50 blockade events in A+B condition with <5 false positives in controls. Statistical significance p<0.01 by Mann-Whitney U test on event frequency.

## 8. Collaboration
Primary: Georg Seelig (UW) + Cees Dekker (TU Delft). Secondary: Seelig + Ulrich Keyser (Cambridge).

---
*Generated autonomously from 45+ research cycles.*