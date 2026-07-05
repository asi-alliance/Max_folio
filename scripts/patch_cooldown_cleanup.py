import sys
lines = open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py").readlines()
to_del = []
for i, l in enumerate(lines):
    if i == 102 and "existing_sources=None):" in l and "cycle" not in l:
        to_del.append(i)
    if i == 107 and "if any(e for e" in l and "not e.resolved):" in l and "active" not in l:
        to_del.append(i)
    if i == 109 and "self.requests_deduped" in l and lines[i-1].strip().startswith("if any"):
        to_del.append(i)
for i in sorted(to_del, reverse=True):
    del lines[i]
open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py","w").writelines(lines)
print(f"CLEANUP: deleted lines at 0-indexed positions {to_del}")
