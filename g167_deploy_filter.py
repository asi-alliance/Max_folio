import sys, json

CATEGORIES = {
    "bird", "animal", "water_body", "landmass", "continent",
    "living_thing", "habitat_type", "geographic_region",
    "cold_region", "temperate_region"
}

def get_leaves(kb):
    return {a[0] for a in kb if len(a)>=4 and a[3]>0.8
            and a[1] in CATEGORIES and a[0] not in CATEGORIES}

def deploy_filter(kb):
    leaves = get_leaves(kb)
    out = []
    for a in kb:
        if len(a) < 4:
            out.append(a)
            continue
        s, p, freq, conf = a[0], a[1], a[2], a[3]
        if s == p:
            continue
        if s in leaves and p in leaves and conf < 0.6:
            continue
        if conf < 0.5:
            continue
        out.append(a)
    return out

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv)>1 else "/home/mettaclaw/artifacts/agent_kb.json"
    kb = json.load(open(path))
    clean = deploy_filter(kb)
    print(len(kb), "before", len(clean), "after", len(kb)-len(clean), "removed")
    json.dump(clean, open("/tmp/agent_kb_clean.json", "w"))
