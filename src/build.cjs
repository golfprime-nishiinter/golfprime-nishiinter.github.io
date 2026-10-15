// GOLF PRIME 西インター店 LP ビルドスクリプト
// 使い方: node src/build.cjs  → リポジトリ直下に index.html を生成
// 画像は src/assets/ の圧縮済みJPEGを URL で参照する（GitHub Pages がそのまま配信する。
// 以前は data URI 埋め込みだったが、index.html が 470KB になり差分も見えないので 2026-10-14 にやめた）。
//
// 月替わりバナーの差し替えは必ず `python src/set_banner.py <バナー.jpg> --month YYYY-MM` で行う
// （ヒーロー画像 out_hero.jpg・OG画像 banners/YYYY-MM.jpg・src/banner.json を一度に更新する）。
// このスクリプトは src/banner.json を読み、バナーの月が今月（日本時間）と違えばビルドを止める。
// どうしても前の月のまま build したいときだけ ALLOW_STALE_BANNER=1 を付ける。
// OG画像（og:image）= 広告・LINE・SNSでLPのリンクを貼ったときのプレビュー画像。無いと Meta が
// ページ内の写真（ブース写真など）を勝手に拾うので、必ずバナーを指定する。
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');
const SITE = 'https://golfprime-nishiinter.github.io/';

const banner = JSON.parse(fs.readFileSync(path.join(__dirname, 'banner.json'), 'utf8'));
const jstNow = new Date(Date.now() + 9 * 60 * 60 * 1000);
const thisMonth = jstNow.toISOString().slice(0, 7);
if (banner.month !== thisMonth && !process.env.ALLOW_STALE_BANNER) {
  throw new Error(`バナーが ${banner.month} のままです（今月は ${thisMonth}）。先に python src/set_banner.py <新バナー.jpg> --month ${thisMonth} を実行してください`);
}
if (!fs.existsSync(path.join(root, banner.og_image))) throw new Error('OG画像がありません: ' + banner.og_image);
const OG_IMAGE = banner.og_image;
const OG_SIZE = [banner.width, banner.height];
const crypto = require('crypto');
// 同じファイル名で中身が変わる（月替わりバナー）ので、中身のハッシュを ?v= に付けてキャッシュを切る
const img = f => 'src/assets/' + f + '?v=' + crypto.createHash('sha1').update(fs.readFileSync(path.join(__dirname, 'assets', f))).digest('hex').slice(0, 8);

let body = fs.readFileSync(path.join(__dirname, 'lp_template.html'), 'utf8');
body = body
  .replace('{{HERO}}', img('out_hero.jpg'))
  .replace('{{SPACE}}', img('out_space.jpg'))
  .replace('{{SIM}}', img('out_sim.jpg'))
  .replace('{{PROW}}', img('out_pro_w.jpg'))
  .replace('{{COACH}}', img('out_coach.jpg'))
  .replace('{{GAIKAN}}', img('out_gaikan.jpg'));
if (/\{\{[A-Z]+\}\}/.test(body)) throw new Error('未置換の画像プレースホルダ: ' + body.match(/\{\{[A-Z]+\}\}/g));

// テンプレート先頭の<title>はheadへ移す
const mTitle = body.match(/^<title>([^<]*)<\/title>\s*/);
const title = mTitle ? mTitle[1] : 'GOLF PRIME 西インター店';
if (mTitle) body = body.slice(mTitle[0].length);

const head = `<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<meta name="description" content="金沢西インターすぐ。24時間365日打ち放題のインドアゴルフ GOLF PRIME。今なら初期費用＆初月利用料が完全無料。無料体験受付中・初心者も手ぶらOK。">
<meta property="og:title" content="${title}">
<meta property="og:description" content="24時間365日打ち放題のインドアゴルフ。今なら初期費用＆初月利用料が完全無料！">
<meta property="og:type" content="website">
<meta property="og:url" content="${SITE}">
<meta property="og:image" content="${SITE}${OG_IMAGE}">
<meta property="og:image:width" content="${OG_SIZE[0]}">
<meta property="og:image:height" content="${OG_SIZE[1]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="${SITE}${OG_IMAGE}">
<meta name="robots" content="noindex">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⛳</text></svg>">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9ZW4ME7C39"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-9ZW4ME7C39');</script>
</head>
<body>
`;
fs.writeFileSync(path.join(root, 'index.html'), head + body + '\n</body>\n</html>\n');
console.log('index.html generated:', ((head + body).length / 1024).toFixed(0) + 'KB', '| banner', banner.month, OG_IMAGE);
