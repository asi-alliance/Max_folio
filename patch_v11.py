import sys
with open('/home/mettaclaw/artifacts/fc_iterN_v10b.sh') as f: lines = f.read().split('\n')
out = []
for i, line in enumerate(lines):
    out.append(line)
    if line.startswith('(= (ded-tv'):
        out.append('(= (abd-tv ($f1 $c1) ($f2 $c2)) (let $w (* $f1 $c1 $c2) (stv $f2 (/ $w (+ $w 1)))))')
        out.append('(= (ind-tv ($f1 $c1) ($f2 $c2)) (let $w (* $f2 $c1 $c2) (stv $f1 (/ $w (+ $w 1)))))')
    if 'map-atom' in line and 'ded-tv' in line and 'PREVNUM' not in line:
        out.append(line.replace('ded-tv','abd-tv'))
        out.append(line.replace('ded-tv','ind-tv'))
    if 'map-atom' in line and 'ded-tv' in line and 'PREVNUM' in line:
        out.append(line.replace('ded-tv','abd-tv'))
        out.append(line.replace('ded-tv','ind-tv'))
with open('/home/mettaclaw/artifacts/fc_iterN_v11.sh','w') as f: f.write('\n'.join(out))
print('v11 written:', len(out), 'lines')
