import sys
sys.path.insert(0, "/home/mettaclaw/artifacts")
from datetime import datetime
from cert_layer_v05 import certify, Verdict, QuarantineClass
from quarantine_tracker_v03 import QuarantineTracker, QuarantineRecord

def certify_and_track(f, c, depth, tracker, cycle, term, belief_id, thresholds=None):
    verdict, qclass, reasons, margins = certify(f, c, thresholds=thresholds, depth=depth)
    if verdict == Verdict.QUARANTINE:
        rec = QuarantineRecord(
            belief_id=belief_id,
            term=term,
            f=f,
            c=c,
            reasons=reasons,
            quarantined_at=datetime.now().isoformat(),
            quarantined_cycle=cycle,
            quarantine_class=qclass
        )
        tracker.register(rec)
    return verdict, qclass, reasons, margins
