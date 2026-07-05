def cert_layer(f, c, chain_len=1, sim=0.5, social_hops=0, context="default"):
    s1 = (1.0 - 2.0*abs(f - 0.5)) * c
    s2 = 1.0 - c
    s3 = min(1.0, chain_len / 5.0)
    s4 = 1.0 - sim
    s5 = 1.0 - (0.9 ** social_hops)
    I = 0.25*s1 + 0.20*s2 + 0.20*s3 + 0.20*s4 + 0.15*s5
    margin = 1.0 - I
    thresholds = {"routine": 0.30, "default": 0.40, "adversarial": 0.55}
    t = thresholds.get(context, 0.40)
    verdict = "ADMIT" if margin > t else "QUARANTINE"
    return {"instability": round(I,4), "margin": round(margin,4), "threshold": t, "verdict": verdict,
            "sub": {"contradiction": round(s1,4), "weak": round(s2,4), "brittle": round(s3,4), "semantic_jump": round(s4,4), "low_trust": round(s5,4)}}