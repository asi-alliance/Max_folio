import re
f=open('/home/mettaclaw/artifacts/md2html_v4.py','r')
lines=f.readlines()
f.close()
# Find line 't = open' and insert Unicode normalization after it
idx=next(i for i,l in enumerate(lines) if 'open(sys.argv' in l)
new_lines=['t=t.replace(chr(8212),chr(45)+chr(45)).replace(chr(8211),chr(45))\n','t=t.replace(chr(8216),chr(39)).replace(chr(8217),chr(39)).replace(chr(8220),chr(34)).replace(chr(8221),chr(34))\n']
lines=lines[:idx+1]+new_lines+lines[idx+1:]
f=open('/home/mettaclaw/artifacts/md2html_v4.py','w')
f.writelines(lines)
f.close()
print('unicode fix applied')
