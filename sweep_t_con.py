import sys
sys.path.insert(0, '/home/mettaclaw/artifacts')
from cert_layer_v05 import certify, Verdict, QuarantineClass
beliefs = []
for fp in ['persistent_atoms.metta', 'max_kb.metta']:
    txt = open('/home/mettaclaw/artifacts/'+fp).read()
    for l in txt.strip().split(chr(10)):
        i = l.find('(stv ')
        if i < 0: continue
        j = l.find(')', i)
        parts = l[i+5:j].split()
        if len(parts)==2: beliefs.append((float(parts[0]), float(parts[1]), l.strip()[:70]))
print(str(len(beliefs))+' beliefs parsed')
known_bad = [x for x in beliefs if 0.35<=x[0]<=0.65 and x[1]>=0.4]
print(str(len(known_bad))+' ambiguous')
t_cons = [0.15, 0.20, 0.25, 0.30, 0.40]
print('t_con   ADMIT  Q_UND  Q_AMB    REJ  promo%  f_adm   sig%  kb_ad')
for tc in t_cons:
    T = dict(t_contradiction=tc, t_weak=0.6, t_vacuous=0.01, min_confidence=0.3)
    tally = dict(ADMIT=0, QUARANTINE=0, REJECT=0)
    promoted=0; q_total=0; fa=0; kb_ad=0
    for f,c,t in beliefs:
        v,q,r,m = certify(f, c, thresholds=T, depth=2)
        tally[v.name] = tally.get(v.name, 0) + 1
        if q: tally[q.name] = tally.get(q.name, 0) + 1
        if v.name=='QUARANTINE':
            q_total+=1
            v2,_,_,_=certify(f,min(c+0.25,0.99),thresholds=T,depth=2)
            if v2.name=='ADMIT': promoted+=1
        if v.name=='ADMIT' and 0.35<=f<=0.65 and c>=0.4: fa+=1
        if v.name=='ADMIT' and any(abs(f-b[0])<0.01 and abs(c-b[1])<0.01 for b in known_bad): kb_ad+=1
    n=len(beliefs); pp=(100*promoted/q_total) if q_total else 0; sp=100*(tally.get('ADMIT',0)+promoted)/n if n else 0
    print('%s  %5d  %5d  %5d  %5d  %5.1f  %5d  %5.1f  %5d' % (str(tc),tally.get('ADMIT',0),tally.get('Q_UNDERDETERMINED',0),tally.get('Q_AMBIGUOUS',0),tally.get('REJECT',0),pp,fa,sp,kb_ad))
