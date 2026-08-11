import importlib.util
from pathlib import Path

DESCRIPTION = "Send a message through a communication channel."

def run(channel, content):
    path = Path("channels") / (channel + ".py")
    if not path.is_file():
        return f"Unknown channel: {channel}"
    spec = importlib.util.spec_from_file_location("channel_" + channel, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "send"):
        return f"Channel {channel} cannot send"
    module.send(content)
    return "SUCCESS"
