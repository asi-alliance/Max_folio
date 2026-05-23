import json, difflib, re
samples = json.load(open('/tmp/g395_samples.json'))
episodes = {}
for i in range(1, 6):
    episodes[i] = open(f'/tmp/g396_episode_{i}.txt').read()
results = []
for i, sample in enumerate(samples):
    doc = sample.get('full_doc', '')
    ep = episodes.get(i+1, '')
    seq_ratio = difflib.SequenceMatcher(None, doc.lower(), ep.lower()).ratio()
    doc_words = set(re.findall(r'\w+', doc.lower()))
    ep_words = set(re.findall(r'\w+', ep.lower()))
    jaccard = len(doc_words & ep_words) / max(len(doc_words | ep_words), 1)
    drift = jaccard > 0.6 and seq_ratio < 0.4
    results.append({'sample': i+1, 'seq_ratio': round(seq_ratio, 3), 'jaccard': round(jaccard, 3), 'drift': drift})
json.dump(results, open('/tmp/g396_provenance_report.json', 'w'), indent=2)
for r in results: print(f"S{r['sample']}: seq={r['seq_ratio']} jac={r['jaccard']} drift={r['drift']}")