import sys, json

def topk_filter(classified, limits=None):
    if limits is None:
        limits = {'deduction': 5, 'abduction': 3, 'induction': 2}
    groups = {}
    for p1, p2, rtype in classified:
        groups.setdefault(rtype, []).append((p1, p2, rtype))
    result = []
    for rtype, items in groups.items():
        if rtype == 'novel':
            continue
        sorted_items = sorted(items, key=lambda x: min(float(x[0][3]), float(x[1][3])), reverse=True)
        cap = limits.get(rtype, 2)
        result.extend(sorted_items[:cap])
    return result

if __name__ == '__main__':
    print('topk_filter module loaded')
