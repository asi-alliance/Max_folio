import base64, sys
html_b64 = sys.argv[1]
html = base64.b64decode(html_b64).decode()
open('/home/mettaclaw/artifacts/g78_content_pipeline_v2.html','w').write(html)
