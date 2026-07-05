import sys,os,json,random,time
sys.path.insert(0,'/home/mettaclaw/artifacts')
from cert_layer_v04 import certify, Verdict
from quarantine_tracker_v02 import QuarantineTracker,QuarantineRecord,QOutcome

def nal_revise(f1,c1,f2,c2):
    w1,w2=c1/(1-c1),c2/(1-c2)
    w=w1+w2
    f=(w1*f1+w2*f2)/w
    c=w/(w+1)
    return f,c

def gen_scaled_kb(total,noise_pct=0.18,seed=42):
    random.seed(seed)
    n_noise=int(total*noise_pct)
    n_real=total-n_noise
    beliefs=[]
    bid=0
    # real beliefs: 3 bands, depth 1-4
    for band,name,fr,cr in [('high','h',(0.7,1.0),(0.7,0.9)),('mid','m',(0.4,0.7),(0.4,0.7)),('low','l',(0.1,0.4),(0.15,0.4))]:
        n=n_real//3
        terms=[f"{name}_t{i}" for i in range(max(1,n//3))]
        for i in range(n):
            f=random.uniform(*fr)
            c=random.uniform(*cr)
            d=random.choice([1,2,3,4,4,4,3,2])
            t=random.choice(terms)
            beliefs.append({"id":f"b{bid}","term":t,"f":f,"c":c,"depth":d,"band":band})
            bid+=1
    # noise: unique terms, depth 0
    for i in range(n_noise):
        f=random.uniform(0.0,1.0)
        c=random.uniform(0.1,0.5)
        beliefs.append({"id":f"b{bid}","term":f"noise_unique_{i}","f":f,"c":c,"depth":0,"band":"noise"})
        bid+=1
    return beliefs

def run_stress(beliefs,inject_per_wave,waves,budget_frac,label):
    tracker=QuarantineTracker()
    term_dict={}
    for b in beliefs:
        term_dict.setdefault(b["term"],[]).append(b)
    cycle=0
    ts="2026-01-01T00:00"
    admitted,quarantined,rejected=[],[],[]
    for b in beliefs:
        v,_,rsns=certify(b["f"],b["c"],depth=b["depth"])
        b["reasons"]=rsns
        if v==Verdict.ADMIT:
            admitted.append(b)
        elif v==Verdict.QUARANTINE:
            qr=QuarantineRecord(belief_id=b["id"],term=b["term"],f=b["f"],c=b["c"],reasons=rsns,quarantined_at=ts,quarantined_cycle=cycle)
            tracker.register(qr)
            quarantined.append(b)
        else:
            rejected.append(b)
    print(f"[{label}] Initial: {len(admitted)}A {len(quarantined)}Q {len(rejected)}R")
    wave_data=[]
    total_promoted=0
    promotion_waves=[]
    next_bid=len(beliefs)
    for wave in range(1,waves+1):
        cycle+=10
        # inject new noise beliefs
        for _ in range(inject_per_wave):
            nb={"id":f"b{next_bid}","term":f"new_noise_{next_bid}","f":random.random(),"c":random.uniform(0.1,0.4),"depth":0,"band":"noise"}
            v,_,rsns=certify(nb["f"],nb["c"],depth=nb["depth"])
            if v==Verdict.QUARANTINE:
                qr=QuarantineRecord(belief_id=nb["id"],term=nb["term"],f=nb["f"],c=nb["c"],reasons=rsns,quarantined_at=ts,quarantined_cycle=cycle)
                tracker.register(qr)
            next_bid+=1
        # corroboration pass with budget
        pending=[id for id,rec in tracker.records.items() if rec.outcome==QOutcome.PENDING]
        k=max(1,int(len(pending)*budget_frac))
        selected=tracker.fair_select(k)
        promoted=0
        for bid in selected:
            rec=tracker.records[bid]
            partners=[p for p in term_dict.get(rec.term,[]) if p["id"]!=bid]
            if not partners:
                continue
            best=max(partners,key=lambda p:p["c"])
            fn,cn=nal_revise(rec.f,rec.c,best["f"],best["c"])
            if cn>=0.5:
                tracker.records[bid].outcome=QOutcome.PROMOTED
                promoted+=1
                promotion_waves.append(wave)
        noise_pending=sum(1 for id,rec in tracker.records.items() if rec.outcome==QOutcome.PENDING and 'noise' in rec.term)
        total_pending=sum(1 for id,rec in tracker.records.items() if rec.outcome==QOutcome.PENDING)
        total_promoted+=promoted
        wave_data.append({"wave":wave,"promoted":promoted,"pending":total_pending,"noise_pending":noise_pending})
    pending_plateau=max(w["pending"] for w in wave_data)
    promo_rate=total_promoted/max(1,len(tracker.records))
    avg_waves=sum(promotion_waves)/max(1,len(promotion_waves)) if promotion_waves else 0
    final_noise=sum(1 for id,rec in tracker.records.items() if rec.outcome==QOutcome.PENDING and 'noise' in rec.term)
    print(f"[{label}] {waves} waves done.")
    print(f"  total_promoted={total_promoted} promo_rate={promo_rate:.3f}")
    print(f"  pending_plateau={pending_plateau} avg_waves_to_promote={avg_waves:.1f}")
    print(f"  final_noise_pool={final_noise}")
    print(f"  last5_waves: {wave_data[-5:]}")
    return {"label":label,"total_promoted":total_promoted,"promo_rate":promo_rate,"pending_plateau":pending_plateau,"avg_waves_to_promote":avg_waves,"final_noise_pool":final_noise,"waves":wave_data}

if __name__=="__main__":
    kb=gen_scaled_kb(500,noise_pct=0.18)
    print(f"Generated {len(kb)} beliefs")
    print("\n=== STRESS_A: inject=10, budget=10% ===")
    ra=run_stress(kb,inject_per_wave=10,waves=30,budget_frac=0.10,label="STRESS_A")
    print("\n=== STRESS_B: inject=20, budget=5% ===")
    kb2=gen_scaled_kb(500,noise_pct=0.18)
    rb=run_stress(kb2,inject_per_wave=20,waves=30,budget_frac=0.05,label="STRESS_B")
    results={"STRESS_A":ra,"STRESS_B":rb}
    json.dump(results,open('/home/mettaclaw/artifacts/stress_test_v04b_results.json','w'),indent=2)
    print("\nResults saved to stress_test_v04b_results.json")