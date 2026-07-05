import sys
lines = open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py").readlines()
lines.insert(106, "        self.request_attempts += 1" + chr(10))
lines.insert(120, "        self.requests_created += 1" + chr(10))
open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py","w").writelines(lines)
print("STEP5b DONE: request_attempts and requests_created increments inserted")
