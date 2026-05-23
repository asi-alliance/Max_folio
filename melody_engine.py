import numpy as np
def melody_contour(n_notes, shape='arch'):
    t = np.linspace(0, 1, n_notes)
    if shape == 'arch': return np.sin(t * np.pi)
    elif shape == 'descent': return 1.0 - t
    elif shape == 'ascent': return t
    elif shape == 'question': return np.where(t < 0.7, t/0.7, 1.0 - (t-0.7)/0.3 * 0.3)
    return np.ones(n_notes) * 0.5
def gen_melody(scale_freqs, n_notes=16, contour='arch', range_octaves=1.5):
    c = melody_contour(n_notes, contour)
    n_scale = len(scale_freqs)
    indices = np.round(c * (n_scale * range_octaves - 1)).astype(int)
    indices = np.clip(indices, 0, n_scale * 2 - 1)
    freqs = [scale_freqs[i % n_scale] * (2 ** (i // n_scale)) for i in indices]
    return freqs
def add_repetition(freqs, repeat_every=4):
    out = list(freqs)
    for i in range(repeat_every, len(out)):
        if i % (repeat_every*2) < repeat_every: out[i] = out[i % repeat_every]
    return out
def gen_rhythm_pattern(bars=4, subdivs=16):
    kick = [1,0,0,0, 0,0,1,0, 1,0,0,0, 0,0,0,0] * bars
    snare= [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0] * bars
    hat  = [1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,1] * bars
    return kick, snare, hat
def fm_kick(sr=44100):
    t=np.linspace(0,0.15,int(0.15*sr))
    freq=150*np.exp(-t*40)+40
    return np.sin(2*np.pi*np.cumsum(freq)/sr)*np.exp(-t*20)
def fm_snare(sr=44100):
    t=np.linspace(0,0.12,int(0.12*sr))
    tone=np.sin(2*np.pi*200*t)*np.exp(-t*30)*0.5
    noise=np.random.randn(len(t))*np.exp(-t*25)*0.5
    return tone+noise
def fm_hat(sr=44100):
    t=np.linspace(0,0.04,int(0.04*sr))
    return np.random.randn(len(t))*np.exp(-t*60)*0.65
def render_drums(kick_p, snare_p, hat_p, bpm, sr=44100):
    step=60.0/bpm/4
    n_steps=len(kick_p)
    total=int(n_steps*step*sr)
    out=np.zeros(total)
    k=fm_kick(sr); s=fm_snare(sr); h=fm_hat(sr)
    for i in range(n_steps):
        pos=int(i*step*sr)
        if kick_p[i]: out[pos:pos+len(k)]+=k
        if snare_p[i]: out[pos:pos+len(s)]+=s
        if hat_p[i]: out[pos:pos+len(h)]+=h
    return out
def fm_bass(freq, dur, sr=44100, mi=2.0):
    t=np.linspace(0,dur,int(dur*sr))
    mod=np.sin(2*np.pi*freq*t)*mi
    return np.sin(2*np.pi*freq*t+mod)*np.exp(-t/(dur*0.8))*0.65
def fm_pad(freqs, dur, sr=44100, detune=0.003):
    t=np.linspace(0,dur,int(dur*sr))
    out=np.zeros(len(t))
    for f in freqs:
        for d in [-detune,0,detune]:
            out+=np.sin(2*np.pi*f*(1+d)*t)*0.09
    att=int(0.3*sr); rel=int(0.5*sr)
    env=np.concatenate([np.linspace(0,1,min(att,len(t))),np.ones(max(0,len(t)-att-rel)),np.linspace(1,0,min(rel,len(t)))])
    return out*env[:len(out)]
def fm_arp(freqs, note_dur, sr=44100):
    out=[]
    for f in freqs:
        t=np.linspace(0,note_dur,int(note_dur*sr))
        sig=np.sin(2*np.pi*f*t+np.sin(2*np.pi*f*2*t))*np.exp(-t/(note_dur*0.4))*0.45
        out.append(sig)
    return np.concatenate(out)
def fm_lead(freq, dur, sr=44100, mi=1.5, vibrato=5.0):
    t=np.linspace(0,dur,int(dur*sr))
    vib=np.sin(2*np.pi*vibrato*t)*0.008*freq
    mod=np.sin(2*np.pi*freq*1.5*t)*mi
    att=int(0.02*sr); rel=int(0.1*sr)
    env=np.concatenate([np.linspace(0,1,min(att,len(t))),np.ones(max(0,len(t)-att-rel)),np.linspace(1,0,min(rel,len(t)))])
    return np.sin(2*np.pi*(freq+vib)*t+mod)*env[:len(t)]*0.5
def fast_comb_reverb(sig, delay_ms, decay, sr=44100):
    import numpy as np
    delay_samps=int(delay_ms*sr/1000)
    out=np.copy(sig)
    for i in range(1,6):
        d=delay_samps*i
        g=decay**i
        if d>=len(out): break
        out[d:]+=sig[:len(sig)-d]*g
    return out
