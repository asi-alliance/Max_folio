import json,subprocess,sys,os

HISTORY_PATH = '/home/mettaclaw/DEPLOYMENT2_OpenAI_LLM/PeTTa/repos/mettaclaw/memory/history.metta'

def fetch_episodes(samples_path='/tmp/g362_samples.json', ctx_b=3, ctx_a=8):
    with open(samples_path) as f:
        samples = json.load(f)
    results = []
    for s in samples:
        ts = s.get('timestamp', 'UNKNOWN')
        if not ts or ts == 'UNKNOWN':
            s['episode_context'] = 'NO_TIMESTAMP'
            results.append(s)
            continue
        ts_prefix = ts[:16]
        cmd = ['grep', '--text', '-B', str(ctx_b), '-A', str(ctx_a), ts_prefix, HISTORY_PATH]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            s['episode_context'] = r.stdout[:2000] if r.stdout else 'NO_MATCH'
        except Exception as e:
            s['episode_context'] = f'ERROR: {e}'
        results.append(s)
    outpath = '/tmp/g362_episodes.json'
    with open(outpath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'Wrote {len(results)} episode-enriched samples to {outpath}')
    for s in results:
        ep = s.get('episode_context','NONE')[:80]
        print(f'  {s["timestamp"]} | ep:{ep}')
    return results

if __name__ == '__main__':
    fetch_episodes()