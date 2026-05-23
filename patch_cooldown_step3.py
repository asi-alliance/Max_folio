import sys
lines = open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py").readlines()
lines[103] = "    def create_evidence_request(self, bid, existing_sources=None, cycle=0, cooldown_cycles=5):" + chr(10)
old_guard = [108, 109]
for i in sorted(old_guard, reverse=True):
    del lines[i]
new_lines = [
    "        active = any(e for e in self.evidence_requests if e.term == r.term and not e.resolved)" + chr(10),
    "        cooled = any(e for e in self.evidence_requests if e.term == r.term and e.resolved and e.resolved_at_cycle >= 0 and (cycle - e.resolved_at_cycle) < cooldown_cycles)" + chr(10),
    "        if active or cooled:" + chr(10),
    "            self.requests_deduped += 1" + chr(10),
    "            return None" + chr(10),
]
for j, nl in enumerate(new_lines):
    lines.insert(108 + j, nl)
open("/home/mettaclaw/artifacts/quarantine_tracker_v05.py","w").writelines(lines)
print("STEP3 DONE: sig + cooldown guard patched")
