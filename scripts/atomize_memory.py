import re, sys
patterns = [(r"(\w+)\s+(?:is|are)\s+(?:a\s+)?(\w+)", "-->"), (r"(\w+)\s+(?:has|have)\s+(?:a\s+)?(\w+)", "has"), (r"(\w+)\s+(?:causes|leads.to)\s+(\w+)", "causes"), (r"(\w+)\s+(?:makes|creates)\s+(\w+)", "makes"), (r"(\w+)\s+(?:wants|needs)\s+(\w+)", "wants")]
out = sys.argv[1] if len(sys.argv)>1 else "/dev/stdout"
lines = [c.strip() for l in sys.stdin for c in re.split(r"[.;]", l) if c.strip()]
atoms = []
for line in lines:
    for pat, rel in patterns:
        for m in re.finditer(pat, line, re.I):
            atoms.append(f"(({rel} {m.group(1)} {m.group(2)}) (stv 0.9 0.9))")
with open(out, "w") as f:
    f.write("\n".join(atoms))
print(f"Wrote {len(atoms)} atoms to {out}")