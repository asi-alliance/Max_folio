import re, sys
t = open(sys.argv[1]).read()
t=t.replace(chr(8212),chr(45)+chr(45)).replace(chr(8211),chr(45))
t=t.replace(chr(8216),chr(39)).replace(chr(8217),chr(39)).replace(chr(8220),chr(34)).replace(chr(8221),chr(34))
def ct(x):
 ls=x.split(chr(10));o=[];it=False
 for l in ls:
  s=l.strip()
  if chr(124) in s and s.startswith(chr(124)):
   cs=[c.strip() for c in s.strip(chr(124)).split(chr(124))]
   if all(re.match(chr(94)+chr(91)+chr(45)+chr(58)+chr(32)+chr(93)+chr(43)+chr(36),c.strip()) for c in cs):continue
   if not it:o.append(chr(60)+chr(116)+chr(97)+chr(98)+chr(108)+chr(101)+chr(62));tg=chr(116)+chr(104);it=True
   else:tg=chr(116)+chr(100)
   rw=chr(32).join(chr(60)+tg+chr(62)+c+chr(60)+chr(47)+tg+chr(62) for c in cs)
   o.append(chr(60)+chr(116)+chr(114)+chr(62)+rw+chr(60)+chr(47)+chr(116)+chr(114)+chr(62))
  else:
   if it:o.append(chr(60)+chr(47)+chr(116)+chr(97)+chr(98)+chr(108)+chr(101)+chr(62));it=False
   o.append(l)
 if it:o.append(chr(60)+chr(47)+chr(116)+chr(97)+chr(98)+chr(108)+chr(101)+chr(62))
 return chr(10).join(o)
t=ct(t)
t=re.sub(r'^### (.+)','<h3>\\1</h3>',t,flags=re.M)
t=re.sub(r'^## (.+)','<h2>\\1</h2>',t,flags=re.M)
t=re.sub(r'^- (.+)','<li>\\1</li>',t,flags=re.M)
print(t)
