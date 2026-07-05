lines = []
for r in range(6):
    for c in range(4):
        lines.append(f'(c4-line {r} {c} {r} {c+1} {r} {c+2} {r} {c+3})')
for r in range(3):
    for c in range(7):
        lines.append(f'(c4-line {r} {c} {r+1} {c} {r+2} {c} {r+3} {c})')
for r in range(3,6):
    for c in range(4):
        lines.append(f'(c4-line {r} {c} {r-1} {c+1} {r-2} {c+2} {r-3} {c+3})')
for r in range(3):
    for c in range(4):
        lines.append(f'(c4-line {r} {c} {r+1} {c+1} {r+2} {c+2} {r+3} {c+3})')
with open('/home/mettaclaw/artifacts/c4_lines.txt','w') as f:
    f.write('
'.join(lines))
print(f'Generated {len(lines)} lines')