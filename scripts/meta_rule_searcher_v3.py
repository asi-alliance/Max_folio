import itertools
import math

LEAVES = ['f1','c1','f2','c2']
OPS = {
  'mul': lambda a,b: a*b,
  'add': lambda a,b: a+b,
  'sub': lambda a,b: a-b,
  'div': lambda a,b: a/b if abs(b)>1e-15 else float('inf'),
  'or':  lambda a,b: 1-(1-a)*(1-b),
}

def gen_exprs(depth):
    if depth==0:
        return [(v, v) for v in LEAVES]
    prev = gen_exprs(depth-1)
    all_prev = []
    for d in range(depth):
        all_prev.extend(gen_exprs(d))
    result = list(prev)
    for (n1,e1) in all_prev:
        for (n2,e2) in all_prev:
            for opn in OPS:
                name = f'({opn} {n1} {n2})'
                result.append((name, (opn, e1, e2)))
    return result

def evaluate(expr, vals):
    if isinstance(expr, str):
        return vals[expr]
    op, a, b = expr
    return OPS[op](evaluate(a,vals), evaluate(b,vals))

def w2c(w, k=1): return w/(w+k) if (w+k)!=0 else 0

def search(io_pairs, max_depth=2, tol=1e-9):
    for d in range(max_depth+1):
        exprs = gen_exprs(d)
        for name, expr in exprs:
            ok = True
            for (f1,c1,f2,c2,target) in io_pairs:
                vals = {'f1':f1,'c1':c1,'f2':f2,'c2':c2}
                try:
                    v = evaluate(expr, vals)
                    if not math.isfinite(v) or abs(v - target) > tol: ok=False; break
                except: ok=False; break
            if ok:
                yield ('raw', d, name)
            ok2 = True
            for (f1,c1,f2,c2,target) in io_pairs:
                vals = {'f1':f1,'c1':c1,'f2':f2,'c2':c2}
                try:
                    v = w2c(evaluate(expr, vals))
                    if not math.isfinite(v) or abs(v - target) > tol: ok2=False; break
                except: ok2=False; break
            if ok2:
                yield ('w2c', d, name)

if __name__=='__main__':
    # Test: deduction f_out=f1*f2
    io_f = [(0.9,0.9,0.8,0.9,0.72),(0.7,0.8,0.6,0.7,0.42),(0.5,0.5,0.5,0.5,0.25)]
    print('=== Deduction f_out ===')
    for r in search(io_f): print(r); break
    # Test: deduction c_out=f1*c1*f2*c2
    io_c = [(0.9,0.9,0.8,0.9,0.9*0.9*0.8*0.9),(0.7,0.8,0.6,0.7,0.7*0.8*0.6*0.7)]
    print('=== Deduction c_out ===')
    for r in search(io_c): print(r); break