import subprocess, re, sys, os, tempfile

PETTA_DIR = '/home/mettaclaw/DEPLOYMENT2_OpenAI_LLM/PeTTa'

ROUNDS = [
  {'name':'R1 Deduction','metta':'(|- ((--> robin bird) (stv 1.0 0.9)) ((--> bird animal) (stv 0.9 0.9)))','exp_f':0.9,'exp_c':0.729,'pts':2},
  {'name':'R2 Abduction','metta':'(|- ((--> animal mortal) (stv 1.0 0.9)) ((--> sam mortal) (stv 0.8 0.9)))','exp_f':0.8,'exp_c':0.4475,'pts':3},
  {'name':'R3 Revision','metta':'(|- ((--> cat friendly) (stv 0.9 0.8)) ((--> cat friendly) (stv 0.3 0.9)))','exp_f':0.485,'exp_c':0.929,'pts':3},
  {'name':'R4 Conditional','metta':'(|- ((==> (--> $1 bird) (--> $1 fly)) (stv 0.8 0.9)) ((--> penguin bird) (stv 1.0 0.9)))','exp_f':0.8,'exp_c':0.648,'pts':4},
  {'name':'R5 Chain','metta':'(|- ((--> dog mammal) (stv 0.95 0.9)) ((--> mammal animal) (stv 1.0 0.9)))','exp_f':0.95,'exp_c':0.7695,'pts':4},
]

def parse_stv(text):
    text = re.sub(r'\x1b\[[\d;*]*m', '', text)
    m = re.search(r'stv\s+([\d.]+)\s+([\d.]+)', text)
    if m: return float(m.group(1)), float(m.group(2))
    return None, None

def run_metta(expr):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.metta', dir=PETTA_DIR, delete=False) as f:
        f.write('!(' + expr + ')\n')
        tmp = f.name
    try:
        r = subprocess.run(['sh', 'run.sh', tmp], capture_output=True, text=True,
                           cwd=PETTA_DIR, timeout=30, stdin=subprocess.DEVNULL)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return 'TIMEOUT'
    finally:
        os.unlink(tmp)

def score(r, af, ac):
    if af is None or ac is None: return 0
    fe = abs(r['exp_f'] - af); ce = abs(r['exp_c'] - ac)
    if fe < 0.01 and ce < 0.05: return r['pts']
    if fe < 0.05 and ce < 0.1: return r['pts'] // 2
    return 0

def main():
    print('Event 1 Syllogism Sprint - Auto-Harness v0.3')
    print('=' * 50)
    tot = 0; mx = 0
    for r in ROUNDS:
        mx += r['pts']
        print(f"  {r['name']}: running...", end=' ')
        out = run_metta(r['metta'])
        af, ac = parse_stv(out)
        s = score(r, af, ac)
        tot += s
        print(f"got f={af} c={ac} exp f={r['exp_f']} c={r['exp_c']} -> {s}/{r['pts']} pts")
    print(f"Total: {tot}/{mx}")
    return tot == mx

if __name__ == '__main__':
    ok = main()
    sys.exit(0 if ok else 1)