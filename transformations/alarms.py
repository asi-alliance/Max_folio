import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALARMS_DIR = ROOT / "memory" / "alarms"

def transform(messages, tools):
    ALARMS_DIR.mkdir(parents=True, exist_ok=True)
    now = time.time()

    for alarm_file in sorted(ALARMS_DIR.glob("*")):
        try:
            target_time = float(alarm_file.name)
        except ValueError:
            continue

        if now >= target_time:
            content = alarm_file.read_text().strip()
            lines = content.split("\n", 1)

            if len(lines) == 2:
                channel, msg = lines
            else:
                channel, msg = "terminal", content

            alarm_file.unlink()

            messages.append({
                "role": "user",
                "content": f"Step {time.strftime('%Y-%m-%d %H:%M:%S')}: [{channel}] [ALARM] {msg}"
            })

    return messages, tools
