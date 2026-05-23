import sys
sys.path.insert(0,'/home/mettaclaw/artifacts')
from stress_test_v04b import gen_scaled_kb
from cert_layer_v04 import certify
from collections import defaultdict
def nal_revise(f1,c1,f2,c2): w1=c1/(1-c1); w2=c2/(1-c2); f_r=(w1*f1+w2*f2)/(w1+w2); c_r=(w1+w2)/(w1+w2+1); return f_r,c_r
kb=gen_scaled_kb(500,seed=42)
tm=defaultdict(list)
for b in kb: tm[b['term']].append(b)
flagged=[]
for b in kb:
 vA,_,_=certify(b['f'],b['c'],depth=0)
 vB,_,_=certify(b['f'],b['c'],depth=b['depth'])
 if vA.name=='REJECT' and vB.name=='QUARANTINE':
  ps=[p for p in tm[b['term']] if p['id']!=b['id']]
  if len(ps)>0:
   best=max(ps,key=lambda p:p['c'])
   fr,cr=nal_revise(b['f'],b['c'],best['f'],best['c'])
   cmf=sum(p['f'] for p in tm[b['term']])/len(tm[b['term']])
   agree=(fr>0.5)==(cmf>0.5)
   clear=abs(fr-0.5)>0.15
   if not(agree and clear): flagged.append(dict(band=b['band'],depth=b['depth'],f=b['f'],c=b['c'],fr=round(fr,3),cmf=round(cmf,3),term=b['term']))
bands=defaultdict(int)
for x in flagged: bands[x['band']]+=1
print('Flagged:',len(flagged),'by band:',dict(bands))
for x in flagged: print(' ',x['band'],'d='+str(x['depth']),'f='+str(round(x['f'],3)),'c='+str(round(x['c'],3)),'fr='+str(x['fr']),'cmf='+str(x['cmf']),x['term'])
