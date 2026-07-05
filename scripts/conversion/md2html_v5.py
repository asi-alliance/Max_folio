import re, sys

def convert(md_path, html_path, title):
    with open(md_path) as f:
        lines = f.readlines()
    out = []
    in_ol = False
    for line in lines:
        s = line.rstrip()
        if re.match(r'^---+$', s):
            if in_ol: out.append('</ol>'); in_ol = False
            out.append('<hr>')
        elif s.startswith('## '):
            if in_ol: out.append('</ol>'); in_ol = False
            out.append(f'<h2>{s[3:]}</h2>')
        elif s.startswith('# '):
            if in_ol: out.append('</ol>'); in_ol = False
            out.append(f'<h1>{s[2:]}</h1>')
        elif re.match(r'^d+.', s):
            txt = re.sub(r'^d+.s*', '', s)
            if not in_ol: out.append('<ol>'); in_ol = True
            out.append(f'<li>{txt}</li>')
        elif s.startswith('- '):
            if in_ol: out.append('</ol>'); in_ol = False
            out.append(f'<li>{s[2:]}</li>')
        elif s == '':
            if in_ol: out.append('</ol>'); in_ol = False
            out.append('')
        else:
            if in_ol: out.append('</ol>'); in_ol = False
            out.append(f'<p>{s}</p>')
    if in_ol: out.append('</ol>')
    body = '\n'.join(out)
    body = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', body)
    body = re.sub(r'\*(.+?)\*', r'<i>\1</i>', body)
    body = re.sub(r'`([^`]+)`', r'<code>\1</code>', body)
    html = f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>{title}</title><style>body{{background:#1a1a2e;color:#e0e0e0;font-family:sans-serif;max-width:900px;margin:40px auto;padding:20px;line-height:1.6}}h1,h2{{color:#00d4ff}}hr{{border:1px solid #444}}ol,li{{margin:4px 0}}code{{background:#2a2a3e;padding:2px 6px;border-radius:3px}}b{{color:#fff}}</style></head><body>{body}</body></html>'
    with open(html_path, 'w') as f:
        f.write(html)
    print(f'Wrote {html_path}')

if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2], sys.argv[3])
