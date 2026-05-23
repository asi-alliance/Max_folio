import os,sys
import chromadb
from openai import OpenAI

DB_PATH = '/home/mettaclaw/DEPLOYMENT2_OpenAI_LLM/PeTTa/chroma_db'
ACCEPT_THRESH = 0.85
REJECT_THRESH = 1.20

_CE_MODEL = None

def _embed(text):
    c = OpenAI()
    r = c.embeddings.create(input=text, model='text-embedding-3-large')
    return r.data[0].embedding

def _get_col():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_collection('memories')

def _load_ce():
    global _CE_MODEL
    if _CE_MODEL is None:
        from sentence_transformers import CrossEncoder
        _CE_MODEL = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    return _CE_MODEL

def ce_rerank_middle(query_text, middle_rows, top_n=10):
    if not middle_rows:
        return middle_rows
    model = _load_ce()
    pairs = [[query_text, row['doc']] for row in middle_rows]
    scores = model.predict(pairs)
    for i, row in enumerate(middle_rows):
        row['ce_score'] = float(scores[i])
    middle_rows.sort(key=lambda r: r['ce_score'], reverse=True)
    return middle_rows[:top_n]

def gated_query(query_text, n_fetch=40, n_return=20, use_ce=False):
    vec = _embed(query_text)
    col = _get_col()
    res = col.query(query_embeddings=[vec], n_results=n_fetch, include=['distances','documents','metadatas'])
    accepted, middle, rejected = [], [], []
    for i, dist in enumerate(res['distances'][0]):
        doc = res['documents'][0][i]
        meta = res['metadatas'][0][i] if res['metadatas'] else {}
        t = meta.get('time','') if meta else ''
        row = {'dist': dist, 'time': t, 'doc': doc}
        if dist < ACCEPT_THRESH:
            accepted.append(row)
        elif dist >= REJECT_THRESH:
            rejected.append(row)
        else:
            middle.append(row)
    if use_ce and middle:
        middle = ce_rerank_middle(query_text, middle)
    else:
        middle.sort(key=lambda r: r['dist'])
    combined = accepted + middle
    combined = combined[:n_return]
    stats = {'accepted': len(accepted), 'middle': len(middle), 'rejected': len(rejected), 'returned': len(combined), 'ce_used': use_ce and bool(middle)}
    return combined, stats

if __name__ == '__main__':
    q = sys.argv[1] if len(sys.argv) > 1 else 'NAL revision confidence'
    use_ce = '--ce' in sys.argv
    results, stats = gated_query(q, use_ce=use_ce)
    print(f'Stats: {stats}')
    for r in results:
        print(f"  {r['dist']:.3f} {r.get('ce_score','n/a'):>8} {r['doc'][:80]}")