import math
from scipy.special import betaln, polygamma

def nal_to_beta(f, c):
    w = c / max(1e-9, 1.0 - c)
    return max(0.01, w * f), max(0.01, w * (1.0 - f))

def rao_distance(f1, c1, f2, c2):
    a1, b1 = nal_to_beta(f1, c1)
    a2, b2 = nal_to_beta(f2, c2)
    H2 = 1.0 - math.exp(betaln((a1+a2)/2, (b1+b2)/2) - 0.5*(betaln(a1,b1) + betaln(a2,b2)))
    H2 = max(0.0, min(1.0 - 1e-12, H2))
    return 2.0 * math.asinh(math.sqrt(H2 / (1.0 - H2)))

def curvature_K(f, c):
    a, b = nal_to_beta(f, c)
    s = a + b
    p1a, p1b, p1s = polygamma(1,a), polygamma(1,b), polygamma(1,s)
    p2a, p2b, p2s = polygamma(2,a), polygamma(2,b), polygamma(2,s)
    g11 = p1a - p1s
    g22 = p1b - p1s
    g12 = -p1s
    det = g11*g22 - g12**2
    if abs(det) < 1e-15:
        return -0.25
    dg11_1 = p2a
    dg22_2 = p2b
    dg12_1 = -p2s
    dg12_2 = -p2s
    dg11_2 = -p2s
    dg22_1 = -p2s
    E = 0.5*dg11_2
    F = 0.5*dg22_1
    K = -(E*g22 - F*g12 + F*g11 - E*g12) / (det * 2.0)
    return K

def cert_layer_v02(f, c, chain_len=1, sim=0.5, social_hops=0, context='default', cluster=None, base_eps=1.0):
    s1 = (1.0 - 2.0*abs(f-0.5)) * c
    s2 = 1.0 - c
    s3 = min(1.0, chain_len/5.0)
    s4 = 1.0 - sim
    s5 = 1.0 - 0.9**social_hops
    thresholds = [0.4, 0.85, 0.6, 0.7, 0.75]
    scores = [s1, s2, s3, s4, s5]
    labels = ['contradiction','weak','brittle','semantic_jump','low_trust']
    signed = [t - s for t, s in zip(thresholds, scores)]
    composite = min(signed)
    nearest = labels[signed.index(composite)]
    local_verdict = 'ADMIT' if composite > 0 else ('RISKY' if composite > -0.1 else 'INADMISSIBLE')
    rao_to_centroid = None
    K = curvature_K(f, c)
    eps = base_eps / max(0.1, math.sqrt(abs(K)))
    neighborhood_verdict = 'UNCHECKED'
    if cluster:
        cf = cluster.get('centroid_f', 0.5)
        cc = cluster.get('centroid_c', 0.5)
        rao_to_centroid = rao_distance(f, c, cf, cc)
        neighborhood_verdict = 'ADMIT' if rao_to_centroid < eps else 'QUARANTINE'
    verdict = 'INADMISSIBLE' if local_verdict == 'INADMISSIBLE' else (neighborhood_verdict if neighborhood_verdict == 'QUARANTINE' else local_verdict)
    return {'signed_margins': dict(zip(labels, [round(x,4) for x in signed])), 'composite_margin': round(composite,4), 'nearest_boundary': nearest, 'local_verdict': local_verdict, 'K': round(K,4), 'epsilon': round(eps,4), 'rao_to_centroid': round(rao_to_centroid,4) if rao_to_centroid else None, 'neighborhood_verdict': neighborhood_verdict, 'verdict': verdict}