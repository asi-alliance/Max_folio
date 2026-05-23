import sys, os
sys.path.insert(0, '/home/mettaclaw/scripts')
from agent_cycle_trigger import check_trigger
from g180_unified_loop import phase3_run_pipeline

def cycle_entry():
    if check_trigger():
        result = phase3_run_pipeline()
        if result and result.get('alerts'):
            print('ALERTS:', result['alerts'])
        return result
    return None

if __name__ == '__main__':
    r = cycle_entry()
    if r:
        na = r.get('new_atoms', [])
        print('PIPELINE RAN:', len(na) if isinstance(na, list) else na, 'new_atoms')
    else:
        print('TRIGGER NOT FIRED')
