import sys
lines = open("/home/mettaclaw/artifacts/cert_integration_v02.py").readlines()
for i, l in enumerate(lines):
    if "tracker.create_evidence_request(belief_id)" in l and "cycle" not in l:
        lines[i] = l.replace("create_evidence_request(belief_id)", "create_evidence_request(belief_id, cycle=cycle)")
    if "tracker.create_evidence_request(bid)" in l and "cycle" not in l:
        lines[i] = l.replace("create_evidence_request(bid)", "create_evidence_request(bid, cycle=cycle)")
open("/home/mettaclaw/artifacts/cert_integration_v02.py","w").writelines(lines)
print("STEP4 DONE: cycle=cycle added to both call sites")
