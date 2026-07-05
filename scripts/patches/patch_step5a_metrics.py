import sys
lines = open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py").readlines()
lines.insert(68, "        self.request_attempts = 0" + chr(10))
lines.insert(69, "        self.requests_created = 0" + chr(10))
open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py","w").writelines(lines)
print("STEP5a DONE: added request_attempts and requests_created to __init__")
