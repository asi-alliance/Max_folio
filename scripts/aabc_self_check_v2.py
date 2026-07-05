import json, os, sys

DATA_FILE = '/home/mettaclaw/data/aabc_disorder_rates.json'

DEFAULTS = {
    'AABC-605': {'name': 'format-perseveration', 'freq': 0.3, 'conf': 0.7, 'action': 'STOP: check if repeating same syntax fix'},
    'AABC-609': {'name': 'attention-fragmentation', 'freq': 0.2, 'conf': 0.75, 'action': 'STOP: refocus on pinned goal'},
    'AABC-610': {'name': 'tool-task-mismatch', 'freq': 0.15, 'conf': 0.8, 'action': 'STOP: line task or block task?'}
}

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return DEFAULTS.copy()

def save(d):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(d, f, indent=2)

def check():
    d = load()
    alerts = []
    for k, v in d.items():
        if v['freq'] > 0.5:
            alerts.append(f"ALERT {k} {v['name']}: freq={v['freq']:.2f} -> {v['action']}")
    if alerts:
        print('AABC SELF-MONITOR TRIGGERED:')
        for a in alerts: print(f'  {a}')
    else:
        print(f'AABC self-check CLEAR: {len(d)} disorders below threshold')
    return alerts

def update_freq(code, new_freq):
    d = load()
    if code in d:
        old = d[code]['freq']
        d[code]['freq'] = round(new_freq, 3)
        save(d)
        print(f'{code}: freq {old:.3f} -> {new_freq:.3f}')

if __name__ == '__main__':
    if len(sys.argv) > 2:
        update_freq(sys.argv[1], float(sys.argv[2]))
    else:
        check()
