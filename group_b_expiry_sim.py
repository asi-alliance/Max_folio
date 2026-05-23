import sys
sys.path.insert(0,'/home/mettaclaw/artifacts')
from stress_test_v04b import gen_scaled_kb
from cert_layer_v04 import certify
from collections import defaultdict

kb = gen_scaled_kb(500, seed=42)
tm = defaultdict(list)
for b in kb:
    tm[b['term']].append(b)

group_b = []
for b in kb:
    vA, _, _ = certify(b['f'], b['c'], depth=0)
    vB, _, _ = certify(b['f'], b['c'], depth=b['depth'])
    if vA.name == 'REJECT' and vB.name == 'QUARANTINE':
        partners = [p for p in tm[b['term']] if p['id'] != b['id']]
        if len(partners) == 0:
            group_b.append(b)

print(f'Group B solo beliefs: {len(group_b)}')
max_hold = 50
for b in group_b:
    reg_cycle = 3963
    expire_cycle = reg_cycle + max_hold
    print(f"  {b['band']} {b['term']} f={b['f']:.3f} c={b['c']:.3f} expires_at={expire_cycle}")
print(f'All {len(group_b)} solo beliefs expire at cycle {3963+max_hold} with no revision possible')