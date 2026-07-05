import numpy as np, sys
sys.path.insert(0,'/home/mettaclaw/artifacts')
from melody_engine import *
from fm_synth_engine_v2 import fm_oscillator
sr=44100; base=220.0
def edo19(step): return base*2**(step/19.0)
# 19EDO scale: 0=A, 5=minor3rd, 6=major3rd, 11=fifth, 14=major6th
scale=[0,3,5,6,8,11,14,16]; scale_freqs=[edo19(s) for s in scale]
# SECTION DURATIONS: intro=30s@63bpm, build=30s@63->126, full=45s@126, collapse=45s@126->63
total_dur=150
mix=np.zeros(int(total_dur*sr),dtype=np.float64)
# --- SECTION 1: INTRO pad only @63bpm (womb comfort) ---
pad_chords=[[0,6,11],[5,11,14],[3,8,14],[0,6,11]]
for ci,chord in enumerate(pad_chords):
    freqs=[edo19(s) for s in chord]
    p=fm_pad(freqs, 7.5, sr)
    pos=int(ci*7.5*sr)
    mix[pos:pos+len(p)]+=p*0.6
# --- SECTION 2: BUILD @63->126bpm, add bass+drums ---
sec2_start=30.0; sec2_dur=30.0
for bar in range(8):
    bpm=63+bar*7.875
    beat=60.0/bpm
    t0=sec2_start+bar*sec2_dur/8
    # bass note cycles through root-fifth-third-root
    bass_steps=[0,11,6,0]
    bf=edo19(bass_steps[bar%4])*0.5
    b=fm_bass(bf, beat*4, sr)
    pos=int(t0*sr); end=min(pos+len(b),len(mix))
    mix[pos:end]+=b[:end-pos]*0.5
    # drums
    k,s,h=gen_rhythm_pattern(1)
    d=render_drums(k,s,h,bpm,sr)
    end2=min(pos+len(d),len(mix))
    mix[pos:end2]+=d[:end2-pos]*0.4
# --- SECTION 3: FULL @126bpm, all layers ---
sec3_start=60.0; sec3_dur=45.0
bpm_full=126; beat_f=60.0/bpm_full
mel_freqs=gen_melody(scale_freqs, 32, 'arch', 1.5)
mel_freqs=add_repetition(mel_freqs, 4)
for bar in range(12):
    t0=sec3_start+bar*sec3_dur/12
    pos=int(t0*sr)
    k,s,h=gen_rhythm_pattern(1)
    d=render_drums(k,s,h,bpm_full,sr)*0.6
    end=min(pos+len(d),len(mix)); mix[pos:end]+=d[:end-pos]
    bf=edo19([0,11,5,0,3,11,0,5,6,0,11,3][bar%12])*0.5
    b=fm_bass(bf, sec3_dur/12, sr)*0.6
    end=min(pos+len(b),len(mix)); mix[pos:end]+=b[:end-pos]
    chord=[0,6,11] if bar%2==0 else [5,11,14]
    p=fm_pad([edo19(s) for s in chord], sec3_dur/12, sr)*0.55
    end=min(pos+len(p),len(mix)); mix[pos:end]+=p[:end-pos]
    arp_notes=[scale_freqs[(bar+i)%len(scale_freqs)] for i in range(4)]
    a=fm_arp(arp_notes, beat_f, sr)*0.5
    end=min(pos+len(a),len(mix)); mix[pos:end]+=a[:end-pos]
    for ni in range(4):
        mf=mel_freqs[(bar*4+ni)%len(mel_freqs)]
        l=fm_lead(mf, beat_f*2, sr)*0.5
        lp=pos+int(ni*beat_f*2*sr); le=min(lp+len(l),len(mix))
        mix[lp:le]+=l[:le-lp]
# --- SECTION 4: COLLAPSE @126->63bpm, voices converge to A220 ---
sec4_start=105.0; sec4_dur=45.0
for bar in range(12):
    bpm=126-bar*5.25
    beat=60.0/bpm
    t0=sec4_start+bar*sec4_dur/12
    pos=int(t0*sr)
    fade=1.0-bar/12.0
    k,s,h=gen_rhythm_pattern(1)
    d=render_drums(k,s,h,bpm,sr)*0.4*fade
    end=min(pos+len(d),len(mix)); mix[pos:end]+=d[:end-pos]
    convergence=bar/11.0
    cf=base*(1-convergence)+edo19([0,6,11,5,3,0,0,0,0,0,0,0][bar])*convergence
    b=fm_bass(cf*0.5, sec4_dur/12, sr)*0.4*fade
    end=min(pos+len(b),len(mix)); mix[pos:end]+=b[:end-pos]
    p=fm_pad([base*(1-convergence*0.5)+edo19(s)*convergence*0.5 for s in [0,6,11]], sec4_dur/12, sr)*0.3*fade
    end=min(pos+len(p),len(mix)); mix[pos:end]+=p[:end-pos]
mix=np.tanh(mix/(max(abs(mix).max(),1e-9)*0.15))*0.95
# removed duplicate tanh
# removed duplicate normalization
out=(mix*32767).astype(np.int16)
import wave as wv
wf=wv.open('/home/mettaclaw/artifacts/degenerate_conic.wav','w')
wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(sr)
wf.writeframes(out.tobytes());wf.close()
print('OK',len(out)/sr,'s RMS',int(np.sqrt(np.mean(out.astype(float)**2))))
