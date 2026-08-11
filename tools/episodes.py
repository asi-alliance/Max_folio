import re
from collections import deque
from datetime import datetime
from pathlib import Path

DESCRIPTION = "Search transcript history for entries around a given timestamp. Returns surrounding context lines."

TS_RE = re.compile(r'^\("(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"')
HISTORY_PATH = Path.home() / "PeTTa" / "repos" / "mettaclaw" / "memory" / "history.metta"

def extract_timestamp(line):
    m = TS_RE.search(line)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

def run(time_string, k=10):
    time_string = time_string.replace(r'\"', '').replace('"', '').strip()
    k = int(k)
    
    if not HISTORY_PATH.is_file():
        return f"No history.metta found at {HISTORY_PATH}"
    
    try:
        target = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return "Invalid time format. Use: YYYY-MM-DD HH:MM:SS"
    
    best_lineno = None
    best_diff = None
    buffer = deque(maxlen=k+1)
    
    with open(HISTORY_PATH, "r", encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, 1):
            buffer.append(line)
            ts = extract_timestamp(line)
            if ts is None:
                continue
            diff = abs((ts - target).total_seconds())
            if best_diff is None or diff < best_diff:
                best_diff = diff
                best_lineno = lineno
    
    if best_lineno is None:
        return f"No timestamped entries found near {time_string}"
    
    # Now seek back to best_lineno and read k lines before and after
    result = []
    with open(HISTORY_PATH, "r", encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, 1):
            if best_lineno - k <= lineno <= best_lineno + k:
                result.append(f"{lineno}:{line[:500]}")
            if lineno > best_lineno + k:
                break
    
    return "".join(result)
