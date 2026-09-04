# GOLF PRIME 西インター店 キャンペーンLP

広告（Meta広告）のリンク先として使うランディングページ。GitHub Pagesで公開。

- 公開URL: https://kota0206h7-sketch.github.io/golfprime-lp/
- `src/lp_template.html` … LP本体のテンプレート（画像はプレースホルダ）
- `src/assets/` … 圧縮済み画像。月替わりバナーは `out_hero.jpg` を差し替える
- `node src/build.cjs` … `index.html` を生成（画像埋め込み・GA4タグ付き）
- 〆切日・カウントダウンは「その月の月末」を自動計算するのでメンテ不要
- 編集したら build → commit → push で数分後に公開反映
