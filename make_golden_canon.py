import numpy as np,wave
from scipy.signal import lfilter
exec(open("/home/mettaclaw/artifacts/fm_synth_engine_v2.py").read())
sr=44100;dur=90;N=sr*dur;pi2=6.283185307
phi=(1+5**0.5)/2
notes_hz=[];f=220.0
for i in range(13):
    notes_hz.append(f);f=f*1.5
    while f>880: f/=2
notes_hz=sorted(notes_hz);notes=np.array(notes_hz)
bpm=72;beat=60.0/bpm;note_dur=int(sr*beat*2)
seq1=[notes[i%len(notes)] for i in range(N//note_dur+1)]
v1_freq=np.zeros(N)
for i,fr in enumerate(seq1):
    s=i*note_dur;e=min(s+note_dur,N);v1_freq[s:e]=fr
delay=int(N/phi);v2_freq=np.zeros(N)
for i,fr in enumerate(seq1):
    s=i*note_dur+delay;e=min(s+note_dur,N)
    if s<N: v2_freq[s:e]=fr
v1_freq=portamento(v1_freq,300);v2_freq=portamento(v2_freq,300)
t=np.arange(N,dtype=np.float64)/sr
mod1=np.cumsum(pi2*v1_freq*2/sr)
lead1=0.35*np.sin(np.cumsum(pi2*v1_freq/sr)+2.5*np.sin(mod1))*(v1_freq>0)
mod2=np.cumsum(pi2*v2_freq*1.5/sr)
lead2=0.3*np.sin(np.cumsum(pi2*v2_freq/sr)+2.0*np.sin(mod2))*(v2_freq>0)
bass_f=portamento(np.where(v1_freq>0,v1_freq*0.5,110),500)
bass=0.2*waveshape(np.sin(np.cumsum(pi2*bass_f/sr)),1.3)
mix=lead1+lead2+bass+breath_noise(N,0.04,0.015)
env=np.ones(N);fi=sr*3;fo=sr*5;env[:fi]=np.linspace(0,1,fi);env[-fo:]=np.linspace(1,0,fo)
mix*=env*(0.5+0.5*np.sin(pi2*t/(dur/phi))**2)
mix=comb_reverb(mix,40,0.3)
b=[1,-0.97];a=[1];mix=lfilter(b,a,mix)
mix=mix/(np.max(np.abs(mix))+1e-9)
out=(mix*32767).astype(np.int16)
wf=wave.open("/home/mettaclaw/artifacts/golden_canon.wav","w")
wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(sr)
wf.writeframes(out.tobytes());wf.close()
print("Done",N,"samples")
