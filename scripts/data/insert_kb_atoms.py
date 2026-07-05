import sys
p = '/home/mettaclaw/artifacts/unified_fc_bc_v4_scale.metta'
lines = open(p).readlines()
new_atoms = [
    '!(add-atom &self ((--> eagle bird) (stv 0.95 0.9)))\n',
    '!(add-atom &self ((--> penguin bird) (stv 0.8 0.9)))\n',
    '!(add-atom &self ((--> penguin swimmer) (stv 0.95 0.9)))\n',
    '!(add-atom &self ((--> shark fish) (stv 0.9 0.9)))\n',
    '!(add-atom &self ((--> fish animal) (stv 0.95 0.9)))\n',
    '!(add-atom &self ((--> whale mammal) (stv 0.95 0.9)))\n',
    '!(add-atom &self ((--> mammal animal) (stv 0.95 0.9)))\n',
    '!(add-atom &self ((--> dolphin mammal) (stv 0.9 0.9)))\n',
    '!(add-atom &self ((--> swimmer aquatic) (stv 0.9 0.9)))\n',
    '!(add-atom &self ((--> aquatic living) (stv 0.9 0.9)))\n',
]
last_kb = -1
for i, L in enumerate(lines):
    if 'add-atom' in L and '-->' in L:
        last_kb = i
if last_kb == -1:
    print('ERROR: no KB atoms found'); sys.exit(1)
out = lines[:last_kb+1] + new_atoms + lines[last_kb+1:]
open(p, 'w').writelines(out)
print(f'INSERTED OK, total lines: {len(out)}, add-atom count: {sum(1 for x in out if "add-atom" in x)}')