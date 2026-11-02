import json,pathlib,xml.etree.ElementTree as ET
p=pathlib.Path('docs');sheets=json.loads((p/'data.js').read_text()[14:-1])
assert len(sheets)==39
assert len({s['id'] for s in sheets})==39
required={'Windows','Active Directory','Microsoft Graph','Entra ID','Exchange Online','Azure','FortiGate','Sophos','Cisco','Juniper','Ubiquiti','HPE','Dell','Dell Data Domain'}
assert required <= {s['product'] for s in sheets}
for s in sheets:
 page=(p/'sheets'/s['id']/'index.html').read_text(encoding='utf-8')
 assert s['source'].startswith('https://')
 assert 'rel="canonical"' in page
 if s.get('walkthrough'):
  assert len(s['walkthrough'])==len(s['rows'])==4
  assert all(len(step)>90 for step in s['walkthrough'])
  assert 'Walkthrough' in page and s['updated'] in page
 urls=ET.parse(p/'sitemap.xml').getroot()
 assert len(urls)==45
assert (p/'CNAME').read_text().strip()=='packetly.ly'
assert (p/'.nojekyll').exists() and (p/'404.html').exists()
assert 'reports.js' not in (p/'index.html').read_text(encoding='utf-8')
print('PASS: 39 unique sheets, requested products, complete walkthroughs, canonical pages, 45 sitemap URLs, CNAME and Pages extras.')
