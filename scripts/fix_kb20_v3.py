import ospath = '/home/mettaclaw/scripts/test_kb_20.nal'
f = open(path, 'r')
data = f.read()
f.close()
data = data.replace('dummy
', '')
data = data.replace('0.85)(-->', '0.85)
(-->')
f = open(path, 'w')
f.write(data)
f.close()
print('DONE')
