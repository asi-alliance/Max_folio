"""
Quaff v2 — a drinking-themed toy programming language.

  pour x = expr       assign (pour a drink into a glass)
  fill x              increment (fill the glass up more)
  spill x             set to 0 (knocked over your drink!)
  sip x               decrement (take a sip)
  belch expr          print (let it out!)
  chug ... until      do-while loop (keep chugging until done)
  sniff <cond> ... spit  if-then (sniff to check, spit to end)
  cheers a OP b       comparison operator for conditions
                      where OP is ==, !=, <, >, <=, >= (default ==)

Grammar (EBNF):
  program = { stmt } ;
  stmt    = assign | incr | zero | decr | print | loop | cond ;
  assign  = "pour" ident "=" expr ;
  incr    = "fill" ident ;
  zero    = "spill" ident ;
  decr    = "sip" ident ;
  print   = "belch" expr ;
  loop    = "chug" { stmt } "until" bexpr ;
  cond    = "sniff" bexpr { stmt } "spit" ;
  bexpr   = "cheers" expr (op) expr | expr (op) expr ;
  op      = "==" | "!=" | "<" | ">" | "<=" | ">=" ;
  expr    = term { ("+" | "-") term } ;
  term    = factor { ("*" | "/") factor } ;
  factor  = int | ident | "(" expr ")" ;
"""
import re

DESCRIPTION = "Run Quaff source code. Pass Quaff program as string."

class Interp:
    def __init__(self):
        self.vars = {}
        self.lines = []
        self.pc = 0
        self.output = []

    def tokenize(self, src):
        toks = []
        for line in src.strip().split('\n'):
            line = line.split('#')[0].strip()
            if not line: continue
            toks.append(re.findall(r'==|!=|<=|>=|[A-Za-z_]\w*|\d+|[+\-*/()=<>%]', line))
        return toks

    def run(self, src):
        self.lines = self.tokenize(src)
        self.pc = 0
        while self.pc < len(self.lines):
            self.exec_stmt(self.lines[self.pc])
            self.pc += 1
        return ' '.join(str(x) for x in self.output) if self.output else 'Done'

    def exec_stmt(self, toks):
        kw = toks[0]
        if kw == 'pour':   self.vars[toks[1]] = self.eval_expr(toks[3:])
        elif kw == 'fill': self.vars[toks[1]] = self.vars.get(toks[1], 0) + 1
        elif kw == 'spill': self.vars[toks[1]] = 0
        elif kw == 'sip':  self.vars[toks[1]] = self.vars.get(toks[1], 0) - 1
        elif kw == 'belch': self.output.append(self.eval_expr(toks[1:]))
        elif kw == 'chug': self.exec_loop()
        elif kw == 'sniff': self.exec_cond(toks)
        else: raise SyntaxError(f"Unknown keyword: {kw}")

    def exec_loop(self):
        body_start = self.pc + 1; depth = 1; until_line = None
        i = self.pc + 1
        while i < len(self.lines):
            if self.lines[i][0] == 'chug': depth += 1
            elif self.lines[i][0] == 'until':
                depth -= 1
                if depth == 0: until_line = i; break
            i += 1
        if until_line is None: raise SyntaxError("chug without until")
        cond_toks = self.lines[until_line][1:]
        while True:
            j = body_start
            while j < until_line:
                self.pc = j; self.exec_stmt(self.lines[j])
                j = self.pc + 1
            if self.eval_bexpr(cond_toks): break
        self.pc = until_line

    def exec_cond(self, toks):
        bexpr = toks[1:]
        body_start = self.pc + 1; depth = 1; spit_line = None
        i = self.pc + 1
        while i < len(self.lines):
            if self.lines[i][0] == 'sniff': depth += 1
            elif self.lines[i][0] == 'spit':
                depth -= 1
                if depth == 0: spit_line = i; break
            i += 1
        if spit_line is None: raise SyntaxError("sniff without spit")
        if self.eval_bexpr(bexpr):
            j = body_start
            while j < spit_line:
                self.pc = j; self.exec_stmt(self.lines[j])
                j = self.pc + 1
        self.pc = spit_line

    def eval_bexpr(self, toks):
        # Handle "cheers a OP b" or "cheers a b" (== implied) or "a OP b"
        if toks[0] == 'cheers':
            toks = toks[1:]  # strip 'cheers'
        # Find comparison operator
        for i, t in enumerate(toks):
            if t in {'==','!=','<','>','<=','>='}:
                l = self.eval_expr(toks[:i])
                r = self.eval_expr(toks[i+1:])
                return {'==':l==r,'!=':l!=r,'<':l<r,'>':l>r,'<=':l<=r,'>=':l>=r}[t]
        # No operator found — truthiness of single expression
        return bool(self.eval_expr(toks))

    def eval_expr(self, toks): return self.parse_add(toks, [0])
    def parse_add(self, t, i):
        v = self.parse_mul(t, i)
        while i[0] < len(t) and t[i[0]] in ('+','-'):
            op=t[i[0]]; i[0]+=1; r=self.parse_mul(t,i)
            v = v+r if op=='+' else v-r
        return v
    def parse_mul(self, t, i):
        v = self.parse_atom(t, i)
        while i[0] < len(t) and t[i[0]] in ('*','/','%'):
            op=t[i[0]]; i[0]+=1; r=self.parse_atom(t,i)
            v = v*r if op=='*' else (v%r if op=='%' else v//r)
        return v
    def parse_atom(self, t, i):
        x = t[i[0]]
        if x == '(': i[0]+=1; v=self.parse_add(t,i); i[0]+=1; return v
        i[0] += 1
        return int(x) if x.isdigit() else self.vars.get(x, 0)

def run(code=''):
    """Run a Quaff program. Pass source as string."""
    interp = Interp()
    result = interp.run(code)
    return result

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(run(open(sys.argv[1]).read()))
    else:
        print("=== Countdown ===")
        print(run("pour goblet = 5\nchug\n  belch goblet\n  sip goblet\nuntil cheers goblet 0\nbelch goblet"))
        print()
        print("=== Fill/Spill ===")
        print(run("pour x = 3\nfill x\nfill x\nbelch x\nspill x\nbelch x"))
        print()
        print("=== Sniff/Spit (if-then) ===")
        print(run("pour a = 10\nsniff cheers a > 5\n  belch 99\nspit\nbelch 1"))
