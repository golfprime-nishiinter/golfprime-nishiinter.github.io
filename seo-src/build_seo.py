# -*- coding: utf-8 -*-
"""
GOLF PRIME 西インター店 SEOサイト（HP）ビルドスクリプト

使い方:  python seo-src/build_seo.py
入力:    seo-src/pages/<path>/page.html … 1ページ1ファイル（記事本文）
           1行目 <!-- title: ... -->   … <title>とOGタイトル
           2行目 <!-- description: ... --> … meta description（検索結果の説明文）
           <article>…</article>        … 本文（h1・結論を3行で・見出し・FAQ）
           <section class="related">…</section> … 任意。「あわせて読みたい」
         リンクはサイト内絶対パス（例 /practice/slice/）で書く。画像は /assets/xxx.jpg
         セクション一覧ページ（/beginner/ など）のカード一覧と、トップページのカード一覧は
         配下の記事から自動生成されるので、記事を追加するだけで一覧に載る
出力:    guide/<path>/index.html, guide/sitemap.xml, guide/sitemap.html, robots.txt
公開URL: https://golfprime-nishiinter.github.io/guide/
"""
import re, os, sys, io, html, datetime, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(ROOT, 'seo-src', 'pages')
OUT = os.path.join(ROOT, 'guide')
BASE = '/guide'
ORIGIN = 'https://golfprime-nishiinter.github.io'
GA4 = 'G-9ZW4ME7C39'
SITE = 'GOLF PRIME 金沢西インター店'
FORM = 'https://golfprime.jp/form/nishiinter/'
LINE = 'https://line.me/R/ti/p/@350tbhny'

def esc(t):
    return html.escape(t, quote=True)

# ---------- 共通パーツ ----------
STYLE = io.open(os.path.join(ROOT, 'seo-src', 'style.css'), encoding='utf-8').read()
FONTS = '<link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@700;800&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">'
FAVICON = io.open(os.path.join(ROOT, 'seo-src', 'favicon.txt'), encoding='utf-8').read().strip()
GA = ('<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
      "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','%s');</script>" % (GA4, GA4))

NAV = [('/', 'ホーム'), ('/price/', '料金'), ('/facility/', '設備'), ('/lesson/', 'レッスン'),
       ('/beginner/', '初心者ガイド'), ('/practice/', '練習法'), ('/simulator/', '数値の見方'),
       ('/gear/', '道具'), ('/access/', 'アクセス'), ('/faq/', 'FAQ')]

HEADER = ('<header class="site-head">\n'
          '  <a class="logo" href="%s/"><span class="logo-gp">GOLF PRIME</span><span class="logo-sub">金沢西インター店</span></a>\n'
          '  <button class="nav-toggle" aria-label="メニュー" aria-expanded="false" data-nav-toggle>☰</button>\n'
          '  <nav class="site-nav" data-nav>' % BASE
          + ''.join('<a href="%s%s">%s</a>' % (BASE, p, t) for p, t in NAV)
          + '<a class="nav-cta" href="%s" rel="noopener">無料体験</a></nav>\n</header>' % FORM)

CTA = ('<section class="cta-box">\n'
       '  <h2>まずは無料体験から</h2>\n'
       '  <p class="cta-camp"><span data-mdw="{M}月{D}日({W})">月末</span>まで、初期費用＆初月利用料 0円</p>\n'
       '  <p>月額7,700円(税込)で24時間365日・回数制限なし。貸クラブがあるので手ぶらでOK、しつこい勧誘はありません。</p>\n'
       '  <div class="cta-btns">\n'
       '    <a class="btn btn-main" href="%s" rel="noopener">無料体験を予約する<small>フォームで1分・24時間受付</small></a>\n'
       '    <a class="btn btn-line" href="%s" rel="noopener">LINEで質問・相談する<small>公式LINEに登録して気軽に聞く</small></a>\n'
       '  </div>\n'
       '  <p class="cta-note">※体験のお申し込みは店頭では受け付けておりません。フォームまたはLINEからお願いします。</p>\n'
       '</section>' % (FORM, LINE))

FOOTER = ('<footer class="site-foot">\n  <div class="foot-store">\n'
          '    <p class="foot-name">GOLF PRIME 金沢西インタースタジオ</p>\n'
          '    <p>〒921-8061 石川県金沢市森戸2丁目198<br>営業時間：24時間・年中無休｜TEL：090-9443-0562<br>金沢西インターすぐそば・駐車場あり</p>\n'
          '    <p><a href="https://www.google.com/maps/search/%%E3%%82%%B4%%E3%%83%%AB%%E3%%83%%95%%E3%%83%%97%%E3%%83%%A9%%E3%%82%%A4%%E3%%83%%A0%%E9%%87%%91%%E6%%B2%%A2%%E8%%A5%%BF%%E3%%82%%A4%%E3%%83%%B3%%E3%%82%%BF%%E3%%83%%BC%%E3%%82%%B9%%E3%%82%%BF%%E3%%82%%B8%%E3%%82%%AA" rel="noopener">Googleマップで開く</a>｜<a href="https://golfprime.jp/nishiinter/" rel="noopener">公式サイト</a>｜<a href="%s/sitemap.html">サイトマップ</a></p>\n'
          '  </div>\n  <p class="copy">© GOLF PRIME</p>\n</footer>' % BASE)

STICKY = ('<div class="stickybar">\n  <a class="sb-line" href="%s" rel="noopener">LINEで相談</a>\n'
          '  <a class="sb-main" href="%s" rel="noopener">無料体験を予約</a>\n</div>' % (LINE, FORM))

MODAL = ('<div class="exit-modal" id="exitModal" role="dialog" aria-modal="true" aria-hidden="true">\n  <div class="m-inner">\n'
         '    <button class="m-close" aria-label="閉じる" data-close>✕</button>\n'
         '    <p class="m-until"><span data-mdw="{M}月{D}日({W})">月末</span>まで</p><p class="m-big">初期費用＆初月利用料 0円は<br>今月で終了です</p>\n'
         '    <p class="m-h">ちょっと待ってください！</p>\n'
         '    <p>月額7,700円(税込)だけで24時間打ち放題。まずは無料体験で試してみませんか？</p>\n'
         '    <a class="btn btn-main" href="%s" rel="noopener">無料体験を予約する</a>\n'
         '    <a class="btn btn-line" href="%s" rel="noopener">LINEで質問・相談する</a>\n'
         '    <button class="m-later" data-close>あとで検討する</button>\n  </div>\n</div>' % (FORM, LINE))

SCRIPT = io.open(os.path.join(ROOT, 'seo-src', 'site.js'), encoding='utf-8').read()

# ---------- ページ読み込み ----------
def load_pages():
    pages = {}
    for dirpath, _, files in os.walk(PAGES):
        if 'page.html' not in files:
            continue
        rel = os.path.relpath(dirpath, PAGES).replace(os.sep, '/')
        path = '/' if rel == '.' else '/' + rel + '/'
        src = io.open(os.path.join(dirpath, 'page.html'), encoding='utf-8').read()
        title = re.search(r'<!--\s*title:\s*(.*?)\s*-->', src).group(1)
        desc = re.search(r'<!--\s*description:\s*(.*?)\s*-->', src).group(1)
        article = re.search(r'<article>(.*?)</article>', src, re.S).group(1).strip()
        rel_m = re.search(r'<section class="related">.*?</section>', src, re.S)
        h1 = re.search(r'<h1>(.*?)</h1>', article, re.S)
        pages[path] = dict(path=path, title=title, desc=desc, article=article,
                           related=rel_m.group(0) if rel_m else '',
                           h1=re.sub(r'<[^>]+>', '', h1.group(1)) if h1 else title.split('｜')[0],
                           mtime=datetime.date.fromtimestamp(os.path.getmtime(os.path.join(dirpath, 'page.html'))))
    return pages

pages = load_pages()

def section_of(path):
    parts = path.strip('/').split('/')
    return '/' + parts[0] + '/' if path != '/' else '/'

def children(section):
    return sorted(p for p in pages if p != section and section_of(p) == section and p.count('/') == 3)

def short_title(p):
    return pages[p]['title'].split('｜GOLF PRIME')[0]

def cards(section):
    return ('<div class="cards">' + ''.join(
        '<a class="card" href="%s"><h3>%s</h3><p>%s</p></a>' % (c, esc(short_title(c)), esc(pages[c]['desc']))
        for c in children(section)) + '</div>')

def to_base(fragment):
    fragment = re.sub(r'(href|src)="/(?!/)', r'\1="%s/' % BASE, fragment)
    return fragment

DEADLINE_RE = re.compile(r'\d{1,2}月\d{1,2}日\([日月火水木金土]\)')
def dyn_deadline(fragment):
    return DEADLINE_RE.sub(lambda m: '<span data-mdw="{M}月{D}日({W})">%s</span>' % m.group(0), fragment)

def crumb(p):
    if p == '/':
        return ''
    sec = section_of(p)
    items = ['<a href="%s/">ホーム</a>' % BASE]
    if p != sec and sec in pages:
        items.append('<a href="%s%s">%s</a>' % (BASE, sec, esc(short_title(sec))))
    items.append('<span>%s</span>' % esc(pages[p]['h1']))
    return '<nav class="crumb" aria-label="パンくず">' + ' › '.join(items) + '</nav>'

def render(p):
    pg = pages[p]
    body = pg['article']
    if p == '/':
        # トップ: セクション見出しの下のカード一覧を自動生成に置き換え
        def re_cards(m):
            sec = m.group(2)
            return '<h3>%s</h3>\n%s' % (m.group(1), cards(sec))
        body = re.sub(r'<h3>([^<]*)</h3>\s*<p><div class="cards"><a class="card" href="(/[^/]+/)[^"]*".*?</div></p>', re_cards, body, flags=re.S)
        body = body.replace('<!-- CTA -->', CTA)
    elif p == section_of(p) and children(p):
        body = body.rstrip() + '\n' + cards(p)
    body = dyn_deadline(to_base(body))
    related = to_base(pg['related'])
    url = ORIGIN + BASE + p
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(pg['title'])}</title>
<meta name="description" content="{esc(pg['desc'])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{'website' if p == '/' else 'article'}">
<meta property="og:title" content="{esc(pg['title'])}">
<meta property="og:description" content="{esc(pg['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{SITE}">
{FONTS}
{FAVICON}
{GA}
<style>{STYLE}</style>
</head>
<body>
{HEADER}
<main class="wrap">
  {crumb(p)}
  <article>
{body}
  </article>
  {CTA}
  {related}
</main>
{FOOTER}
{STICKY}
{MODAL}
{SCRIPT}
</body>
</html>
"""

# ---------- 出力 ----------
if os.path.isdir(OUT):
    for name in os.listdir(OUT):
        if name != 'assets':
            q = os.path.join(OUT, name)
            shutil.rmtree(q) if os.path.isdir(q) else os.remove(q)

for p in pages:
    d = os.path.join(OUT, p.strip('/').replace('/', os.sep)) if p != '/' else OUT
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n').write(render(p))

xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in sorted(pages):
    xml.append('  <url><loc>%s%s%s</loc><lastmod>%s</lastmod></url>' % (ORIGIN, BASE, p, pages[p]['mtime'].isoformat()))
xml.append('</urlset>')
io.open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write('\n'.join(xml) + '\n')

groups = {}
for p in sorted(pages):
    groups.setdefault(section_of(p), []).append(p)
items = ''.join('<h2>%s</h2><ul>%s</ul>' % (esc(short_title(sec)) if sec in pages else sec,
                ''.join('<li><a href="%s%s">%s</a></li>' % (BASE, p, esc(short_title(p))) for p in lst))
                for sec, lst in groups.items())
sm = render('/')  # 雛形として使い、中身だけ差し替える
sm = re.sub(r'<title>.*?</title>', '<title>サイトマップ｜%s</title>' % SITE, sm)
sm = re.sub(r'<main class="wrap">.*?</main>', '<main class="wrap"><article><h1>サイトマップ</h1><section class="related">%s</section></article>%s</main>' % (items, CTA), sm, flags=re.S)
sm = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s%s/sitemap.html"><meta name="robots" content="noindex,follow">' % (ORIGIN, BASE), sm)
io.open(os.path.join(OUT, 'sitemap.html'), 'w', encoding='utf-8', newline='\n').write(sm)

io.open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8', newline='\n').write(
    'User-agent: *\nAllow: /\nSitemap: %s%s/sitemap.xml\n' % (ORIGIN, BASE))

# ---------- 内部リンク検査 ----------
broken = []
for p in pages:
    d = os.path.join(OUT, p.strip('/').replace('/', os.sep)) if p != '/' else OUT
    doc = io.open(os.path.join(d, 'index.html'), encoding='utf-8').read()
    for href in re.findall(r'(?:href|src)="(%s/[^"#]*)"' % BASE, doc):
        rel = href[len(BASE) + 1:]
        target = os.path.join(OUT, rel.replace('/', os.sep))
        if rel.endswith('/') or rel == '':
            target = os.path.join(target, 'index.html')
        if not os.path.isfile(target):
            broken.append((p, href))
    for href in re.findall(r'href="(/[^"]*)"', doc):
        if not href.startswith(BASE):
            broken.append((p, 'missing base: ' + href))
print('pages:', len(pages), ' broken links:', len(broken))
for b in broken:
    print('  BROKEN', b)
sys.exit(1 if broken else 0)
