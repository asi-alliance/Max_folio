import pathlib
p = pathlib.Path('/home/mettaclaw/artifacts/quarantine_tracker_v05.py')
t = p.read_text()
NL = chr(10)
old1 = 'self.evidence_requests: List[EvidenceRequest] = []'
new1 = old1 + NL + '        self.requests_deduped = 0'
t = t.replace(old1, new1, 1)
guard = 'if any(e for e in self.evidence_requests if e.term == r.term and not e.resolved):' + NL + '            self.requests_deduped += 1' + NL + '            return None' + NL + '        '
old2 = 'req = EvidenceRequest('
new2 = guard + old2
t = t.replace(old2, new2, 1)
p.write_text(t)
print('PATCHED' if 'requests_deduped' in p.read_text() else 'FAIL')
