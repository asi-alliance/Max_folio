import sys
sys.path.insert(0, '/home/mettaclaw/artifacts')
from datetime import datetime
from cert_layer_v05 import certify, Verdict, QuarantineClass
from quarantine_tracker_v05 import QuarantineTracker, QuarantineRecord, QuarantineClass, QOutcome

C_GENUINE_THRESHOLD = 0.7

def certify_and_track(f, c, depth, tracker, cycle, term, belief_id, thresholds=None):
    verdict, qclass, reasons, margins = certify(f, c, thresholds=thresholds, depth=depth)
    result = dict(verdict=verdict, qclass=qclass, reasons=reasons, margins=margins,
                  subtype=None, trigger_created=False, planner_called=False, leakage_count=0)
    if verdict == Verdict.QUARANTINE:
        rec = QuarantineRecord(
            belief_id=belief_id, term=term, f=f, c=c, reasons=reasons,
            quarantined_at=datetime.now().isoformat(), quarantined_cycle=cycle,
            quarantine_class=qclass)
        tracker.register(rec)
        if qclass == QuarantineClass.Q_AMBIGUOUS:
            subtype = 'Q_AMB_GENUINE' if c >= C_GENUINE_THRESHOLD else 'Q_AMB_RESOLVABLE'
            result['subtype'] = subtype
            tracker.update_ambiguity_state(belief_id, f)
            if tracker.trigger_check(belief_id, tau=5, k=2):
                if subtype == 'Q_AMB_RESOLVABLE':
                    req = tracker.create_evidence_request(belief_id, cycle=cycle)
                    result['trigger_created'] = True
                    result['planner_called'] = True
    result['leakage_count'] = len(tracker.leakage_log)
    return verdict, qclass, reasons, margins, result

def update_existing_ambiguous(bid, new_f, new_c, tracker, thresholds=None, depth=0, cycle=0):
    if bid not in tracker.records:
        return None
    r = tracker.records[bid]
    if r.quarantine_class != QuarantineClass.Q_AMBIGUOUS:
        return None
    subtype = 'Q_AMB_GENUINE' if new_c >= C_GENUINE_THRESHOLD else 'Q_AMB_RESOLVABLE'
    tracker.update_ambiguity_state(bid, new_f)
    result = dict(subtype=subtype, trigger_created=False, planner_called=False)
    if tracker.trigger_check(bid, tau=5, k=2) and subtype == 'Q_AMB_RESOLVABLE':
        req = tracker.create_evidence_request(bid, cycle=cycle)
        result['trigger_created'] = True
        result['planner_called'] = True
    if not (0.35 <= new_f <= 0.65):
        tracker.promote_with_recert(bid, new_f, new_c, 'ambiguity_resolved', datetime.now().isoformat(), thresholds=thresholds, depth=depth)
        result['reclassified'] = True
    return result

def sweep_tracked_ambiguous(tracker, kb_atoms, cycle):
    actions = []
    for bid, rec in tracker.records.items():
        if rec.outcome != QOutcome.PENDING:
            continue
        if rec.quarantine_class != QuarantineClass.Q_AMBIGUOUS:
            continue
        if bid not in kb_atoms:
            continue
        new_f, new_c = kb_atoms[bid]
        r = update_existing_ambiguous(bid, new_f, new_c, tracker, cycle=cycle)
        if r:
            actions.append((bid, r))
    return actions

_term_last_served = {}

def consume_evidence_requests(tracker, budget=3, cycle=0, window=5):
    actionable = []
    for req in tracker.evidence_requests:
        if getattr(req, 'resolved', False):
            continue
        if req.term in _term_last_served and cycle - _term_last_served[req.term] < window:
            continue
        actionable.append(dict(term=req.term, priority=req.priority, gap=req.confidence_gap, direction=req.direction))
        _term_last_served[req.term] = cycle
        req.resolved = True
        req.resolved_at_cycle = cycle
        if len(actionable) >= budget:
            break
    return actionable
