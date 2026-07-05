import sys,json
sys.path.insert(0,'/home/mettaclaw/artifacts')
from coherence_metric import kb_coherence_v4

def kb_coherence(kb_path='/home/mettaclaw/artifacts/agent_kb.json'):
    conflicts,worst=kb_coherence_v4(kb_path=kb_path)
    return conflicts,worst

if __name__=='__main__':
    c,w=kb_coherence()
    print(f'Conflicts: {len(c)}, Worst: {w:.4f}')
    for x in c: print(x)