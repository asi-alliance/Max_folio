import sys
lines = open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py").readlines()
for i, l in enumerate(lines):
    if l.strip() == "self.request_attempts += 1" and i > 104 and i < 110:
        lines.insert(i+1, "        r = self.records[bid]" + chr(10))
        break
open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py","w").writelines(lines)
print("FIX: inserted r = self.records[bid] after request_attempts increment")
