import os
path = "/home/mettaclaw/scripts/test_kb_20.nal"
f = open(path, 'r')
data = f.read()
f.close()
idx = data.find('0.85)(-->')
part1 = data[:idx+5] + chr(10) + data[idx+5:]
result = part1.replace('dummy' + chr(10), '')
f = open(path, 'w'); f.write(result); f.close()
print('DONE lines=' + str(result.count(chr(10))))
