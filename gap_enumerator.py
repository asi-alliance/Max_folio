import re
from itertools import combinations
f=open('/home/mettaclaw/artifacts/persistent_atoms.metta')
lines=f.readlines()
f.close()
subjects=set()
predicates=set()
sp_map={}
ps_map={}
for line in lines:
 line=line.strip()
 if not line: continue
 m=re.match(r'\(\(-->\s+(\S+)\s+(\S+)\)\s+\(stv',line)
 if m:
  s,p=m.group(1),m.group(2)
  subjects.add(s)
  predicates.add(p)
  sp_map.setdefault(s,set()).add(p)
  ps_map.setdefault(p,set()).add(s)
print(f'SUBJECTS: {len(subjects)}')
print(f'PREDICATES: {len(predicates)}')
for p in sorted(ps_map):
 if len(ps_map[p])>1: print(f'  {p} <- {ps_map[p]} [CLUSTER]')
print('ANOMALY PAIRS:')
count=0
for a,b in combinations(sorted(subjects),2):
 shared=sp_map.get(a,set())&sp_map.get(b,set())
 ded=bool(sp_map.get(a,set())&{b}) or bool(sp_map.get(b,set())&{a})
 if not shared and not ded:
  count+=1
  print(f'  [{count}] ({a},{b})')
print(f'Total: {count}')