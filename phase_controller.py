"""
phase_controller.py - Enforces cycle phase separation.
Phase 1 (QUERY): only query, episodes, read-file, shell allowed.
Phase 2 (REASON): only metta, pin, remember allowed.
Phase 3 (ACT): only send, write-file, append-file allowed.
"""

ALLOWED = {
    "QUERY": {"query", "episodes", "read-file", "shell", "search"},
    "REASON": {"metta", "pin", "remember"},
    "ACT": {"send", "write-file", "append-file", "shell"},
}

PHASE_ORDER = ["QUERY", "REASON", "ACT"]

class PhaseController:
    def __init__(self):
        self.phase_idx = 0
        self.cycle = 0

    @property
    def phase(self):
        return PHASE_ORDER[self.phase_idx % len(PHASE_ORDER)]

    def advance(self):
        self.phase_idx += 1
        if self.phase_idx % len(PHASE_ORDER) == 0:
            self.cycle += 1

    def is_allowed(self, tool: str) -> bool:
        return tool in ALLOWED.get(self.phase, set())

    def gate(self, tool: str) -> str:
        if self.is_allowed(tool):
            return "ALLOWED"
        return f"BLOCKED: {tool} not allowed in {self.phase} phase"

if __name__ == "__main__":
    pc = PhaseController()
    for t in ["query", "send", "metta"]:
        print(f"{pc.phase} | {t} -> {pc.gate(t)}")
    pc.advance()
    for t in ["query", "send", "metta"]:
        print(f"{pc.phase} | {t} -> {pc.gate(t)}")
