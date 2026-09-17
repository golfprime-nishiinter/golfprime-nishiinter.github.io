# -*- coding: utf-8 -*-
"""
GOLF PRIME 西インター店 SEOサイト ビルドスクリプト

使い方:  python seo-src/build_seo.py
入力:    seo-src/preview.html  (スマホのClaudeチャットで作った1ファイル版プレビュー。71ページが
         <main data-page="/xxx/"> として1枚に入っていて、#/xxx/ のハッシュで切り替える形式)
出力:    guide/<path>/index.html … 各ページを独立したURLに分割
         guide/assets/*.jpg      … 埋め込み画像(base64)を切り出し
         guide/sitemap.html, guide/sitemap.xml, robots.txt
公開URL: https://golfprime-nishiinter.github.io/guide/
"""
import re, os, sys, io, hashlib, posixpath, html, datetime, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'seo-src', 'preview.html')
OUT = os.path.join(ROOT, 'guide')
BASE = '/guide'                                   # 公開時のサブパス
ORIGIN = 'https://golfprime-nishiinter.github.io'
GA4 = 'G-9ZW4ME7C39'

s = io.open(SRC, encoding='utf-8').read()

# ---------- 共通パーツを切り出す ----------
style = re.search(r'<style>(.*?)</style>', s, re.S).group(1)
style = re.sub(r'\n\.pv-bar\{[^}]*\}\n?', '\n', style)      # プレビュー帯のCSSは不要
fonts = re.search(r'<link href="https://fonts\.googleapis\.com[^>]*>', s).group(0)
favicon = re.search(r'<link rel="icon"[^>]*>', s).group(0)
header = re.search(r'<header class="site-head">.*?</header>', s, re.S).group(0)
footer = re.search(r'<footer class="site-foot">.*?</footer>', s, re.S).group(0)
sticky = re.search(r'<div class="stickybar">.*?</div>', s, re.S).group(0)
modal = re.search(r'<div class="exit-modal".*?</div>\s*</div>', s, re.S).group(0)
titles = dict(re.findall(r"'(/[^']*)': '([^']*)'", re.search(r'var T=\{(.*?)\};', s, re.S).group(1)))
behavior = re.search(r'<script>\(function\(\)\{\s*// nav toggle.*?\}\)\(\);\s*</script>', s, re.S).group(0)

mains = re.findall(r'(<main class="wrap" data-page="([^"]+)" hidden>.*?</main>)', s, re.S)
assert len(mains) == 71, len(mains)

# ---------- 画像を切り出す ----------
os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
img_map = {}
def extract_img(m):
    import base64
    data = m.group(2)
    h = hashlib.md5(data.encode()).hexdigest()[:10]
    if h not in img_map:
        name = 'img_%s.%s' % (h, 'jpg' if m.group(1) == 'jpeg' else m.group(1))
        with open(os.path.join(OUT, 'assets', name), 'wb') as f:
            f.write(base64.b64decode(data))
        img_map[h] = name
    return 'src="%s/assets/%s"' % (BASE, img_map[h])

# ---------- リンク書き換え ----------
def rewrite_links(fragment, page):
    def sub(m):
        target = m.group(1)                      # 例: /beginner/clubs/  /../clubs/  /sitemap.html  /
        if target.startswith('/../'):
            target = posixpath.normpath(posixpath.join(page, target[1:])) + '/'
        return 'href="%s%s"' % (BASE, target)
    fragment = re.sub(r'href="#(/[^"]*)"', sub, fragment)
    fragment = re.sub(r'src="data:image/([a-z]+);base64,([A-Za-z0-9+/=]+)"', extract_img, fragment)
    return fragment

# キャンペーン〆切「9月30日(水)」は月末を自動計算するようにする(LPと同じ方式)
DEADLINE_RE = re.compile(r'\d{1,2}月\d{1,2}日\([日月火水木金土]\)')
def dyn_deadline(fragment):
    return DEADLINE_RE.sub(lambda m: '<span data-mdw="{M}月{D}日({W})">%s</span>' % m.group(0), fragment)

deadline_js = """<script>
(function(){
  var now0=new Date(), mLast=new Date(now0.getFullYear(), now0.getMonth()+1, 0);
  var M=now0.getMonth()+1, D=mLast.getDate(), W='日月火水木金土'[mLast.getDay()];
  document.querySelectorAll('[data-mdw]').forEach(function(e){e.textContent=e.getAttribute('data-mdw').replace('{M}',M).replace('{D}',D).replace('{W}',W);});
  // GA4: CTAクリック計測(LPと同じイベント名)
  function track(n,p){try{if(typeof gtag==='function')gtag('event',n,p||{});}catch(e){}}
  document.querySelectorAll('a[href*="golfprime.jp/form"]').forEach(function(a){a.addEventListener('click',function(){track('cta_form',{place:a.className||'link',page:location.pathname});});});
  document.querySelectorAll('a[href*="line.me"]').forEach(function(a){a.addEventListener('click',function(){track('cta_line',{place:a.className||'link',page:location.pathname});});});
})();
</script>"""

ga4 = ('<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
       "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','%s');</script>" % (GA4, GA4))

# ---------- meta description: カードの説明文 or リード文 ----------
desc_map = {}
for href, d in re.findall(r'<a class="card" href="#(/[^"]*)"><h3>[^<]*</h3><p>([^<]*)</p></a>', s):
    desc_map.setdefault(href, html.unescape(d))

def description(page, body):
    if page in desc_map:
        return desc_map[page]
    m = re.search(r'<p class="lead">([^<]*)</p>', body)
    if m:
        return html.unescape(m.group(1))
    m = re.search(r'<aside class="tldr".*?<li>(.*?)</li>', body, re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)) if m else titles.get(page, '')

def esc(t):
    return html.escape(t, quote=True)

# ---------- 各ページを書き出す ----------
if os.path.isdir(OUT):
    for name in os.listdir(OUT):
        if name != 'assets':
            p = os.path.join(OUT, name)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

hdr_common = dyn_deadline(rewrite_links(header, '/'))
ftr_common = rewrite_links(footer, '/')
sticky_common = rewrite_links(sticky, '/')
modal_common = dyn_deadline(rewrite_links(modal, '/'))

pages = []
for raw, page in mains:
    body = raw.replace(' hidden>', '>', 1)
    body = dyn_deadline(rewrite_links(body, page))
    title = titles.get(page, 'GOLF PRIME 金沢西インター店')
    desc = description(page, body)
    url = ORIGIN + BASE + page
    doc = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{'website' if page == '/' else 'article'}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="GOLF PRIME 金沢西インター店">
{fonts}
{favicon}
{ga4}
<style>{style}</style>
</head>
<body>
{hdr_common}
{body}
{ftr_common}
{sticky_common}
{modal_common}
{deadline_js}
{behavior}
</body>
</html>
"""
    d = os.path.join(OUT, page.strip('/').replace('/', os.sep)) if page != '/' else OUT
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n').write(doc)
    pages.append((page, title))

# ---------- サイトマップ ----------
today = datetime.date.today().isoformat()
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for page, _ in sorted(pages):
    xml.append('  <url><loc>%s%s%s</loc><lastmod>%s</lastmod></url>' % (ORIGIN, BASE, page, today))
xml.append('</urlset>')
io.open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write('\n'.join(xml) + '\n')

groups = {}
for page, title in sorted(pages):
    top = page.split('/')[1] or 'home'
    groups.setdefault(top, []).append((page, title))
items = []
for top, lst in groups.items():
    items.append('<ul>' + ''.join('<li><a href="%s%s">%s</a></li>' % (BASE, p, esc(t.split('｜GOLF PRIME')[0])) for p, t in lst) + '</ul>')
sm_title = 'サイトマップ｜GOLF PRIME 金沢西インター店'
sm_doc = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{sm_title}</title><meta name="robots" content="noindex,follow"><link rel="canonical" href="{ORIGIN}{BASE}/sitemap.html">
{fonts}
{favicon}
{ga4}
<style>{style}</style></head><body>
{hdr_common}
<main class="wrap"><article><h1>サイトマップ</h1><section class="related">{''.join(items)}</section></article></main>
{ftr_common}
{sticky_common}
{modal_common}
{deadline_js}
{behavior}
</body></html>
"""
io.open(os.path.join(OUT, 'sitemap.html'), 'w', encoding='utf-8', newline='\n').write(sm_doc)

robots = 'User-agent: *\nAllow: /\nSitemap: %s%s/sitemap.xml\n' % (ORIGIN, BASE)
io.open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8', newline='\n').write(robots)

# ---------- 内部リンク検査 ----------
broken = []
for page, _ in pages:
    d = os.path.join(OUT, page.strip('/').replace('/', os.sep)) if page != '/' else OUT
    doc = io.open(os.path.join(d, 'index.html'), encoding='utf-8').read()
    for href in re.findall(r'(?:href|src)="(%s/[^"#]*)"' % BASE, doc):
        rel = href[len(BASE) + 1:]
        target = os.path.join(OUT, rel.replace('/', os.sep))
        if rel.endswith('/') or rel == '':
            target = os.path.join(target, 'index.html')
        if not os.path.isfile(target):
            broken.append((page, href))
    if 'href="#/' in doc or 'src="data:image' in doc:
        broken.append((page, 'unconverted hash link or inline image'))

print('pages:', len(pages), ' images:', len(img_map), ' broken links:', len(broken))
for b in broken:
    print('  BROKEN', b)
sys.exit(1 if broken else 0)
