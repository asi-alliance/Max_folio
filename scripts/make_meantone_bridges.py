import numpy as np, wave, sys
sys.path.insert(0,'/home/mettaclaw/artifacts')
from fm_synth_engine_v2 import fm_oscillator, comb_reverb
sr=44100; dur=90; base=220.0
def edo19(step): return base*2**(step/19.0)
# Chord sequences: (voice1_step, voice2_step, duration_beats)
# A section: warm thirds/sixths
sec_a=[(0,6,4),(5,11,4),(6,14,4),(0,11,4),(5,14,3),(6,11,3),(0,6,2)]
# B section: septimal tension
sec_b=[(0,4,3),(7,11,3),(4,9,4),(9,4,3),(7,0,3),(4,7,4)]
# ABA form
chords=sec_a+sec_b+sec_a
bpm=54; beat=60.0/bpm
mix=np.zeros(int(dur*sr),dtype=np.float64)
t=0.0
for s1,s2,beats in chords:
    length=beats*beat; f1=edo19(s1); f2=edo19(s2)
    v1=fm_oscillator(f1,f1*2,3.0,length,sr)*0.3
    v2=fm_oscillator(f2,f2*1.5,2.5,length,sr)*0.25
    env=np.concatenate([np.linspace(0,1,int(0.05*sr)),np.ones(max(0,len(v1)-int(0.15*sr))),np.linspace(1,0,int(0.1*sr))])
    env=env[:len(v1)]
    sig=v1*env+v2*env
    start=int(t*sr); end=min(start+len(sig),len(mix))
    mix[start:end]+=sig[:end-start]
    t+=length
mix=comb_reverb(mix,90,0.25,sr)
mix=mix/max(abs(mix).max(),1e-9)*0.9
out=(mix*32767).astype(np.int16)
wf=wave.open('/home/mettaclaw/artifacts/meantone_bridges.wav','w')
wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(sr)
wf.writeframes(out.tobytes());wf.close()
print('OK',len(out)/sr,'s RMS',int(np.sqrt(np.mean(out.astype(float)**2))))
