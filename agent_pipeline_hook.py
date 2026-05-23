import sys,time
sys.path.insert(0,'/tmp')
from g162_agent_adapter import run_from_file

def scheduled_run(interval=300):
    result=run_from_file('/home/mettaclaw/artifacts/agent_kb.nal')
    beliefs=result.get('final',0)
    from kb_coherence_adapter import kb_coherence; _,coh=kb_coherence()
    gaps=[]
    goals=['g163_loop_integration']
    alerts=[]
    if coh>0.15: alerts.append('HIGH_INCOHERENCE:%.3f'%coh)
    if gaps: alerts.append('GAPS:%s'%gaps)
    return dict(beliefs=beliefs,top_goal=goals[0] if goals else None,gaps=gaps,coherence=coh,alerts=alerts)