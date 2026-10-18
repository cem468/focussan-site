"""Check the built site through the local preview server (python _araclar/serve.py 8765)."""
import json
import re
import sys
import urllib.error
import urllib.request

BASE = 'http://localhost:8765'
sitemap = urllib.request.urlopen(BASE + '/sitemap.xml').read().decode()
pages = [u.replace('https://focussan.com', '') or '/' for u in re.findall(r'<loc>([^<]+)</loc>', sitemap)]
titles, canon, problems, checked = {}, {}, [], {}


def status(path):
    if path in checked:
        return checked[path]
    try:
        req = urllib.request.Request(BASE + path, method='GET')
        code = urllib.request.urlopen(req).status
    except urllib.error.HTTPError as e:
        code = e.code
    checked[path] = code
    return code


for p in pages:
    html = urllib.request.urlopen(BASE + p).read().decode()
    title = re.search(r'<title>([^<]+)</title>', html).group(1)
    c = re.search(r'<link rel="canonical" href="([^"]+)"', html).group(1)
    titles.setdefault(title, []).append(p)
    canon.setdefault(c, []).append(p)
    if c.replace('https://focussan.com', '') != (p if p != '/' else '/') and not (p == '/' and c == 'https://focussan.com/'):
        problems.append(f'{p}: canonical {c}')
    alts = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', html))
    if set(alts) != {'tr', 'en', 'x-default'}:
        problems.append(f'{p}: hreflang {alts}')
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.S):
        try:
            json.loads(block)
        except Exception as e:
            problems.append(f'{p}: bad JSON-LD {e}')
    if html.count('<section class="page') != 1:
        problems.append(f'{p}: {html.count("<section class=\"page")} page sections')
    if 'href="#/' in html:
        problems.append(f'{p}: hash link left')
    if html.count('<h1') != 1:
        problems.append(f'{p}: {html.count("<h1")} h1')
    refs = set(re.findall(r'(?:href|src|poster)="(/[^"#?]*)', html))
    refs |= {x.split()[0] for m in re.findall(r'(?:srcset|imagesrcset)="([^"]+)"', html) for x in m.split(',')}
    refs |= set(re.findall(r"url\('?(/[^')]+)'?\)", html))
    refs |= set(re.findall(r"'(/media/[^']+)'", html))
    for r in sorted(refs):
        if r.startswith('/') and status(r) != 200:
            problems.append(f'{p}: {r} -> {status(r)}')

for t, ps in titles.items():
    if len(ps) > 1:
        problems.append(f'duplicate title "{t}": {ps}')
for c, ps in canon.items():
    if len(ps) > 1:
        problems.append(f'duplicate canonical {c}: {ps}')
print(f'pages checked: {len(pages)}, distinct resources: {len(checked)}')
print('\n'.join(problems) if problems else 'no problems found')
sys.exit(1 if problems else 0)
