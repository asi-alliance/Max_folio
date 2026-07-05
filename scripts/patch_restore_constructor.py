import sys
lines = open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py").readlines()
lines.insert(110, "        req = EvidenceRequest(" + chr(10))
open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py","w").writelines(lines)
print("FIX: inserted req = EvidenceRequest( at line 111")
