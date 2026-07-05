# g406 FC-STEP + SW-REVISE PIPELINE PROCEDURE
## INVARIANT: ALWAYS remove-atom old TV before add-atom new TV in &persistent.

## ROOT CAUSE (CORRECTED 2026-05-12 Cy6633-6635): fc-step5-novel-via-v4 KNOWN branch does NOT call add-atom — it was NOT overwriting. Real bug: add-atom on existing atom creates DUPLICATE phantom versions in &persistent; match returns first match (old TV). Fix: ALWAYS remove-atom old TV THEN add-atom new TV. Phantom duplicate pattern confirmed from Cy1807/Cy3049.

## PROCEDURE (6 steps, all in agent loop):
1. metta (fc-step5-novel-via-v4) — capture full output
2. Parse output: identify NOVEL and KNOWN items
3. For each KNOWN item: metta query existing TV + VIA provenance from &persistent
4. Compute Jaccard between existing VIA provenance and new VIA derivation
5. shell python3 /tmp/sw_revise_cli.py f1 c1 t1 f2 c2 t2 jaccard — get revised TV
6. metta remove-atom old TV THEN add-atom revised TV for each KNOWN item

## CRITICAL CONSTRAINTS:
- &persistent NOT shared across shell subprocess PeTTa instances
- All metta queries MUST run in agent loop, only math via shell python3
- Steps 3-6 MUST complete before next fc-step invocation
- If agent cycle breaks between step 1 and step 6, re-apply remove+add before any fc-step

## VERIFIED FIX: remove-atom then add-atom prevents phantom duplicates (confirmed Cy6635-6649)
## ARTIFACTS: /tmp/sw_revise_cli.py, /tmp/fc_step_parser.py