# GOLF PRIME 西インター店 キャンペーンLP

広告（Meta広告）のリンク先として使うランディングページ。GitHub Pagesで公開。

- 公開URL: https://golfprime-nishiinter.github.io/
- `src/lp_template.html` … LP本体のテンプレート（画像はプレースホルダ）
- `src/assets/` … 圧縮済み画像。`out_hero.jpg`（月替わりバナー）は手で差し替えず `src/set_banner.py` で更新する
- **月替わりバナー**: `python src/set_banner.py <受け取ったバナー.jpg> --month YYYY-MM` → ヒーロー画像・OG画像（`banners/YYYY-MM.jpg`）・`src/banner.json` が一度に更新される。build は banner.json の月が今月と違うと止まる。広告マネージャの画像差し替えと確認手順は `ads/README.md`
- `banners/` … 月替わりバナーの原本（LINEで受領）と公開用コピー。LPの og:image（リンクプレビュー画像）と広告マネージャにアップロードする画像はここのファイルを使う
- `node src/build.cjs` … `index.html` を生成（画像埋め込み・GA4タグ・og:image付き）
- 〆切日・カウントダウンは「その月の月末」を自動計算するのでメンテ不要
- 編集したら build → commit → push で数分後に公開反映

## SEOサイト（HP・全71ページ） `/guide/`

- 公開URL: https://golfprime-nishiinter.github.io/guide/
- 元データ: `seo-src/pages/<パス>/page.html`（1記事1ファイル。1行目 title、2行目 description、`<article>` 本文、任意で `<section class="related">`）
  - 共通部品: `seo-src/style.css`（見た目）、`seo-src/site.js`（メニュー・ポップアップ・〆切の月末自動計算・GA4クリック計測）、`seo-src/favicon.txt`
  - `seo-src/preview.html` は最初にスマホのClaudeチャットで作った1ファイル版（参考用。ビルドには使わない）
- `python seo-src/build_seo.py` … `guide/` 配下に各ページを独立URLで生成（GA4タグ・canonical・sitemap.xml・robots.txt付き）。リンク切れがあると失敗する
- 記事を増やすときは `seo-src/pages/<セクション>/<記事名>/page.html` を作るだけ。セクション一覧ページとトップのカード一覧は自動で更新される
- キャンペーンの〆切日はLPと同じく月末を自動計算する
- 直したら build → commit → push で数分後に反映
