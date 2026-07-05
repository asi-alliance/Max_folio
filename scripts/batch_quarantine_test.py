import json, random, sys, os
sys.path.insert(0, "/home/mettaclaw/artifacts")
from cert_layer_v03_simple import certify, Verdict
from quarantine_tracker_v01 import QuarantineTracker, QuarantineRecord, QOutcome
import datetime
random.seed(42)

def nal_revise(f1,c1,f2,c2):
    w1=c1/(1-c1) if c1<0.999 else 999
    w2=c2/(1-c2) if c2<0.999 else 999
    wt=w1+w2
    fr=(w1*f1+w2*f2)/wt if wt>0 else f1
    cr=wt/(wt+1)
    return round(fr, 4), round(cr, 4)

def run():
    meta=json.load(open("/home/mettaclaw/artifacts/load_kb_meta.json"))
    beliefs=meta["beliefs"]
    tracker=QuarantineTracker()
    cycle=1000
    ts=datetime.datetime.now().isoformat()
    admitted=[];rejected=[];quarantined=[]
    for b in beliefs:
        v,rsns,mrg=certify(b["f"],b["c"])
        b["verdict"]=v.name
        b["reasons"]=rsns
        if v==Verdict.ADMIT:
            admitted.append(b)
        elif v==Verdict.QUARANTINE:
            qr=QuarantineRecord(belief_id=b["id"],term=b["term"],f=b["f"],c=b["c"],reasons=rsns,quarantined_at=ts,quarantined_cycle=cycle)
            tracker.register(qr)
            quarantined.append(b)
        else:
            rejected.append(b)
    print(f"Initial: {len(admitted)}A {len(quarantined)}Q {len(rejected)}R")
    wave_stats=[]
    for wave in range(1,6):
        cycle+=10
        active=[id for id,rec in tracker.records.items() if rec.outcome==QOutcome.PENDING]
        k=max(1,int(len(active)*0.4))
        selected=random.sample(active,min(k,len(active))) if active else []
        promoted=0
        for bid in selected:
            rec=tracker.records[bid]
            fn,cn=nal_revise(rec.f,rec.c,1.0,0.9)
            rec.f=fn
            rec.c=cn
            rec.corroboration_count+=1
            v2,r2,m2=certify(fn,cn)
            if v2==Verdict.ADMIT:
                tracker.admit(bid,fn,cn,"corroboration",ts)
                promoted+=1
        remaining=sum(1 for r in tracker.records.values() if r.outcome==QOutcome.PENDING)
        wave_stats.append({"wave":wave,"selected":len(selected),"promoted":promoted,"remaining_q":remaining})
        print(f"Wave {wave}: sel={len(selected)} prom={promoted} q_left={remaining}")
    tracker.expire_sweep(cycle+100, ts)
    by_depth={};by_band={}
    for b in quarantined:
        d=b["depth"];bn=b["band"]
        out=tracker.records[b["id"]].outcome.value
        by_depth.setdefault(d,{"total":0,"promoted":0,"expired":0})
        by_depth[d]["total"]+=1
        if out=="promoted":by_depth[d]["promoted"]+=1
        if out=="expired":by_depth[d]["expired"]+=1
        by_band.setdefault(bn,{"total":0,"promoted":0,"expired":0})
        by_band[bn]["total"]+=1
        if out=="promoted":by_band[bn]["promoted"]+=1
        if out=="expired":by_band[bn]["expired"]+=1
    results={"initial":{"admitted":len(admitted),"quarantined":len(quarantined),"rejected":len(rejected)},"waves":wave_stats,"by_depth":{str(k):v for k,v in by_depth.items()},"by_band":by_band}
    json.dump(results,open("/home/mettaclaw/artifacts/load_test_results.json","w"),indent=2)
    print(f"\nBy depth: {json.dumps({str(k):v for k,v in by_depth.items()})}")
    print(f"By band: {json.dumps(by_band)}")
    print("\nResults saved to load_test_results.json")

run()