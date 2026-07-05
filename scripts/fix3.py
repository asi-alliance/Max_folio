import re
with open('/home/mettaclaw/artifacts/md2html_v4.py','r') as f: L=f.readlines()
for i in [19,20,21]:
    L[i]=L[i].replace(chr(92)+'1',chr(92)+chr(92)+'1')
with open('/home/mettaclaw/artifacts/md2html_v4.py','w') as f: f.writelines(L)
print('patched')
