import json, os, time, sys

ARTIFACTS = '/home/mettaclaw/artifacts'
KB_PATH = os.path.join(ARTIFACTS, 'agent_kb.json')
TRIGGER_PATH = '/tmp/agent_cycle_count.json'
sys.path.insert(0, ARTIFACTS)

from g162_agent_adapter import run_pipeline

def _load_trigger():
    data = {'count': 0, 'last_run': 0}
    if os.path.exists(TRIGGER_PATH):
        with open(TRIGGER_PATH) as f:
            data = json.load(f)
    return data

def _save_trigger(data):
    with open(TRIGGER_PATH, 'w') as f:
        json.dump(data, f)

def check_trigger(every_n=50, every_sec=300):
    data = _load_trigger()
    data['count'] = data.get('count', 0) + 1
    now = time.time()
    by_count = data['count'] % every_n == 0
    by_time = (now - data.get('last_run', 0)) > every_sec
    fire = by_count or by_time
    triggered_by = None
    if fire:
        triggered_by = 'count' if by_count else 'time'
        data['last_run'] = now
    _save_trigger(data)
    return fire, triggered_by

def agent_hook(seed=None):
    fire, reason = check_trigger()
    if not fire:
        return None
    result = run_pipeline(seed=seed)
    result['triggered_by'] = reason
    return result

if __name__ == '__main__':
    r = agent_hook()
    print('RESULT:', r)
