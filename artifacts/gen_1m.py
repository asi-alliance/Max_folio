import random, os
random.seed(42)
N = 1000000
path = '/home/mettaclaw/artifacts/mork_1m_facts.mm2'
f = open(path, 'w')
for i in range(N):
    a = 'e' + str(random.randint(0, 99999))
    b = 'e' + str(random.randint(0, 99999))
    f.write('(edge ' + a + ' ' + b + ')
')
f.close()
sz = os.path.getsize(path)
print('Generated ' + str(N) + ' facts, ' + str(round(sz/1048576, 1)) + ' MB')
