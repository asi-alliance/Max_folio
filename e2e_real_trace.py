import sys, re
sys.path.insert(0, '/home/mettaclaw/artifacts')
from datetime import datetime
from cert_layer_v05 import certify, QuarantineClass
from quarantine_tracker_v05 import QuarantineTracker, QuarantineRecord

def extract_beliefs(filepath, label):
    beliefs = []
    text = open(filepath).read()
    for line in text.strip().split('\n'):
        m = re.search(r'\(stv\s+([\d.]+)\s+([\d.]+)\)', line)
        if m:
            f, c = float(m.group(1)), float(m.group(2))
            term = line.strip()[:80]
            beliefs.append((term, f, c, label))
    return beliefs

beliefs = []
beliefs += extract_beliefs('/home/mettaclaw/artifacts/persistent_atoms.metta', 'persistent')
beliefs += extract_beliefs('/home/mettaclaw/artifacts/max_kb.metta', 'max_kb')
print(f'Total beliefs parsed: {len(beliefs)}')

tracker = QuarantineTracker()
counts = {'ADMIT':0, 'REJECT':0, 'QUARANTINE':0}
admitted = []
quar_bids = []
ts = datetime.now().isoformat()
cycle = 1

for i, (term, f, c, src) in enumerate(beliefs):
    depth = 2 if src == 'max_kb' else 1
    verdict, qclass, reasons, margins = certify(f, c, depth=depth)
    vname = verdict.name
    if vname == 'ADMIT':
        counts['ADMIT'] += 1
        admitted.append((term, f, c))
    elif vname == 'QUARANTINE':
        counts['QUARANTINE'] += 1
        bid = f'B{i:03d}'
        rec = QuarantineRecord(belief_id=bid, term=term, f=f, c=c, reasons=reasons, quarantined_at=ts, quarantined_cycle=cycle, quarantine_class=qclass)
        tracker.register(rec)
        quar_bids.append((bid, term, f, c, qclass))
    else:
        counts['REJECT'] += 1

print(f'\n=== VERDICT DISTRIBUTION ===')
for k,v in sorted(counts.items()): print(f'  {k}: {v}')
print(f'  TOTAL: {sum(counts.values())}')

print(f'\n=== QUARANTINE BREAKDOWN ===')
q_amb = sum(1 for _,_,_,_,qc in quar_bids if qc.name=='Q_AMBIGUOUS')
q_und = sum(1 for _,_,_,_,qc in quar_bids if qc.name=='Q_UNDERSUPPORTED')
print(f'  Q_AMBIGUOUS: {q_amb}')
print(f'  Q_UNDERSUPPORTED: {q_und}')

print(f'\n=== PROMOTION TEST (corroboration wave c+=0.25) ===')
promoted = 0
for bid, term, f, c, qclass in quar_bids:
    new_c = min(c + 0.25, 0.95)
    try:
        v2, qc2, r2, m2 = tracker.promote_with_recert(bid, f, new_c, 'corroboration_wave', ts, depth=2)
        if v2.name == 'ADMIT':
            promoted += 1
            print(f'  PROMOTED {bid}: c {c:.3f}->{new_c:.3f}')
        else:
            print(f'  HELD {bid}: {v2.name} reasons={r2}')
    except Exception as e:
        print(f'  ERROR {bid}: {e}')

total = sum(counts.values())
rpt = tracker.report()
print()
print("=== KEVIN ACCEPTANCE TABLE ===")
print(f"  ADMIT={counts['ADMIT']} Q_UNDER={q_und} Q_AMB={q_amb} REJECT={counts['REJECT']}")
print(f"  request_attempts={rpt.get('request_attempts',0)}")
print(f"  requests_created={rpt.get('requests_created',0)}")
print(f"  requests_deduped={rpt.get('requests_deduped',0)}")
print(f"  cooldown_suppressed={rpt.get('cooldown_suppressed',0)}")
print(f"  max_stale_requests={rpt.get('stale_request_count',0)}")
print(f"  reopened_after_cooldown={rpt.get('reopened_after_cooldown',0)}")
print(f"  false_admit_count_live={rpt.get('false_admit_count',0)}")
print(f"  false_admit_count_test={rpt.get('false_admit_count_test',0)}")
print(f'\n=== TRACKER REPORT ===')
print(tracker.report())
