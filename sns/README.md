# GOLF PRIME 金沢西インター店 Instagram / Facebook 投稿の仕組み

目的: 会員の集客。HPの記事（/guide/）を1本ずつ「投稿」に焼き直して、Instagram と Facebook に同時投稿する。追加費用ゼロ。

## アカウント（2026-09-17 確認）
- Facebookページ「Golfprime西インター店」（Meta Business Suite の asset_id=216693628182499 / business_id=1377582139498198）
- Instagram「golfprime_nishiinter」（同ページに連携済み。フォロワー221人）
- どちらも康太さんのFacebookアカウントで Meta Business Suite（https://business.facebook.com/latest/composer?asset_id=216693628182499&business_id=1377582139498198 ）から投稿できる

## ファイル
- `posts.json` … 投稿の予定表。1件= id / photo（元写真）/ title・lines（画像カードの文字）/ caption（本文）/ article（HPの記事パス）/ hashtags / status（draft → posted）
- `make_card.py` … 写真+文字の1080x1080画像カードを作る（Pillow、Windows標準フォント BIZ UDゴシック）
- `render_posts.py` … posts.json から `out/<id>/card.jpg`・`instagram.txt`・`facebook.txt` を生成
- `out/` … 生成物（gitには入れない）

## 投稿の手順（自動化タスクが行うこと）
1. `python sns/render_posts.py` で当日分を生成
2. Meta Business Suite の「投稿を作成」を開く（上のURL）。投稿先に Facebookページ と Instagram の両方が選ばれていることを確認
3. 「写真・動画を追加」→ `out/<id>/card.jpg` をアップロード
4. 本文: Instagram/Facebook 別々に設定できるので、それぞれ `instagram.txt` / `facebook.txt` を貼る（Instagramは本文にURLを貼れないため「プロフィールのリンク」表現）
5. 「公開する」（または「日時を指定」で朝7:30 / 昼12:15 / 夜20:30 のいずれか）
6. posts.json の status を posted に変え、投稿URLがあれば `posted_url` に記録

## ネタの作り方（週3本）
- HPの記事（seo-src/pages/**/page.html）の「結論を3行で」をそのままカードの lines にする。本文は結論→理由→施設の使い方→誘導（無料体験は予約フォーム/LINE）
- 季節ネタ（雪・梅雨・猛暑・シーズン開始）、施設の使い方（手ぶら・24時間・半個室）、数値の見方（ミート率など）をローテーション
- 書かないこと: 架空の実績・お客様の声、料金7,700円以外の価格、「必ず」「最短」「No.1」、他店名

## 注意
- Chromeの拡張機能経由でのファイルアップロードは、環境によってブロックされることがある。その場合はカードを生成したうえで、康太さんにアップロードだけ頼む
- Chromeのウィンドウが最小化されていると操作できない（画面サイズ0になる）
