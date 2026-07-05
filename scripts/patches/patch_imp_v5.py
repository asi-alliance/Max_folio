import sys
p = '/home/mettaclaw/artifacts/unified_fc_bc_v4_scale.metta'
lines = open(p).readlines()

# Find where to insert: after ind-tv def line
ins_tv = None
for i, L in enumerate(lines):
    if 'ind-tv' in L and '= (ind-tv' in L:
        ins_tv = i + 1

if ins_tv is None:
    print('ERROR: could not find ind-tv line'); sys.exit(1)

# Insert imp-ded-tv function after ind-tv
imp_tv = ['; NAL-5 conditional deduction (modus ponens)\n',
          '(= (imp-ded-tv ($f1 $c1) ($f2 $c2)) (stv (* $f1 $f2) (* (* $f1 $c1) (* $f2 $c2))))\n']

# Find FC Pass 1 header and insert imp pass after induction pass
fc1_ind = None
for i, L in enumerate(lines):
    if 'fc-ind 1' in L and 'map-atom' in L:
        fc1_ind = i + 1

if fc1_ind is None:
    print('ERROR: could not find fc-ind 1 pass'); sys.exit(1)

# FC imp pass 1: match (==> A B)(stv) + (A stv) -> derive (B stv)
imp_pass = ['; NAL-5 modus ponens FC pass\n',
            '!(map-atom (unique-atom (collapse (match &self ((==> $A $B) (stv $f1 $c1)) (match &self ($A (stv $f2 $c2)) (let $tv (imp-ded-tv ($f1 $c1) ($f2 $c2)) (fc-imp 1 ($B $tv))))))) $x persist $x))\n']

# Add test ==> KB atoms after last add-atom
last_kb = -1
for i, L in enumerate(lines):
    if 'add-atom' in L:
        last_kb = i

imp_kb = ['; NAL-5 test implications\n',
          '!(add-atom &self ((==> bird flyer) (stv 0.9 0.9)))\n',
          '!(add-atom &self ((==> flyer mobile) (stv 0.85 0.9)))\n',
          '!(add-atom &self (bird (stv 1.0 0.9)))\n']

# Apply in reverse order to preserve line indices
out = lines[:]
# 1. Insert imp-tv after ind-tv
out = out[:ins_tv] + imp_tv + out[ins_tv:]
# Adjust offsets
off1 = len(imp_tv)

# 2. Insert imp KB after last add-atom
adj_kb = last_kb + off1
out = out[:adj_kb+1] + imp_kb + out[adj_kb+1:]
off2 = off1 + len(imp_kb)

# 3. Insert imp FC pass after fc-ind 1
adj_fc1 = fc1_ind + off2
out = out[:adj_fc1+1] + imp_pass + out[adj_fc1+1:]

open(p, 'w').writelines(out)
print(f'PATCHED: {len(out)} lines. Added imp-ded-tv, 3 imp KB atoms, FC imp pass.')