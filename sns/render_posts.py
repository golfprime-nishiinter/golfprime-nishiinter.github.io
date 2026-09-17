# -*- coding: utf-8 -*-
"""
sns/posts.json の各投稿について、画像カード(1080x1080)と本文テキストを sns/out/<id>/ に書き出す。
  python sns/render_posts.py            … status が draft/ready の投稿を全部
  python sns/render_posts.py <id>       … 指定した投稿だけ
出力:
  sns/out/<id>/card.jpg        … Instagram/Facebook に添付する画像
  sns/out/<id>/instagram.txt   … Instagram 用本文（ハッシュタグ付き。リンクは貼れないので「プロフィールのリンク」）
  sns/out/<id>/facebook.txt    … Facebook 用本文（記事URL付き）
"""
import json, os, subprocess, sys, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HP = 'https://golfprime-nishiinter.github.io/guide'
posts = json.load(io.open(os.path.join(ROOT, 'sns', 'posts.json'), encoding='utf-8'))
only = sys.argv[1] if len(sys.argv) > 1 else None

for p in posts:
    if only and p['id'] != only:
        continue
    if not only and p.get('status') not in (None, 'draft', 'ready'):
        continue
    d = os.path.join(ROOT, 'sns', 'out', p['id'])
    os.makedirs(d, exist_ok=True)
    subprocess.check_call([sys.executable, os.path.join(ROOT, 'sns', 'make_card.py'),
                           '--photo', os.path.join(ROOT, p['photo']), '--title', p['title'],
                           '--lines', *p['lines'], '--out', os.path.join(d, 'card.jpg')])
    ig = p['caption'] + '\n\n' + p['hashtags']
    fb = p['caption'].replace('プロフィールのリンク', 'こちら') + '\n\n▶ 記事: ' + HP + p['article'] + '\n▶ 無料体験の予約: https://golfprime.jp/form/nishiinter/\n▶ 公式LINE: https://line.me/R/ti/p/@350tbhny'
    io.open(os.path.join(d, 'instagram.txt'), 'w', encoding='utf-8', newline='\n').write(ig)
    io.open(os.path.join(d, 'facebook.txt'), 'w', encoding='utf-8', newline='\n').write(fb)
    print('rendered', p['id'])
