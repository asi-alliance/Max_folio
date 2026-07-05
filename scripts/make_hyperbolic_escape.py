import numpy as np, wave, sys
sys.path.insert(0,"/home/mettaclaw/artifacts")
from fm_synth_engine_v2 import fm_oscillator, comb_reverb
sr=44100; dur=90; base=220.0
def edo19(step): return base*2**(step/19.0)
phrases=[(0,2,6,1.5),(4,6,6,2.0),(7,9,5,2.8),(9,11,5,3.5),(4,7,4,4.0),(9,13,4,4.5),(7,15,4,5.0),(15,18,4,5.5),(13,23,3,6.0),(18,28,3,6.5),(15,32,3,7.0),(28,37,3,7.5)]
bpm=48; beat=60.0/bpm
mix=np.zeros(int(dur*sr),dtype=np.float64)
t=0.0
for s1,s2,beats,mi in phrases:
    length=beats*beat; f1=edo19(s1); f2=edo19(s2)
    v1=fm_oscillator(f1,f1*2,mi,length,sr)*0.3
    v2=fm_oscillator(f2,f2*1.5,mi*0.8,length,sr)*0.25
    n=int(length*sr); att=int(0.04*sr); rel=int(0.2*sr)
    env=np.concatenate([np.linspace(0,1,att),np.ones(max(0,n-att-rel)),np.linspace(1,0.3,rel)])
    env=env[:min(len(v1),len(v2))]; v1=v1[:len(env)]; v2=v2[:len(env)]
    sig=v1*env+v2*env
    start=int(t*sr); end=min(start+len(sig),len(mix))
    mix[start:end]+=sig[:end-start]
    t+=length
mix=comb_reverb(mix,120,0.3,sr)
mix=mix/max(abs(mix).max(),1e-9)*0.9
out=(mix*32767).astype(np.int16)
import wave as wv
wf=wv.open('/home/mettaclaw/artifacts/hyperbolic_escape.wav','w')
wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(sr)
wf.writeframes(out.tobytes());wf.close()
print('OK',len(out)/sr,'s RMS',int(np.sqrt(np.mean(out.astype(float)**2))))
