def semantic_role_mutation(clusters, parse_atom, norm):
    relabelled = 0
    for cluster in clusters:
        if cluster.get("quarantined", False):
            continue
        subject_groups = {}
        for claim in cluster["claims"]:
            parts = parse_atom(claim["term"])
            if len(parts) >= 3:
                subj = norm(parts[1])
                subject_groups.setdefault(subj, []).append(claim)
        for subj, group in subject_groups.items():
            if len(group) < 2:
                continue
            predicates = {}
            for claim in group:
                parts = parse_atom(claim["term"])
                pred = norm(parts[2])
                score = claim["f"] * claim["c"]
                if pred not in predicates or score > predicates[pred]["f"] * predicates[pred]["c"]:
                    predicates[pred] = claim
            if len(predicates) < 2:
                continue
            ranked = sorted(predicates.values(), key=lambda c: c["f"] * c["c"], reverse=True)
            winner = ranked[0]
            for loser in ranked[1:]:
                winner["sources"] = winner.get("sources", set()) | loser.get("sources", set())
                cluster["claims"].remove(loser)
                relabelled += 1
    return relabelled