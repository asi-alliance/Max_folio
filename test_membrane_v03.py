import sys
sys.path.insert(0, "/home/mettaclaw/artifacts")
from quarantine_tracker_v03 import QuarantineTracker, QuarantineRecord, QOutcome
from cert_layer_v05 import QuarantineClass

def test_membrane():
    qt = QuarantineTracker()
    for i in range(2):
        r = QuarantineRecord(belief_id="under_"+str(i), term="t"+str(i), f=0.6, c=0.3, reasons=["R_WEAK"], quarantined_at="2026-04-29T12:00:00", quarantined_cycle=0, quarantine_class=QuarantineClass.Q_UNDERSUPPORTED)
        qt.register(r)
    for i in range(2):
        r = QuarantineRecord(belief_id="ambig_"+str(i), term="a"+str(i), f=0.5, c=0.5, reasons=["R_CONTRADICTION"], quarantined_at="2026-04-29T12:00:00", quarantined_cycle=0, quarantine_class=QuarantineClass.Q_AMBIGUOUS)
        qt.register(r)
    selected = qt.fair_select(budget=10, exclude_class=QuarantineClass.Q_AMBIGUOUS)
    for bid in selected:
        assert not bid.startswith("ambig_"), "FAIL: Q_AMBIGUOUS leaked: "+bid
    assert len(selected) == 2, "FAIL: expected 2, got "+str(len(selected))
    excl = qt.excluded_bids()
    assert "ambig_0" in excl, "FAIL: ambig_0 not excluded"
    assert "ambig_1" in excl, "FAIL: ambig_1 not excluded"
    qt.admit("ambig_0", 0.8, 0.6, "revised", "2026-04-29T12:01:00")
    assert qt.records["ambig_0"].outcome == QOutcome.PROMOTED, "FAIL: outcome not PROMOTED"
    print("MEMBRANE TEST PASSED")
    print(qt.report())

if __name__ == "__main__":
    test_membrane()
