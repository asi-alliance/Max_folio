import numpy as np
from collections import Counter

def revise(f1,c1,f2,c2):
    w1=c1/(1-c1) if c1<0.999 else 999.0
    w2=c2/(1-c2) if c2<0.999 else 999.0
    ws=w1+w2
    return (w1*f1+w2*f2)/ws, ws/(ws+1.0)

def entropy(fs, bins=10):
    counts,_=np.histogram(fs, bins=bins, range=(0,1))
    p=counts/counts.sum()
    p=p[p>0]
    return -np.sum(p*np.log(p))

def make_topology(name, n):
    adj=np.zeros((n,n))
    if name=='complete':
        adj=np.ones((n,n))-np.eye(n)
    elif name=='chain':
        for i in range(n-1): adj[i][i+1]=1; adj[i+1][i]=1
    elif name=='ring':
        for i in range(n): adj[i][(i+1)%n]=1; adj[(i+1)%n][i]=1
    elif name=='star':
        for i in range(1,n): adj[0][i]=1; adj[i][0]=1
    return adj

np.random.seed(42)
N=8; ROUNDS=30; TRUST=0.7
seeds_f=np.linspace(0.1,0.9,N)
seeds_c=np.full(N,0.5)
sti=np.random.uniform(0.3,0.9,N)
STI_THRESH=0.5

print('=== CONDITION A: TOPOLOGY-ONLY (fixed seeds, no ECAN, varied topo) ===')
for topo in ['chain','star','ring','complete']:
    fs,cs=seeds_f.copy(),seeds_c.copy()
    adj=make_topology(topo,N)
    for r in range(ROUNDS):
        fn,cn=fs.copy(),cs.copy()
        for i in range(N):
            for j in range(N):
                if adj[i][j]>0:
                    fn[i],cn[i]=revise(fs[i],cs[i],fs[j],cs[j],)
        fs,cs=fn,cn
    print(f'  {topo:10s} H={entropy(fs):.4f} f_range=[{fs.min():.3f},{fs.max():.3f}]')

print('\n=== CONDITION B: ENCODING-ONLY (varied seeds each round, no ECAN, complete) ===')
adj=make_topology('complete',N)
for noise in [0.01,0.05,0.1,0.2]:
    fs,cs=seeds_f.copy(),seeds_c.copy()
    for r in range(ROUNDS):
        fs+=np.random.normal(0,noise,N)
        fs=np.clip(fs,0.001,0.999)
        fn,cn=fs.copy(),cs.copy()
        for i in range(N):
            for j in range(N):
                if adj[i][j]>0:
                    fn[i],cn[i]=revise(fs[i],cs[i],fs[j],cs[j])
        fs,cs=fn,cn
    print(f'  noise={noise:.2f} H={entropy(fs):.4f} f_range=[{fs.min():.3f},{fs.max():.3f}]')

print('\n=== CONDITION C: ATTENTION-ONLY (fixed seeds, ECAN gating, complete) ===')
adj=make_topology('complete',N)
for thresh in [0.3,0.5,0.7,0.9]:
    fs,cs=seeds_f.copy(),seeds_c.copy()
    for r in range(ROUNDS):
        fn,cn=fs.copy(),cs.copy()
        for i in range(N):
            if sti[i]<thresh: continue
            for j in range(N):
                if adj[i][j]>0 and sti[j]>=thresh:
                    fn[i],cn[i]=revise(fs[i],cs[i],fs[j],cs[j])
        fs,cs=fn,cn
    print(f'  thresh={thresh:.1f} H={entropy(fs):.4f} f_range=[{fs.min():.3f},{fs.max():.3f}] active={sum(sti>=thresh)}/{N}')