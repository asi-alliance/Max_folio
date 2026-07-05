import pathlib;p=pathlib.Path('/home/mettaclaw/artifacts/live_loop_replay.py');lines=p.read_text().splitlines(True);out=[];i=0;exec("while i<len(lines):
 s=lines[i].rstrip(chr(10))
 if i+1<len(lines) and s.endswith(chr(40)+chr(39)):
  out.append(s+lines[i+1].lstrip());i+=2
 else:
  out.append(lines[i]);i+=1
");p.write_text(''.join(out));print('JOINED',len(lines),'->',len(out))