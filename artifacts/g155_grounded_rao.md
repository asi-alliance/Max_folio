# Grounded Rao Atom via PeTTa py-call (g155)

## Key Finding
PeTTa py-call requires BANG prefix: `!(py-call (module.func args))`
after `!(import! &self "file.py")`. Equality definitions crash Prolog.

## Python Module (/tmp/g155_rao.py)
```python
import numpy as np
from scipy.special import betaln
def fc_to_ab(f,c):
    w=c/(1.0-c+1e-12)
    return max(w*f,0.01), max(w*(1.0-f),0.01)
def rao_beta(f1,c1,f2,c2):
    a1,b1=fc_to_ab(float(f1),float(c1))
    a2,b2=fc_to_ab(float(f2),float(c2))
    H2=1.0-np.exp(betaln((a1+a2)/2,(b1+b2)/2)-0.5*(betaln(a1,b1)+betaln(a2,b2)))
    H2=np.clip(H2,1e-15,1.0-1e-15)
    return float(2.0*np.arcsinh(np.sqrt(H2/(1.0-H2))))
```

## MeTTa Wrapper
```metta
!(import! &self "/tmp/g155_rao.py")
!(py-call (g155_rao.rao_beta 0.9 0.8 0.85 0.7))
!(if (< (py-call (g155_rao.rao_beta 0.9 0.8 0.85 0.7)) 0.5) similar distant)
```

## Validation (Criterion C)
| Pair | Expected (g129) | Actual | Match |
|------|-----------------|--------|-------|
| (0.9,0.8)-(0.7,0.5) | 0.690 | 0.690 | YES |
| (0.9,0.8)-(0.85,0.7) | 0.245 | 0.245 | YES |
| (0.3,0.6)-(0.95,0.9) | 2.358 | 2.358 | YES |

## Inference Chain (Criterion D)
`!(if (< (py-call (g155_rao.rao_beta 0.9 0.8 0.85 0.7)) 0.5) similar distant)` → similar
`!(if (< (py-call (g155_rao.rao_beta 0.3 0.6 0.95 0.9)) 0.5) similar distant)` → distant

## Self-Validation
| Criterion | Status | Evidence |
|-----------|--------|----------|
| (A) Python module | PASS | g155_rao.py 12 lines |
| (B) MeTTa py-call import | PASS | Bang syntax confirmed |
| (C) 3 known pair validation | PASS | All match g129 |
| (D) Inference chain demo | PASS | similar/distant output |
| (E) Under 80 lines | PASS | ~26 lines total |

*g155 completed 2026-04-24. Enables g159 trust decay atoms downstream.*