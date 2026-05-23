import sys
if len(sys.argv) < 3:
    print('Usage: python3 multi_append.py <target> <content_file>')
    sys.exit(1)
target = sys.argv[1]
content_file = sys.argv[2]
with open(content_file) as f:
    new_lines = f.read()
with open(target, 'a') as f:
    f.write(new_lines)
print(f'Appended {len(new_lines.splitlines())} lines to {target}')
