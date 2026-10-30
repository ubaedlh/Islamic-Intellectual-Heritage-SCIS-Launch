"""Check rendered exhibition structure and local references without dependencies."""
from pathlib import Path
from html.parser import HTMLParser
import json
from render import render
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.refs=[];self.images=[];self.milestones=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='article' and 'milestone' in a.get('class','').split():self.milestones.append(a['id'])
        for k in ['href','src']:
            if a.get(k):self.refs.append(a[k])
        if tag=='img' and a.get('src') and a.get('aria-hidden')!='true':self.images.append(a)
text=(ROOT/'index.html').read_text();assert text==render(),'Renderer output out of sync'
p=Page();p.feed(text)
assert len(p.ids)==len(set(p.ids)),'Duplicate IDs'
assert set(p.milestones)=={f'milestone-{i}' for i in range(1,13)},'Missing milestone'
for ref in p.refs:
    assert ref[1:] in p.ids if ref.startswith('#') else (ROOT/ref).is_file(),f'Broken reference: {ref}'
for im in p.images:assert im.get('alt'),'Missing image alternative'
d=json.loads((ROOT/'content.json').read_text())
assert len(d['archiveObjects'])==6
for m in d['milestones']:assert m['description'] in __import__('html').unescape(text)
assert 'image-placeholder' not in text
assert sum(o['width']*o['height']>0 for o in d['archiveObjects'])==6
print('PASS: renderer, 12 milestones, local assets/anchors, alt text, six object views, static narrative')
