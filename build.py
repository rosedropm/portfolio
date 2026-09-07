"""Build the portfolio with Python 3.11+ and no third-party dependencies."""
import argparse, html, json, os, re, shutil
from pathlib import Path
from urllib.parse import urlsplit, quote

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--output', default='_site')
args = parser.parse_args()
OUT = (ROOT / args.output).resolve()
if OUT == ROOT or ROOT not in OUT.parents:
    raise SystemExit('Output must be a child directory of this project.')
OUT.mkdir(parents=True, exist_ok=True)
E = lambda value: html.escape(str(value or ''), quote=True)
site = json.loads((ROOT / 'content/site.json').read_text(encoding='utf-8'))
for name in ['home', 'about']:
    site.update(json.loads((ROOT/f'content/{name}.json').read_text(encoding='utf-8')))
base = (site.get('site_url') or os.environ.get('SITE_URL', '')).strip().rstrip('/')
if base and (urlsplit(base).scheme != 'https' or not urlsplit(base).netloc):
    raise SystemExit('site_url must be an absolute HTTPS URL, or leave it blank.')
manifest_path = OUT / '.build-manifest.json'
previous_files = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else []
assets = set()
routes = []

def read_collection(name):
    items = []
    slugs = set()
    for file in sorted((ROOT/'content'/name).glob('*.json')):
        item = json.loads(file.read_text(encoding='utf-8'))
        if item.get('published', True) is False: continue
        slug = item.get('slug', '')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or slug in slugs:
            raise ValueError(f'Invalid or duplicate slug in {file.name}: {slug}')
        slugs.add(slug)
        for field in ['title', 'short_title', 'category', 'summary', 'role']:
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f'{file.name}: {field} is required.')
        items.append(item)
    return sorted(items, key=lambda x: (x['order'] if x.get('order') is not None else 999, x['slug']))

projects = read_collection('projects')
works = read_collection('works')
photos = read_collection('photography')

def asset(path, prefix):
    if not path: return ''
    path = path.lstrip('/')
    resolved = (ROOT/path).resolve()
    if not path.startswith('assets/') or ROOT/'assets' not in resolved.parents or not resolved.is_file():
        raise ValueError(f'Missing or invalid media file: {path}')
    assets.add(path)
    return prefix + quote(path, safe='/')

def paragraphs(text):
    return ''.join('<p>'+E(p).replace('\n','<br>')+'</p>' for p in (text or '').split('\n\n') if p.strip())

def image(path, alt, prefix, eager=False, cls=''):
    return f'<img src="{asset(path,prefix)}" alt="{E(alt)}" class="{cls}" loading="{"eager" if eager else "lazy"}" decoding="async"'+(' fetchpriority="high"' if eager else '')+'>'

def external(url):
    parts = urlsplit(url)
    if parts.scheme not in ['https','http'] or not parts.netloc:
        raise ValueError(f'External links must use https:// or http://: {url}')
    return E(url)

def arrow(): return '<span aria-hidden="true">↗</span>'

def nav(prefix, active):
    links = [('index.html','首頁','home'),('projects/index.html','專案案例','projects'),('works/index.html','內容作品','works'),('photography/index.html','攝影','photography'),('about/index.html','關於我','about')]
    items = ''.join(f'<a href="{prefix}{url}"'+(' aria-current="page"' if active == key else '')+f'>{label}</a>' for url,label,key in links)
    return f'''<a class="skip" href="#main">跳到主要內容</a><header class="site-header"><div class="header-inner">
    <a class="wordmark" href="{prefix}index.html" aria-label="{E(site['name'])} 首頁">{E(site['name'])}<span class="brand-star" aria-hidden="true">✳</span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav">選單 <span aria-hidden="true">＋</span></button>
    <nav id="main-nav" aria-label="主選單">{items}<a class="nav-contact" href="{prefix}about/index.html#contact">聯絡我 {arrow()}</a></nav></div></header>'''

def footer(prefix):
    return f'''<footer class="site-footer"><div><a class="wordmark" href="{prefix}index.html">{E(site['name'])}<span class="brand-star" aria-hidden="true">✳</span></a><p>{E(site['tagline'])}</p></div><div class="footer-right"><a href="mailto:{E(site['email'])}">{E(site['email'])} {arrow()}</a><p>{E(site['location'])} · <a href="{prefix}sitemap.html">網站地圖</a></p><small>作品依各專案標示個人負責範圍與協作分工。</small></div></footer>'''

def layout(route, title, description, body, active, prefix=''):
    canonical = f'<link rel="canonical" href="{E(base)}/{route}">' if base else ''
    page = f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>{E(title)}｜{E(site['name'])}</title><meta name="description" content="{E(description)}">{canonical}<meta property="og:title" content="{E(title)}｜{E(site['name'])}"><meta property="og:description" content="{E(description)}"><meta property="og:type" content="website"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="preconnect" href="https://font.emtech.cc"><link rel="stylesheet" href="https://font.emtech.cc/css/GenKiMinJP/400"><link rel="stylesheet" href="https://font.emtech.cc/css/GenKiMinJP/500"><link rel="stylesheet" href="https://font.emtech.cc/css/GenKiMinJP/600"><link rel="stylesheet" href="{prefix}assets/style.css"><script src="{prefix}assets/app.js" defer></script></head><body>{nav(prefix,active)}<main id="main">{body}</main>{footer(prefix)}<dialog id="lightbox" aria-label="作品圖片放大檢視"><div class="lightbox-bar"><span id="lightbox-caption"></span><button type="button" id="lightbox-close" autofocus>關閉 ×</button></div><img id="lightbox-image" alt=""><div class="lightbox-controls"><button type="button" id="lightbox-prev" aria-label="上一張圖片">← 上一張</button><span id="lightbox-count" aria-live="polite"></span><a id="lightbox-original" target="_blank" rel="noopener noreferrer">開啟原圖 ↗<span class="sr-only">（另開分頁）</span></a><button type="button" id="lightbox-next" aria-label="下一張圖片">下一張 →</button></div></dialog></body></html>'''
    dest=OUT/route;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(page,encoding='utf-8')
    if route != '404.html': routes.append(route)

def card(item, group, prefix, number=None):
    href=f"{prefix}{group}/{item['slug']}/index.html"
    if item.get('cover'):
        art=image(item['cover'],item.get('cover_alt') or item['short_title'],prefix)
    else:
        art=f'<div class="type-art"><span class="type-art-label">{E(item["category"])} / SELECTED WORDS</span><p>{E(item.get("quote") or item["title"]).replace(chr(10),"<br>")}</p><span class="type-art-bottom">Esther Jhang <span aria-hidden="true">✳</span></span></div>'
    number_html=f'<span class="card-number">{number:02}</span>' if number is not None else ''
    stat=f'<p class="card-stat"><strong>{E(item["metric"])}</strong> {E(item["metric_label"])}</p>' if item.get('metric') else ''
    return f'''<article class="work-card {group}-card" data-category="{E(item['category'])}"><a class="card-link" href="{href}"><div class="card-image">{art}{number_html}<span class="card-open" aria-hidden="true">↗</span></div><div class="card-body"><p class="eyebrow">{E(item['category'])}</p><h3>{E(item['short_title'])}</h3><p class="card-summary">{E(item['summary'])}</p>{stat}</div></a></article>'''

def section_head(kicker,title,url='',label='看全部'):
    return f'<div class="section-head"><div><p class="eyebrow">{kicker}</p><h2>{title}</h2></div>'+(f'<a class="text-link" href="{url}">{label} {arrow()}</a>' if url else '')+'</div>'

def home():
    body=f'''<section class="hero wrap"><div class="hero-copy"><p class="eyebrow">BRAND MARKETING & CONTENT</p><h1>{E(site['hero_title']).replace(chr(10),'<br>')}</h1><p class="hero-intro">{E(site['intro'])}</p><div class="hero-actions"><a class="button" href="projects/index.html">探索精選專案 {arrow()}</a><a class="text-link" href="about/index.html">認識 Esther <span aria-hidden="true">→</span></a></div><p class="hero-signature">{E(site['role'])}<span></span>{E(site['location'])}</p></div><figure class="hero-photo">{image(site['hero_image'],site['hero_alt'],'',True)}<figcaption>{E(site['hero_caption'])}</figcaption><span class="photo-mark" aria-hidden="true">❊</span></figure></section>
    <div class="disciplines wrap"><span>01 / 品牌內容策略</span><span>02 / 文字與影像</span><span>03 / 專案整合</span><span class="small-note">Thoughtfully made. Clearly told.</span></div>
    <section class="section wrap">{section_head('SELECTED PROJECTS','讓想法，走到實際發生。','projects/index.html','所有專案')}<div class="cards three">{''.join(card(p,'projects','',i+1) for i,p in enumerate([p for p in projects if p.get('featured')][:3]))}</div></section>
    <section class="work-section"><div class="section wrap">{section_head('WORDS & VISUALS','內容的不同表情。','works/index.html','所有內容作品')}<div class="cards three">{''.join(card(p,'works','') for p in [p for p in works if p.get('featured')][:3])}</div></div></section>
    <section class="section wrap">{section_head('THROUGH MY LENS','把光與日常，留在畫面裡。','photography/index.html','走進攝影作品')}<div class="photo-teasers">{''.join(card(p,'photography','') for p in photos[:3])}</div></section>
    <section class="about-teaser wrap"><div class="about-teaser-photo">{image(site['portrait'],site['portrait_alt'],'')}</div><div><p class="eyebrow">A LITTLE ABOUT ME</p><h2>{E(site['about_title']).replace(chr(10),'<br>')}</h2><p>{E(site['about_intro'])}</p><a class="text-link" href="about/index.html">更多關於我 {arrow()}</a></div></section>'''
    layout('index.html',site['role']+'・作品集',site['intro'],body,'home')

def listing(group,items,title,kicker,intro):
    prefix='../'
    filters=''
    if group!='projects':
        cats=list(dict.fromkeys(i['category'] for i in items))
        filters='<div class="filters" role="group" aria-label="作品分類" hidden><button type="button" data-filter="all" aria-pressed="true">全部</button>'+''.join(f'<button type="button" data-filter="{E(c)}" aria-pressed="false">{E(c)}</button>' for c in cats)+'</div><p class="filter-status sr-only" aria-live="polite"></p>'
    body=f'<section class="page-head wrap"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p>{E(intro)}</p></section><section class="listing wrap">{filters}<div class="cards {"two" if group=="projects" else "three"}">'+''.join(card(p,group,prefix,i+1 if group=='projects' else None) for i,p in enumerate(items))+'</div></section>'
    layout(group+'/index.html',title,intro,body,group,prefix)

def gallery(items,prefix,photo=False):
    figures=[]
    for i,p in enumerate(items):
        caption=p.get('caption') or p.get('alt') or f'作品 {i+1}'
        source=asset(p['image'],prefix)
        figures.append(f'<figure><a class="zoom-image" href="{source}" data-caption="{E(caption)}" aria-label="放大：{E(p.get("alt") or caption)}">{image(p["image"],p.get("alt") or caption,prefix)}<span class="zoom-label" aria-hidden="true">放大 ↗</span></a><figcaption>{E(caption)}</figcaption></figure>')
    return '<div class="gallery '+('photo-gallery' if photo else 'artifact-gallery')+'">'+''.join(figures)+'</div>'

def detail(item,group):
    prefix='../../'
    labels={'projects':'專案案例','works':'內容作品','photography':'攝影'}
    isphoto=group=='photography'
    intro=f'''<section class="detail-head wrap"><a class="back-link" href="../index.html">← {labels[group]}</a><p class="eyebrow">{E(item['category'])}</p><h1>{E(item['title']).replace(chr(10),'<br>')}</h1><p class="detail-summary">{E(item['summary'])}</p><dl class="detail-meta"><div><dt>期間 / PERIOD</dt><dd>{E(item.get('period'))}</dd></div><div><dt>我的角色 / ROLE</dt><dd>{E(item['role'])}</dd></div></dl></section>'''
    if item.get('metric'):
        intro+=f'<aside class="result-band wrap"><strong>{E(item["metric"])}</strong><div><h2>{E(item["metric_label"])}</h2><p>{E(item.get("metric_note"))}</p></div></aside>'
    if item.get('cover') and not isphoto:
        intro+=f'<figure class="detail-cover wrap">{image(item["cover"],item.get("cover_alt") or item["short_title"],prefix,True)}</figure>'
    elif item.get('quote'):
        intro+=f'<blockquote class="work-quote wrap"><p>{E(item["quote"]).replace(chr(10),"<br>")}</p></blockquote>'
    sections=item.get('sections') or []
    toc=''.join(f'<a href="#section-{i}">{i+1:02} {E(s["title"])}</a>' for i,s in enumerate(sections))
    writing=''.join(f'<section id="section-{i}" class="story-section"><span class="eyebrow">{i+1:02}</span><h2>{E(s["title"])}</h2>{paragraphs(s.get("text"))}</section>' for i,s in enumerate(sections))
    if sections:
        intro+=f'<div class="story-layout wrap"><aside class="story-toc" aria-label="本頁目錄">{toc}</aside><div class="story-copy">{writing}</div></div>'
    if item.get('gallery'):
        intro+=f'<section class="wrap section">{section_head("SELECTED IMAGES" if isphoto else "THE OUTPUT","影像選集" if isphoto else "代表產出")}{gallery(item["gallery"],prefix,isphoto)}</section>'
    if item.get('note'):intro+=f'<p class="content-note narrow">{E(item["note"])}</p>'
    if item.get('links'):
        intro+='<section class="narrow source-links"><h2>原始作品</h2>'+''.join(f'<a href="{external(l["url"])}" target="_blank" rel="noopener noreferrer">{E(l["title"])} {arrow()}<span class="sr-only">（另開分頁）</span></a>' for l in item['links'])+'</section>'
    if item.get('collaboration'):
        intro+=f'<aside class="narrow credit"><p class="eyebrow">ROLE & CREDITS</p><h2>負責範圍與協作</h2>{paragraphs(item["collaboration"])}</aside>'
    allitems={'projects':projects,'works':works,'photography':photos}[group]
    others=[x for x in allitems if x['slug']!=item['slug']]
    if others:
        n=others[0];intro+=f'<div class="next-work wrap"><span class="eyebrow">CONTINUE EXPLORING</span><a href="../{n["slug"]}/index.html">{E(n["short_title"])} {arrow()}</a></div>'
    layout(f'{group}/{item["slug"]}/index.html',item['short_title'],item['summary'],intro,group,prefix)

def about():
    prefix='../'
    body=f'''<section class="about-hero wrap"><div><p class="eyebrow">ABOUT ESTHER</p><h1>{E(site['about_title']).replace(chr(10),'<br>')}</h1><p class="about-name">{E(site['name'])} / {E(site['chinese_name'])}</p><p>{E(site['about_intro'])}</p></div><figure>{image(site['portrait'],site['portrait_alt'],prefix,True)}<figcaption>{E(site['location'])}</figcaption></figure></section>
    <section class="about-story narrow">{paragraphs(site['about_body'])}</section>
    <section class="section wrap">{section_head('WHAT I BRING','我的工作方式。')}<div class="skills-grid">{''.join(f'<article><span class="eyebrow">0{i+1}</span><h3>{E(s["title"])}</h3><p>{E(s["text"])}</p></article>' for i,s in enumerate(site.get('skills') or []))}</div></section>
    <section class="section wrap">{section_head('THE JOURNEY','從內容製作，到品牌整合。')}<div class="timeline">{''.join(f'<article><p class="eyebrow">{E(j["period"])}</p><div><h3>{E(j["company"])}</h3><p class="job-role">{E(j["role"])}</p><p>{E(j["text"])}</p></div></article>' for j in (site.get('experience') or []))}</div></section>
    <section class="section wrap">{section_head('TOOLS IN PRACTICE','讓內容落地的工具。')}<div class="skills-grid">{''.join(f'<article><h3>{E(t["title"])}</h3><p>{E(t["text"])}</p></article>' for t in (site.get('tools') or []))}</div><p class="collaboration-note">{E(site['collaboration'])}</p></section>
    <section id="contact" class="contact"><div class="wrap"><p class="eyebrow">GET IN TOUCH</p><h2>{E(site['contact_title']).replace(chr(10),'<br>')}</h2><p>{E(site['contact_text'])}</p><a class="contact-email" href="mailto:{E(site['email'])}">{E(site['email'])} {arrow()}</a>'''
    if site.get('resume'):body+=f'<p><a class="button" href="{asset(site["resume"],prefix)}" download>下載履歷 ↓</a></p>'
    body+='</div></section>'
    layout('about/index.html','關於我',site['about_intro'],body,'about',prefix)

home()
listing('projects',projects,'專案案例。','PROJECTS',site['projects_intro'])
listing('works',works,'文字與影像。','CONTENT & CREATIVE',site['works_intro'])
listing('photography',photos,'光裡的日常。','PHOTOGRAPHY',site['photography_intro'])
about()
for group,items in [('projects',projects),('works',works),('photography',photos)]:
    for item in items:detail(item,group)
mapbody='<section class="page-head wrap"><p class="eyebrow">SITEMAP</p><h1>網站地圖。</h1></section><div class="narrow sitemap"><a href="index.html">首頁</a><a href="about/index.html">關於我</a>'
for group,items,title in [('projects',projects,'專案案例'),('works',works,'內容作品'),('photography',photos,'攝影')]:
    mapbody+=f'<h2><a href="{group}/index.html">{title}</a></h2><ul>'+''.join(f'<li><a href="{group}/{x["slug"]}/index.html">{E(x["short_title"])}</a></li>' for x in items)+'</ul>'
mapbody+='</div>'
layout('sitemap.html','網站地圖','Esther Jhang 作品集網站地圖',mapbody,'')
# A 404 is served at arbitrary depths: use the published base URL when available.
notfound_prefix=base+'/' if base else './'
layout('404.html','找不到頁面','這個頁面可能已搬家。',f'<section class="page-head wrap error-page"><p class="eyebrow">404 / PAGE NOT FOUND</p><h1>這頁暫時迷路了。</h1><p>回到作品集，繼續探索文字與影像。</p><a class="button" href="{E(notfound_prefix)}index.html">回到首頁 →</a></section>','',notfound_prefix)
assets.update(['assets/style.css','assets/app.js','assets/favicon.svg'])
for path in sorted(assets):
    target=OUT/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/path,target)
(OUT/'.nojekyll').write_text('',encoding='utf-8')
if base:
    urls=''.join(f'<url><loc>{E(base)}/{route}</loc></url>' for route in routes)
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls+'</urlset>',encoding='utf-8')
    (OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n',encoding='utf-8')
else:
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n',encoding='utf-8')
generated = set(routes + ['404.html', '.nojekyll', 'robots.txt']) | assets
if base: generated.add('sitemap.xml')
for old in previous_files:
    if old not in generated:
        candidate = (OUT/old).resolve()
        if OUT in candidate.parents and candidate.is_file(): candidate.unlink()
manifest_path.write_text(json.dumps(sorted(generated)), encoding='utf-8')
print(f'Built {len(routes)+1} HTML pages and {len(assets)} assets into {OUT.name}.')
