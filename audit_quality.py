"""Reproducible technical publishing checks, not a promise of AdSense approval."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import json
import re
from foundation_review import REVIEWS

root = Path('docs')
expected = b'google.com, pub-4081538671702116, DIRECT, f08c47fec0942fa0\n'
assert (root / 'ads.txt').read_bytes() == expected, 'Unexpected ads.txt seller, format or encoding'
raw = (root / 'data.js').read_text(encoding='utf-8')
sheets = json.loads(raw.split('window.SHEETS=', 1)[1].split(';window.PAGES=', 1)[0])

class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_sources = False
        self.source_links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'section' and attrs.get('class') == 'sources':
            self.in_sources = True
        for key in ('href', 'src'):
            url = attrs.get(key, '')
            if url.startswith('/') and not url.startswith('//'):
                local = url.split('?', 1)[0].split('#', 1)[0]
                target = root / local.lstrip('/')
                if local.endswith('/'):
                    target /= 'index.html'
                assert target.exists(), f'Missing local target {url}'
        if self.in_sources and tag == 'a' and attrs.get('href', '').startswith('https://'):
            self.source_links.append(attrs['href'])

    def handle_endtag(self, tag):
        if tag == 'section':
            self.in_sources = False

for sheet in sheets:
    body = (root / 'sheets' / sheet['id'] / 'index.html').read_text(encoding='utf-8')
    parser = PageLinks()
    parser.feed(body)
    assert parser.source_links and len(set(parser.source_links)) == len(parser.source_links), sheet['id']
    assert sheet['source'] in parser.source_links, sheet['id']
    assert 'Fictional teaching scenario' in body, sheet['id']
    if sheet['id'] in REVIEWS:
        case = sheet['case']
        assert all(case.get(field) for field in ('evidence', 'interpretation', 'verification', 'escalation'))
        assert all(step['detail'] not in sheet['walkthrough'] for step in case['steps']), sheet['id']
        assert sheet['updated'] == '2026-11-25'
    assert len(re.findall(r'adsbygoogle\.js\?client=ca-pub-4081538671702116', body)) == 1
    assert 'google-adsense-account" content="ca-pub-4081538671702116"' in body

for page in root.rglob('*.html'):
    PageLinks().feed(page.read_text(encoding='utf-8'))

assert 'Disallow: /' not in (root / 'robots.txt').read_text(encoding='utf-8')
print(f'PASS: ads.txt bytes and matching publisher ID; {len(sheets)} guides; {len(REVIEWS)} expanded cases; unique primary references; local links/assets; labeled examples')
print('LIMIT: checks do not verify live HTTP responses, external link uptime, command execution on vendor platforms, or editorial originality against the entire web.')
