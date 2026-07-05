import numpy as np, pretty_midi, wave, sys
sys.path.insert(0,'/home/mettaclaw/artifacts')
from fm_synth_engine_v2 import fm_oscillator, comb_reverb
sr=44100; pm=pretty_midi.PrettyMIDI('/home/mettaclaw/artifacts/ellipse_orbit_2x.mid')
dur=int(93*sr); mix=np.zeros(dur,dtype=np.float64)
for inst in pm.instruments:
    for n in inst.notes:
        freq=440*2**((n.pitch-69)/12); length=n.end-n.start; amp=n.velocity/127.0*0.4; start=int(n.start*sr); ratio=2.0 if 'FocusA' in inst.name else 3.0; sig=fm_oscillator(freq,freq*ratio,amp*4,length,sr)*amp; env=np.linspace(1,0,len(sig))**0.5; sig=sig*env; end=min(start+len(sig),dur); mix[start:end]+=sig[:end-start]
mix=comb_reverb(mix,80,0.3,sr); mix=mix/max(abs(mix))*0.9
out=(mix*32767).astype(np.int16); wf=wave.open('/home/mettaclaw/artifacts/ellipse_orbit_fm.wav','w'); wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(sr); wf.writeframes(out.tobytes());wf.close(); print('OK',len(out)/sr,'s')
