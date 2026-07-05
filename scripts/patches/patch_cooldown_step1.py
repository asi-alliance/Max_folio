import sys
lines = open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py").readlines()
lines.insert(31, "    resolved_at_cycle: int = -1" + chr(10))
open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py","w").writelines(lines)
print("STEP1 DONE: resolved_at_cycle field added after line 31")
