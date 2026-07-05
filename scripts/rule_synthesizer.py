import sysOPS = {'mul':'*','add':'+','sub':'-','div':'/','or':'or-op'}
def expr_to_metta(e):
for po,mo in OPS.items(): e = e.replace('('+po+' ', '('+mo+' ')
for v in ['f1','c1','f2','c2']: e = e.replace(' '+v+' ', ' $'+v+' ').replace('('+v+' ', '($'+v+' ')
e = e.replace(' '+v+')', ' $'+v+')').replace('('+v+')', '($'+v+')')
return e
TEMPLATES = {'deduction':{'p1':'((--> $A $M) (stv $f1 $c1))','p2':'((--> $M $B) (stv $f2 $c2))','conclusion':'(--> $A $B)'},'abduction':{'p1':'((--> $A $M) (stv $f1 $c1))','p2':'((--> $B $M) (stv $f2 $c2))','conclusion':'(--> $B $A)'},'induction':{'p1':'((--> $M $A) (stv $f1 $c1))','p2':'((--> $M $B) (stv $f2 $c2))','conclusion':'(--> $A $B)'}}
def synthesize(rt, fo, co, fw=False, cw=False):
t=TEMPLATES[rt]; fm=expr_to_metta(fo); cm=expr_to_metta(co)
if fw: fm='(w2c '+fm+')'
if cw: cm='(w2c '+cm+')'
return '(= (nal-'+rt+')
  (match &self
    '+t['p1']+'
    '+t['p2']+'
    ('+t['conclusion']+' (stv '+fm+' '+cm+'))))'
if __name__=='__main__':
rt=sys.argv[1] if len(sys.argv)>1 else 'deduction'
fo=sys.argv[2] if len(sys.argv)>2 else '(mul f1 f2)'
co=sys.argv[3] if len(sys.argv)>3 else '(mul (mul f1 c1) (mul f2 c2))'
