import sys
beliefs = []
bid = 0
files = ["persistent_atoms.metta", "max_kb.metta"]
for fp in ["/home/mettaclaw/artifacts/persistent_atoms.metta", "/home/mettaclaw/artifacts/max_kb.metta"]:
    with open(fp) as fh:
        for line in fh:
            if "stv " not in line: continue
            idx = line.find("stv ") + 4
            rest = line[idx:].replace(")", " ").split()
            if len(rest) < 2: continue
            f, c = float(rest[0]), float(rest[1])
            j = line.find("-->")
            if j < 0: j = line.find("==>")
            if j < 0: continue
            term = line[j:line.find(")", j)]
            beliefs.append(("b" + str(bid), term.strip(), f, c))
            bid += 1
for b in beliefs: print(b)
print("TOTAL:", len(beliefs), "beliefs extracted")
