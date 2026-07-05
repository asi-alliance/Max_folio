import re, subprocess, os, sys, math, itertools

# g160 v27 Unified Meta-Rule Discovery Pipeline
# Stages: parse_kb -> pair_gen -> classify -> novel_extract -> search

V25_PATH = '/tmp/g160_v25_test.metta'
PETTA_DIR = '/home/mettaclaw/DEPLOYMENT2_OpenAI_LLM/PeTTa'
SEARCHER_PATH = '/home/mettaclaw/artifacts/meta_rule_searcher_v3.py'

# --- Stage 1: Parse KB atoms ---
def parse_kb(metta_text):
    pat = re.compile('\(-->\s+(\w+)\s+(\w+)\)\s*(?:\(stv\s+([\d.]+)\s+([\d.]+)\))?')
    atoms = []
    for line in metta_text.split('\n'):
        if line.strip().startswith(';'): continue
        for m in pat.finditer(line):
            atoms.append((m.group(1), m.group(2), float(m.group(3) or 1.0), float(m.group(4) or 0.9)))
    return list(set(atoms))

# --- Stage 2: Generate unique pairs with frozenset dedup ---
def pair_gen(atoms):
    seen = set()
    pairs = []
    for a, b in itertools.permutations(atoms, 2):
        key = frozenset([a, b])
        if key in seen: continue
        seen.add(key)
        # Canonical order: P1.subject <= P2.subject lexicographically
        if a[0] <= b[0]:
            pairs.append((a, b))
        else:
            pairs.append((b, a))
    return pairs

# --- Stage 3: Classify via PeTTa subprocess ---
def classify_pair(p1, p2, v25_path=None):
    s1, p1p = p1[:2]
    s2, p2p = p2[:2]
    if p1p == s2:
        return ("deduction", (s1, p2p))
    elif p1p == p2p:
        return ("abduction", (s2, s1))
    elif s1 == s2:
        return ("induction", (p1p, p2p))
    elif p2p == s1:
        return ("deduction", (s2, p1p))
    elif p2p == p1p:
        return ("abduction", (s1, s2))
    elif s2 == s1:
        return ("induction", (p2p, p1p))
    else:
        return ("novel", None)

def find_novel(atoms):
    pairs = pair_gen(atoms)
    known = {'deduction', 'abduction', 'induction'}
    novel = []
    for p1, p2 in pairs:
        result = classify_pair(p1, p2)
        if result and not any(k in result for k in known):
            novel.append((p1, p2, result))
    return novel

def generate_candidates(pairs):
    candidates = []
    for p1, p2 in pairs:
        t1 = set(p1[:2]) if isinstance(p1,tuple) else set(p1.replace("(","").replace(")","").split())
        t2 = set(p2[:2]) if isinstance(p2,tuple) else set(p2.replace("(","").replace(")","").split())
        shared = t1 & t2 - {"-->", "Inheritance", "stv"}
        uniq1 = t1 - t2 - {"-->", "Inheritance", "stv"}
        uniq2 = t2 - t1 - {"-->", "Inheritance", "stv"}
        if shared and uniq1 and uniq2:
            s = list(shared)[0]
            u1 = list(uniq1)[0]
            u2 = list(uniq2)[0]
            candidates.append((s, u1, u2))
    return candidates

# --- Main ---
import subprocess, os, tempfile


import subprocess, tempfile, os, re

def infer_candidates(classified, atoms, v20_path="/home/mettaclaw/artifacts/fc_iterN_v20_autostop.sh"):
    seen = set()
    for p1, p2, rtype in classified:
        seen.add((p1[0], p1[1], p1[2], p1[3]))
        seen.add((p2[0], p2[1], p2[2], p2[3]))
    for s, p, fc, cc in atoms:
        seen.add((s, p, fc, cc))
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".metta", delete=False)
    for s, p, fc, cc in seen:
        tmp.write(f"((--> {s} {p}) (stv {fc} {cc}))"+"\n")
    tmp.close()
    try:
        out = subprocess.run(["bash", v20_path, "10", tmp.name, "none", "none"], capture_output=True, text=True, timeout=120)
        raw = re.sub(r"\x1b\[[0-9;]*m", "", out.stdout)
        matches = re.findall(r"\(\(--> \S+ \S+\) \(stv[\s0-9.]+\)\)", raw)
        output_str = "; ".join(matches) if matches else "no stv match"
        results = [(("batch","batch",1.0,1.0),("batch","batch",1.0,1.0),"batch_fc", output_str)]
        return results
    except Exception as e:
        print(f"ERROR: {e}")
        return []
    finally:
        os.unlink(tmp.name)



def parse_conclusions(inferred):
    new_atoms = []
    for p1, p2, rtype, output in inferred:
        found = re.findall(r'-->\s+(\S+)\s+(\S+)\).*?stv\s+([\d.]+)\s+([\d.]+)', output)
        for s, p, f, c in found:
            new_atoms.append((s, p, float(f), float(c)))
    return new_atoms

def nal_revision(f1, c1, f2, c2):
    w1 = c1 / (1 - c1) if c1 < 1.0 else 999
    w2 = c2 / (1 - c2) if c2 < 1.0 else 999
    ws = w1 + w2
    f_rev = (w1 * f1 + w2 * f2) / ws if ws > 0 else f1
    c_rev = ws / (ws + 1)
    return f_rev, c_rev

def inject_conclusions(atoms, new_atoms):
    idx_map = {}
    for i, a in enumerate(atoms):
        idx_map[(a[0], a[1])] = i
    added = 0
    revised = 0
    for s, p, f, c in new_atoms:
        if s == p: continue
        if c < 0.2: continue
        if (s, p) in idx_map:
            i = idx_map[(s, p)]
            old = atoms[i]
            if len(old) >= 4 and (abs(old[2] - f) > 1e-6 or abs(old[3] - c) > 1e-6):
                f_r, c_r = nal_revision(old[2], old[3], f, c)
                atoms[i] = (s, p, f_r, c_r)
                revised += 1
        else:
            atoms.append((s, p, f, c))
            idx_map[(s, p)] = len(atoms) - 1
            added += 1
    if revised > 0:
        print(f"  Revision-merged {revised} existing atoms")
    return added
if __name__ == '__main__':
    test_kb = '''
    (= (-->srobin bird) True)
    (= (-->sbird animal) True)
    (= (-->spenguin bird) True)
    (= (-->srobin flyer) True)
    '''
    atoms = parse_kb(test_kb)
    print(f'Parsed {len(atoms)} atoms: {atoms}')
    for iteration in range(3):
        print(f"\n==== Iteration {iteration+1} ====")
        pairs = pair_gen(atoms)
        print(f'Generated {len(pairs)} unique pairs')
        for p1, p2 in pairs:
            print(f'  P1=(-->s{p1[0]} {p1[1]}) P2=(-->s{p2[0]} {p2[1]})')
        print('\nClassifying pairs via PeTTa...')
        classified = []
        for p1, p2 in pairs[:10]:
            try:
                r = classify_pair(p1, p2)
                print(f'  (-->s{p1[0]} {p1[1]}) + (-->s{p2[0]} {p2[1]}) -> {r}')
                if r[0] in ('deduction','abduction','induction'): classified.append((p1,p2,r[0]))
            except Exception as e:
                print(f'  ERROR: {e}')
    
        print()
        print("Stage 4: Novel pair extraction...")
        novel = find_novel(atoms)
        print(f"  Found {len(novel)} novel pairs")
        print()
        print("Stage 5: Candidate generation...")
        cands = generate_candidates([(p1,p2) for p1,p2,t in classified])
        for c in cands:
            print(f"  candidate: {c}")
        print("Stage 6: METTa NAL inference...")
        inferred = infer_candidates(classified, atoms)
        print("Stage 7: Feedback loop...")
        new_atoms = parse_conclusions(inferred)
        added = inject_conclusions(atoms, new_atoms)
        print(f"  Parsed {len(new_atoms)} conclusions, injected {added} new atoms, KB now {len(atoms)}")
        if added == 0:
            print("  Fixpoint reached, no new atoms.")
            break
    print(f"  {len(inferred)} inferences executed")
