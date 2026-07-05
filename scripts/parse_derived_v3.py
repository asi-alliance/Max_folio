import re,sys

# Load KB pairs as exclusion set
kb_pairs = set()
if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        for line in f:
            m = re.search(r'-->\s+(\S+)\s+(\S+)', line)
            if m:
                kb_pairs.add((m.group(1), m.group(2)))

for line in sys.stdin.readlines():
    m = re.search(r'derived\s+(\d+)\s+\(\(-->\s+(\S+)\s+(\S+)\)\s+\(stv\s+([\d.]+)\s+([\d.]+)\)', line)
    if m:
        print(f'Depth{m.group(1)}  {m.group(2)} --> {m.group(3)}  f={m.group(4)} c={m.group(5)}')
        continue
    m = re.search(r'\(\(-->\s+(\S+)\s+(\S+)\)\s+\(stv\s+([\d.]+)\s+([\d.]+)\)', line)
    if m:
        pair = (m.group(1), m.group(2))
        if pair in kb_pairs:
            continue
        print(f'BCFINAL  {m.group(1)} --> {m.group(2)}  f={m.group(3)} c={m.group(4)}')
