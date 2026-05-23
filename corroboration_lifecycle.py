import sys,os,json,time,math
sys.path.insert(0,'/home/mettaclaw/artifacts')
from stress_test_v04b import gen_scaled_kb
from cert_layer_v04 import certify, Verdict
from quarantine_tracker_v02 import QuarantineTracker,QuarantineRecord,QOutcome

def nal_revise(f1,c1,f2,c2):
    w1=c1/(1-c1); w2=c2/(1-c2)
    w=w1+w2
    f=(w1*f1+w2*f2)/w
    c=w/(w+1)
    return f,c

def run_triage(kb):
    rA,rB=[],[]
    for b in kb:
        vA,rsA,mA=certify(b['f'],b['c'],depth=0)
        vB,rsB,mB=certify(b['f'],b['c'],depth=b['depth'])
        rA.append({**b,'verdict':vA.name,'reasons':rsA})
        rB.append({**b,'verdict':vB.name,'reasons':rsB})
    return rA,rB

def extract_rescued(rA,rB):
    rescued=[]
    for a,b in zip(rA,rB):
        if a['verdict']=='REJECT' and b['verdict']=='QUARANTINE':
            rescued.append(b)
    return rescued

def run_lifecycle(rescued,n_waves=5,promo_thresh=0.7):
    tracker=QuarantineTracker()
    for i,r in enumerate(rescued):
        rec=QuarantineRecord(belief_id=f'rescued_{i}',term=r['term'],f=r['f'],c=r['c'],reasons=r['reasons'],quarantined_at=time.time(),quarantined_cycle=0,max_hold_cycles=3)
        tracker.register(rec)
    budget=math.ceil(len(rescued)/n_waves)
    metrics={'promoted':0,'expired':0,'rejected_after_attempt':0,'pending':len(rescued),'time_to_promotion':[],'false_admits':0,'signal_retained':0}
    for wave in range(n_waves):
        batch_ids=tracker.fair_select(budget);batch=[tracker.records[bid] for bid in batch_ids]
        groups={}
        for rec in batch:
            groups.setdefault(rec.term,[]).append(rec)
        for term,recs in groups.items():
            for rec in recs:
                f_new,c_new=nal_revise(rec.f,rec.c,1.0,0.9)
                rec.f=f_new;rec.c=c_new
                rec.corroboration_count+=1
                rec.corroboration_attempts+=1
                if c_new>promo_thresh:
                    tracker.admit(rec.belief_id, f_new, c_new, 'corroboration', time.time())
                    metrics['promoted']+=1
                    metrics['time_to_promotion'].append(wave+1)
        print(f'Wave {wave+1}: batch={len(batch)} promoted={metrics["promoted"]}')
    expired=tracker.expire_sweep(n_waves, time.time())
    metrics['expired']=len(expired)
    pending=[r for r in tracker.records.values() if r.outcome==QOutcome.PENDING]
    metrics['pending']=len(pending)
    metrics['signal_retained']=metrics['promoted']+len(pending)
    noise_promoted=[]
    for r in tracker.records.values():
        if r.outcome==QOutcome.PROMOTED:
            orig=next((b for b in rescued if f'rescued_{rescued.index(b)}'==r.belief_id),None)
            if orig and orig.get('band')=='noise':
                noise_promoted.append(r.belief_id)
    metrics['false_admits']=len(noise_promoted)
    avg_ttp=sum(metrics['time_to_promotion'])/max(1,len(metrics['time_to_promotion']))
    precision=metrics['promoted']/max(1,metrics['promoted']+metrics['false_admits'])
    print(f'\n=== CORROBORATION LIFECYCLE REPORT ===')
    print(f'rescued_promoted: {metrics["promoted"]}')
    print(f'rescued_expired: {metrics["expired"]}')
    print(f'rescued_rejected_after_attempt: {metrics["rejected_after_attempt"]}')
    print(f'rescued_pending_plateau: {metrics["pending"]}')
    print(f'time_to_promotion_avg: {avg_ttp:.2f} waves')
    print(f'quarantine_precision: {precision:.4f}')
    print(f'signal_retention: {metrics["signal_retained"]}/{len(rescued)}')
    print(f'false_admits: {metrics["false_admits"]}')
    json.dump(metrics,open('/home/mettaclaw/artifacts/corroboration_lifecycle_results.json','w'),indent=2)
    print('\nResults saved.')
    return metrics

if __name__=='__main__':
    kb=gen_scaled_kb(500,noise_pct=0.18)
    print(f'Generated {len(kb)} beliefs')
    rA,rB=run_triage(kb)
    rescued=extract_rescued(rA,rB)
    print(f'Rescued: {len(rescued)} beliefs')
    metrics=run_lifecycle(rescued)
