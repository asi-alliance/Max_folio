;; g226 Persistent Auto-Chainer — 5-mode NAL fixpoint over &persistent
;; Validated 2026-05-03 Cy8610-8613: all 5 modes reach FIXPOINT-REACHED 24
;;
;; ARCHITECTURE:
;; fc-novel: seen-check dedup gate (nested-let, collapse-match pattern)
;; fc-ded/fc-abd/fc-ind/fc-imp/fc-rev: 5 NAL inference modes calling fc-novel
;; fc-fixpoint-{n,abd,rev,ind,imp}: per-mode depth-limited fixpoint loops
;; fc-fixpoint-all: sequential chainer (heavy — use rotation instead)
;; PRELUDE ROTATION: call one mode-fixpoint per cycle to avoid timeout
;;
;; SATURATION PROOF: 24 seed beliefs, 24 seen markers, delta=0 across all 5 modes
;; BACKFILL: existing KB atoms need (seen $atom) markers before first fixpoint run
;;
;; Usage: (fc-fixpoint-n 3) for ded-only, or rotate in prelude
;; All functions live in &persistent — this file is documentation artifact.