# よりみち練習用


ハッカソンに向けた個人練習用リポジトリ
SNS「よりみち」趣味の口コミ匿名SNS

## 技術スタック

- Python  3.11 
- Flask   2.2.2 / Werkzeug 2.2.2
- MySQL 8.0
- Jinja2(Flask の依存として自動導入)
- Docker / Docker Compose

## 構成
|ファイル|役割|
|---|---|
|`app.py`|Flaskアプリ。`/`でDBから投稿を取得してテンプレートに渡す|
|`requirements.txt`|使用ライブラリとバージョンの指定|
|`Dockerfile`|イメージのビルド手順|
|`docker-compose.yml`|複数コンテナの定義と接続情報をまとめたもの|
|`init/01_create_posts.sql`|初回起動時に自動実行されるテーブル作成SQL|
|`templates/index.html`|投稿の一覧を表示するJinja2テンプレート|

## 動かし方
```bash
docker compose up
```
ブラウザで　http://localhost:5000　を開くと、postsテーブルの投稿が一覧表示される。
停止は　ctrl + C → docker compose down まで実行すれば、コンテナとネットワークを削除。データは消えない。
ソースを変更したときは、docker compose up --build (COPYで焼きこむため再ビルドが必要)

## 詰まったメモ
### 9/23 記述
- Dockerfile の Python を Pyton と打ち間違え、ベースイメージのPullとコンテナ起動で失敗。
- Docker Desktop が pause 状態でビルド不可→Resume で解決。
- Flask だけ固定して、 Werkzeug 未固定→ url_quote の ImportError → Werkzeug==2.2.2 を追加して解決。

### 9/23 追記
- ERROR 1045 パスワードの渡し方ミス（-p の直後に空白を入れない）
- ERROR 1406 VARCHARの桁不足。prefecture を広げて解決。同時に category も文字数拡張。

### 9/26 追記
- RuntimeError: 'cryptography' package is required → MySQL 8.0 の caching_sha2_password 認証に必要。requirements.txt に cryptography==42.0.5 を追加して解決。
- ブラウザで日本語が二重エンコードで化けた。原因は seed.sql を流した際に mysql クライアントが latin1 で接続していたこと。mysql> から見ると正常に見えるため気づきにくい。DELETE 後、--default-character-set=utf8mb4 を付けて流し直して解決。
- docker compose exec でリダイレクト投入するときは -T が必要（2回目）。
- app.py を変更しても docker compose up だけでは反映されない。--build が必要。
