import sys
sys.path.insert(0,"/home/mettaclaw/artifacts")
from stress_test_v04b import gen_scaled_kb
kb=gen_scaled_kb(500)
terms={}
for b in kb: terms.setdefault(b["term"],[]).append(b)
solo=[t for t,bs in terms.items() if len(bs)==1]
multi=[t for t,bs in terms.items() if len(bs)>1]
print("total=%d unique_terms=%d solo=%d multi=%d" % (len(kb),len(terms),len(solo),len(multi)))
noise_solo=[t for t in solo if "noise" in t]
print("noise_solo=%d signal_solo=%d" % (len(noise_solo),len(solo)-len(noise_solo)))
noise_multi=[t for t in multi if 'noise' in t]
print('noise_multi=%d signal_multi=%d' % (len(noise_multi),len(multi)-len(noise_multi)))
print('signal_solo_terms:', [t for t in solo if 'noise' not in t][:10])
from cert_layer_v04 import certify,Verdict
rescued=[]
for b in kb:
    vA,_,_=certify(b['f'],b['c'],depth=0); vB,rsns,_=certify(b['f'],b['c'],depth=b['depth'])
    if vA==Verdict.REJECT and vB==Verdict.QUARANTINE: rescued.append(b)
rescued_solo=[b for b in rescued if b['term'] in solo]
rescued_multi=[b for b in rescued if b['term'] in multi]
print('rescued=%d groupA_multi=%d groupB_solo=%d' % (len(rescued),len(rescued_multi),len(rescued_solo)))
rescued_solo_detail=[(b['id'],b['term'],b['band'],b['f'],b['c'],b['depth']) for b in rescued_solo]
print('Group_B_solo_details:');[print('  ',x) for x in rescued_solo_detail]
