# GOLF PRIME 西インター店 キャンペーンLP

広告（Meta広告）のリンク先として使うランディングページ。GitHub Pagesで公開。

- 公開URL: https://golfprime-nishiinter.github.io/
- `src/lp_template.html` … LP本体のテンプレート（画像はプレースホルダ）
- `src/assets/` … 圧縮済み画像。月替わりバナーは `out_hero.jpg` を差し替える
- `node src/build.cjs` … `index.html` を生成（画像埋め込み・GA4タグ付き）
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
