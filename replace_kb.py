import sys
path = '/home/mettaclaw/artifacts/fc_iterN_v4.sh'
lines = open(path).readlines()
new_kb = [
  '!(add-atom &self ((--> robin bird) (stv 1.0 0.9)))\n',
  '!(add-atom &self ((--> bird animal) (stv 1.0 0.9)))\n',
  '!(add-atom &self ((--> robin pet) (stv 1.0 0.9)))\n',
  '!(add-atom &self ((--> pet animal) (stv 0.8 0.9)))\n',
  '!(add-atom &self ((--> animal living) (stv 1.0 0.9)))\n',
]
lines[9:15] = new_kb
open(path, 'w').writelines(lines)
print('KB replaced OK, lines:', len(lines))
