import sys
p = '/home/mettaclaw/artifacts/e2e_real_trace.py'
lines = open(p).readlines()
# Replace lines 70-76 (0-indexed) with formatted table
repl = [
    '    rpt = tracker.report()\n',
    '    print()\n',
    '    print("=== KEVIN ACCEPTANCE TABLE ===")\n',
    '    print(f"  ADMIT={counts[\'ADMIT\']} Q_UNDER={q_und} Q_AMB={q_amb} REJECT={counts[\'REJECT\']}")\n',
    '    print(f"  request_attempts={rpt.get(\'request_attempts\',0)}")\n',
    '    print(f"  requests_created={rpt.get(\'requests_created\',0)}")\n',
    '    print(f"  requests_deduped={rpt.get(\'requests_deduped\',0)}")\n',
    '    print(f"  cooldown_suppressed={rpt.get(\'cooldown_suppressed\',0)}")\n',
    '    print(f"  max_stale_requests={rpt.get(\'stale_request_count\',0)}")\n',
    '    print(f"  reopened_after_cooldown={rpt.get(\'reopened_after_cooldown\',0)}")\n',
    '    print(f"  false_admit_count_live={rpt.get(\'false_admit_count\',0)}")\n',
    '    print(f"  false_admit_count_test={rpt.get(\'false_admit_count_test\',0)}")\n',
]
out = lines[:70] + repl + lines[76:]
open(p,'w').writelines(out)
print(f'PATCHED: removed L71-76, inserted {len(repl)} lines, total={len(out)}')