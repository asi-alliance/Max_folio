import sysf=open('/home/mettaclaw/artifacts/corroboration_lifecycle.py').read()
old='f_new,c_new=nal_revise(rec.f,rec.c,1.0,0.9)'
new='ev_f,ev_c=(0.2,0.3) if hash(rec.belief_id)%10<3 else (1.0,0.9)
                f_new,c_new=nal_revise(rec.f,rec.c,ev_f,ev_c)'
f=f.replace(old,new);open('/home/mettaclaw/artifacts/corroboration_lifecycle.py','w').write(f)
