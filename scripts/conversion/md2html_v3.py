import re, sys
t = open(sys.argv[1]).read()
t = re.sub(r'^### (.+)', r'<h3></h3>', t, flags=re.M)
t = re.sub(r'^## (.+)', r'<h2></h2>', t, flags=re.M)
t = re.sub(r'^- (.+)', r'<li></li>', t, flags=re.M)
print(t)
