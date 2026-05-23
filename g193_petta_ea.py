from pyswip import Prolog
import alogos
import signal
q = chr(34)
nl = chr(10)
ebnf_lines = [q+q+q]
ebnf_lines.append(chr(101)+chr(120)+chr(112)+chr(114)+chr(32)+chr(61)+chr(32)+chr(110)+chr(117)+chr(109)+chr(32)+chr(124)+chr(32)+q+chr(40)+q+chr(32)+chr(44)+chr(32)+chr(111)+chr(112)+chr(32)+chr(44)+chr(32)+q+chr(32)+q+chr(32)+chr(44)+chr(32)+chr(101)+chr(120)+chr(112)+chr(114)+chr(32)+chr(44)+chr(32)+q+chr(32)+q+chr(32)+chr(44)+chr(32)+chr(101)+chr(120)+chr(112)+chr(114)+chr(32)+chr(44)+chr(32)+q+chr(41)+q+chr(32)+chr(59))
ebnf_lines.append(chr(111)+chr(112)+chr(32)+chr(61)+chr(32)+q+chr(43)+q+chr(32)+chr(124)+chr(32)+q+chr(45)+q+chr(32)+chr(124)+chr(32)+q+chr(42)+q+chr(32)+chr(124)+chr(32)+q+chr(47)+q+chr(32)+chr(59))
ebnf_lines.append(chr(110)+chr(117)+chr(109)+chr(32)+chr(61)+chr(32)+chr(100)+chr(105)+chr(103)+chr(105)+chr(116)+chr(32)+chr(44)+chr(32)+chr(100)+chr(105)+chr(103)+chr(105)+chr(116)+chr(32)+chr(44)+chr(32)+chr(100)+chr(105)+chr(103)+chr(105)+chr(116)+chr(32)+chr(124)+chr(32)+chr(100)+chr(105)+chr(103)+chr(105)+chr(116)+chr(32)+chr(44)+chr(32)+chr(100)+chr(105)+chr(103)+chr(105)+chr(116)+chr(32)+chr(124)+chr(32)+chr(100)+chr(105)+chr(103)+chr(105)+chr(116)+chr(32)+chr(59))
ebnf_lines.append(chr(100)+chr(105)+chr(103)+chr(105)+chr(116)+chr(32)+chr(61)+chr(32)+q+chr(48)+q+chr(32)+chr(124)+chr(32)+q+chr(49)+q+chr(32)+chr(124)+chr(32)+q+chr(50)+q+chr(32)+chr(124)+chr(32)+q+chr(51)+q+chr(32)+chr(124)+chr(32)+q+chr(52)+q+chr(32)+chr(124)+chr(32)+q+chr(53)+q+chr(32)+chr(124)+chr(32)+q+chr(54)+q+chr(32)+chr(124)+chr(32)+q+chr(55)+q+chr(32)+chr(124)+chr(32)+q+chr(56)+q+chr(32)+chr(124)+chr(32)+q+chr(57)+q+chr(32)+chr(59))
ebnf_lines.append(q+q+q)
ebnf = nl.join(ebnf_lines)
g = alogos.Grammar(ebnf_text=ebnf)
p = Prolog()
p.consult(chr(47)+chr(104)+chr(111)+chr(109)+chr(101)+chr(47)+chr(109)+chr(101)+chr(116)+chr(116)+chr(97)+chr(99)+chr(108)+chr(97)+chr(119)+chr(47)+chr(68)+chr(69)+chr(80)+chr(76)+chr(79)+chr(89)+chr(77)+chr(69)+chr(78)+chr(84)+chr(50)+chr(95)+chr(79)+chr(112)+chr(101)+chr(110)+chr(65)+chr(73)+chr(95)+chr(76)+chr(76)+chr(77)+chr(47)+chr(80)+chr(101)+chr(84)+chr(84)+chr(97)+chr(47)+chr(115)+chr(114)+chr(99)+chr(47)+chr(109)+chr(101)+chr(116)+chr(116)+chr(97)+chr(95)+chr(110)+chr(111)+chr(106)+chr(97)+chr(110)+chr(117)+chr(115)+chr(46)+chr(112)+chr(108))
def petta_eval(expr):
    try:
        qs = chr(112)+chr(114)+chr(111)+chr(99)+chr(101)+chr(115)+chr(115)+chr(95)+chr(109)+chr(101)+chr(116)+chr(116)+chr(97)+chr(95)+chr(115)+chr(116)+chr(114)+chr(105)+chr(110)+chr(103)+chr(40)+chr(34)+chr(33)+expr+chr(34)+chr(44)+chr(32)+chr(82)+chr(41)
        r = list(p.query(qs))
        if r and chr(82) in r[0]:
            v = r[0][chr(82)]
            return float(v[0]) if isinstance(v, list) else float(v)
    except: pass
    return 99999
TARGET = 201238
def objective(s):
    expr = s.replace(chr(32)*2, chr(32)).strip()
    val = petta_eval(expr)
    if val == 99999:
        return val
    return abs(val - TARGET) + 0.01 * len(expr)
ea = alogos.EvolutionaryAlgorithm(g, objective, 'min', max_generations=50, population_size=100, verbose=True)
best = ea.run()
print(chr(66)+chr(69)+chr(83)+chr(84)+chr(58), best.phenotype, chr(70)+chr(73)+chr(84)+chr(58), best.fitness)
