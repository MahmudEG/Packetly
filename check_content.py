"""Content and SEO assertions. Run after build.py, before pushing."""
import json, pathlib, re, xml.etree.ElementTree as ET

p = pathlib.Path('docs')
raw = (p / 'data.js').read_text(encoding='utf-8')
cut = raw.index(';window.PAGES=')
sheets = json.loads(raw[len('window.SHEETS='):cut])
pages = json.loads(raw[cut + len(';window.PAGES='):-1])

BASE = 'https://packetly.ly'
INFO = ['about', 'editorial', 'privacy', 'terms', 'contact']

# ---- content ----------------------------------------------------------
assert len(sheets) == 39, len(sheets)
assert len({s['id'] for s in sheets}) == 39
required = {'Windows', 'Active Directory', 'Microsoft Graph', 'Entra ID', 'Exchange Online',
            'Azure', 'FortiGate', 'Sophos', 'Cisco', 'Juniper', 'Ubiquiti', 'HPE', 'Dell',
            'Dell Data Domain'}
assert required <= {s['product'] for s in sheets}
assert set(pages) == set(INFO), set(pages)
assert all(len(v) >= 3 for v in pages.values())

read = lambda rel: (p / rel).read_text(encoding='utf-8')


def head_of(html_text):
    return html_text[html_text.index('<head>'):html_text.index('</head>')]


# ---- every indexable page carries the full head ------------------------
titles, descs = set(), set()
for rel, path in ([('index.html', '/')]
                  + [('sheets/%s/index.html' % s['id'], '/sheets/%s/' % s['id']) for s in sheets]
                  + [('%s/index.html' % n, '/%s/' % n) for n in INFO]):
    page = read(rel)
    head = head_of(page)
    assert '<link rel="canonical" href="%s%s">' % (BASE, path) in head, rel
    assert 'og:url" content="%s%s"' % (BASE, path) in head, rel
    assert 'twitter:card" content="summary_large_image"' in head, rel
    assert 'max-image-preview:large' in head, rel
    assert BASE + '/og.png' in head, rel
    assert '@import' not in page and 'fonts.googleapis.com/css2' in head, rel
    t = re.search(r'<title>(.*?)</title>', head).group(1)
    d = re.search(r'<meta name="description" content="(.*?)">', head).group(1)
    assert t not in titles, 'duplicate title: ' + t
    assert d not in descs, 'duplicate description on ' + rel
    titles.add(t)
    descs.add(d)
    # og/twitter must track the page, not the site default
    assert 'og:title" content="%s"' % t in head, rel

# ---- sheet bodies ------------------------------------------------------
for s in sheets:
    page = read('sheets/%s/index.html' % s['id'])
    body = page[page.index('<main'):]
    assert s['source'].startswith('https://')
    assert '<thead>' in body and '<tbody>' in body
    assert 'class="crumbs"' in body
    assert 'related-static' in body
    assert '"@type": "BreadcrumbList"' in page
    assert '"@type": "TechArticle"' in page
    assert '<p></p>' not in body, 'empty paragraph in ' + s['id']
    if s.get('walkthrough'):
        assert len(s['walkthrough']) == len(s['rows']) == 4
        assert all(len(step) > 90 for step in s['walkthrough'])
        assert 'Walkthrough' in body and s['updated'] in page
        assert '"@type": "HowTo"' in page
        assert 'id="step-4"' in body

# ---- info pages are server-rendered, not empty shells ------------------
for n in INFO:
    body = read('%s/index.html' % n)
    body = body[body.index('<main'):body.index('</main>')]
    # guards the regression where these rendered as empty <main> shells
    assert len(body) > 450, '%s is an empty shell (%d chars)' % (n, len(body))
    assert pages[n][1][:60] in body, n

# ---- homepage ----------------------------------------------------------
home = read('index.html')
assert '"@type": "CollectionPage"' in home and '"@type": "ItemList"' in home
assert '"@type": "Organization"' in home and '"@type": "WebSite"' in home
for s in sheets:
    assert '/sheets/%s/' % s['id'] in home, 'homepage does not link ' + s['id']

# ---- sitemap, robots, llms, assets -------------------------------------
root = ET.parse(p / 'sitemap.xml').getroot()
ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
assert len(root) == 45, len(root)
assert all(u.find(ns + 'lastmod') is not None for u in root)
locs = {u.find(ns + 'loc').text for u in root}
assert locs == {BASE + '/'} | {BASE + '/sheets/%s/' % s['id'] for s in sheets} \
       | {BASE + '/%s/' % n for n in INFO}

robots = read('robots.txt')
for bot in ['GPTBot', 'ClaudeBot', 'PerplexityBot', 'Google-Extended', 'OAI-SearchBot']:
    assert 'User-agent: %s' % bot in robots, bot
assert 'Sitemap: %s/sitemap.xml' % BASE in robots

llms = read('llms.txt')
assert llms.startswith('# Packetly')
for s in sheets:
    assert '/sheets/%s/' % s['id'] in llms, 'llms.txt missing ' + s['id']

assert (p / 'og.png').stat().st_size > 5000
assert (p / 'CNAME').read_bytes() == b'packetly.ly'
assert (p / '.nojekyll').exists()
assert 'noindex' in head_of(read('404.html'))
assert 'adsbygoogle' not in read('404.html')
assert 'reports.js' not in home

print('PASS: %d sheets, %d pages, unique titles/descriptions, canonical + OG + Twitter on all 45 '
      'URLs, structured data, crumbs, related links, sitemap lastmod, AI crawler rules, llms.txt, '
      'og.png.' % (len(sheets), len(pages)))
