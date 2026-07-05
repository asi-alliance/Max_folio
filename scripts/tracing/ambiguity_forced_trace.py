import sys
sys.path.insert(0,'/home/mettaclaw/artifacts')
from quarantine_tracker_v05 import QuarantineTracker, QuarantineRecord, EvidenceRequest
try:
    from cert_layer_v05 import QuarantineClass
except:
    from enum import Enum
    class QuarantineClass(Enum):
        Q_AMBIGUOUS='Q_AMBIGUOUS'
        Q_UNDERSUPPORTED='Q_UNDERSUPPORTED'
from cert_integration_v02 import consume_evidence_requests, _term_last_served
from datetime import datetime
t=QuarantineTracker()
now=datetime.now().isoformat()
cy=0
print('=== P1: Register 3 Q_AMBIGUOUS beliefs ===')
for i,term in enumerate(['amb_A','amb_B','amb_C']):
    r=QuarantineRecord(belief_id=f'B{i}',term=term,f=0.50,c=0.45,reasons=['R_CONTRADICTION'],quarantined_at=now,quarantined_cycle=cy,quarantine_class=QuarantineClass.Q_AMBIGUOUS)
    t.register(r)
    print(f'  registered {r.belief_id} term={term}')
print('=== P2: Oscillate f to force flip_count>=2 ===')
osc=[0.62,0.42,0.60,0.45,0.58]
for step,nf in enumerate(osc):
    cy+=1
    for bid in ['B0','B1','B2']:
        t.update_ambiguity_state(bid,nf)
    r0=t.records['B0']
    print(f'  step{step}: f={nf} flip={r0.flip_count} dir={r0.last_direction}')
print('=== P3: trigger_check + create_evidence_request ===')
cy+=1
req_created=0
deduped=0
for bid in ['B0','B1','B2']:
    fired=t.trigger_check(bid,tau=5,k=2)
    print(f'  trigger_check({bid})={fired}')
    if fired:
        er=t.create_evidence_request(bid,existing_sources=['web'],cycle=cy,cooldown_cycles=5)
        if er:
            req_created+=1
            print(f'  request created for {bid}')
        else:
            deduped+=1
            print(f'  deduped {bid}')
print(f'  totals: created={req_created} deduped={deduped}')
print('=== P4: consume budget=1 ===')
_term_last_served.clear()
actions=consume_evidence_requests(t,budget=1,cycle=cy,window=1)
print(f'  consumed={len(actions)} resolved={sum(1 for e in t.evidence_requests if e.resolved)}')
print('=== P5: re-request within cooldown ===')
cy+=1
cool_suppressed=0
for bid in ['B0','B1','B2']:
    er=t.create_evidence_request(bid,existing_sources=['web'],cycle=cy,cooldown_cycles=5)
    if er is None:
        cool_suppressed+=1
print(f'  cooldown_suppressed={cool_suppressed}')
print('=== P6: re-request after cooldown expires ===')
cy+=10
reopened=0
for bid in ['B0','B1','B2']:
    er=t.create_evidence_request(bid,existing_sources=['web'],cycle=cy,cooldown_cycles=5)
    if er:
        reopened+=1
        print(f'  reopened {bid}')
print(f'  reopened_count={reopened}')
rpt=t.report(cy)
print(f'REPORT: {rpt}')
print('ALL PHASES COMPLETE')