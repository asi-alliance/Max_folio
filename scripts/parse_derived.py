import re,sys
for line in sys.stdin.readlines():
    m = re.search(r'derived\s+(\d+)\s+\(\(-->\s+(\S+)\s+(\S+)\)\s+\(stv\s+([\d.]+)\s+([\d.]+)\)', line)
    if m:
        print(f'Depth{m.group(1)}  {m.group(2)} --> {m.group(3)}  f={m.group(4)} c={m.group(5)}')
