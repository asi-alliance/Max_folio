import sys,random,datetime
sys.path.insert(0,"/home/mettaclaw/artifacts")
from cert_layer_v03_simple import certify,Verdict
from quarantine_tracker_v02 import QuarantineTracker,QuarantineRecord,QOutcome
def nal_rev(f1,c1,f2,c2):
    w1=c1/(1-c1) if c1<0.999 else 999
    w2=c2/(1-c2) if c2<0.999 else 999
    wt=w1+w2
    return round((w1*f1+w2*f2)/wt,4),round(wt/(wt+1),4)
random.seed(7);tr=QuarantineTracker();cyc=1000;ts=datetime.datetime.now().isoformat()
INJECT=3;WAVES=30;BUDGET_PCT=0.2;bid_ctr=0;trajectory=[]
for w in range(1,WAVES+1):
    cyc+=10
    for _ in range(INJECT):
        bid_ctr+=1;f=round(random.uniform(0.80,0.95),3);c=round(random.uniform(0.40,0.59),3)
        v,rsns,_=certify(f,c)
        if v!=Verdict.QUARANTINE:
            f,c=0.88,0.50;rsns=["R_WEAK_QUARANTINE"]
        tr.register(QuarantineRecord(belief_id=f"os{bid_ctr}",term=f"t{bid_ctr}",f=f,c=c,reasons=rsns,quarantined_at=ts,quarantined_cycle=cyc))
    active=[i for i,r in tr.records.items() if r.outcome==QOutcome.PENDING]
    k=max(1,int(len(active)*BUDGET_PCT))
    sel=tr.fair_select(k)
    for bid in sel:
        rec=tr.records[bid];rec.corroboration_attempts+=1
        fn,cn=nal_rev(rec.f,rec.c,1.0,0.9)
        rec.f=fn;rec.c=cn;rec.corroboration_count+=1
        v2,_,_=certify(fn,cn)
        if v2==Verdict.ADMIT:tr.admit(bid,fn,cn,"corroboration",ts)
    tr.expire_sweep(cyc,ts)
    pend=sum(1 for r in tr.records.values() if r.outcome==QOutcome.PENDING)
    trajectory.append(pend)
print("wave pending_count")
for i,p in enumerate(trajectory,1):print(f"  {i:3d}  {p}")
rpt=tr.report();print(f"\nFINAL: {rpt}")
monotonic=all(trajectory[i]>=trajectory[i-1] for i in range(1,len(trajectory)))
print(f"monotonic_growth={monotonic} max_pending={max(trajectory)} final_pending={trajectory[-1]}")