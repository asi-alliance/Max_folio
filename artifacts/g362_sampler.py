import chromadb,json,random,sys,os

def sample_memories(n=10):
    c = chromadb.PersistentClient(path='/home/mettaclaw/DEPLOYMENT2_OpenAI_LLM/PeTTa/chroma_db')
    col = c.get_collection('memories')
    all_ids = col.get(include=[])['ids']
    sample_ids = random.sample(all_ids, min(n, len(all_ids)))
    data = col.get(ids=sample_ids, include=['documents','metadatas'])
    results = []
    for i, doc, meta in zip(data['ids'], data['documents'], data['metadatas']):
        ts = meta.get('time', 'UNKNOWN') if meta else 'UNKNOWN'
        results.append({'id': i, 'timestamp': ts, 'doc_preview': doc[:200], 'full_doc': doc})
    return results

def write_samples(n=10, outpath='/tmp/g362_samples.json'):
    samples = sample_memories(n)
    with open(outpath, 'w') as f:
        json.dump(samples, f, indent=2)
    print(f'Wrote {len(samples)} samples to {outpath}')
    for s in samples:
        print(f"  {s['timestamp']} | {s['doc_preview'][:80]}")
    return samples

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    write_samples(n)