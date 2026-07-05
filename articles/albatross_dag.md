# Island Ecology DAG: Albatross → Endangered

## Topology (not a chain — a true DAG)
```
        albatross
       /    |    \
      /     |     \
  ocean- slow-   long-range-
  feeder reprod.  flyer
   / \      |      / \
  /   \     |     /   \
 plast. high- low-  nests- high-
 ingest energy repl. remote energy
  |     |     \    |     |
 toxin  forag.  \   hab.  forag.
 accum  press.   \  vuln  press.
  |      |       \ |     |
 pop-    +---------+-----+
 decline    population-stress
  |            |
  +----rev-----+
         |
     ENDANGERED
```

## 17 Premises (mixed confidence — not all 1.0)
| ID | Premise | stv |
|---|---|---|
| P1 | albatross → ocean-feeder | (0.95, 0.9) |
| P2 | ocean-feeder → plastic-ingester | (0.85, 0.9) |
| P3 | plastic-ingester → toxin-accumulator | (0.80, 0.85) |
| P4 | toxin-accumulator → population-decline | (0.75, 0.85) |
| P5 | albatross → long-range-flyer | (0.95, 0.9) |
| P6 | long-range-flyer → nests-remote-islands | (0.90, 0.9) |
| P7 | nests-remote-islands → habitat-vulnerable | (0.70, 0.85) |
| P8 | habitat-vulnerable → population-stress | (0.80, 0.85) |
| P9 | albatross → slow-reproducer | (0.90, 0.9) |
| P10 | slow-reproducer → low-replacement | (0.95, 0.85) |
| P11 | low-replacement → population-stress | (0.85, 0.85) |
| P12 | ocean-feeder → high-energy-demand | (0.90, 0.9) |
| P13 | long-range-flyer → high-energy-demand | (0.85, 0.9) |
| P14 | high-energy-demand → foraging-pressure | (0.80, 0.85) |
| P15 | foraging-pressure → population-stress | (0.75, 0.85) |
| P16 | population-decline → population-stress | (0.90, 0.85) |
| P17 | population-stress → endangered | (0.85, 0.85) |

## 4 Independent Paths to population-stress
| Path | Route | Hops | Final stv |
|---|---|---|---|
| A (food-web) | P1→P2→P3→P4→P16 | 5 | (0.436, 0.055) |
| B (habitat) | P5→P6→P7→P8 | 4 | (0.479, 0.144) |
| C (life-history) | P9→P10→P11 | 3 | (0.727, 0.404) |
| D (diamond-energy) | P1→P12→P14→P15 + P5→P13→P14→P15 | 4 | (0.513, 0.148) |

## Revision Cascade
- Rev(B,C) → (0.670, 0.550)
- Rev(BC,D) → (0.650, 0.583)
- Rev(BCD,A) → **(0.642, 0.593)** ← 47% conf boost over best single path

## Final: albatross → endangered
Deduction from revised pop-stress: **stv(0.722, 0.522)**

## Structural Properties (vs Carroll linear chain)
- **Shared nodes**: ocean-feeder and long-range-flyer each serve 2 paths (diamond)
- **Mixed confidence**: premises range 0.70–0.95, not uniform 1.0
- **Convergent revision**: 4 independent evidence streams merge
- **Confidence rescue**: deepest path (A, 5-hop) alone yields only 0.055 confidence — useless in isolation, but contributes to revision
- **True DAG**: 7 nodes have in-degree > 1; not reducible to tree or chain