# Flame chart generator - complete
cycles=[(5160,'17:50',['shell','shell','shell','pin','shell'],1),(5161,'17:50',['shell','pin','shell','shell','shell'],0),(5162,'17:51',['shell','shell','pin','shell','query'],0),(5163,'17:51',['pin','send','shell','query','write-file'],0),(5164,'17:51',['append-file']*4,0),(5165,'17:52',['append-file']*5,0),(5166,'17:52',['append-file']*4+'shell'.split(),1),(5167,'17:53',['shell','pin','append-file','append-file','append-file'],0),(5168,'17:53',['shell','append-file','append-file','append-file','pin'],0),(5169,'17:53',['append-file']*5,0),(5170,'17:54',['append-file']*4+['shell'],0),(5171,'17:54',['append-file']*4+['pin'],1),(5172,'17:54',['append-file']*4+['pin'],0),(5173,'17:55',['shell','append-file','append-file','pin','shell'],0),(5174,'17:55',['shell']*2+['pin']+['shell']*2,0),(5175,'17:55',['shell']*2+['pin']+['shell']*2,1),(5176,'17:56',['query']*2+['pin','send','shell'],1),(5178,'17:56',['query','pin','shell','query','shell'],1),(5179,'17:57',['query']*2+['pin','write-file','append-file'],0),(5180,'17:57',['append-file']*5,0),(5181,'17:58',['append-file']*4+['pin'],0),(5182,'17:58',['shell']+['append-file']*3+['pin'],0),(5183,'17:58',['shell','pin','query','shell','send'],0),(5184,'17:58',['shell']*4+['pin'],0),(5185,'17:59',['shell']*4+['pin'],0),(5186,'17:59',['shell','pin','query','query','query'],0),(5187,'17:59',['shell']*2+['pin','query','query'],0),(5188,'18:00',['shell']*2+['pin']+['shell']*2,0),(5189,'18:01',['pin','remember','send','query','episodes'],0),(5190,'18:01',['query']*2+['shell','episodes','query'],0),(5191,'18:02',['episodes']*2+['pin','query','shell'],0),(5192,'18:02',['shell','pin','shell','query','episodes'],0)]
colors={'shell':'#4CAF50','query':'#2196F3','pin':'#FFC107','send':'#FF9800','append-file':'#9C27B0','write-file':'#E91E63','remember':'#00BCD4','episodes':'#607D8B'}
bh=28;rh=36;ml=80;bw=35;th=len(cycles)*rh+100;swh=ml+5*bw;40
h=[]
h.append('<!DOCTYPE html><html><head><title>Sweep Flame Chart</title>')
h.append('<style>body{background:#1a1a2e;color:#eee;font-family:monospace;margin:20px}h1,h2{color:#fff}</style></head><body>')
h.append('<h1>🔥 Sweep Attempt Flame Chart</h1>')
h.append('<h2>Cy5160-5192 (17:50-18:02)</h2>')
h.append('<p>Red border = ERROR_FEEDBACK cycle</p>')
h.append(f'<svg width="{swh}" height="{th}">')
for idx,(cy,ts,cmds,err) in enumerate(cycles):
    y=10+idx*rh
    h.append(f'<text x="2" y="{y+bh//2+4}" fill="#ccc" font-size="11">{ts} Cy{cy}</text>')
    for j,cmd in enumerate(cmds):
        x=ml+j*bw;b=' stroke="red" stroke-width="2.5"' if err else ''
        h.append(f'<rect x="{x}" y="{y}" width="{bw-2}" height="{bh}" fill="{colors.get(cmd,"#666")}" rx="3"{b}/>')
h.append('</svg>')
from collections import Counter
ac=[c for r in cycles for c in r[2]];ct=Counter(ac);tc=len(ac);ec=sum(1 for r in cycles if r[3])
h.append(f'<h2>Stats</h2><p>{len(cycles)} cycles, {tc} cmds, {ec} errors ({100*ec//len(cycles)}%)</p>')
h.append('<table style="border-collapse:collapse">')
for cmd,cnt in ct.most_common():
    h.append(f'<tr><td style="padding:4px 12px;border:1px solid #555">{cmd}</td><td style="padding:4px 12px;border:1px solid #555">{cnt}</td><td style="padding:4px 12px;border:1px solid #555">{100*cnt//tc}%</td></tr>')
h.append('</table><p>Base64 strategy at Cy5188 solved quote hell in 1 cycle.</p></body></html>')
open('/home/mettaclaw/artifacts/flame_chart.html','w').write('\n'.join(h))
print('wrote flame_chart.html', len(h), 'lines')