import sys
lines = open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py").readlines()
to_del = []
for i, l in enumerate(lines):
    s = l.strip()
    if s.startswith("if any(e for e") and "not e.resolved):" in s and "active" not in l:
        to_del.append(i)
    if s == "self.requests_deduped += 1" and i > 0 and "if any(e for e" in lines[i-1] and "active" not in lines[i-1]:
        to_del.append(i)
for i in sorted(to_del, reverse=True):
    del lines[i]
open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py","w").writelines(lines)
print(f"CLEANUP2: deleted 0-indexed {to_del}")
