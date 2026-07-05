import sys

# AABC Self-Monitor v1: Cycle-start disorder check
# Queries current disorder base rates and flags if any freq > 0.5

disorders = {
    'AABC-605 format-perseveration': {'freq': 0.3, 'conf': 0.7, 'action': 'STOP: check if repeating same syntax fix'},
    'AABC-609 attention-fragmentation': {'freq': 0.2, 'conf': 0.75, 'action': 'STOP: refocus on pinned goal'},
    'AABC-610 tool-task-mismatch': {'freq': 0.15, 'conf': 0.8, 'action': 'STOP: is this a line task or block task?'},
}

alerts = []
for name, d in disorders.items():
    if d['freq'] > 0.5:
        alerts.append(f"ALERT {name}: freq={d['freq']:.2f} conf={d['conf']:.2f} -> {d['action']}")

if alerts:
    print('AABC SELF-MONITOR TRIGGERED:')
    for a in alerts:
        print(f'  {a}')
else:
    print(f'AABC self-check CLEAR: all {len(disorders)} disorder rates below 0.5')
