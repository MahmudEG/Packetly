"""Generates the Packetly static site into docs/.

guides.py holds the long-form field guides, pages.py the standalone page copy.
docs/app.js, docs/fx.js, docs/style.css and docs/consent.js are hand-authored and
are not written by this script; everything else under docs/ is generated.
"""
import json, pathlib, html, re
from guides import GUIDES
from pages import INFO
from enrich import enrich
p = pathlib.Path(__file__).parent / 'docs'; p.mkdir(exist_ok=True)
F='https://docs.fortinet.com/document/fortigate/7.4.0/cli-troubleshooting-cheat-sheet/420966/cli-troubleshooting-cheat-sheet'
C='https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9400/software/release/26-x/command_reference/b_26x_9400_cr/interface_and_hardware_commands.html'
specs=[
('FortiGate CLI essentials','Fortinet','Cybersecurity','The everyday commands for finding your way around a FortiGate.','get system status|Identify firmware and device information;get system performance status|Inspect CPU, memory and uptime;get system interface|Inspect interface information;get system arp|Inspect learned IPv4 neighbors;get router info routing-table all|Inspect active routes'),
('Cisco IOS essentials','Cisco','Networking','Get oriented, inspect interfaces, and understand your device.','show version|Identify software and device information;show ip interface brief|Check interface addresses and status;show interfaces|Inspect interface counters;show running-config|Review active configuration;show inventory|List hardware inventory'),
('FortiGate routing & ARP','Fortinet','Networking','Follow a packet from its next hop to the routing table.','get router info routing-table all|Inspect active routes;get system arp|Resolve local neighbors;diagnose ip arp list|Inspect detailed ARP entries;diagnose ip route list|Inspect kernel routes'),
('Cisco interface diagnostics','Cisco','Networking','Find link failures and read the counters that matter.','show ip interface brief|Summarize interface state;show interfaces status|Inspect switch port status;show interfaces counters errors|Inspect switch errors;show interfaces description|Inspect configured descriptions'),
('FortiGate VPN health','Fortinet','Cybersecurity','Inspect IPsec tunnel health and security associations.','get vpn ipsec tunnel summary|Summarize tunnel state;diagnose vpn tunnel list|Inspect IPsec tunnel details;diagnose vpn ike gateway list|Inspect IKE gateways;diagnose vpn ipsec status|Inspect IPsec status'),
('Cisco VLANs & trunks','Cisco','Networking','Understand access VLANs, tagged links, and Layer 2 boundaries.','show vlan brief|Inspect VLAN membership;show interfaces trunk|Inspect trunk status;show interfaces switchport|Inspect switchport settings;show spanning-tree|Inspect spanning tree state'),
('FortiGate HA & system health','Fortinet','Cybersecurity','Check cluster membership and baseline appliance health.','get system ha status|Inspect cluster members;get system performance status|Inspect resource usage;diagnose sys ntp status|Inspect time synchronization;get system status|Identify firmware'),
('Cisco routing basics','Cisco','Networking','Read connected, static, and learned routes with confidence.','show ip route|Inspect IPv4 routes;show ip protocols|Inspect routing protocols;show ip arp|Inspect IPv4 neighbors;show ip interface brief|Inspect interface status'),
('FortiGate session inspection','Fortinet','Cybersecurity','Connect policy decisions with live traffic sessions.','get system session status|Inspect session totals;diagnose sys session stat|Inspect session statistics;diagnose sys session list|Inspect session entries;get system performance status|Inspect appliance load'),
('Cisco neighbor discovery','Cisco','Networking','Map the devices directly connected to your switch.','show cdp neighbors|List Cisco discovery neighbors;show cdp neighbors detail|Inspect neighbor details;show lldp neighbors|List LLDP neighbors;show lldp neighbors detail|Inspect LLDP details'),
('Linux network essentials','Linux','IT fundamentals','A small toolkit for inspecting a Linux host’s network.','ip address show|Inspect interface addresses;ip route show|Inspect routing table;ip neigh show|Inspect neighbors;ss -tuln|Inspect listening TCP and UDP sockets'),
('Cloud network fundamentals','Vendor neutral','Cloud','Connect subnets, routes, security rules, and DNS into one model.','CIDR|An address prefix defines a network range;Subnet|A segment of a virtual network;Route table|Maps destination prefixes to next hops;Security group|Controls permitted traffic for associated resources;Private DNS|Resolves internal service names')]
data=[]
for i,(title,vendor,cat,desc,rows) in enumerate(specs):
 slug=title.lower().replace(' & ','-').replace(' ','-')
 data.append(dict(id=slug,title=title,vendor=vendor,category=cat,description=desc,rows=[x.split('|') for x in rows.split(';')],source=F if vendor=='Fortinet' else C if vendor=='Cisco' else 'https://man7.org/linux/man-pages/man8/ip.8.html' if vendor=='Linux' else 'https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html',level='Beginner',time=4+i%4))
for s in data:
 s['product']='FortiGate' if s['vendor']=='Fortinet' else s['vendor']
 s['updated']='2026-11-01'
data.extend(GUIDES)
enrich(data)

# ===========================================================  site constants
BASE = 'https://packetly.ly'
NAME = 'Packetly'
BLURB = ('Free cheat sheets for IT, cybersecurity and network engineers. '
         'Inspection commands for Windows, Active Directory, Entra ID, Azure, '
         'FortiGate, Cisco, Juniper, Sophos, Ubiquiti, HPE, Dell and Linux, '
         'each with a plain-English walkthrough.')
UPDATED = max(s['updated'] for s in data)

# Search engine ownership verification. Paste the token only (the content="..."
# value from the HTML tag method), then rebuild and push. Empty means no tag.
GOOGLE_VERIFY = 'uyA0gp5cAEzX3VMe_ldHXcZLLz-H3jNKjg9TGF1vplg'
BING_VERIFY = ''

groups = {}
for s in data:
    groups.setdefault(s['category'], []).append(s)
for g in groups.values():
    g.sort(key=lambda x: x['title'])
SLUG = {c: re.sub(r'[^a-z0-9]+', '-', c.lower()).strip('-') for c in groups}
INTRO = {
    'Cloud': 'Cloud references for Azure, AWS, Kubernetes and Terraform: inventory, virtual networks, effective routes, security groups, pod readiness, workspaces and recorded infrastructure state, with practical investigation cases.',
    'Cybersecurity': 'Security inspection references for FortiGate, Sophos and Kali Linux: firewall and cluster health, IPsec tunnels, session and traffic investigation, port discovery and packet analysis.',
    'IT fundamentals': 'Everyday troubleshooting references for Windows and Linux hosts: addressing, DNS resolution, TCP reachability, systemd services, journals, event logs, time synchronization, Git changes and listening sockets.',
    'Identity & Microsoft 365': 'Identity and Microsoft 365 references for Active Directory, Entra ID, Microsoft Graph and Exchange Online: users and groups, replication health, sign-in investigation, mailboxes, message tracing and Group Policy application.',
    'Infrastructure': 'Infrastructure references for servers, storage, databases and automation: HPE and Dell health, Linux capacity, Windows DHCP and SMB, Docker, Ansible, Redis, PostgreSQL and MySQL investigations.',
    'Networking': 'Network references for Cisco, Juniper, FortiGate, HPE Aruba, Ubiquiti, curl and NGINX: interfaces, VLANs, routes, neighbors, ARP, HTTP redirects, TLS certificates and reverse-proxy upstream investigation.',
}
TOPICS = {SLUG[c]: c for c in groups}

e = lambda x: html.escape(str(x), quote=True)
ld = lambda o: '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + '</script>'

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap">')
ICON = ("<link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'"
        " viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='10' fill='%23c6f36b'/%3E%3Cpath"
        " d='M10 28V12h13l6 8-6 8H10m7-10v5h6' fill='none' stroke='%23101310'"
        " stroke-width='3'/%3E%3C/svg%3E\">")
CONSENT = ("<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
           "gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',"
           "ad_personalization:'denied',analytics_storage:'denied',wait_for_update:500});"
           "try{if(localStorage.getItem('packetly-consent')==='granted')gtag('consent','update',"
           "{ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',"
           "analytics_storage:'granted'})}catch(e){}</script>")
GTAG = ('<script async src="https://www.googletagmanager.com/gtag/js?id=G-QG6N52FTQC"></script>'
        "<script>gtag('js',new Date());gtag('config','G-QG6N52FTQC');</script>")
ADS = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'
       '?client=ca-pub-4081538671702116" crossorigin="anonymous"></script>')
ASSETS = ('<link rel="stylesheet" href="/style.css"><script defer src="/data.js"></script>'
          '<script defer src="/app.js"></script><script defer src="/fx.js"></script>'
          '<script defer src="/consent.js"></script>')

ORG = {'@type': 'Organization', '@id': BASE + '/#org', 'name': NAME, 'url': BASE + '/',
       'description': BLURB,
       'logo': {'@type': 'ImageObject', 'url': BASE + '/og.png', 'width': 1200, 'height': 630}}


def body(main, nsheets):
    return ('<body><aside><a class="brand" href="/">\u25b0 <span>packetly<span class="dot">.</span>'
            '</span></a><div class="aside-label">YOUR FIELD GUIDE</div><nav>'
            '<a href="/" class="navlink active">\u25a6 <span>All cheat sheets</span><b>' + str(nsheets) + '</b></a>'
            '<button id="saved">\u25b1 <span>Bookmarks</span><b id="savecount">0</b></button>'
            '<button id="path">\u2341 <span>Learning path</span><small>NEW</small></button></nav>'
            '<div class="aside-label">EXPLORE BY TOPIC</div><nav id="sidecats">' + ''.join('<a class="navlink" href="/topics/' + SLUG[cat] + '/">' + e(cat) + '</a>' for cat in sorted(groups)) + '</nav>'
            '<div class="aside-bottom"><div class="status"><i></i> Built for the real world</div>'
            '<p>Less tab hopping.<br>More problem solving.</p>'
            '<a href="/about/">About Packetly \u2197</a></div></aside>'
            '<div class="workspace"><header><div class="crumb">The knowledge base <span>/</span> '
            '<strong id="crumb">All cheat sheets</strong></div><div class="head-right">'
            '<span class="online">\u25cf Always in your toolkit</span>'
            '<button id="theme" aria-label="Toggle color theme">\u263c</button>'
            '<a class="github" href="/about/">About the project \u2197</a></div></header>'
            '<main id="main">' + main + '</main><footer><a class="brand" href="/">\u25b0 packetly.</a>'
            '<span>Practical knowledge. One sheet away.</span><div>'
            '<a href="/editorial/">Editorial policy</a><a href="/privacy/">Privacy</a>'
            '<a href="/terms/">Terms</a><a href="/contact/">Contact</a></div>'
            '<small>\u00a9 2026 Packetly \u00b7 Independent reference. Not affiliated with vendors.</small>'
            '</footer></div><div id="toast" role="status"></div></body></html>')


def page(title, desc, path, main, extra='', robots=None, ads=True):
    url = BASE + path
    kind = 'article' if path.startswith('/sheets/') else 'website'
    r = robots or 'index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1'
    head = ('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>' + e(title) + '</title>'
            '<meta name="description" content="' + e(desc) + '">'
            '<meta name="robots" content="' + r + '">'
            '<link rel="canonical" href="' + url + '">'
            '<link rel="alternate" type="application/atom+xml" title="Packetly guide updates" href="/feed.xml">'
            '<meta name="theme-color" content="#101310">'
            + ('<meta name="google-site-verification" content="' + GOOGLE_VERIFY + '">'
               if GOOGLE_VERIFY else '')
            + ('<meta name="msvalidate.01" content="' + BING_VERIFY + '">'
               if BING_VERIFY else '')
            +             '<meta property="og:type" content="' + kind + '">'
            '<meta property="og:site_name" content="' + NAME + '">'
            '<meta property="og:locale" content="en_US">'
            '<meta property="og:title" content="' + e(title) + '">'
            '<meta property="og:description" content="' + e(desc) + '">'
            '<meta property="og:url" content="' + url + '">'
            '<meta property="og:image" content="' + BASE + '/og.png">'
            '<meta property="og:image:width" content="1200">'
            '<meta property="og:image:height" content="630">'
            '<meta property="og:image:alt" content="Packetly cheat sheets">'
            '<meta name="twitter:card" content="summary_large_image">'
            '<meta name="twitter:title" content="' + e(title) + '">'
            '<meta name="twitter:description" content="' + e(desc) + '">'
            '<meta name="twitter:image" content="' + BASE + '/og.png">'
            + ICON + FONT + CONSENT + GTAG + (ADS if ads else '') + ASSETS + extra)
    return '<!doctype html><html lang="en"><head>' + head + '</head>' + body(main, len(data))


# ===============================================================  client data
(p / 'data.js').write_text(
    'window.SHEETS=' + json.dumps(data, ensure_ascii=False) + ';'
    'window.PAGES=' + json.dumps(INFO, ensure_ascii=False) + ';'
    'window.TOPICS=' + json.dumps(TOPICS, ensure_ascii=False) + ';'
    'window.TOPIC_INTRO=' + json.dumps(INTRO, ensure_ascii=False) + ';', encoding='utf-8')

# ==================================================================  homepage
home = ('<section><h1>IT, cybersecurity and network cheat sheets</h1>'
        '<p>' + e(BLURB) + '</p>'
        '<p>Every sheet lists the command, what it inspects, and how to read the output, '
        'with a step-by-step walkthrough and a link to the vendor\u2019s own documentation. '
        'All ' + str(len(data)) + ' are free, need no account, and print cleanly.</p>')
home += ('<section class="home-group"><h2>Recently added</h2><ul>'
         + ''.join('<li><a href="/sheets/' + e(s['id']) + '/">' + e(s['title']) + '</a> — ' + e(s['description']) + '</li>' for s in reversed(data[-5:]))
         + '</ul></section>')
for cat in sorted(groups):
    home += ('<div class="home-group"><h2><a href="/topics/' + SLUG[cat] + '/">'
             + e(cat) + ' cheat sheets</a></h2><ul>')
    for s in groups[cat]:
        home += ('<li><a href="/sheets/' + s['id'] + '/">' + e(s['title']) + '</a> \u2014 '
                 + e(s['description']) + '</li>')
    home += '</ul></div>'
home += '</section>'

home_ld = ld({'@context': 'https://schema.org', '@graph': [
    ORG,
    {'@type': 'WebSite', '@id': BASE + '/#site', 'url': BASE + '/', 'name': NAME,
     'description': BLURB, 'inLanguage': 'en', 'publisher': {'@id': BASE + '/#org'}},
    {'@type': 'CollectionPage', '@id': BASE + '/#page', 'url': BASE + '/',
     'name': 'IT, cybersecurity and network cheat sheets', 'description': BLURB,
     'isPartOf': {'@id': BASE + '/#site'}, 'inLanguage': 'en',
     'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(data),
                    'itemListElement': [{'@type': 'ListItem', 'position': i + 1,
                                         'url': BASE + '/sheets/' + s['id'] + '/',
                                         'name': s['title']} for i, s in enumerate(data)]}}]})

(p / 'index.html').write_text(
    page('Packetly \u2014 IT, cybersecurity & network cheat sheets', BLURB, '/', home, home_ld),
    encoding='utf-8')

# =============================================================  sheet pages
for s in data:
    url = BASE + '/sheets/' + s['id'] + '/'
    d = p / 'sheets' / s['id']
    d.mkdir(parents=True, exist_ok=True)

    rel = [x for x in data if x['id'] != s['id'] and x['vendor'] == s['vendor']]
    rel += [x for x in data if x['id'] != s['id'] and x['category'] == s['category'] and x not in rel]
    rel = rel[:4]

    kind = s.get('kind', 'Command')
    label = kind if kind != 'Command' else ('Concept' if s['vendor'] == 'Vendor neutral' else 'Command')

    art = ('<article><nav class="crumbs"><a href="/">All cheat sheets</a><span>/</span>'
           '<a href="/topics/' + SLUG[s['category']] + '/">' + e(s['category']) + '</a>'
           '<span>/</span>' + e(s['title']) + '</nav>'
           '<h1>' + e(s['title']) + ' cheat sheet</h1>'
           '<p>' + e(s['description']) + '</p>')
    if s.get('scope'):
        art += '<p>' + e(s['scope']) + '</p>'
    art += ('<p>Updated <time datetime="' + s['updated'] + '">' + s['updated'] + '</time> \u00b7 '
            + e(s['vendor']) + ' \u00b7 ' + str(s['time']) + ' min read</p>'
            '<table><thead><tr><th>' + e(label) + '</th><th>What it does</th></tr></thead><tbody>'
            + ''.join('<tr><td><code>' + e(a) + '</code></td><td>' + e(b) + '</td></tr>'
                      for a, b in s['rows'])
            + '</tbody></table>')

    if s.get('walkthrough'):
        art += '<h2>Walkthrough</h2><p>' + e(s['prerequisites']) + '</p>'
        for i, ((a, b), step) in enumerate(zip(s['rows'], s['walkthrough']), 1):
            art += ('<section id="step-' + str(i) + '"><h3>Step ' + str(i) + ': ' + e(b) + '</h3>'
                    '<p><code>' + e(a) + '</code></p><p>' + e(step) + '</p></section>')

    case = s['case']
    art += ('<section class="case-study" id="practical-case"><p class="eyebrow">WORKED INCIDENT</p>'
            '<h2>Practical case: ' + e(case['title']) + '</h2>'
            '<p class="case-label">Fictional teaching scenario; observations are examples, not captured production output.</p>'
            '<h3>Situation</h3><p>' + e(case['symptom']) + '</p>'
            '<h3>Investigation sequence</h3>')
    for i, step in enumerate(case['steps'], 1):
        art += ('<section class="step"><h3>' + str(i) + '. ' + e(step['purpose'])
                + '</h3><code>' + e(step['action']) + '</code><p>' + e(step['detail']) + '</p></section>')
    if case.get('evidence'):
        art += '<h3>Example findings</h3><p>' + e(case['evidence']) + '</p>'
    art += ('<h3>Interpret the findings</h3><p>' + e(case['interpretation']) + '</p>'
            '<h3>Verify the outcome</h3><p>' + e(case['verification']) + '</p>')
    if case.get('escalation'):
        art += '<h3>Escalation handoff</h3><p>' + e(case['escalation']) + '</p>'
    art += '</section>'
    for source in s.get('sources', []):
        art += '<p><a href="' + e(source['url']) + '" rel="noopener" target="_blank">' + e(source['label']) + '</a></p>'
    art += ('<p><a href="' + e(s['source']) + '" rel="nofollow noopener" target="_blank">'
            + e(s.get('sourceLabel', 'Official documentation')) + '</a></p>')
    if rel:
        art += ('<nav class="related-static"><h2>Related cheat sheets</h2><ul>'
                + ''.join('<li><a href="/sheets/' + x['id'] + '/">' + e(x['title']) + '</a></li>'
                          for x in rel) + '</ul></nav>')
    art += '</article>'

    graph = [
        {'@type': 'TechArticle', '@id': url + '#article', 'headline': s['title'] + ' cheat sheet',
         'description': s['description'], 'datePublished': '2026-11-01', 'dateModified': s['updated'],
         'inLanguage': 'en', 'url': url, 'mainEntityOfPage': url,
         'author': {'@id': BASE + '/#org'}, 'publisher': {'@id': BASE + '/#org'},
         'about': s['product'], 'keywords': ', '.join(
             [s['title'], s['product'], s['category'], 'cheat sheet', 'commands']),
         'proficiencyLevel': s.get('level', 'Beginner'),
         'citation': list(dict.fromkeys([s['source']] + [ref['url'] for ref in s.get('sources', [])])),
         'image': BASE + '/og.png'},
        ORG,
        {'@type': 'BreadcrumbList', '@id': url + '#crumbs', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'All cheat sheets', 'item': BASE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': s['category'],
             'item': BASE + '/topics/' + SLUG[s['category']] + '/'},
            {'@type': 'ListItem', 'position': 3, 'name': s['title']}]},
    ]
    if s.get('walkthrough'):
        graph.append({'@type': 'HowTo', '@id': url + '#howto',
                      'name': s['title'] + ' walkthrough',
                      'description': s['description'], 'totalTime': 'PT' + str(s['time']) + 'M',
                      'inLanguage': 'en',
                      'step': [{'@type': 'HowToStep', 'position': i, 'name': b, 'text': step,
                                'url': url + '#step-' + str(i)}
                               for i, ((a, b), step) in enumerate(zip(s['rows'], s['walkthrough']), 1)]})

    (d / 'index.html').write_text(
        page(s['title'] + ' cheat sheet | Packetly', s['description'],
             '/sheets/' + s['id'] + '/', art,
             ld({'@context': 'https://schema.org', '@graph': graph})), encoding='utf-8')

# A standards-based update feed using actual editorial dates, not build time.
from xml.etree.ElementTree import Element, SubElement, ElementTree, register_namespace
register_namespace('', 'http://www.w3.org/2005/Atom')
def atom(parent, name, text=None, **attrs):
    node = SubElement(parent, '{http://www.w3.org/2005/Atom}' + name, attrs)
    node.text = text
    return node
feed = Element('{http://www.w3.org/2005/Atom}feed')
atom(feed, 'id', BASE + '/')
atom(feed, 'title', 'Packetly guide updates')
atom(feed, 'link', href=BASE + '/feed.xml', rel='self')
atom(feed, 'link', href=BASE + '/')
atom(feed, 'updated', max(s['updated'] for s in data) + 'T00:00:00Z')
atom(atom(feed, 'author'), 'name', 'Packetly')
for s in sorted(data, key=lambda s: (s['updated'], s['id']), reverse=True):
    entry = atom(feed, 'entry')
    atom(entry, 'id', BASE + '/sheets/' + s['id'] + '/')
    atom(entry, 'title', s['title'] + ' cheat sheet')
    atom(entry, 'link', href=BASE + '/sheets/' + s['id'] + '/')
    atom(entry, 'updated', s['updated'] + 'T00:00:00Z')
    atom(entry, 'summary', s['description'])
ElementTree(feed).write(p / 'feed.xml', encoding='utf-8', xml_declaration=True)

# ==============================================================  info pages
INFO_DESC = {
    'about': 'What Packetly is, who it is for, and how the cheat sheets are put together.',
    'editorial': 'How Packetly sources, scopes and revises its command references.',
    'privacy': 'What Packetly stores, what Google Analytics and AdSense collect, and how to opt out.',
    'terms': 'Terms of use for Packetly\u2019s educational command references.',
    'contact': 'How to report an error in a cheat sheet or request a new reference.',
}
for name, copy in INFO.items():
    title, paras = copy[0], copy[1:]
    d = p / name
    d.mkdir(exist_ok=True)
    art = ('<article class="detail prose"><nav class="crumbs"><a href="/">All cheat sheets</a>'
           '<span>/</span>' + e(name.capitalize()) + '</nav><h1>' + e(title) + '</h1>'
           + ''.join('<p>' + e(x) + '</p>' for x in paras) + '</article>')
    crumbs = ld({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'All cheat sheets', 'item': BASE + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': title}]})
    (d / 'index.html').write_text(
        page(title.rstrip('.') + ' | Packetly', INFO_DESC[name], '/' + name + '/', art, crumbs),
        encoding='utf-8')

# ===============================================================  hubs
for cat in sorted(groups):
    slug, sheets_in = SLUG[cat], groups[cat]
    path = '/topics/%s/' % slug
    url = BASE + path
    d = p / 'topics' / slug
    d.mkdir(parents=True, exist_ok=True)
    title = cat + ' cheat sheets'
    desc = INTRO[cat]

    art = ('<article><nav class="crumbs"><a href="/">All cheat sheets</a><span>/</span>'
           + e(cat) + '</nav><h1>' + e(title) + '</h1><p>' + e(desc) + '</p>'
           '<p>' + str(len(sheets_in)) + ' free reference'
           + ('s' if len(sheets_in) != 1 else '') + ' in this topic. Each lists the command, '
           'what it inspects and how to read the result.</p><ul>')
    for s in sheets_in:
        art += ('<li><a href="/sheets/' + s['id'] + '/">' + e(s['title']) + '</a> \u2014 '
                + e(s['description']) + '</li>')
    art += ('</ul><nav class="related-static"><h2>Other topics</h2><ul>'
            + ''.join('<li><a href="/topics/' + SLUG[c] + '/">' + e(c) + ' cheat sheets</a></li>'
                      for c in sorted(groups) if c != cat)
            + '</ul></nav></article>')

    hub_ld = ld({'@context': 'https://schema.org', '@graph': [
        {'@type': 'CollectionPage', '@id': url + '#page', 'url': url, 'name': title,
         'description': desc, 'inLanguage': 'en', 'isPartOf': {'@id': BASE + '/#site'},
         'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(sheets_in),
                        'itemListElement': [{'@type': 'ListItem', 'position': i + 1,
                                             'url': BASE + '/sheets/' + s['id'] + '/',
                                             'name': s['title']}
                                            for i, s in enumerate(sheets_in)]}},
        {'@type': 'BreadcrumbList', '@id': url + '#crumbs', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'All cheat sheets', 'item': BASE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': cat}]}]})

    (d / 'index.html').write_text(
        page(title + ' | Packetly', desc, path, art, hub_ld), encoding='utf-8')

# ===============================================  robots, sitemap, llms.txt
AI_BOTS = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-User',
           'Claude-SearchBot', 'PerplexityBot', 'Perplexity-User', 'Google-Extended',
           'Applebot-Extended', 'CCBot', 'Amazonbot', 'meta-externalagent', 'Bingbot']
robots = 'User-agent: *\nAllow: /\n\n'
robots += ''.join('User-agent: %s\nAllow: /\n\n' % b for b in AI_BOTS)
robots += 'Sitemap: %s/sitemap.xml\n' % BASE
(p / 'robots.txt').write_bytes(robots.encode('utf-8'))

urls = ([('/', UPDATED)]
        + [('/topics/%s/' % SLUG[c], max(s['updated'] for s in groups[c]))
           for c in sorted(groups)]
        + [('/sheets/%s/' % s['id'], s['updated']) for s in data]
        + [('/%s/' % n, UPDATED) for n in INFO])
(p / 'sitemap.xml').write_bytes(
    ('<?xml version="1.0" encoding="UTF-8"?>'
     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
     + ''.join('<url><loc>%s%s</loc><lastmod>%s</lastmod></url>' % (BASE, u, m) for u, m in urls)
     + '</urlset>').encode('utf-8'))

llms = ['# Packetly', '', '> ' + BLURB, '',
        'Packetly publishes %d command references for IT, cybersecurity and network engineers. '
        'Each sheet pairs a command with what it inspects and how to interpret the output, '
        'and links to the vendor documentation it is based on. Content is editorial, '
        'not vendor certification material.' % len(data), '', '## Cheat sheets', '']
for cat in sorted(groups):
    llms.append('### [%s cheat sheets](%s/topics/%s/)' % (cat, BASE, SLUG[cat]))
    llms.append('')
    llms.append(INTRO[cat])
    llms.append('')
    for s in groups[cat]:
        llms.append('- [%s](%s/sheets/%s/): %s' % (s['title'], BASE, s['id'], s['description']))
    llms.append('')
llms += ['## About', '']
llms += ['- [%s](%s/%s/): %s' % (INFO[n][0].rstrip('.'), BASE, n, INFO_DESC[n]) for n in INFO]
(p / 'llms.txt').write_bytes(('\n'.join(llms) + '\n').encode('utf-8'))

# ===========================================================  sharing image
try:
    from PIL import Image, ImageDraw, ImageFont

    def font(size, bold=True):
        for path in ['C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',
                     'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',
                     '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']:
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
        return ImageFont.load_default()

    img = Image.new('RGB', (1200, 630), '#111411')
    dr = ImageDraw.Draw(img)
    dr.rounded_rectangle([80, 78, 152, 150], 18, fill='#c3ed7a')
    dr.polygon([(97, 131), (124, 97), (139, 97), (112, 131)], fill='#111411')
    dr.text((176, 114), 'packetly.', font=font(58), fill='#edf0e8', anchor='lm')
    dr.text((80, 250), 'Less searching.', font=font(86), fill='#edf0e8')
    dr.text((80, 346), 'More solving.', font=font(86), fill='#c3ed7a')
    dr.text((80, 492), 'IT  \u00b7  CYBERSECURITY  \u00b7  NETWORKING  \u00b7  CLOUD',
            font=font(26, False), fill='#8c9681')
    dr.text((80, 540), '%d free cheat sheets \u00b7 packetly.ly' % len(data),
            font=font(26, False), fill='#8c9681')
    dr.rectangle([0, 622, 1200, 630], fill='#c3ed7a')
    img.save(p / 'og.png', optimize=True)
    print('og.png written')
except ImportError:
    print('Pillow missing: keeping the existing og.png')

# ======================================================  GitHub Pages extras
(p / 'ads.txt').write_bytes(b'google.com, pub-4081538671702116, DIRECT, f08c47fec0942fa0' + bytes([10]))
(p / 'CNAME').write_bytes(b'packetly.ly')
(p / '.nojekyll').write_text('', encoding='utf-8')

nf = ('<article class="detail prose"><h1>That page is not in the library.</h1>'
      '<p>The address may have changed or the sheet may have been renamed.</p>'
      '<p><a href="/">Back to all cheat sheets</a></p></article>')
(p / '404.html').write_text(
    page('Page not found | Packetly', 'That page is not in the library.', '/404.html', nf,
         robots='noindex,follow', ads=False)
    .replace('<script defer src="/data.js"></script>', '')
    .replace('<script defer src="/app.js"></script>', ''), encoding='utf-8')

print('built %d sheets + %d hubs + %d pages' % (len(data), len(groups), len(INFO)))
