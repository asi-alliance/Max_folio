import select
import sys

def receive():
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.readline().strip()
    return ""

def send(content):
    print(content)
