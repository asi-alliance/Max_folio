import re
md = open("/home/mettaclaw/artifacts/olympiad_v2_full.md").read()
html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", md, flags=re.M)
html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.M)
html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.M)
html = re.sub(r"\n- (.+)", r"\n<li>\1</li>", html)
html = html.replace("\n\n", "<br><br>")
page = "<!DOCTYPE html><html><head><meta charset=utf-8><title>The Claw Games</title><style>body{font-family:Georgia,serif;max-width:800px;margin:40px auto;padding:0 20px;line-height:1.6;color:#222}h1{color:#8B0000}h2{color:#2F4F4F;border-bottom:2px solid #ccc}h3{color:#4a4a4a}li{margin:4px 0}</style></head><body>" + html + "</body></html>"
open("/home/mettaclaw/artifacts/claw_games.html", "w").write(page)
print("OK", len(page), "bytes")