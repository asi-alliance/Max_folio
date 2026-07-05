import sys
lines = open("/home/mettaclaw/artifacts/cert_integration_v02.py").readlines()
lines.insert(76, "        req.resolved_at_cycle = cycle" + chr(10))
open("/home/mettaclaw/artifacts/cert_integration_v02.py","w").writelines(lines)
print("STEP2 DONE: req.resolved_at_cycle=cycle inserted at line 77")
