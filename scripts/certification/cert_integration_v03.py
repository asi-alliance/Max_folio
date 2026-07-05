import sys
sys.path.insert(0, "/home/mettaclaw/artifacts")
from cert_integration_v02 import (
    certify_and_track,
    update_existing_ambiguous,
    sweep_tracked_ambiguous,
    consume_evidence_requests,
)

def run_cycle(tracker, kb_atoms, budget=3, cycle=0, thresholds=None, window=5):
    """Orchestrate one full cert integration cycle.
    Returns dict with sweep_actions, consume_actions, and full report metrics."""
    sweep_result = sweep_tracked_ambiguous(tracker, kb_atoms, cycle)
    consume_result = consume_evidence_requests(tracker, budget, cycle, window)
    report = tracker.report(current_cycle=cycle)
    return {
        "cycle": cycle,
        "sweep_actions": sweep_result,
        "consume_actions": consume_result,
        **report,
    }

if __name__ == "__main__":
    print("cert_integration_v03 loaded. run_cycle() available.")
