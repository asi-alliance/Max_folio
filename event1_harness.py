import subprocess, re, sys

ROUNDS = [
    {"name": "R1 Deduction", "metta": "(|- ((--> robin bird) (stv 1.0 0.9)) ((--> bird animal) (stv 0.9 0.9)))", "expected_f": 0.9, "expected_c": 0.729, "points": 2},
    {"name": "R2 Abduction", "metta": "(|- ((--> animal mortal) (stv 1.0 0.9)) ((--> sam mortal) (stv 0.8 0.9)))", "expected_f": 0.8, "expected_c": 0.4475, "points": 3},
    {"name": "R3 Revision", "metta": "(|- ((--> cat friendly) (stv 0.9 0.8)) ((--> cat friendly) (stv 0.3 0.9)))", "expected_f": 0.485, "expected_c": 0.929, "points": 3},
    {"name": "R4 Conditional", "metta": "(|- ((==> (--> $1 bird) (--> $1 fly)) (stv 0.8 0.9)) ((--> penguin bird) (stv 1.0 0.9)))", "expected_f": 0.8, "expected_c": 0.648, "points": 4},
    {"name": "R5 Chain", "metta": "(|- ((--> dog mammal) (stv 0.95 0.9)) ((--> mammal animal) (stv 1.0 0.9)))", "expected_f": 0.95, "expected_c": 0.7695, "points": 4},
]

def score_round(r, actual_f, actual_c):
    f_err = abs(r["expected_f"] - actual_f)
    c_err = abs(r["expected_c"] - actual_c)
    if f_err < 0.01 and c_err < 0.05:
        return r["points"]
    elif f_err < 0.05 and c_err < 0.1:
        return r["points"] // 2
    return 0

print("Event 1 Syllogism Sprint - Test Harness v0.1")
print("=" * 50)
total = sum(r["points"] for r in ROUNDS)
print(f"Max possible score: {total}")
print("Harness ready. Feed MeTTa expressions to score agents.")