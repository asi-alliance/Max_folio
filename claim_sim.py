from collections import defaultdict
import re

class Claim:
    def __init__(self, term, f, c, source_set=None):
        self.term = term; self.f = f; self.c = c
        self.source_set = source_set or set(); self.cluster_id = -1; self.quarantined = False

class Cluster:
    def __init__(self, cid, claims=None):
        self.cid = cid; self.claims = claims or []
        self.quarantined = False; self.quarantine_class = None
    def avg_frequency(self):
        return sum(c.f for c in self.claims) / len(self.claims) if self.claims else 0.0
    def coherence(self):
        if len(self.claims) <= 1: return 1.0
        terms = set(c.term for c in self.claims); return len(terms) / len(self.claims)
    def contradiction_pressure(self, delta):
        n = len(self.claims)
        if n <= 1: return 0.0
        overlap = 0
        for i in range(n):
            for j in range(i+1, n):
                if norm(self.claims[i].term.split()[-1]) == norm(self.claims[j].term.split()[-1]):
                    if self.claims[i].term != self.claims[j].term: overlap += 1
        return delta * overlap / (n * (n-1) / 2)

class ClaimPopulation:
    def __init__(self, theta_split=0.3, delta_contra=0.4):
        self.theta_split = theta_split; self.delta_contra = delta_contra
        self.claims = []; self.clusters = []; self.quarantine_membrane = {}
        self.history = []; self.next_cid = 0
    def add_claim(self, term, f, c, source_set=None):
        claim = Claim(term, f, c, source_set); self.claims.append(claim); return claim
    def assign_initial_clusters(self):
        for claim in self.claims:
            cid = self.next_cid; self.next_cid += 1
            cluster = Cluster(cid, [claim]); claim.cluster_id = cid; self.clusters.append(cluster)
        return self.clusters
    def structural_split(self):
        for cluster in self.clusters:
            pressure = cluster.contradiction_pressure(self.delta_contra)
            if pressure > self.theta_split and len(cluster.claims) >= 2:
                high = [c for c in cluster.claims if c.f >= cluster.avg_frequency()]
                low = [c for c in cluster.claims if c.f < cluster.avg_frequency()]
                if high and low:
                    cid_h = self.next_cid; self.next_cid += 1
                    cid_l = self.next_cid; self.next_cid += 1
                    cluster_h = Cluster(cid_h, high); cluster_l = Cluster(cid_l, low)
                    cluster_h.quarantined = True; cluster_h.quarantine_class = 'Q_AMBIGUOUS'
                    self.quarantine_membrane[cluster_h.cid] = 'one-way'
                    self.clusters.remove(cluster); self.clusters.append(cluster_h); self.clusters.append(cluster_l)
                    return True
        return False
    def _revise_same_term(self):
        for cluster in self.clusters:
            term_groups = defaultdict(list)
            for claim in cluster.claims: term_groups[claim.term].append(claim)
            new_claims = []
            for term, group in term_groups.items():
                if len(group) == 1: new_claims.append(group[0])
                else:
                    merged_f, merged_c = group[0].f, group[0].c
                    for g in group[1:]: merged_f, merged_c = truth_rev(merged_f, merged_c, g.f, g.c)
                    all_srcs = set(); [all_srcs.update(g.source_set) for g in group]
                    new_claim = Claim(term, merged_f, merged_c, all_srcs)
                    new_claim.cluster_id = cluster.cid; new_claims.append(new_claim)
            cluster.claims = new_claims
    def _infer_deduction(self):
        for cluster in self.clusters:
            if cluster.quarantined: continue
            pairs = [(c1, c2) for c1 in cluster.claims for c2 in cluster.claims if c1 is not c2]
            for c1, c2 in pairs:
                p1 = parse_atom(c1.term); p2 = parse_atom(c2.term)
                if len(p1) > 2 and len(p2) > 2 and norm(p1[2]) == norm(p2[1]):
                    new_f, new_c = truth_ded(c1.f, c1.c, c2.f, c2.c)
                    new_term = f'(--> {norm(p1[1])} {norm(p2[2])})'
                    new_src = c1.source_set | c2.source_set; derived = Claim(new_term, new_f, new_c, new_src)
                    derived.cluster_id = cluster.cid; cluster.claims.append(derived)
    def _infer_induction(self):
        for cluster in self.clusters:
            if cluster.quarantined: continue
            pairs = [(c1, c2) for c1 in cluster.claims for c2 in cluster.claims if c1 is not c2]
            for c1, c2 in pairs:
                p1 = parse_atom(c1.term); p2 = parse_atom(c2.term)
                if len(p1) > 2 and len(p2) > 2 and norm(p1[1]) == norm(p2[1]):
                    new_f, new_c = truth_ind(c1.f, c1.c, p2.f, p2.c)
                    new_term = f'(--> {norm(p1[2])} {norm(p2[2])})'
                    new_src = c1.source_set | c2.source_set; derived = Claim(new_term, new_f, new_c, new_src)
                    derived.cluster_id = cluster.cid; cluster.claims.append(derived)
    def _infer_abduction(self):
        for cluster in self.clusters:
            if cluster.quarantined: continue
            pairs = [(c1, c2) for c1 in cluster.claims for c2 in cluster.claims if c1 is not c2]
            for c1, c2 in pairs:
                p1 = parse_atom(c1.term); p2 = parse_atom(c2.term)
                if len(p1) > 2 and len(p2) > 2 and norm(p1[2]) == norm(p2[2]):
                    new_f, new_c = truth_abd(c1.f, c1.c, p2.f, p2.c)
                    new_term = f'(--> {norm(p1[1])} {norm(p2[1])})'
                    new_src = c1.source_set | c2.source_set; derived = Claim(new_term, new_f, new_c, new_src)
                    derived.cluster_id = cluster.cid; cluster.claims.append(derived)
    def _enforce_quarantine(self):
        for cluster in self.clusters:
            if not cluster.quarantined: continue
            for claim in cluster.claims:
                if claim.f > 0.5 and cluster.quarantine_class == 'Q_AMBIGUOUS':
                    claim.quarantined = True
    def _macro_observables(self):
        total_claims = sum(len(c.claims) for c in self.clusters); total_clusters = len(self.clusters)
        quarantined_clusters = sum(1 for c in self.clusters if c.quarantined)
        avg_coherence = sum(c.coherence() for c in self.clusters) / len(self.clusters) if self.clusters else 1.0
        avg_contra = sum(c.contradiction_pressure(self.delta_contra) for c in self.clusters) / len(self.clusters) if self.clusters else 0.0
        snapshot = {'claims': total_claims, 'clusters': total_clusters, 'quarantined': quarantined_clusters, 'avg_coherence': avg_coherence, 'avg_contra': avg_contra}
        self.history.append(snapshot); return snapshot
    def tick(self):
        self._revise_same_term(); self._infer_deduction(); self._infer_induction()
        self._infer_abduction(); self._enforce_quarantine(); self.structural_split()
        return self._macro_observables()

def parse_atom(term):
    parts = re.findall(r'[^()\s]+', term); return tuple(parts) if parts else (term,)

def norm(s): return s.lower().rstrip('s') if isinstance(s, str) else str(s).lower().rstrip('s')

def truth_rev(f1, c1, f2, c2):
    w1=c1/(1-c1+1e-9); w2=c2/(1-c2+1e-9); f=(w1*f1+w2*f2)/(w1+w2+1e-9); c=(w1+w2)/(w1+w2+2); return f, c

def truth_ded(f1, c1, f2, c2): f=f1*f2; c=f1*f2*c1*c2; return f, c

def truth_ind(f1, c1, f2, c2): f=f1; c=f1*c2*c1/(c1+1e-9); return f, c

def truth_abd(f1, c1, f2, c2): f=f1; c=f1*c2*c1/(c2+1e-9); return f, c

if __name__ == '__main__':
    pop = ClaimPopulation(theta_split=0.3, delta_contra=0.4)
    pop.add_claim('(; sam friend)', 0.8, 0.9, {'src1'}); pop.add_claim('(; sam friend)', 0.6, 0.7, {'src2'})
    pop.add_claim('(; friend happy)', 0.7, 0.8, {'src1'}); pop.add_claim('(; sam happy)', 0.6, 0.7, {'src1'})
    pop.add_claim('(; dog animal)', 0.9, 0.9, {'src3'}); pop.add_claim('(; animal being)', 0.8, 0.8, {'src3'})
    pop.add_claim('(; sky blue)', 0.9, 0.9, {'src4'}); pop.add_claim('(; sky green)', 0.8, 0.8, {'src5'})
    pop.assign_initial_clusters(); print('Initial clusters:', len(pop.clusters))
    for i in range(3): obs = pop.tick(); print(f'Tick {i+1}:', obs)
    print('Final clusters:'); [print(f'  C{c.cid}: quarantined={c.quarantined} claims={len(c.claims)}') for c in pop.clusters]