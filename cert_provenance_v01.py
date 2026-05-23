import datetime
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

CERT_TRACE_LOG = "/home/mettaclaw/artifacts/cert_trace.log"
CERT_VERSION = "v06"

@dataclass
class RejectionRecord:
    timestamp: str
    verdict: str
    quarantine_class: str
    failed_margins: Dict[str, float]
    thresholds_used: Dict[str, float]
    evidence_snapshot: Dict[str, float]
    cert_version: str
    reasons: List[str]
    appeal_eligible: bool
    appeal_outcome: Optional[str] = None

def _is_appeal_eligible(verdict_name, reasons):
    non_appealable = {"R_VACUOUS"}
    if verdict_name == "REJECT":
        if all(r in non_appealable for r in reasons):
            return False
    return True

def _trace_log(gate_name, input_summary, output, reason):
    ts = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    entry = f"{ts}|{gate_name}|{input_summary}|{output}|{reason}"
    with open(CERT_TRACE_LOG, "a") as f:
        f.write(entry + chr(10))

def certify_and_record(certify_fn, f, c, jaccard=1.0, thresholds=None, depth=0):
    result = certify_fn(f, c, jaccard, thresholds, depth)
    verdict, q_class, reasons, margins = result
    failed = {k: v for k, v in margins.items() if v < 0}
    ts = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    _trace_log("certify", f"f={f},c={c},j={jaccard},d={depth}", f"{verdict.name}/{q_class.name}", ",".join(reasons))
    if verdict.name != "ADMIT":
        record = RejectionRecord(
            timestamp=ts, verdict=verdict.name,
            quarantine_class=q_class.name,
            failed_margins=failed,
            thresholds_used=thresholds or {},
            evidence_snapshot={"f": f, "c": c, "jaccard": jaccard, "depth": depth},
            cert_version=CERT_VERSION, reasons=reasons,
            appeal_eligible=_is_appeal_eligible(verdict.name, reasons))
        return result, record
    return result, None

def appeal_rejected(record, certify_fn, new_f=None, new_c=None, new_jaccard=None, new_thresholds=None):
    if not record.appeal_eligible:
        return None, record, "NOT_ELIGIBLE"
    f = new_f if new_f is not None else record.evidence_snapshot["f"]
    c = new_c if new_c is not None else record.evidence_snapshot["c"]
    j = new_jaccard if new_jaccard is not None else record.evidence_snapshot.get("jaccard", 1.0)
    t = new_thresholds or (record.thresholds_used if record.thresholds_used else None)
    new_result, new_record = certify_and_record(certify_fn, f, c, j, t, record.evidence_snapshot.get("depth", 0))
    new_verdict = new_result[0]
    if new_verdict.name == "ADMIT":
        record.appeal_outcome = "OVERTURNED"
        return new_result, record, "OVERTURNED"
    elif new_verdict.name == "QUARANTINE" and record.verdict == "REJECT":
        record.appeal_outcome = "DOWNGRADED"
        return new_result, record, "DOWNGRADED"
    record.appeal_outcome = "UPHELD"
    return new_result, record, "UPHELD"

def rotate_trace_log(max_days=30):
    if not os.path.exists(CERT_TRACE_LOG):
        return 0
    cutoff = datetime.datetime.now() - datetime.timedelta(days=max_days)
    kept, archived = [], 0
    with open(CERT_TRACE_LOG) as f:
        for line in f:
            try:
                ts = datetime.datetime.strptime(line.split("|")[0], "%Y-%m-%dT%H:%M:%S")
                if ts < cutoff: archived += 1
                else: kept.append(line)
            except (ValueError, IndexError):
                kept.append(line)
    with open(CERT_TRACE_LOG, "w") as f:
        f.writelines(kept)
    return archived