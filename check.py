"""Check the generated website without external packages or a browser."""
import json, sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

root=Path(sys.argv[1] if len(sys.argv)>1 else '_site').resolve()
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.refs=[];self.images=[];self.h1=0;self.title=False;self.errors=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):
            if a['id'] in self.ids:self.errors.append('duplicate ID: '+a['id'])
            self.ids.add(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='title':self.title=True
        for key in ['href','src']:
            if a.get(key):self.refs.append(a[key])
        if tag=='img' and a.get('id')!='lightbox-image':
            if not a.get('alt'):self.errors.append('image without description')
            if not a.get('src'):self.errors.append('image without source')
pages={}
for file in root.rglob('*.html'):
    p=Page();p.feed(file.read_text(encoding='utf-8'));pages[file]=p
errors=[]
for file,p in pages.items():
    if p.h1!=1:errors.append(f'{file.relative_to(root)}: expected one h1, found {p.h1}')
    if not p.title:errors.append(f'{file.relative_to(root)}: missing page title')
    errors.extend(f'{file.relative_to(root)}: {e}' for e in p.errors)
    for ref in p.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=(file.parent/unquote(u.path)).resolve() if u.path else file
        if target.is_dir():target=target/'index.html'
        if root not in target.parents or not target.exists():errors.append(f'{file.relative_to(root)}: missing local target {ref}')
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{file.relative_to(root)}: missing anchor {ref}')
for file in root.rglob('*'):
    if file.is_file() and file.suffix in ['.html','.css','.js','.xml','.txt']:
        text=file.read_text(encoding='utf-8')
        if 'X-Amz-' in text or 'prod-files-secure' in text:errors.append('Temporary Notion URL found: '+str(file))
if not pages:errors.append('No pages found')
if errors:
    print('\n'.join(errors));sys.exit(1)
print(json.dumps({'status':'passed','html_pages':len(pages),'local_references':sum(len(p.refs) for p in pages.values()),'checks':['local links','image files','alt text','headings','anchors','temporary URL absence']},ensure_ascii=False))
