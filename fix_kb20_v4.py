import ospath = '/home/mettaclaw/scripts/test_kb_20.nal'
f = open(path, 'r')
lines = f.readlines()
f.close()
cleaned = []
for line in lines:
if line.strip() == 'dummy':
continue
if ')(-->' in line:
