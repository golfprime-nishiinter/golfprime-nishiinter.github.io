# -*- coding: utf-8 -*-
"""
月替わりバナーを「1か所」で差し替えるスクリプト。
LPのヒーロー画像・OG画像（リンクプレビュー）・広告マネージャに入れる画像が、
すべて同じ元画像から作られるようにして、月ごとの食い違いを防ぐ。

使い方（LINEで新しいバナーを受け取ったら）:
  python src/set_banner.py <受け取ったバナー.jpg> --month 2026-11
  node src/build.cjs
  git add -A && git commit -m "lp: 11月バナー" && git push

やること:
  1. banners/<month>.jpg … 広告マネージャにアップロードする画像・LPのOG画像（元画像を圧縮したコピー）
  2. src/assets/out_hero.jpg … LPのヒーロー画像（720x900に縮小）
  3. src/banner.json … いま使っているバナーの月とファイル名。build.cjs がこれを読み、
     今月と違う月のままなら build を止める（差し替え忘れの検知）
"""
import argparse, json, os, re, sys
from datetime import datetime, timedelta, timezone
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JST = timezone(timedelta(hours=9))
HERO_SIZE = (720, 900)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src', help='受け取ったバナー画像（jpg/png）')
    ap.add_argument('--month', default=datetime.now(JST).strftime('%Y-%m'), help='このバナーの月 YYYY-MM（省略時は今月）')
    a = ap.parse_args()
    if not re.fullmatch(r'\d{4}-\d{2}', a.month):
        sys.exit('--month は YYYY-MM の形式で指定してください: ' + a.month)

    im = Image.open(a.src).convert('RGB')
    if im.width < 1000 or im.height < 1000:
        sys.exit(f'バナーが小さすぎます {im.size}。LINEは「オリジナル画質」で受け取り直してください')

    og_rel = f'banners/{a.month}.jpg'
    og_path = os.path.join(ROOT, og_rel)
    im.save(og_path, quality=85, optimize=True, progressive=True)

    # ヒーロー画像は 720x900（4:5）。比率が違う場合は中央を切り出す
    tw, th = HERO_SIZE
    scale = max(tw / im.width, th / im.height)
    rs = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left, top = (rs.width - tw) // 2, (rs.height - th) // 2
    hero = rs.crop((left, top, left + tw, top + th))
    hero_path = os.path.join(ROOT, 'src', 'assets', 'out_hero.jpg')
    hero.save(hero_path, quality=88, optimize=True, progressive=True)

    meta = {'month': a.month, 'og_image': og_rel, 'width': im.width, 'height': im.height,
            'source': os.path.basename(a.src), 'set_at': datetime.now(JST).strftime('%Y-%m-%d %H:%M')}
    with open(os.path.join(ROOT, 'src', 'banner.json'), 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print(f'OK: {og_rel} ({im.width}x{im.height}, {os.path.getsize(og_path)//1024}KB)')
    print(f'OK: src/assets/out_hero.jpg ({tw}x{th})')
    print(f'OK: src/banner.json month={a.month}')
    print('次: node src/build.cjs → commit → push。広告マネージャの画像は', og_rel, 'をアップロードする')

if __name__ == '__main__':
    main()
