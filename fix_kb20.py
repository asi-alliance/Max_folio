import sys
path = '/home/mettaclaw/scripts/test_kb_20.nal'
f = open(path, 'r')
lines = f.readlines()
f.close()
# Remove dummy line at index 0 if present
if lines[0].strip() == 'dummy':
    lines = lines[1:]
# Fix merged last line
fixed = []
for line in lines:
    if '0.85)(--> organism' in line:
        parts = line.split('0.85)(--> organism')
        fixed.append(parts[0] + '0.85)')
        fixed.append('(--> organism' + parts[1])
    else:
        fixed.append(line)
# Ensure all lines end with newline
fixed = [l.rstrip() + '
' for l in fixed]
f = open(path, 'w')
f.writelines(fixed)
f.close()
print(f'Written {len(fixed)} lines')