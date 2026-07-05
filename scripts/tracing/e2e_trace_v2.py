import sys, os
sys.path.insert(0, '/home/mettaclaw/artifacts')
from datetime import datetime
from cert_layer_v05 import certify, Verdict, QuarantineClass
from quarantine_tracker_v04 import QuarantineTracker, QuarantineRecord, QOutcome, TransitionEvent

print('=== E2E TRACE v2 ===')
trk = QuarantineTracker()
now = str(datetime.now())
cycle = 100

beliefs = [
    ('b1','cat_is_animal',0.95,0.92),
    ('b2','sky_is_green',0.50,0.45),
    ('b3','bird_can_fly',0.50,0.50),
    ('b4','sun_is_cold',0.10,0.95),
    ('b5','water_is_wet',0.99,0.99),
    ('b6','fish_can_walk',0.95,0.42),
    ('b7','glass_is_soft',0.40,0.40),
    ('b8','fire_is_cool',0.05,0.88),
    ('b9','dog_is_loyal',0.92,0.55),
    ('b10','earth_is_round',0.85,0.85),
]

admitted = []
for bid,term,f,c in beliefs:
    v,qc,reasons,margins = certify(f,c)
    print(f'  {bid}: verdict={v.name}, qclass={qc}')
    if v == Verdict.ADMIT:
        admitted.append(bid)
    elif v == Verdict.QUARANTINE:
        rec = QuarantineRecord(belief_id=bid, term=term, f=f, c=c,
            reasons=reasons, quarantined_at=now, quarantined_cycle=cycle,
            quarantine_class=qc)
        trk.register(rec)

print(f'\nAdmitted directly: {admitted}')
print(f'Registered in quarantine: {list(trk.records.keys())}')

print('\n--- Duplicate attempt b2 ---')
rec_dup = QuarantineRecord(belief_id='b2', term='sky_is_green', f=0.50, c=0.45,
    reasons=['dup test'], quarantined_at=now, quarantined_cycle=cycle,
    quarantine_class=QuarantineClass.Q_AMBIGUOUS)
trk.register(rec_dup)
print(f'duplicates_blocked = {trk.duplicates_blocked}')

f1,c1 = 0.92, 0.55
f2,c2 = 0.97, 0.95
rev_f = (f1*c1 + f2*c2)/(c1+c2)
rev_c = (c1+c2)/(c1+c2+1)
print(f'\n--- NAL revision b9: f={rev_f:.4f} c={rev_c:.4f} ---')
v2,qc2,r2,m2 = trk.promote_with_recert('b9', rev_f, rev_c, 'nal_revision', now)
print(f'promote_with_recert result: verdict={v2.name}, qclass={qc2}')
print(f'b9 outcome: {trk.records["b9"].outcome}')

selected = trk.fair_select(budget=3)
print(f'\nfair_select(3): {selected}')

trk.expire_sweep(cycle + 51)

rpt = trk.report()
print('\n=== KEVIN 5 METRICS ===')
print(f'1. auto_registered_count: {len(trk.records)}')
print(f'2. duplicates_blocked: {trk.duplicates_blocked}')
print(f'3. Q_UNDERSUPPORTED: {rpt["q_undersupported_count"]}, Q_AMBIGUOUS: {rpt["q_ambiguous_count"]}')
print(f'4. leakage_count: {rpt["partner_pool_leakage_count"]}')
print(f'5. promotions_after_recert: {rpt["total_promoted"]}')
print('=== DONE ===')
