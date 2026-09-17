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
- 元データ: `seo-src/preview.html`（スマホのClaudeチャットで作った1ファイル版プレビュー）
- `python seo-src/build_seo.py` … `guide/` 配下に各ページを独立URLで生成（画像切り出し・GA4タグ・サイトマップ付き）
- キャンペーンの〆切日（「9月30日(水)まで」等）はLPと同じく月末を自動計算する
- ページを直したいときは `seo-src/preview.html` を編集 → build → commit → push
