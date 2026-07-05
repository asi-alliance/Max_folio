import sys,os,json
sys.path.insert(0,"/home/mettaclaw/artifacts")
from cert_layer_v04 import certify,Verdict
from stress_test_v04b import gen_scaled_kb

def triage(beliefs,force_depth=None,label=""):
    counts={v.name:0 for v in Verdict}
    rescued=0
    results=[]
    for b in beliefs:
        d=force_depth if force_depth is not None else b["depth"]
        v,rsns,margins=certify(b["f"],b["c"],depth=d)
        counts[v.name]+=1
        if "R_CHAIN_RESCUED" in rsns: rescued+=1
        results.append({**b,"verdict":v.name,"reasons":rsns,"depth_used":d})
    print("[%s] A=%d Q=%d R=%d rescued=%d" % (label,counts["ADMIT"],counts["QUARANTINE"],counts["REJECT"],rescued))
    return results,counts,rescued

kb=gen_scaled_kb(500,noise_pct=0.18)
print("Beliefs: %d" % len(kb))
print("\n=== ARM A: depth=0 (no chain penalty) ===")
rA,cA,rscA=triage(kb,force_depth=0,label="ARM_A")
print("\n=== ARM B: actual depth (chain penalty active) ===")
rB,cB,rscB=triage(kb,force_depth=None,label="ARM_B")
print("\n=== COMPARISON ===")
for v in ["ADMIT","QUARANTINE","REJECT"]:
    delta=cB[v]-cA[v]
    print("  %s: A=%d B=%d delta=%+d" % (v,cA[v],cB[v],delta))
print("  chain_rescued: A=%d B=%d" % (rscA,rscB))
nA=sum(1 for r in rA if r["verdict"]=="ADMIT" and r["band"]=="noise")
nB=sum(1 for r in rB if r["verdict"]=="ADMIT" and r["band"]=="noise")
print("  noise_admitted: A=%d B=%d (must be 0)" % (nA,nB))
dpB=sum(1 for r in rB if "R_CHAIN_RESCUED" in r["reasons"] and r["depth_used"]>=2)
print("  deep_rescued(d>=2): %d" % dpB)
results={"ARM_A":cA,"ARM_B":cB,"rescued_A":rscA,"rescued_B":rscB,"noise_A":nA,"noise_B":nB,"deep_B":dpB}
json.dump(results,open("/home/mettaclaw/artifacts/ab_chain_penalty_results.json","w"),indent=2)
print("\nResults saved.")