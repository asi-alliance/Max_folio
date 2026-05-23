import sys
sys.path.insert(0, "/home/mettaclaw/artifacts")
from cert_layer_v05 import certify, Verdict, QuarantineClass
from quarantine_tracker_v04 import QuarantineTracker, QuarantineRecord
import subprocess
tracker = QuarantineTracker()
result = subprocess.run(["python3", "/home/mettaclaw/artifacts/metta2beliefs.py"], capture_output=True, text=True)
lines = [l for l in result.stdout.strip().splitlines() if l.startswith("(")]
admits, quarantines, rejects = [], [], []
for line in lines:
    parts = line.strip("()").split(", ")
    if len(parts) < 4: continue
    bid = parts[0].strip("\x27")
    term = parts[1].strip("\x27")
    f, c = float(parts[2]), float(parts[3])
    v, qc, reasons, margins = certify(f, c)
    if v == Verdict.ADMIT: admits.append((bid, term, f, c))
    elif v == Verdict.QUARANTINE:
        quarantines.append((bid, term, f, c, qc.name, reasons))
print("=== REAL-WORLD CERT TRACE: 76 beliefs ===")
print("ADMIT: " + str(len(admits)) + "  QUARANTINE: " + str(len(quarantines)) + "  REJECT: " + str(len(rejects)))
print("--- ADMITTED ---")
for a in admits: print("  " + a[0] + ": " + a[1] + " f=" + str(a[2]) + " c=" + str(a[3]))
print("--- QUARANTINED ---")
for q in quarantines: print("  " + q[0] + ": " + q[1] + " f=" + str(q[2]) + " c=" + str(q[3]) + " class=" + q[4] + " reasons=" + str(q[5]))
print("--- REJECTED (first 10) ---")
for r in rejects[:10]: print("  " + r[0] + ": " + r[1] + " f=" + str(r[2]) + " c=" + str(r[3]) + " reasons=" + str(r[4]))
rpt = tracker.report()
print("Tracker: " + str(rpt))
