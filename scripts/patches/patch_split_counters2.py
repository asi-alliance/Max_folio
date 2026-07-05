import sys
Q = chr(39)
p = '/home/mettaclaw/artifacts/quarantine_tracker_v05.py'
lines = open(p).readlines()
out = []
old_init = 'self.false_admit_count = 0'
old_inc = 'self.false_admit_count += 1'
old_rpt = 'false_admit_count=self.false_admit_count,'
for L in lines:
    if old_init in L and 'live' not in L:
        out.append(L.replace(old_init, 'self.false_admit_count_live = 0'))
        out.append(L.replace(old_init, 'self.false_admit_count_test = 0'))
    elif old_inc in L and 'live' not in L:
        sp = L[:len(L)-len(L.lstrip())]
        out.append(sp + 'if test_mode:' + chr(10))
        out.append(sp + '    self.false_admit_count_test += 1' + chr(10))
        out.append(sp + 'else:' + chr(10))
        out.append(sp + '    self.false_admit_count_live += 1' + chr(10))
    elif old_rpt in L and 'live' not in L:
        sp = L[:len(L)-len(L.lstrip())]
        out.append(sp + 'false_admit_count_live=self.false_admit_count_live,' + chr(10))
        out.append(sp + 'false_admit_count_test=self.false_admit_count_test,' + chr(10))
    else:
        out.append(L)
open(p, 'w').writelines(out)
print('PATCHED OK lines:', len(out))