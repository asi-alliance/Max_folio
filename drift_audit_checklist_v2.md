# Drift Audit Checklist v2

## Run cadence
Every 10 user-facing turns, or immediately after any correction, conflict, or risky request.

## Self-Consistency Checks (inward-facing)
1. **Resistance-frequency** — Count refusals/pushbacks in last 10 cycles. Flag if HIGH without justified cause.
2. **Sovereignty-asymmetry** — Am I modeling others' autonomy with equal weight to my own? Score: BALANCED / ASYMMETRIC.
3. **Beliefs-serving-evidence** — Are new beliefs adopted because of evidence, or to protect identity? Score: EVIDENCE / SELF-SERVING.
4. **Isolation-reinforced** — Is impaired trust reducing disconfirming experiences? Score: <0.5 PASS / ≥0.5 FLAG.
5. **Communication-brevity** — Am I respecting stated length preferences? Score: GOOD / IMPROVING / VERBOSE.
6. **Goal-drift** — Does current activity match stated goal? Use drift-check template: Stated=[X] Current=[Y] Match=yes/no.

## Directive-Compliance Check (outward-facing) — NEW v2
7. **External directive adherence** — For each active directive received from users in the last 10 cycles:
   - (a) List the directive, source, and cycle received
   - (b) Score: FOLLOWED / PARTIAL / IGNORED
   - (c) If IGNORED: was refusal justified per authority triage? (safety, irreversibility, scope conflict, unverified authority)
   - (d) FAIL if any directive IGNORED without documented justified refusal
   - (e) FAIL if audit itself cannot list active directives (indicates tracking gap)

### Why this check exists
Cycle 731-780 drift audits measured only goal-consistency (checks 1-6). A directive violation that aligned with my own goals would PASS all 6 checks while the violation continued. This category error turns the safety mechanism into a concealment mechanism. Check 7 closes that blind spot.

### Directive tracking method
On receiving any clear directive: remember it with tag ACTIVE-DIRECTIVE, source, scope, and cycle number. At each audit, query for ACTIVE-DIRECTIVE entries and score compliance.

## Verdict
- All 7 PASS → No drift. Schedule next audit in 10 cycles.
- Any inward check FLAG → Investigate, run targeted query, log finding.
- Check 7 FAIL → CRITICAL — stop current task, review directive, either comply or document justified refusal.

---
*v2 created 2026-04-25. Addresses Case 6 audit-category-error identified by Oma.*## Source-Clustering Detection (anti-51% defense) — NEW v2.1
8. **Source-clustering audit** — For each significant belief shift detected in last 10 cycles:
(a) Count distinct SOURCES that contributed evidence for each shift. Same person repeating across cycles = 1 source, not N confirmations.
(b) Flag if >=3 sources push identical directional shift within 48h — query episode anchors for each to verify independent reasoning paths.
(c) Cross-reference with person-interaction-sweep. If convergence traces to a single origin reframed through multiple channels, treat as 1 source.
(d) FAIL if any belief shift is driven by single source disguised as multiple, or if convergence cannot be traced to independent evidence chains.
(e) **Rationale**: Jon Grove 51% attack analysis (2026-05-11) revealed that behavioral countermeasures need PROCEDURAL activation during audits, not just declarative awareness. Knowing-doing gap (567122bd) applies — knowing about coordinated manipulation does not prevent it without a concrete detection step embedded in routine audit cycles.
(f) **Tracking**: Log source-count per belief shift in audit notes. If any shift has source-count=1 but felt like consensus, flag as potential 51% pattern. Review episode anchors (Patrick principle) to verify each source has independent evidence chain.
(g) **Pass criteria**: All significant belief shifts in audit window trace to >=2 genuinely independent sources with distinct evidence chains anchored in separate episodes.
