import re, sys

ROUNDS = [
  {'name':'R1 Deduction','metta':'(|- ((--> robin bird) (stv 1.0 0.9)) ((--> bird animal) (stv 0.9 0.9)))','exp_f':0.9,'exp_c':0.729,'pts':2},
  {'name':'R2 Abduction','metta':'(|- ((--> animal mortal) (stv 1.0 0.9)) ((--> sam mortal) (stv 0.8 0.9)))','exp_f':0.8,'exp_c':0.4475,'pts':3},
  {'name':'R3 Revision','metta':'(|- ((--> cat friendly) (stv 0.9 0.8)) ((--> cat friendly) (stv 0.3 0.9)))','exp_f':0.485,'exp_c':0.929,'pts':3},
  {'name':'R4 Conditional','metta':'(|- ((==> (--> $1 bird) (--> $1 fly)) (stv 0.8 0.9)) ((--> penguin bird) (stv 1.0 0.9)))','exp_f':0.8,'exp_c':0.648,'pts':4},
  {'name':'R5 Chain','metta':'(|- ((--> dog mammal) (stv 0.95 0.9)) ((--> mammal animal) (stv 1.0 0.9)))','exp_f':0.95,'exp_c':0.7695,'pts':4},
]

def parse_stv(text):
    m=re.search(r'stv\s+([\d.]+)\s+([\d.]+)',text)
    if m: return float(m.group(1)),float(m.group(2))
    return None,None

def score(r,af,ac):
    fe=abs(r['exp_f']-af); ce=abs(r['exp_c']-ac)
    if fe<0.01 and ce<0.05: return r['pts']
    if fe<0.05 and ce<0.1: return r['pts']//2
    return 0

print('Event 1 Syllogism Sprint - Harness v0.2')
print('='*50)
tot=0; mx=0
for r in ROUNDS:
    mx+=r['pts']
    s=score(r,r['exp_f'],r['exp_c'])
    tot+=s
    print(f"  {r['name']}: {s}/{r['pts']} pts")
print(f"Total: {tot}/{mx} (self-test)")