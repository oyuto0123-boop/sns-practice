# よりみち練習用


ハッカソンに向けた個人練習用リポジトリ
SNS「よりみち」趣味の口コミ匿名SNS

## 技術スタック

- Python  3.11 
- Flask   2.2.2 / Werkzeug 2.2.2
- MySQL 8.0
- Docker / Docker Compose

## 構成
|ファイル|役割|
|---|---|
|`app.py`|最小のFlaskアプリ'/'にアクセスすると「よりみち」を返す|
|`requirements.txt`|使用ライブラリとバージョンの指定|
|`Dockerfile`|イメージのビルド手順|
|`docker-compose.yml`|複数コンテナの定義と接続情報をまとめたもの|
|`init/01_create_posts.sql`|初回起動時に自動実行されるテーブル作成SQL|


## 動かし方
```bash
docker compose up
```
ブラウザで　http://localhost:5000　を開くと「よりみち」と表示される。
停止は　ctrl + C → docker compose down まで実行すれば、コンテナとネットワークを削除。データは消えない。



## 詰まったメモ
9/23 記述
- Dockerfile の Python を Pyton と打ち間違え、ベースイメージのPullとコンテナ起動で失敗。
- Docker Desktop が pause 状態でビルド不可→Resume で解決。
- Flask だけ固定して、 Werkzeug 未固定→ url_quote の ImportError → Werkzeug==2.2.2 を追加して解決。
9/23 追記
- ERROR 1045 パスワードの渡し方ミス（-p の直後に空白を入れない）
- ERROR 1406 VARCHARの桁不足。prefecture を広げて解決。同時に category も文字数拡張。

