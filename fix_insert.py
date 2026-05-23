import sys
if len(sys.argv) < 4:
    print("Usage: python3 fix_insert.py <file> <line_num> <text> [text2 ...]")
    sys.exit(1)
path = sys.argv[1]
line_num = int(sys.argv[2])
new_lines = sys.argv[3:]
lines = open(path).readlines()
for i, txt in enumerate(new_lines):
    lines.insert(line_num - 1 + i, txt + chr(10))
open(path, "w").writelines(lines)
print(f"Inserted {len(new_lines)} line(s) at line {line_num} in {path}, total {len(lines)} lines")