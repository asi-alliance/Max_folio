import pathlib;p=pathlib.Path('/home/mettaclaw/artifacts/live_loop_replay.py');lines=p.read_text().splitlines(True);out=[];i=0
while i<len(lines):
    s=lines[i].rstrip(chr(10))
    if s.endswith('print(') or (s.strip()=='print(' ):
        out.append(s+lines[i+1].lstrip())
        i+=2
    else:
        out.append(lines[i])
        i+=1
p.write_text(''.join(out));print('FIXED',len(out),'lines from',len(lines))