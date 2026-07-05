import math,json
from collections import defaultdict

def hellinger(f1,f2):
    return math.sqrt(0.5*((math.sqrt(f1)-math.sqrt(f2))**2+(math.sqrt(1-f1)-math.sqrt(1-f2))**2))

def kb_coherence_v4(kb_path=None,atoms=None):
    if atoms is None:
        atoms=json.load(open(kb_path))
    groups=defaultdict(list)
    for s,p,f,c in atoms:
        groups[(s,p)].append((f,c))
    conflicts=[]
    for key,vals in groups.items():
        if len(vals)>1:
            for i in range(len(vals)):
                for j in range(i+1,len(vals)):
                    h=hellinger(vals[i][0],vals[j][0])
                    conflicts.append((key,vals[i],vals[j],h))
    worst=max((c[3] for c in conflicts),default=0.0)
    return conflicts,worst

if __name__=='__main__':
    c,w=kb_coherence_v4(kb_path='/home/mettaclaw/artifacts/agent_kb.json')
    print(f'Conflicts: {len(c)}, Worst: {w:.4f}')
    for x in c: print(x)