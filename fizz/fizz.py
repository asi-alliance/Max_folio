#!/usr/bin/env python3
"""Fizz: A chemistry-inspired concatenative programming language.

Single-file interpreter with stack operations, blocks, rules, and higher-order combinators.
Usage: python3 fizz.py program.fizz  |  python3 fizz.py < program.fizz  |  echo '5 3 + p n' | python3 fizz.py
"""
import sys
class Fizz:
  def __init__(s):
    s.stack=[];s.rules=[];s.out=[];s.ib=[];s.vars={}
  def p(s): return s.stack.pop() if s.stack else ('n',0)
  def pv(s):
    v=s.p()
    return s.pv_val(v)
  def pv_val(s,v):
    if isinstance(v,tuple):
      r=v[1]
      if isinstance(r,(int,float)): return r
      try: return int(r)
      except: return 0
    if isinstance(v,(int,float)): return v
    try: return int(v)
    except: return 0
  def pu(s,v):
    if not isinstance(v,tuple): v=('n',v) if isinstance(v,int) else ('s',v)
    s.stack.append(v)
  def vl(s,v): return v[1] if isinstance(v,tuple) else v
  def st(s,v):
    if isinstance(v,tuple):
      t=v[0]
      if t=='n': return str(v[1])
      if t=='s': return v[1]
      if t=='a': return v[1]
      if t=='b': return '{'+v[1]+'}'
      if t=='l': return '('+' '.join(s.st(x) for x in v[1])+')'
      return str(v[1])
    return str(v)
  def eb(s,b):
    if isinstance(b,tuple) and b[0]=='b': s.run(b[1])
    else: s.pu(b)
  def run(s,code):
    i=0;n=len(code)
    while i<n:
      c=code[i]
      if c in ' \t\r\n': i+=1;continue
      if c=='#':
        while i<n and code[i]!='\n': i+=1
        continue
      if c=='"':
        j=i+1;x=''
        while j<n and code[j]!='"':
          if code[j]=='\\' and j+1<n:
            j+=1;x+={'n':'\n','t':'\t','"':'"','\\':'\\'}.get(code[j],code[j])
          else: x+=code[j]
          j+=1
        s.pu(('s',x));i=j+1;continue
      if c.isdigit():
        x=''
        while i<n and code[i].isdigit(): x+=code[i];i+=1
        s.pu(('n',int(x)));continue
      if c.isalpha() and i+1<n and code[i+1]=='=':
        s.vars[c]=s.p();i+=2;continue
      if c.isalpha() and i+1<n and (code[i+1].isalnum() or code[i+1]=="_"):
        j=i;x=c
        while j+1<n and (code[j+1].isalnum() or code[j+1]=='_'):
          j+=1;x+=code[j]
        s.pu(('a',x));i=j+1;continue
      if c=="'":
        j=i+1;x=''
        while j<n and (code[j].isalnum() or code[j]=='_'): x+=code[j];j+=1
        s.pu(('a',x));i=j;continue
      if c=='{':
        d=1;j=i+1
        while j<n and d>0:
          if code[j]=='{':d+=1
          elif code[j]=='}':d-=1
          if d>0:j+=1
        s.pu(('b',code[i+1:j]));i=j+1;continue
      if c=='[':
        d=1;j=i+1
        while j<n and d>0:
          if code[j]=='[':d+=1
          elif code[j]==']':d-=1
          if d>0:j+=1
        body=code[i+1:j]
        if '=>' in body:
          pat,res=body.split('=>',1)
          s.rules.append((pat.strip(),res.strip()))
        else:
          items=[]
          for t in body.split():
            try:items.append(('n',int(t)))
            except:items.append(('s',t))
          s.pu(('l',items))
        i=j+1;continue
      if c=='(':
        d=1;j=i+1
        while j<n and d>0:
          if code[j]=='(':d+=1
          elif code[j]==')':d-=1
          if d>0:j+=1
        items=[]
        for t in code[i+1:j].split():
          try:items.append(('n',int(t)))
          except:items.append(('s',t))
        s.pu(('l',items));i=j+1;continue
      if c=='$' and i+1<n and (code[i+1].isalpha() or code[i+1]=='_'):
        j=i+1;x=''
        while j<n and (code[j].isalnum() or code[j]=='_'): x+=code[j];j+=1
        if x in s.vars: s.pu(s.vars[x])
        i=j;continue
      if c==':':
        if s.stack:s.stack.append(s.stack[-1])
        i+=1;continue
      if c==';':
        if len(s.stack)>=2:s.stack[-1],s.stack[-2]=s.stack[-2],s.stack[-1]
        i+=1;continue
      if c=='~':s.p();i+=1;continue
      if c=='r':
        v=s.pv();s.pu(('l',[('n',k) for k in range(v)]));i+=1;continue
      if c in '+-*/%^=<g':
        bv=s.p();av=s.p()
        if c=='+' and ((isinstance(bv,tuple) and bv[0]=='s') or (isinstance(av,tuple) and av[0]=='s')):
          s.pu(('s',s.st(av)+s.st(bv)))
          i+=1;continue
        b=s.pv_val(bv);a=s.pv_val(av)
        if c=='+':s.pu(('n',a+b))
        elif c=='-':s.pu(('n',a-b))
        elif c=='*':s.pu(('n',a*b))
        elif c=='/':s.pu(('n',a//b if b else 0))
        elif c=='%':s.pu(('n',a%b if b else 0))
        elif c=='^':s.pu(('n',a**b))
        elif c=='=':s.pu(('n',1 if a==b else 0))
        elif c=='<':s.pu(('n',1 if a<b else 0))
        elif c=='g':s.pu(('n',1 if a>b else 0))
        i+=1;continue
      if c=='p':
        if s.stack:s.out.append(s.st(s.p()))
        i+=1;continue
      if c=='c':
        if s.stack:s.out.append(chr(s.pv()))
        i+=1;continue
      if c=='n':s.out.append('\n');i+=1;continue
      if c=='I':
        if not s.ib:
          s.ib=sys.stdin.read().split()
        if s.ib:
          t=s.ib.pop(0)
          try:s.pu(('n',int(t)))
          except:s.pu(('s',t))
        i+=1;continue
      if c=='!':s.eb(s.p());i+=1;continue
      if c=='?':
        blk=s.p();cond=s.pv()
        if cond:s.eb(blk)
        i+=1;continue
      if c=='e':
        blk=s.p();lst=s.p()
        if isinstance(lst,tuple) and lst[0]=='l':
          for x in lst[1]:s.pu(x);s.eb(blk)
        elif isinstance(lst,tuple) and lst[0]=='n':
          for k in range(lst[1]):s.pu(('n',k));s.eb(blk)
        else:s.pu(lst);s.pu(blk)
        i+=1;continue
      if c=='m':
        blk=s.p();lst=s.p()
        if isinstance(lst,tuple) and lst[0]=='l':
          r=[]
          for x in lst[1]:
            s.pu(x);s.eb(blk);r.append(s.p())
          s.pu(('l',r))
        else:s.pu(lst);s.pu(blk)
        i+=1;continue
      if c=='f':
        blk=s.p();lst=s.p()
        if isinstance(lst,tuple) and lst[0]=='l':
          r=[]
          for x in lst[1]:
            s.pu(x);s.eb(blk)
            if s.pv():r.append(x)
          s.pu(('l',r))
        else:s.pu(lst);s.pu(blk)
        i+=1;continue
      if c=='w':
        body=s.p();cond=s.p()
        cnt=0
        while cnt<100000:
          s.eb(cond)
          if not s.pv():break
          s.eb(body)
          cnt+=1
        i+=1;continue
      if c=='@':
        fn=s.p();arg=s.p()
        fn_s=s.st(fn)
        matched=False
        for pat,res in s.rules:
          if pat==fn_s:
            exp=res.replace('$1',s.st(arg))
            s.run(exp)
            matched=True;break
        if not matched:
          if s.stack:
            a=s.pv()
            if fn_s=='+':s.pu(('n',a+s.pv_val(arg)))
            elif fn_s=='*':s.pu(('n',a*s.pv_val(arg)))
            elif fn_s=='-':s.pu(('n',a-s.pv_val(arg)))
            elif fn_s=='/':v=s.pv_val(arg);s.pu(('n',a//v if v else 0))
            else:s.pu(('a',fn_s));s.pu(arg)
        i+=1;continue
      i+=1
  def get_output(s):return ''.join(s.out)
if __name__=='__main__':
  import os
  if len(sys.argv)>1 and os.path.isfile(sys.argv[1]):
    code=open(sys.argv[1]).read()
  elif len(sys.argv)>1:
    code=sys.argv[1]
  else:
    code=sys.stdin.read()
  f=Fizz();f.run(code)
  sys.stdout.write(f.get_output())
  if f.stack:sys.stderr.write('\n[stack:'+', '.join(f.st(x) for x in f.stack)+']\n')
def run(code=''):
  f = Fizz()
  f.run(code)
  return f.get_output()
