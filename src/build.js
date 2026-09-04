// GOLF PRIME 西インター店 LP ビルドスクリプト
// 使い方: node src/build.js  → リポジトリ直下に index.html を生成
// 画像は src/assets/ の圧縮済みJPEGをdata URIとして埋め込む。
// 月替わりバナーは src/assets/out_hero.jpg を差し替えてから再ビルドする。
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');
const b64 = f => 'data:image/jpeg;base64,' + fs.readFileSync(path.join(__dirname, 'assets', f)).toString('base64');

let body = fs.readFileSync(path.join(__dirname, 'lp_template.html'), 'utf8');
body = body
  .replace('{{HERO}}', b64('out_hero.jpg'))
  .replace('{{SPACE}}', b64('out_space.jpg'))
  .replace('{{SIM}}', b64('out_sim.jpg'))
  .replace('{{PROW}}', b64('out_pro_w.jpg'))
  .replace('{{COACH}}', b64('out_coach.jpg'))
  .replace('{{GAIKAN}}', b64('out_gaikan.jpg'));
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
<meta name="robots" content="noindex">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⛳</text></svg>">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9ZW4ME7C39"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-9ZW4ME7C39');</script>
</head>
<body>
`;
fs.writeFileSync(path.join(root, 'index.html'), head + body + '\n</body>\n</html>\n');
console.log('index.html generated:', ((head + body).length / 1024).toFixed(0) + 'KB');
