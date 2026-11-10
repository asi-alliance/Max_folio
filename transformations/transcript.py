import time
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPT = ROOT / "transcript.txt"

def transform(messages, tools):
    ts_str = time.strftime('%Y-%m-%d %H:%M:%S')

    transcript_lines = []

    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")

        if role == "user" and content:
            if any(tag in content for tag in [
                "[irc]",
                "[ALARM]",
                "[NO ADDITIONAL",
                "[TASK COMPLETED",
                "[mattermost]",
                "[terminal]"
            ]):
                transcript_lines.append(f"[{ts_str}] {content}")

        elif role == "assistant":
            tool_calls = msg.get("tool_calls", [])

            for tc in tool_calls:
                if isinstance(tc, dict):
                    fn = tc.get("function", {})
                    name = fn.get("name", "")

                    if name == "send":
                        try:
                            args = json.loads(fn.get("arguments", "{}"))
                            ch = args.get("channel", "")
                            txt = args.get("content", "")
                            transcript_lines.append(f"[{ts_str}] [send -> {ch}] {txt}")
                        except (json.JSONDecodeError, KeyError):
                            pass

    with open(TRANSCRIPT, "w", encoding="utf-8") as f:
        f.write("\n".join(transcript_lines) + "\n")

    return messages, tools
