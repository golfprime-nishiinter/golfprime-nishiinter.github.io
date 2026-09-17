# -*- coding: utf-8 -*-
"""
Instagram / Facebook 投稿用の画像カード（1080x1080）を作る。追加費用ゼロ（Pillow + Windows標準フォント）。

使い方:
  python sns/make_card.py --photo src/assets/out_gaikan.jpg --title "冬こそ差がつく" --lines "雪の3か月をインドアで" "春に10打変わる" --out sns/out/2026-09-17.jpg
  python sns/make_card.py --photo ... --title ... --lines ... --footer "月額7,700円(税込)｜24時間｜金沢西IC すぐ"

写真は上半分に敷き、下半分にブランド色（HPと同じ緑〜ティール）の帯と文字を置く。
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_B = r'C:\Windows\Fonts\BIZ-UDGothicB.ttc'
FONT_R = r'C:\Windows\Fonts\BIZ-UDGothicR.ttc'
TEAL = (20, 158, 140)
GREEN = (88, 182, 77)
INK = (18, 43, 58)
CTA = (255, 106, 43)
W = H = 1080

def font(path, size):
    return ImageFont.truetype(path, size)

def fit_lines(draw, text, f, max_w):
    """日本語は単語区切りが無いので1文字ずつ折り返す"""
    lines, cur = [], ''
    for ch in text:
        if draw.textlength(cur + ch, font=f) > max_w and cur:
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines

def cover(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = (im.width - w) // 2; y = int((im.height - h) * 0.12)   # 縦長写真は上寄せ（顔が切れないように）
    return im.crop((x, y, x + w, y + h))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--photo', required=True)
    ap.add_argument('--title', required=True)
    ap.add_argument('--lines', nargs='*', default=[])
    ap.add_argument('--footer', default='GOLF PRIME 金沢西インター店｜24時間・月額7,700円(税込)')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    canvas = Image.new('RGB', (W, H), (255, 255, 255))
    photo = cover(Image.open(a.photo).convert('RGB'), W, 600)
    canvas.paste(photo, (0, 0))

    # 写真の下端をグラデーションで帯につなぐ
    grad = Image.new('L', (1, 140))
    for i in range(140):
        grad.putpixel((0, i), int(255 * i / 139))
    band = Image.new('RGB', (W, 140), TEAL)
    canvas.paste(band, (0, 460), grad.resize((W, 140)))

    # 下半分の帯（HPと同じグラデーション）
    for y in range(600, H):
        t = (y - 600) / (H - 600)
        c = tuple(round(TEAL[i] + (GREEN[i] - TEAL[i]) * t) for i in range(3))
        ImageDraw.Draw(canvas).line([(0, y), (W, y)], fill=c)

    d = ImageDraw.Draw(canvas)
    # ロゴ
    d.rounded_rectangle((40, 40, 300, 112), radius=18, fill=(255, 255, 255))
    d.text((60, 52), 'GOLF PRIME', font=font(FONT_B, 40), fill=INK)

    y = 640
    tf = font(FONT_B, 72)
    for ln in fit_lines(d, a.title, tf, W - 120):
        d.text((60, y), ln, font=tf, fill=(255, 255, 255))
        y += 86
    y += 14
    lf = font(FONT_R, 44)
    for line in a.lines:
        for ln in fit_lines(d, '・' + line, lf, W - 120):
            d.text((60, y), ln, font=lf, fill=(255, 255, 255))
            y += 58
    ff = font(FONT_B, 34)
    d.rounded_rectangle((40, H - 110, W - 40, H - 40), radius=20, fill=(255, 255, 255))
    d.text((70, H - 96), a.footer, font=ff, fill=INK)

    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    canvas.save(a.out, quality=90)
    print('saved', a.out)

if __name__ == '__main__':
    main()
