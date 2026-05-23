#!/usr/bin/env python3
import subprocess, sys, datetime

def run(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr, r.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -1

tests = [
    ("nal_invoke_help", "python3 /home/mettaclaw/scripts/nal_invoke_v3.py", "command", 10),
    ("insert_belief", "python3 /home/mettaclaw/scripts/insert_belief.py robin bird 1.0 0.9", "revis", 10),
    ("claim_evaluator", "python3 /home/mettaclaw/scripts/claim_evaluator.py", "acc_exp", 10),
    ("auto_chainer", "python3 /home/mettaclaw/scripts/auto_chainer.py", "step", 10),
    ("nal_deduce", "python3 /home/mettaclaw/scripts/nal_invoke_v3.py deduce '(--> robin bird)' '(stv 1.0 0.9)' '(--> bird animal)' '(stv 1.0 0.9)'", "robin animal", 10),
    ("cert_e2e_real_trace", "python3 /home/mettaclaw/artifacts/e2e_real_trace.py", "tracker report", 30),
    ("cert_ambiguity_forced", "python3 /home/mettaclaw/artifacts/ambiguity_forced_trace.py", "all phases complete", 30),
]

stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
passed = 0
for entry in tests:
    name, cmd, expect = entry[0], entry[1], entry[2]
    to = entry[3] if len(entry) > 3 else 30
    out, rc = run(cmd, timeout=to)
    ok = expect.lower() in out.lower() and rc == 0
    status = "PASS" if ok else "FAIL"
    if ok: passed += 1
    print(f"{status}: {name} (rc={rc})")
    if not ok:
        print(f"  expect='{expect}' in output={bool(expect.lower() in out.lower())} rc={rc}")
        print(f"  last100={out[-100:] if out else 'EMPTY'}")

print(f"\n[{stamp}] RESULT: {passed}/{len(tests)} PASS")
sys.exit(0 if passed == len(tests) else 1)