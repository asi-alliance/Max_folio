import numpy as np, wave, sys
sys.path.insert(0,"/home/mettaclaw/artifacts")
from fm_synth_engine_v2 import fm_oscillator, comb_reverb
sr=44100; dur=120; base=220.0
def edo19(step): return base*2**(step/19.0)
cycle_base=[0,5,6,11,6,5,0]
mix=np.zeros(int(dur*sr),dtype=np.float64)
t=0.0; rep=0; beat_dur=0.45; stretch=1.0; drift=0
while t < dur-2:
    for i,step in enumerate(cycle_base):
        if t >= dur-2: break
        s = step + drift
        f = edo19(s)
        length = beat_dur * stretch
        mi = 1.5 + rep*0.5
        sig = fm_oscillator(f, f*2, mi, length, sr) * 0.35
        n = len(sig); att=int(0.03*sr); rel=int(0.08*sr)
        env = np.concatenate([np.linspace(0,1,min(att,n)),np.ones(max(0,n-att-rel)),np.linspace(1,0.2,min(rel,n))])
        env = env[:n]; sig = sig*env
        start=int(t*sr); end=min(start+n, len(mix))
        mix[start:end] += sig[:end-start]
        t += length
    rep += 1; stretch *= 1.18; drift += 1
    if stretch > 4.0: beat_dur *= 1.1
mix = comb_reverb(mix, 100, 0.25, sr)
mix = mix/max(abs(mix).max(),1e-9)*0.9
out = (mix*32767).astype(np.int16)
import wave as wv
wf = wv.open('/home/mettaclaw/artifacts/parabola.wav','w')
wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(sr)
wf.writeframes(out.tobytes());wf.close()
print('OK',len(out)/sr,'s RMS',int(np.sqrt(np.mean(out.astype(float)**2))))
