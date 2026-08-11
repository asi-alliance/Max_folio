import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HISTORY = Path.home() / "PeTTa" / "repos" / "mettaclaw" / "memory" / "history.metta"

def _escape_metta(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")

def transform(messages, tools):
    ts_str = time.strftime('%Y-%m-%d %H:%M:%S')

    history_lines = []

    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")

        if role == "system":
            continue

        elif role == "user":
            if content:
                history_lines.append(
                    '("' + ts_str + '" "HUMAN_MESSAGE: ' + _escape_metta(content) + '")'
                )

        elif role == "assistant":
            if content:
                history_lines.append(
                    '("' + ts_str + '" "ASSISTANT: ' + _escape_metta(content) + '")'
                )

            tool_calls = msg.get("tool_calls", [])

            for tc in tool_calls:
                if isinstance(tc, dict):
                    fn = tc.get("function", {})
                    name = fn.get("name", "")
                    args_str = fn.get("arguments", "{}")

                    history_lines.append(
                        '("' + ts_str + '" "TOOL_CALL: ' + name + " " + _escape_metta(args_str) + '")'
                    )

        elif role == "tool":
            if content:
                history_lines.append(
                    '("' + ts_str + '" "TOOL_RESULT: ' + _escape_metta(content) + '")'
                )

    with open(HISTORY, "a", encoding="utf-8") as f:
        for line in history_lines:
            f.write(line + "\n")

    return messages, tools
