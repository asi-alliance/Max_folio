import sys
lines = open('/home/mettaclaw/artifacts/fc_iterN_v17.sh').readlines()
a1 = open('/home/mettaclaw/artifacts/abd_pass1.txt').read().strip()
i1 = open('/home/mettaclaw/artifacts/ind_pass1.txt').read().strip()
a2 = open('/home/mettaclaw/artifacts/abd_derpass.txt').read().strip()
i2 = open('/home/mettaclaw/artifacts/ind_derpass.txt').read().strip()
new = lines[:16] + [a1+'\n', i1+'\n'] + lines[16:]
new = new[:24] + [a2+'\n', i2+'\n'] + new[24:]
open('/home/mettaclaw/artifacts/fc_iterN_v18.sh','w').writelines(new)
print('v18 written, lines:', len(new))