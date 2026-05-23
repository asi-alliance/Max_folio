import re,sys,shutil,datetime
from pathlib import Path

F=Path("/home/mettaclaw/artifacts/persistent_atoms.metta")
def parse(l):
    l=l.strip()
    if not l: return None,None,None
    m=re.search(r'\(stv\s+([\d.]+)\s+([\d.]+)\)',l)
    if not m: return l,None,None
    f,c=float(m.group(1)),float(m.group(2))
    t=re.sub(r'\(stv\s+[\d.]+\s+[\d.]+\)','',l).strip()
    return re.sub(r'\s+',' ',t),f,c
def compact():
    if not F.exists():
        print("No atom file found.");return
    lines=F.read_text().strip().splitlines()
    best={}
    for ln in lines:
        t,f,c=parse(ln)
        if t is None:continue
        if c is None:
            best.setdefault(t,ln);continue
        if t not in best or c>best[t][1]:best[t]=(f,c,ln)
    import shutil;ts=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy(F,F.parent/f"persistent_atoms_backup_{ts}.metta")
    with open(F,"w") as o:
        for v in best.values():o.write((v[2] if isinstance(v,tuple) else v)+"\n")
    print(f"Compacted: {len(lines)} -> {len(best)} atoms")

if __name__=="__main__":
    compact()
