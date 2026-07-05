import os,time,json
sys_path='/tmp'
COUNTER_FILE='/tmp/agent_cycle_count.json'

def check_trigger(every_n=50,every_sec=300):
    now=time.time()
    if os.path.exists(COUNTER_FILE):
        d=json.load(open(COUNTER_FILE))
    else:
        d=dict(count=0,last_run=0.0)
    d['count']+=1
    fire=(d['count']%every_n==0) or (now-d['last_run']>=every_sec)
    if fire: d['last_run']=now
    json.dump(d,open(COUNTER_FILE,'w'))
    return fire,d['count']