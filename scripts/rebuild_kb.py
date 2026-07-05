import re,json
lines=open("/home/mettaclaw/artifacts/agent_kb.nal").readlines()
atoms=[];[atoms.append([m.group(1),m.group(2),float(m.group(3)),float(m.group(4))]) for l in lines for m in [re.search(r"\(--> (\S+) (\S+)\) \(stv ([\d.]+) ([\d.]+)\)",l)] if m]
import json
json.dump(atoms,open("/home/mettaclaw/artifacts/agent_kb.json","w"))
print("REBUILT:",len(atoms),"atoms")
subjs=sorted(set(s for s,p,f,c in atoms))
print("SUBJECTS:",len(subjs),subjs)
