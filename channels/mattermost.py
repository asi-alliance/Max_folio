import os
import json
import time
import subprocess
import sys
import requests
import websocket
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / ".runtime" / "mattermost"
INBOX = RUNTIME / "inbox"
OUTBOX = RUNTIME / "outbox"
PID = RUNTIME / "pid"
DOWNLOADS = RUNTIME / "downloads"

MM_URL = "https://chat.singularitynet.io"
CHANNEL_ID = "8fjrmabjx7gupy7e5kjznpt5qh"
BOT_TOKEN = ""

_headers = {"Authorization": f"Bearer {BOT_TOKEN}"}
_bot_user_id = None
_seen_post_ids = set()


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
        close_fds=True,
    )
    PID.write_text(str(process.pid))


def stop_daemon():
    try:
        pid = int(PID.read_text())
        os.kill(pid, 15)
        time.sleep(0.5)
        try:
            os.kill(pid, 0)
            os.kill(pid, 9)
        except ProcessLookupError:
            pass
        PID.unlink(missing_ok=True)
        return "Mattermost daemon stopped"
    except FileNotFoundError:
        return "No daemon running"
    except Exception as e:
        return f"Error stopping daemon: {e}"


def restart_daemon():
    stop_daemon()
    time.sleep(0.5)
    ensure_daemon()
    return "Mattermost daemon restarted"


def daemon_status():
    try:
        pid = int(PID.read_text())
        os.kill(pid, 0)
        return f"Running (PID {pid})"
    except FileNotFoundError:
        return "Not running"
    except ProcessLookupError:
        return "Not running (stale PID file)"
    except Exception:
        return "Unknown status"

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

def _get_bot_user_id():
    r = requests.get(f"{MM_URL}/api/v4/users/me", headers=_headers)
    return r.json()["id"]

def _get_display_name(user_id):
    r = requests.get(f"{MM_URL}/api/v4/users/{user_id}", headers=_headers)
    u = r.json()
    if u.get("first_name") or u.get("last_name"):
        return f"{u.get('first_name','')} {u.get('last_name','')}".strip()
    return u["username"]

def _download_file(file_id):
    try:
        DOWNLOADS.mkdir(parents=True, exist_ok=True)
        meta_r = requests.get(f"{MM_URL}/api/v4/files/{file_id}/info", headers=_headers)
        meta_r.raise_for_status()
        meta = meta_r.json()
        filename = meta.get("name", file_id)
        dl_r = requests.get(f"{MM_URL}/api/v4/files/{file_id}", headers=_headers)
        dl_r.raise_for_status()
        safe_name = filename.replace("/", "_").replace("\\", "_")
        filepath = DOWNLOADS / safe_name
        filepath.write_bytes(dl_r.content)
        return f"Downloaded: {filepath} ({len(dl_r.content)} bytes)"
    except Exception as e:
        return f"Download failed for {file_id}: {e}"

def daemon():
    global _bot_user_id
    RUNTIME.mkdir(parents=True, exist_ok=True)
    INBOX.mkdir(exist_ok=True)
    OUTBOX.mkdir(exist_ok=True)
    PID.write_text(str(os.getpid()))

    ws_url = MM_URL.replace("https", "wss") + "/api/v4/websocket"
    ws = websocket.WebSocket()
    ws.connect(ws_url, header=[f"Authorization: Bearer {BOT_TOKEN}"])
    _bot_user_id = _get_bot_user_id()
    last_ping = time.time()

    while True:
        # Send outgoing messages from outbox
        for path in sorted(OUTBOX.glob("*")):
            try:
                content = path.read_text()
                path.unlink()
                requests.post(
                    f"{MM_URL}/api/v4/posts",
                    headers=_headers,
                    json={"channel_id": CHANNEL_ID, "message": content},
                )
            except FileNotFoundError:
                pass
        # Receive incoming messages via WebSocket
        try:
            if time.time() - last_ping > 25:
                ws.ping()
                last_ping = time.time()
            ws.settimeout(1)
            event = json.loads(ws.recv())
            if event.get("event") == "posted":
                post = json.loads(event["data"]["post"])
                if post["channel_id"] == CHANNEL_ID and post["user_id"] != _bot_user_id:
                    if post["id"] not in _seen_post_ids:
                        _seen_post_ids.add(post["id"])
                        sender = _get_display_name(post["user_id"])
                        ts = time.strftime('%Y-%m-%d %H:%M:%S')
                        msg = post.get("message", "")
                        # Handle file attachments
                        file_ids = post.get("file_ids", [])
                        download_info = ""
                        if file_ids:
                            dl_results = []
                            for fid in file_ids:
                                dl_results.append(_download_file(fid))
                            download_info = "\n[File downloads: " + " | ".join(dl_results) + "]"
                        (INBOX / str(time.time_ns())).write_text(f"[{ts}] <{sender}> {msg}{download_info}")
        except (websocket.WebSocketTimeoutException, json.JSONDecodeError, KeyError, BlockingIOError, OSError):
            pass
        time.sleep(0.1)


if __name__ == "__main__" and "--daemon" in sys.argv:
    daemon()
