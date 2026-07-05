f=open('/home/mettaclaw/artifacts/g237_belief_animator_v6.html').read()
if 'function sy' not in f:
 f=f.replace('function draw(cy)','function sy(c){if(c<=0.75){return H-(c/0.75)*(H/2)}else{return(H/2)-((c-0.75)/0.25)*(H/2)}};function draw(cy)',1)
 f=f.replace('H*(1-bt.c)','sy(bt.c)')
 f=f.replace('H*(1-0.99)','sy(0.99)')
 open('/home/mettaclaw/artifacts/g237_belief_animator_v6.html','w').write(f)
 print('INSERTED sy=%d'%f.count('function sy'))
else:
 print('ALREADY EXISTS sy=%d'%f.count('function sy'))