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
|`app.py`|Flaskアプリ。GET:DBから投稿の取得。POST:フォームの内容をpostsにINSERT|
|`requirements.txt`|使用ライブラリとバージョンの指定|
|`Dockerfile`|イメージのビルド手順|
|`docker-compose.yml`|複数コンテナの定義と接続情報をまとめたもの|
|`init/01_create_posts.sql`|初回起動時に自動実行されるテーブル作成SQL|
|`templates/index.html`|投稿の一覧を表示するJinja2テンプレート。投稿ファームも作成|
|`static/style.css`|藍鼠配色をCSS変数で定義、カード表示と中央寄せのレイアウト|
|`.gitignore`|Gitの管理対象から外すファイルの指定。seed.sqlを除外|

## 動かし方
```bash
docker compose up -d
```
ブラウザで http://localhost:5000 を開くと、posts テーブルの投稿が一覧表示される。
フォームから本文とカテゴリを送信すると、posts に INSERT されて一覧に追加される。

### 停止
```bash
docker compose down
```
コンテナとネットワークを削除する。ボリュームは残るのでデータは消えない。
`-d` で起動した場合は `Ctrl+C` では止まらないので、必ず `docker compose down` を使う。

### ソースを変更したとき
```bash
docker compose down && docker compose up --build -d
```
Dockerfile が COPY でソースを焼き込む構造のため、`docker compose up` だけでは反映されない。
対象は `app.py` / `templates/` / `static/` すべて。ブラウザのスーパーリロードでは解決しない。

### DB を直接見る
```bash
docker compose exec db mysql -u niwatori -pcokecoke123 --default-character-set=utf8mb4 yorimichi
```
- `-p` とパスワードの間に空白を入れない（入れると ERROR 1045）
- `--default-character-set=utf8mb4` を必ず付ける（付けないと latin1 で解釈され文字化けする）
- ファイルを流し込むときは `-T` を付ける（例: `docker compose exec -T db mysql ... < seed.sql`）
- コンテナが起動していないと使えない（`service "db" is not running`）

### ログを見る
```bash
docker compose logs -f
```

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

### 9/28 追記
- app.py を編集して dcb で反映したのに動作が変わらない。原因は nvim で保存していなかったこと。切り分けは docker compose exec web cat app.py（コンテナ内）と grep -n（ホスト側）の2段階で、どちらも古ければ保存の問題。
- コンテナ停止中に docker compose exec を実行して service "db" is not running。
- DESCRIBE posts の結果が当初の定義と食い違っていた（category が varchar(20) で NULL 許可）。9/25 の ALTER TABLE で NOT NULL が外れていた。
- INSERT で conn.commit() を忘れるとエラーが出ずに保存されない。
- request.args（URLのクエリ文字列）と request.form（POSTのボディ）は別物。
