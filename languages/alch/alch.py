#!/usr/bin/env python3
"""Alch - Algorithmic Chemistry Golfing Language"""
DESCRIPTION = "Run Alch source code. Chemistry-inspired golfing language with MeTTa atoms and Fontana AlChemy molecules."

def run(code="", **kwargs):
    if not code and kwargs: code = kwargs.get("code", "")
    if isinstance(code, dict): code = code.get("code", "")
    sol = []; var = {}; out = []
    DQ = chr(34); SQ = chr(39); NL = chr(10)
    def is_block(s): return isinstance(s, tuple) and len(s) == 2 and s[0] == "block"
    def parse_block(s, i):
        depth = 1; i += 1; start = i
        while i < len(s) and depth > 0:
            if s[i] == "{": depth += 1
            elif s[i] == "}": depth -= 1
            if depth > 0: i += 1
        return ("block", s[start:i]), i + 1
    def parse_str(s, i):
        i += 1; start = i
        while i < len(s) and s[i] != DQ: i += 1
        return s[start:i], i + 1
    def parse_num(s, i):
        start = i
        if s[i] == "-": i += 1
        while i < len(s) and s[i].isdigit(): i += 1
        return int(s[start:i]), i
    def execute(code_str, sol, var, out):
        i = 0
        while i < len(code_str):
            c = code_str[i]
            if c in (chr(32), chr(9), chr(10), chr(13)): i += 1; continue
            if c.isdigit() or (c == "-" and i+1 < len(code_str) and code_str[i+1].isdigit()):
                num, i = parse_num(code_str, i); sol.append(num); continue
            if c == DQ:
                s, i = parse_str(code_str, i); sol.append(s); continue
            if c == "{":
                blk, i = parse_block(code_str, i); sol.append(blk); continue
            if c == ":":
                i += 1; name = ""
                while i < len(code_str) and (code_str[i].isalnum() or code_str[i] == "_"): name += code_str[i]; i += 1
                if sol: var[name] = sol.pop()
                continue
            if c == ";":
                i += 1; name = ""
                while i < len(code_str) and (code_str[i].isalnum() or code_str[i] == "_"): name += code_str[i]; i += 1
                if name in var: sol.append(var[name])
                continue
            try:
                if c == "+": b, a = sol.pop(), sol.pop(); sol.append(a + b)
                elif c == "-": b, a = sol.pop(), sol.pop(); sol.append(a - b)
                elif c == "*": b, a = sol.pop(), sol.pop(); sol.append(a * b)
                elif c == "/": b, a = sol.pop(), sol.pop(); sol.append(a // b if isinstance(a, int) and isinstance(b, int) and b != 0 else a / b)
                elif c == "%": b, a = sol.pop(), sol.pop(); sol.append(a % b)
                elif c == "^": b, a = sol.pop(), sol.pop(); sol.append(a ** b)
                elif c == "=": b, a = sol.pop(), sol.pop(); sol.append(1 if a == b else 0)
                elif c == "<": b, a = sol.pop(), sol.pop(); sol.append(1 if a < b else 0)
                elif c == ">": b, a = sol.pop(), sol.pop(); sol.append(1 if a > b else 0)
                elif c == "&": b, a = sol.pop(), sol.pop(); sol.append(a & b)
                elif c == "|": b, a = sol.pop(), sol.pop(); sol.append(a | b)
                elif c == "~": a = sol.pop(); sol.append(~a if isinstance(a, int) else (1 - a))
                elif c == "o": out.append(str(sol.pop()))
                elif c == "O": out.append(str(sol.pop()) + NL)
                elif c == "p": out.append(str(sol))
                elif c == "P": sol.pop()
                elif c == "D": sol.append(sol[-1])
                elif c == "s": sol[-1], sol[-2] = sol[-2], sol[-1]
                elif c == "r": n = sol.pop(); sol.append(list(range(n)))
                elif c == "x":
                    a = sol.pop()
                    if isinstance(a, int): sol.append(list(range(a)))
                    elif isinstance(a, list):
                        for e in a: sol.append(e)
                    elif isinstance(a, str):
                        for ch in a: sol.append(ch)
                elif c == "m":
                    blk = sol.pop(); lst = sol.pop()
                    if is_block(blk) and isinstance(lst, list):
                        result = []
                        for e in lst:
                            sub = [e]; execute(blk[1], sub, var, out); result.extend(sub)
                        sol.append(result)
                    else:
                        sol.append(lst)
                elif c == "f":
                    blk = sol.pop(); lst = sol.pop()
                    if is_block(blk) and isinstance(lst, list):
                        result = []
                        for e in lst:
                            sub = [e]; execute(blk[1], sub, var, out)
                            if sub and sub[-1]: result.append(e)
                        sol.append(result)
                    else:
                        sol.append(lst)
                elif c == "F":
                    blk = sol.pop(); lst = sol.pop()
                    if is_block(blk) and isinstance(lst, list) and lst:
                        acc = lst[0]
                        for e in lst[1:]:
                            sub = [acc, e]; execute(blk[1], sub, var, out)
                            acc = sub[-1] if sub else acc
                        sol.append(acc)
                    else:
                        sol.append(lst)
                elif c == "S": a = sol.pop(); sol.append(sorted(a) if isinstance(a, list) else a)
                elif c == "#": a = sol.pop(); sol.append(len(a) if isinstance(a, (list, str)) else 1)
                elif c == "h":
                    a = sol.pop()
                    if isinstance(a, (list, str)) and a: sol.append(a[0])
                    else: sol.append(a)
                elif c == "t":
                    a = sol.pop()
                    if isinstance(a, (list, str)) and a: sol.append(a[1:])
                    else: sol.append(a)
                elif c == "c":
                    b, a = sol.pop(), sol.pop()
                    if isinstance(a, list) and isinstance(b, list): sol.append(a + b)
                    elif isinstance(a, str) and isinstance(b, str): sol.append(a + b)
                    else: sol.append(str(a) + str(b))
                elif c == "j": sep, lst = sol.pop(), sol.pop(); sol.append(str(sep).join(str(x) for x in lst) if isinstance(lst, list) else str(lst))
                elif c == "k":
                    blk = sol.pop()
                    if is_block(blk): execute(blk[1], sol, var, out)
                elif c == "?":
                    blk = sol.pop(); cond = sol.pop()
                    if cond:
                        if is_block(blk): execute(blk[1], sol, var, out)
                        else: sol.append(blk)
                elif c == "!":
                    blk = sol.pop(); cond = sol.pop()
                    if not cond:
                        if is_block(blk): execute(blk[1], sol, var, out)
                        else: sol.append(blk)
                elif c == "w":
                    body = sol.pop(); cond = sol.pop()
                    while True:
                        sub = list(sol)
                        if is_block(cond): execute(cond[1], sub, var, out)
                        if not sub or not sub[-1]: break
                        if is_block(body): execute(body[1], sol, var, out)
                elif c == "W":
                    blk = sol.pop()
                    if is_block(blk):
                        execute(blk[1], sol, var, out)
                        while sol and sol[-1]: execute(blk[1], sol, var, out)
                elif c == "A": a = sol.pop(); sol.append(("Atom", a))
                elif c == "M": pat = sol.pop(); val = sol.pop(); sol.append(1 if str(pat) == str(val) else 0)
                elif c == "C":
                    b, a = sol.pop(), sol.pop()
                    if is_block(a) and is_block(b): sol.append(("block", a[1] + b[1]))
                    else: sol.append(("block", str(a) + str(b)))
                elif c == "N": a = sol.pop(); sol.append(-a if isinstance(a, int) else a)
                elif c == "B": a = sol.pop(); sol.append(bin(a)[2:] if isinstance(a, int) else str(a))
                elif c == "b": a = sol.pop(); sol.append(int(a, 2) if isinstance(a, str) else a)
                elif c == SQ:
                    a = sol.pop()
                    if isinstance(a, int): sol.append(chr(a))
                    elif isinstance(a, str) and len(a) == 1: sol.append(ord(a))
                elif c == "l": a = sol.pop(); sol.append(a.lower() if isinstance(a, str) else a)
                elif c == "u": a = sol.pop(); sol.append(a.upper() if isinstance(a, str) else a)
                elif c == "n": sol.append(NL)
                elif c == "I": a = sol.pop(); sol.append(int(a) if isinstance(a, str) else a)
                elif c == "q": a = sol.pop(); out.append(repr(a))
                else:
                    pass
            except IndexError:
                pass
            except Exception as e:
                out.append(f"Error: {e}")
            i += 1
    execute(code, sol, var, out)
    result = "".join(out)
    if not result and sol:
        result = str(sol[-1])
    return result

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        sys.stdout.write(run(open(sys.argv[1]).read()))
    else:
        sys.stdout.write(run(sys.stdin.read()))
