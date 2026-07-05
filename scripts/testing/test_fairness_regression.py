import json,sys,datetime,random
sys.path.insert(0,"/home/mettaclaw/artifacts")
from cert_layer_v03_simple import certify,Verdict
from quarantine_tracker_v02 import QuarantineTracker,QuarantineRecord,QOutcome

def nal_revise(f1,c1,f2,c2):
    w1=c1/(1-c1) if c1<0.999 else 999
    w2=c2/(1-c2) if c2<0.999 else 999
    wt=w1+w2
    return round((w1*f1+w2*f2)/wt,4),round(wt/(wt+1),4)

def run_test(use_fair=True,label="fair"):
    random.seed(42)
    meta=json.load(open("/home/mettaclaw/artifacts/load_kb_meta.json"))
    tracker=QuarantineTracker()
    cycle=1000;ts=datetime.datetime.now().isoformat();qlist=[]
    for b in meta["beliefs"]:
        v,rsns,mrg=certify(b["f"],b["c"])
        if v==Verdict.QUARANTINE:
            qlist.append(b)
            tracker.register(QuarantineRecord(belief_id=b["id"],term=b["term"],f=b["f"],c=b["c"],reasons=rsns,quarantined_at=ts,quarantined_cycle=cycle))
    for w in range(1,6):
        cycle+=10
        active=[i for i,r in tracker.records.items() if r.outcome==QOutcome.PENDING]
        k=max(1,int(len(active)*0.4))
        if use_fair:
            sel=tracker.fair_select(k)
        else:
            sel=random.sample(active,min(k,len(active))) if active else []
        for bid in sel:
            rec=tracker.records[bid]
            rec.corroboration_attempts+=1
            fn,cn=nal_revise(rec.f,rec.c,1.0,0.9)
            rec.f=fn;rec.c=cn;rec.corroboration_count+=1
            v2,_,_=certify(fn,cn)
            if v2==Verdict.ADMIT:
                tracker.admit(bid,fn,cn,"corroboration",ts)
    tracker.expire_sweep(cycle+100,ts)
    exp=sum(1 for r in tracker.records.values() if r.outcome==QOutcome.EXPIRED)
    prom=sum(1 for r in tracker.records.values() if r.outcome==QOutcome.PROMOTED)
    print(f"{label}: Q={len(qlist)} promoted={prom} expired={exp}")
    return exp

exp_fair=run_test(True,"FAIR")
exp_rand=run_test(False,"RANDOM")
assert exp_fair==0,f"FAIL: fair mode expired {exp_fair}"
assert exp_rand>0,f"FAIL: random mode should have starvation"
print("REGRESSION PASSED: fair=0expired, random>0expired")