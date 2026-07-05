import json, os, sys, time

ARTIFACTS = '/home/mettaclaw/artifacts'
KB_PATH = os.path.join(ARTIFACTS, 'agent_kb.json')
TRIGGER_PATH = '/tmp/agent_cycle_count.json'
sys.path.insert(0, ARTIFACTS)
from topk_filter import topk_filter

from g160_v28_pipeline import (pair_gen, classify_pair,
    generate_candidates, infer_candidates, inject_conclusions, parse_conclusions, parse_kb)

def load_kb():
    if os.path.exists(KB_PATH):
        with open(KB_PATH) as f:
            return [tuple(a) for a in json.load(f)]
    return []

def save_kb(atoms):
    with open(KB_PATH, 'w') as f:
        json.dump([list(a) for a in atoms], f, indent=2)

def check_trigger(every_n=50):
    data = {'count': 0, 'last_run': 0}
    if os.path.exists(TRIGGER_PATH):
        with open(TRIGGER_PATH) as f:
            data = json.load(f)
    data['count'] = data.get('count', 0) + 1
    fire = data['count'] % every_n == 0
    if fire:
        data['last_run'] = time.time()
    with open(TRIGGER_PATH, 'w') as f:
        json.dump(data, f)
    return fire

def run_pipeline(seed=None):
    atoms = load_kb()
    if seed:
        exist = {(s, p) for s, p, *_ in atoms}
        for a in seed:
            if (a[0], a[1]) not in exist:
                atoms.append(tuple(a))
    initial = len(atoms)
    for i in range(5):
        pairs = pair_gen(atoms)
        existing = {(a[0],a[1]) for a in atoms}
        classified = [(a,b,r[0]) for a,b in pairs for r in [classify_pair(a,b)] if r and r[1] not in existing]
        classified = topk_filter(classified)
        cands = generate_candidates(pairs)
        new_atoms = infer_candidates(classified, atoms)
        new_atoms = parse_conclusions(new_atoms)
        before = len(atoms)
        inject_conclusions(atoms, new_atoms)
        if len(atoms) == before:
            break
    save_kb(atoms)
    return {'initial': initial, 'final': len(atoms),
            'iterations': i+1, 'new': len(atoms)-initial}

if __name__ == '__main__':
    seed = [('bird', 'animal', 1.0, 0.9), ('robin', 'bird', 1.0, 0.9),
            ('penguin', 'bird', 1.0, 0.9), ('penguin', 'flies', 0.0, 0.9)]
    print(run_pipeline(seed))

def run_from_file(path):
    kb = parse_kb(open(path).read())
    return run_pipeline(seed=list(kb))
