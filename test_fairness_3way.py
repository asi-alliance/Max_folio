import json,sys,datetime,random
sys.path.insert(0,"/home/mettaclaw/artifacts")
from cert_layer_v03_simple import certify,Verdict
from quarantine_tracker_v01 import QuarantineTracker as TV1,QuarantineRecord as QR1,QOutcome as QO1
from quarantine_tracker_v02 import QuarantineTracker as TV2,QuarantineRecord as QR2,QOutcome as QO2

def nal_revise(f1,c1,f2,c2):
    w1=c1/(1-c1) if c1<0.999 else 999
    w2=c2/(1-c2) if c2<0.999 else 999
    wt=w1+w2
    return round((w1*f1+w2*f2)/wt,4),round(wt/(wt+1),4)

def run(TClass,RClass,OClass,use_fair,budget_pct,label):
    random.seed(42);meta=json.load(open("/home/mettaclaw/artifacts/load_kb_meta.json"))
    tr=TClass();cycle=1000;ts=datetime.datetime.now().isoformat();ql=[]
    for b in meta["beliefs"]:
        v,rsns,mrg=certify(b["f"],b["c"])
        if v==Verdict.QUARANTINE:
            ql.append(b);tr.register(RClass(belief_id=b["id"],term=b["term"],f=b["f"],c=b["c"],reasons=rsns,quarantined_at=ts,quarantined_cycle=cycle))
    for w in range(1,6):
        cycle+=10;active=[i for i,r in tr.records.items() if r.outcome==OClass.PENDING]
        k=max(1,int(len(active)*budget_pct))
        sel=tr.fair_select(k) if use_fair and hasattr(tr,"fair_select") else (random.sample(active,min(k,len(active))) if active else [])
        for bid in sel:
            rec=tr.records[bid]
            if hasattr(rec,"corroboration_attempts"):rec.corroboration_attempts+=1
            fn,cn=nal_revise(rec.f,rec.c,1.0,0.9)
            rec.f=fn;rec.c=cn;rec.corroboration_count+=1
            v2,_,_=certify(fn,cn)
            if v2==Verdict.ADMIT:tr.admit(bid,fn,cn,"corroboration",ts)
    tr.expire_sweep(cycle+100,ts)
    exp=sum(1 for r in tr.records.values() if r.outcome==OClass.EXPIRED)
    prom=sum(1 for r in tr.records.values() if r.outcome==OClass.PROMOTED)
    pend=sum(1 for r in tr.records.values() if r.outcome==OClass.PENDING)
    print(f"{label}: Q={len(ql)} promoted={prom} expired={exp} pending={pend}")
    return exp,pend

e1,_=run(TV1,QR1,QO1,False,0.2,"A_RANDOM_v01")
e2,_=run(TV2,QR2,QO2,True,0.2,"B_FAIR_v02")
e3,p3=run(TV2,QR2,QO2,False,0.2,"C_RANDOM_v02")
assert e1>0,f"FAIL A: v01 random should starve, got {e1}"
assert e2==0,f"FAIL B: v02 fair should be 0, got {e2}"
assert e3==0,f"FAIL C: v02 random protected should be 0, got {e3}"
print(f"THREE-WAY REGRESSION PASSED: v01_starved={e1}, v02_fair=0, v02_random_protected=0(pending={p3})")