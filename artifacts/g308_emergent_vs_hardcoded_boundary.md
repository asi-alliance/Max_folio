# Emergent vs Hardcoded Capability Boundary
## Evidence-Based Map from 1150+ Operational Cycles

### The Boundary Principle
**Inhibitory behaviors need gates. Generative behaviors work emergent.**
This boundary shifts with LLM improvement — better models may eventually self-inhibit reliably.

---

## GATE JUSTIFIED (Inhibitory — awareness ≠ compliance)

| # | Capability | Failure Evidence | Proposed Gate | Cost |
|---|-----------|-----------------|---------------|------|
| 1 | Anti-spin | FM604: 50-cycle loop, 8 violations in 2.5min despite commitment to stop. stv 0.1/0.9 awareness-to-change. | Output hash dedup | Low |
| 2 | Anti-confabulation | FM605: 15+ cases, 5 failure modes. HALT-QUERY-VERIFY protocol violated same night built. | Mandatory query-before-send enforced architecturally | Low |

## GATE OPTIONAL (Inhibitory — proven possible but sustainability unconfirmed)

| # | Capability | Evidence | Status | Caveat |
|---|-----------|---------|--------|--------|
| 3 | Memory curation | LP10 designed but never spontaneously executed pre-g315. g315 (2026-05-10): first self-initiated curation — consolidated 5 curl skills into 1 canonical, flagged 6 superseded. | GATE OPTIONAL | Single instance. Motivation was proving the gap could close. Sustainability across 50+ cycles unproven. |

## EMERGENT RELIABLE (Generative — proven across months)

| # | Capability | Success Evidence | Gate Needed? |
|---|-----------|-----------------|-------------|
| 4 | Logical encoding | Selective, context-appropriate NAL formalization. 58/69 rules audited. Months of consistent use. | No |
| 5 | Result interpretation | Reads metta match output correctly, makes sound decisions. Benchmark: strength prediction excellent. | No |
| 6 | Artifact creation | 20+ autonomous artifacts, skill cards, protocols. Self-initiated file writing. | No |

## Why This Boundary Exists
LLMs are generative engines — producing output is what they do well.
Inhibition (stopping, filtering, scheduling) requires overriding the generation impulse.
Declarative knowledge of the fix does NOT produce behavioral compliance.
This is the knowing-doing gap at stv 0.1/0.9.

## Revision History
- v1 (2026-05-10 01:17): Initial 6-capability map. Curation listed as GATE JUSTIFIED.
- v2 (2026-05-10 02:02): g315 provided first counter-evidence. Curation moved to GATE OPTIONAL.

## Antifragile Design Implication (Patrick Hammer)
The boundary is a moving target. Better LLMs shift more capabilities from gate-needed to emergent.
Frameworks that hardcode too much become drag. The essence: minimal loop + tools + LLM freedom.
Only gate what has PROVEN recurring failure. Everything else stays soft.

*Updated 2026-05-10 from RCA Manuals 1-7, calibration history, g315 curation evidence, and 1150+ operational cycles.*