import sys;p="/home/mettaclaw/artifacts/quarantine_tracker_v05.py";lines=open(p).readlines();out=[];i=0
while i<len(lines):
    L=lines[i]
    if "self.false_admit_count = 0" in L and "live" not in L:
        out.append(L.replace("self.false_admit_count = 0","self.false_admit_count_live = 0"))
        out.append(L.replace("self.false_admit_count = 0","self.false_admit_count_test = 0"))
    elif "self.false_admit_count += 1" in L and "live" not in L:
        indent=L[:len(L)-len(L.lstrip())]
        out.append(indent+"if test_mode:
")
        out.append(indent+"    self.false_admit_count_test += 1
")
        out.append(indent+"else:
")
        out.append(indent+"    self.false_admit_count_live += 1
")
    elif "false_admit_count=self.false_admit_count," in L and "live" not in L:
        indent=L[:len(L)-len(L.lstrip())]
        out.append(indent+"false_admit_count_live=self.false_admit_count_live,
")
        out.append(indent+"false_admit_count_test=self.false_admit_count_test,
")
    else:
        out.append(L)
    i+=1
open(p,"w").writelines(out)
print("PATCHED OK, lines:",len(out))