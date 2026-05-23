import sys, re, os
os.sys.path.insert(0, '/home/mettaclaw/artifacts')
from cert_layer_v02 import cert_layer_v02

pat = re.compile('derived ([0-9]+) [(][(](--> ([^ )]+) ([^ )]+))[)] [(]stv ([0-9.]+) ([0-9.]+)[)][)]')
admitted = []
for line in sys.stdin:
    m = pat.search(line)
    if not m:
        continue
    depth = int(m.group(1))
    rel = m.group(2)
    subj, pred = m.group(3), m.group(4)
    f, c = float(m.group(5)), float(m.group(6))
    r = cert_layer_v02(f, c, chain_len=depth, sim=0.5, social_hops=0)
    v = r['verdict']
    margin = r['composite_margin']
    nearest = r['nearest_boundary']
    tag = f'[{v} m={margin} near={nearest}]'
    if v == 'ADMIT':
        print(f'(= (kb-add) (add-atom &self (({rel}) (stv {f} {c}))))')
        admitted.append((rel, f, c, tag))
    else:
        print(f'; FILTERED {tag}: ({rel}) (stv {f} {c})', file=sys.stderr)
print(f'; === {len(admitted)} atoms admitted ===', file=sys.stderr)
