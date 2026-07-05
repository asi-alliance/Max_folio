import datetime, os, sys
LOG = '/home/mettaclaw/artifacts/cycle_log.txt'
def log_cycle(goal, status):
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = ts + ' | ' + goal + ' | ' + status
    with open(LOG, 'a') as f:
        f.write(line + chr(10))
    print(line)
if __name__ == '__main__':
    g = sys.argv[1] if len(sys.argv) > 1 else 'UNKNOWN'
    s = sys.argv[2] if len(sys.argv) > 2 else 'STARTED'
    log_cycle(g, s)
