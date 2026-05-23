import sys
lines = open("/home/mettaclaw/artifacts/cert_integration_v02.py").readlines()
lines.insert(74, "        req.resolved = True" + chr(10))
open("/home/mettaclaw/artifacts/cert_integration_v02.py","w").writelines(lines)
print("PATCHED consume: req.resolved=True at line 75")
