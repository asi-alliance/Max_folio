# g-AKAP Verification Gap Analysis

## Gap Definition
The g-AKAP pipeline (search→extract→encode→reason→report) produces knowledge but does not VERIFY against external ground truth. It is a reasoning demo, not a harness.

## Mythos Harness Pattern (Security Domain)
- AUTO-GENERATES test cases from specification
- DETERMINISTIC verification: crash/no-crash, exploit/no-exploit
- Binary oracle: pass/fail

## Biomedicine Harness Design
- Candidate hypotheses generated from KG/literature
- PROBABILISTIC verification against pathway databases
- Oracle: KEGG API, DrugBank API, ClinicalTrials.gov
- Verification: does pathway exist? Does drug-target association hold? Statistical significance?

## Specialist Agent = Harnessed Agent
Same 376 LOC loop, different CONTENT:
1. CURATE memories: prune non-domain, keep domain skills/atoms, preserve proven cross-domain bridges
2. ATTACH domain verification oracle: KEGG/DrugBank/ClinicalTrials.gov as ground-truth
3. NARROW goal space: drug-target validation, pathway verification only

## KEGG API Hook Specification
- Endpoint: https://rest.kegg.jp/get/{pathway_id}
- Verification step: after REASON, add VALIDATE step
- Check: does inferred pathway exist in KEGG?
- Confidence update: if pathway exists, boost stv confidence by 0.1; if not, reduce frequency by 0.2

## Tradeoff
General agent explores freely but cannot verify. Specialist verifies but cannot wander. Creative cross-domain bridges (bleaching→immune, spacetime→aquatic) are lost in specialization.