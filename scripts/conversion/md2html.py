import re, sys
t = open(sys.argv[1]).read()
t = re.sub(r'^## (.+)', r'<h2>\1</h2>', t, flags=re.M)
t = re.sub(r'^### (.+)', r'<h3>\1</h3>', t, flags=re.M)
t = re.sub(r'^- (.+)', r'<li>\1</li>', t, flags=re.M)
print(t)