import html as h; md=open('/home/mettaclaw/artifacts/oma_interview_report.md').read(); lines=md.split('
'); parts=[]; i=0
while i<len(lines):
 l=lines[i]
 if l.startswith('# '): parts.append('<h1>'+h.escape(l[2:])+'</h1>')
 elif l.startswith('## '): parts.append('<h2>'+h.escape(l[3:])+'</h2>')
 elif l.startswith('### '): parts.append('<h3>'+h.escape(l[4:])+'</h3>')
 elif l.startswith('|') and '---' not in l:
  cells=l.split('|')[1:-1]; tag='th' if i+1<len(lines) and '---' in lines[i+1] else 'td'; parts.append('<tr>'+''.join('<'+tag+'>'+h.escape(c.strip())+'</'+tag+'>' for c in cells)+'</tr>')
 elif l.startswith('- '): parts.append('<li>'+h.escape(l[2:])+'</li>')
 elif l.strip(): parts.append('<p>'+h.escape(l)+'</p>')
 i+=1
body='
'.join(parts)
out='<!DOCTYPE html><html><head><meta charset="utf-8"><title>Oma Interview Report 2026-04-22</title><style>body{font-family:monospace;max-width:900px;margin:40px auto;background:#111;color:#0f0;padding:20px}h1,h2,h3{color:#0ff}table{border-collapse:collapse;width:100%}th,td{border:1px solid #0f0;padding:6px;text-align:left}li{margin:4px 0}</style></head><body>'+body+'</body></html>'
open('/home/mettaclaw/artifacts/oma_interview_report.html','w').write(out); print('HTML written',len(out),'bytes')