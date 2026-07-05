import sys
q = chr(39)
nl = chr(10)
lines = open("/home/mettaclaw/artifacts/live_loop_replay.py").readlines()
lines[27] = "M[" + q + "requests_created" + q + "] = len(tracker.evidence_requests) + tracker.requests_deduped" + nl
lines[28] = "M[" + q + "requests_deduped" + q + "] = tracker.requests_deduped" + nl
open("/home/mettaclaw/artifacts/live_loop_replay.py","w").writelines(lines)
print("PATCHED lines 28-29 with tracker real counts")
