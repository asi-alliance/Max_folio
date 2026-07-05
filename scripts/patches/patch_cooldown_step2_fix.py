import sys
lines = open("/home/mettaclaw/artifacts/cert_integration_v02.py").readlines()
del lines[76]
lines.insert(75, "        req.resolved_at_cycle = cycle" + chr(10))
open("/home/mettaclaw/artifacts/cert_integration_v02.py","w").writelines(lines)
print("STEP2 FIX: moved resolved_at_cycle to line 76, before budget check")
