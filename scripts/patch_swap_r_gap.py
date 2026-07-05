import sys
lines = open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py").readlines()
ridx = None
for i, l in enumerate(lines):
    if l.strip() == "r = self.records[bid]" and i > 106 and i < 112:
        ridx = i
        break
if ridx:
    del lines[ridx]
    gidx = next(i for i,l in enumerate(lines) if "gap = max(0.0" in l and i > 104)
    lines.insert(gidx, "        r = self.records[bid]" + chr(10))
    open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py","w").writelines(lines)
    print(f"FIX: moved r=self.records[bid] from 0-idx {ridx} to before gap at {gidx}")
else:
    print("ERROR: r assignment line not found in expected range")
