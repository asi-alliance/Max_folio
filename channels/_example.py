import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / ".runtime" / "example"
INBOX = RUNTIME / "inbox"
OUTBOX = RUNTIME / "outbox"
PID = RUNTIME / "pid"

def ensure_daemon():
    RUNTIME.mkdir(parents=True, exist_ok=True)
    INBOX.mkdir(exist_ok=True)
    OUTBOX.mkdir(exist_ok=True)
    try:
        os.kill(int(PID.read_text()), 0)
        return
    except Exception:
        pass
    process = subprocess.Popen(
        [sys.executable, __file__, "--daemon"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True
    )
    PID.write_text(str(process.pid))

def receive():
    ensure_daemon()
    messages = []
    for path in sorted(INBOX.glob("*")):
        try:
            messages.append(path.read_text())
            path.unlink()
        except FileNotFoundError:
            pass
    return "\n".join(messages)

def send(content):
    ensure_daemon()
    (OUTBOX / str(time.time_ns())).write_text(content)

def daemon():
    RUNTIME.mkdir(parents=True, exist_ok=True)
    INBOX.mkdir(exist_ok=True)
    OUTBOX.mkdir(exist_ok=True)
    PID.write_text(str(os.getpid()))
    while True:
        # Maintain persistent connection/state here.
        for path in sorted(OUTBOX.glob("*")):
            try:
                content = path.read_text()
                path.unlink()
                # Send content to external service here.
            except FileNotFoundError:
                pass
        # When an external message arrives:
        #
        # (INBOX / str(time.time_ns())).write_text(message)
        time.sleep(0.1)

if __name__ == "__main__" and "--daemon" in sys.argv:
    daemon()
