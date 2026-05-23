lines = open("/home/mettaclaw/artifacts/g160_v27_pipeline.py").readlines()
lines.insert(132, "    objs = {a[1] for a in atoms if len(a) >= 4}
")
lines.insert(133, "    leaves = {a[0] for a in atoms if len(a) >= 4} - objs
")
