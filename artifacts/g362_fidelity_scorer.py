import json,re,sys,os

def load_episodes(path='/tmp/g362_episodes.json'):
    with open(path) as f:
        return json.load(f)

def split_claims(doc):
    sents = re.split(r'(?<=[.!?])\s+', doc.strip())
    return [s.strip() for s in sents if len(s.strip()) > 10]

def score_sample(sample):
    doc = sample.get('full_doc', '')
    episode = sample.get('episode_context', '')
    claims = split_claims(doc)
    results = []
    for claim in claims:
        keywords = set(re.findall(r'[A-Za-z0-9_]{4,}', claim.lower()))
        if not keywords:
            results.append({'claim': claim[:120], 'score': 0.5, 'reason': 'no_keywords'})
            continue
        ep_lower = episode.lower()
        hits = sum(1 for kw in keywords if kw in ep_lower)
        ratio = hits / len(keywords)
        sc = 1.0 if ratio >= 0.6 else (0.5 if ratio >= 0.3 else 0.0)
        results.append({'claim': claim[:120], 'score': sc, 'kw_ratio': round(ratio,2), 'hits': hits, 'total_kw': len(keywords)})
    agg = sum(r['score'] for r in results) / len(results) if results else 0
    return {'id': sample['id'][:12], 'timestamp': sample['timestamp'], 'n_claims': len(results), 'fidelity': round(agg,3), 'claims': results}

def run():
    samples = load_episodes()
    report = [score_sample(s) for s in samples]
    with open('/tmp/g362_fidelity_report.json','w') as f:
        json.dump(report, f, indent=2)
    print(f'Fidelity report: {len(report)} samples')
    for r in report:
        print(f'  {r["timestamp"]} | fidelity={r["fidelity"]} claims={r["n_claims"]}')
    agg = sum(r['fidelity'] for r in report) / len(report) if report else 0
    print(f'AGGREGATE FIDELITY: {round(agg,3)}')

if __name__ == '__main__':
    run()