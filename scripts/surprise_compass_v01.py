# surprise_compass_v01.py
import json

def detect_boundary(cert_results):
    return [(a, "boundary") for a, v in cert_results if v == "QUARANTINE"]

def gap_enumerate(subjects, predicates):
    gaps = []
    for i, s1 in enumerate(subjects):
        for s2 in subjects[i+1:]:
            shared = predicates.get(s1, set()) & predicates.get(s2, set())
            if len(shared) <= 1:
                gaps.append((s1, s2, list(shared)[0] if shared else None))
    return gaps
def daydream_seed(s1, s2, shared_pred=None):
    return ("bridge_" + s1 + "_" + s2 + "_connector", (0.7, 0.3))

def nal_critic(seeds, threshold=0.4):
    return [(a, s) for a, s in seeds if s[1] < threshold]

def pipeline(subjects, cert_results, predicates):
    boundaries = detect_boundary(cert_results)
    gaps = gap_enumerate(subjects, predicates)
    seeds = [daydream_seed(s1, s2, sp) for s1, s2, sp in gaps]
    surprises = nal_critic(seeds)
    return {"boundaries": boundaries, "gaps": gaps, "seeds": seeds, "surprises": surprises}

if __name__ == "__main__":
    print("surprise_compass_v01 loaded")
