import sys, re, subprocess, json

CHECKER = "/home/mettaclaw/artifacts/aabc_self_check_v2.py"

def extract_freq(s):
    m = re.search(r'stv\s+([\d.]+)\s+([\d.]+)', s)
    return float(m.group(1)) if m else None

def extract_conf(s):
    m = re.search(r'stv\s+([\d.]+)\s+([\d.]+)', s)
    return float(m.group(2)) if m else None

def bridge(code, stv_old, stv_new):
    f1 = extract_freq(stv_old)
    f2 = extract_freq(stv_new)
    c1 = extract_conf(stv_old)
    c2 = extract_conf(stv_new)
    if any(x is None for x in [f1,f2,c1,c2]):
        print("PARSE_FAIL")
        return
    revised = (f1*c1 + f2*c2) / (c1+c2)
    print(f"{code}: {f1:.3f} x {f2:.3f} -> revised {revised:.4f}")
    subprocess.run(["python3", CHECKER, code, str(round(revised, 4))])

if __name__ == "__main__":
    if len(sys.argv) == 4:
        bridge(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: bridge.py CODE stv_old stv_new")
