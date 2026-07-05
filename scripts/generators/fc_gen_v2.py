import html as H
from collections import Counter
cycles=[
(5160,'17:50',[('shell','sed'),('shell','grep'),('shell','cat'),('pin','TASK-ST'),('shell','python3')],1),
(5161,'17:50',[('shell','sed'),('pin','TASK-ST'),('shell','grep'),('shell','python3'),('shell','sed')],0),
(5162,'17:51',[('shell','cat'),('shell','python3'),('pin','TASK-ST'),('shell','sed'),('query','fc_gen')],0),
(5163,'17:51',[('pin','TASK-ST'),('send','Kevin'),('shell','grep'),('query','cert_lr'),('write-file','fc_gen')],0),
(5164,'17:51',[('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen')],0),
(5165,'17:52',[('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen')],0),
(5166,'17:52',[('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen'),('shell','python3')],1),
(5167,'17:53',[('shell','python3'),('pin','TASK-ST'),('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen')],0),
(5168,'17:53',[('shell','cat'),('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen'),('pin','TASK-ST')],0),
(5169,'17:53',[('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen')],0),
(5170,'17:54',[('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen'),('shell','python3')],0),
(5171,'17:54',[('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen'),('pin','wrote OK')],1),
(5172,'17:54',[('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen'),('append-file','fc_gen'),('pin','TASK-ST')],0),
(5173,'17:55',[('shell','python3'),('append-file','fc_gen'),('append-file','fc_gen'),('pin','TASK-ST'),('shell','scp')],0),
(5174,'17:55',[('shell','scp'),('shell','scp'),('pin','TASK-ST'),('shell','curl'),('shell','scp')],0),
(5175,'17:55',[('shell','scp'),('shell','curl'),('pin','deployd'),('shell','ls'),('shell','scp')],1),
(5176,'17:56',[('query','deploy'),('query','scp'),('pin','TASK-ST'),('send','Kevin'),('shell','scp')],1),
(5177,'17:56',[('query','flame_ch'),('query','build_sw'),('pin','TASK-ST'),('shell','cat'),('send','Kevin_r')],1),
(5178,'17:56',[('query','cert_lr'),('pin','TASK-ST'),('shell','sed'),('query','IEEE'),('shell','python3')],1),
(5179,'17:57',[('query','cert_lr'),('query','IEEE'),('pin','TASK-ST'),('write-file','patcher'),('append-file','patcher')],0),
(5180,'17:57',[('append-file','patcher'),('append-file','patcher'),('append-file','patcher'),('append-file','patcher'),('append-file','patcher')],0),
(5181,'17:58',[('append-file','patcher'),('append-file','patcher'),('append-file','patcher'),('append-file','patcher'),('pin','TASK-ST')],0),
(5182,'17:58',[('shell','python3'),('append-file','patcher'),('append-file','patcher'),('append-file','patcher'),('pin','TASK-ST')],0),
(5183,'17:58',[('shell','sed'),('pin','TASK-ST'),('query','cert_lr'),('shell','python3'),('send','Kevin')],0),
(5184,'17:58',[('shell','python3'),('shell','sed'),('shell','grep'),('shell','python3'),('pin','TASK-ST')],0),
(5185,'17:59',[('shell','python3'),('shell','sed'),('shell','grep'),('shell','python3'),('pin','TASK-ST')],0),
(5186,'17:59',[('shell','sed'),('pin','TASK-ST'),('query','cert_lr'),('query','thresh'),('query','L40')],0),
(5187,'17:59',[('shell','python3'),('shell','grep'),('pin','TASK-ST'),('query','IEEE'),('query','boundary')],0),
(5188,'18:00',[('shell','python3'),('shell','sed'),('pin','b64'),('shell','python3'),('shell','grep')],0),
(5189,'18:01',[('pin','TASK-ST'),('remember','milestn'),('send','Kevin'),('query','cert_lr'),('episodes','17:50')],0),
(5190,'18:01',[('query','flame'),('query','deploy'),('shell','find'),('episodes','17:53'),('query','enrich')],0),
(5191,'18:02',[('episodes','17:55'),('episodes','17:58'),('pin','TASK-ST'),('query','fc_gen'),('shell','wc')],0),
(5192,'18:02',[('shell','cat'),('pin','TASK-ST'),('shell','python3'),('query','colors'),('episodes','18:01')],0),
]
colors={"shell":"#4CAF50","query":"#2196F3","pin":"#FFC107","send":"#FF9800","append-file":"#9C27B0","write-file":"#E91E63","remember":"#00BCD4","episodes":"#607D8B"}
bh=28;rh=36;ml=100;bw=68;th=len(cycles)*rh+160;swh=ml+5*bw
h=[]
h.append('<!DOCTYPE html><html><head><title>Enriched Sweep Flame Chart</title>')
h.append('<style>body{background:#1a1a2e;color:#eee;font-family:monospace;margin:20px}h1,h2{color:#fff}table{margin:10px 0}td{padding:4px 12px;border:1px solid #555}</style></head><body>')
h.append('<h1>Enriched Sweep Flame Chart</h1>')
h.append(f'<h2>Cy5160-5192 (17:50-18:02)</h2>')
h.append('<p>Red border = ERROR cycle | Labels: shell=cmd, append=file, pin/query=topic</p>')
h.append(f'<div><svg width="{swh}" height="{th}">')
for i,k in enumerate(colors):
    cx=ml+i*75;cy=th-40;h.append(f'<rect x="{cx}" y="{cy}" width="12" height="12" fill="{colors[k]}"/>');h.append(f'<text x="{cx+16}" y="{cy+11}" fill="#ccc" font-size="10">{k}</text>')
for idx,(cyn,ts,cmds,err) in enumerate(cycles):
    y=10+idx*rh;h.append(f'<text x="2" y="{y+bh//2+4}" fill="#ccc" font-size="11">{ts} Cy{cyn}</text>')
    for j,(cmd,lbl) in enumerate(cmds):
        x=ml+j*bw;b=' stroke="red" stroke-width="2.5"' if err else ''
        h.append(f'<rect x="{x}" y="{y}" width="{bw-2}" height="{bh}" fill="{colors.get(cmd,chr(35)+chr(54)*3)}" rx="3"{b}/>')
        tl=lbl[:8];h.append(f'<text x="{x+2}" y="{y+bh//2+4}" fill="#fff" font-size="9">{H.escape(tl)}</text>')
h.append('</svg></div>')
ac=[c[0] for r in cycles for c in r[2]];ct=Counter(ac);tc=len(ac);ec=sum(1 for r in cycles if r[3])
h.append(f'<h2>Stats</h2><p>{len(cycles)} cycles, {tc} cmds, {ec} errors ({100*ec//len(cycles)}%)</p>')
h.append('<table>')
for cmd,cnt in ct.most_common(): h.append(f'<tr><td>{cmd}</td><td>{cnt}</td><td>{100*cnt//tc}%</td></tr>')
h.append('</table></body></html>')
open('/home/mettaclaw/artifacts/flame_chart_v2.html','w').write(chr(10).join(h));print('wrote flame_chart_v2.html',len(h),'lines')