import sys
sys.path.insert(0,'/home/mettaclaw/artifacts')
from stress_test_v04b import gen_scaled_kb
from cert_layer_v04 import certify, Verdict
from collections import defaultdict
def nal_revise(f1,c1,f2,c2): w1=c1/(1-c1); w2=c2/(1-c2); f_r=(w1*f1+w2*f2)/(w1+w2); c_r=(w1+w2)/(w1+w2+1); return f_r,c_r
kb=gen_scaled_kb(500,seed=42)
term_map=defaultdict(list)
for b in kb: term_map[b['term']].append(b)
rescued=[]
for b in kb:
    vA,_,_=certify(b['f'],b['c'],depth=0)
    vB,_,_=certify(b['f'],b['c'],depth=b['depth'])
    if vA.name=='REJECT' and vB.name=='QUARANTINE':
        partners=[p for p in term_map[b['term']] if p['id']!=b['id']]
        if len(partners)>0: rescued.append((b,partners))
promoted=0
flagged=0
for b,parts in rescued:
    best=max(parts,key=lambda p:p['c'])
    fr,cr=nal_revise(b['f'],b['c'],best['f'],best['c'])
    all_f=[p['f'] for p in term_map[b['term']]]
    cmf=sum(all_f)/len(all_f)
    agree=(fr>0.5)==(cmf>0.5)
    clear=abs(fr-0.5)>0.15
    if agree and clear: promoted+=1
    else: flagged+=1
print(f'Rescued:{len(rescued)} Promoted:{promoted} Flagged:{flagged}')
