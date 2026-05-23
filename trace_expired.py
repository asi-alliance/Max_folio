import json,sys,datetime,random
sys.path.insert(0,"/home/mettaclaw/artifacts")
from cert_layer_v03_simple import certify,Verdict
from quarantine_tracker_v01 import QuarantineTracker,QuarantineRecord,QOutcome
random.seed(42)
meta=json.load(open("/home/mettaclaw/artifacts/load_kb_meta.json"))
beliefs=meta["beliefs"]
tracker=QuarantineTracker()
cycle=1000
ts=datetime.datetime.now().isoformat()
qlist=[]
for b in beliefs:
    v,rsns,mrg=certify(b["f"],b["c"])
    if v==Verdict.QUARANTINE:
        qlist.append(b)
        tracker.register(QuarantineRecord(belief_id=b["id"],term=b["term"],f=b["f"],c=b["c"],reasons=rsns,quarantined_at=ts,quarantined_cycle=cycle))
print(f"Quarantined: {len(qlist)}")
for w in range(1,6):
    cycle+=10
    active=[i for i,r in tracker.records.items() if r.outcome==QOutcome.PENDING]
    k=max(1,int(len(active)*0.4))
    sel=random.sample(active,min(k,len(active))) if active else []
    for bid in sel:
        rec=tracker.records[bid]
        w1=rec.c/(1-rec.c) if rec.c<0.999 else 999
        w2=0.9/(1-0.9)
        wt=w1+w2
        fn=round((w1*rec.f+w2*1.0)/wt,4)
        cn=round(wt/(wt+1),4)
        rec.f=fn;rec.c=cn;rec.corroboration_count+=1
        v2,_,_=certify(fn,cn)
        if v2==Verdict.ADMIT:
            tracker.admit(bid,fn,cn,"corroboration",ts)
tracker.expire_sweep(cycle+100,ts)
for bid,r in tracker.records.items():
    if r.outcome==QOutcome.EXPIRED:
        orig=[b for b in qlist if b["id"]==bid][0]
        print(f"EXPIRED: {bid} post_f={r.f:.4f} post_c={r.c:.4f} orig_f={orig['f']:.3f} orig_c={orig['c']:.3f} depth={orig['depth']} band={orig['band']} domain={orig['domain']}")