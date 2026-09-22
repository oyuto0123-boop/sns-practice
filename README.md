o# よりみち練習用


ハッカソンに向けた個人練習用リポジトリ
SNS「よりみち」趣味の口コミ匿名SNS

## 技術スタック

- Python  3.11 
- Flask   2.2.2 / Werkzeug 2.2.2
- Docker

## 構成
|ファイル|役割|
|---|---|
|`app.py`|最小のFlaskアプリ'/'にアクセスすると「よりみち」を返す|
|`requirements.txt`|使用ライブラリとバージョンの指定|
|`Dockerfile`|イメージのビルド手順|

## 動かし方
```bash
docker build -t yorimichi . # イメージを作る
docker run -p 5000:5000 yorimichi # 起動する

ブラウザで　http://localhost:5000　を開くと「よりみち」と表示される。
停止は　ctrl + C
```


## 詰まったメモ
9/23 記述
- Dockerfile の Python を Pyton と打ち間違え、ベースイメージのPullとコンテナ起動で失敗。
- Docker Desktop が pause 状態でビルド不可→Resume で解決。
- Flask だけ固定して、 Werkzeug 未固定→ url_quote の ImportEroor → Werkzeug==2.2.2 を追加して解決。


