# HotTip

リマインダのようにちょっとした情報(Tips)を定期的に自動配信するbotです。
チャンネルに登録したTipsたちを決まったスケジュールで順番に配信します。

配信先は、Slack、Webhook(未実装)、Email(未実装)です。

## 環境構築

稼働方法は、docker-compose.yml を参考にしてください。
構成要素は以下のとおりです。

* アプリサーバー
  * データ編集操作用のサーバー
  * 認証にアプリ固有のアカウント管理と、Google OAuth2認証が使える
* 配信バッチサーバー (アプリサーバーと兼用することも可能)
  * スケジュールに応じたTipsの配信を行う
* データベース Postgresql、Sqlite(開発用)

以下にDockerイメージを作ってあります。

* https://cloud.docker.com/repository/docker/namutaka/hottip


起動に指定する環境変数は以下の通りです。

| env variable                     | 値例                                     | 説明 |
| --                               | --                                       | --   |
| DATABASE_TYPE                    | postgresql,sqlite                        | 利用するデータベースの種類を指定する |
| DATABASE_HOST                    | localhost                                | DBホスト名。postgresqlの場合のみ |
| DATABASE_PORT                    | 5432                                     | DBポート番号 |
| DATABASE_NAME                    | hottip                                   | DB名 |
| DATABASE_USER                    | hottip                                   | DB接続ユーザ名 |
| DATABASE_PASSWORD                | password                                 | DB接続パスワード |
| HOTTIP_SLACK_WEBHOOK_URL         | `https://hooks.slack.com/services/ZZZ/ZZZ` | Slack送信用のWebhook URL |
| HOTTIP_BATCH_MODE                | 1,0                                      | 配信バッチ処理を実行するかどうか(1: 実行する、0: 実行しない) |
| SOCIAL_AUTH_GOOGLE_OAUTH2_KEY    |                                          | Google OAuth2認証キー |
| SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET |                                          | Google OAuth2 認証のシークレットトークン |
| DJANGO_MANAGEPY_MIGRATE          | on,off                                   | アプリ起動時にDBマイグレーションを実行するかどうか(on: 実行する)。Dockerイメージでのみ使用 |
| DJANGO_MANAGEPY_CREATESUPERUSER  | on,off                                   | アプリ起動時にSuperUserを必ず１つは存在するように自動生成するかどうか(on: 実行する)。Dockerイメージでのみ使用 |


## 開発向け情報

開発用にはPythonとNodeの環境を使用します。
開発時のアプリは以下の２つで構成されます。

* プロジェクトルートディレクトリのDjango
  * django-adminによる管理画面
  * フロントエンド向けのGraphQLサーバー
* frontendフォルダ下でVue.jsアプリ
  * Django上のGraphQLを利用したフロントエンド
  * Djangoサーバー側に一部パスをproxyする

DjangoとVue.jsの２つのサーバーを起動させた上で、Vue.js側のURLにアクセスします。


### 初期セットアップ

1. プロジェクトルートディレクトリでPython依存モジュールをインストール
```
$ pipenv install --dev
```
2. frontendディレクトリでNode依存モジュールをインストール
```
$ cd frontend
$ yarn install
```
3. 開発用DBサーバーを起動する (Sqliteを使う場合は不要)
```
$ docker-compose up db -d
```
4. `.env`ファイルを作成し、必要な環境変数を指定する。
  * DB接続設定を指定
  * SlackのWebhook URLを取得し、それを指定
5. マイグレーションを実行する
```
$ pipenv run python manage.py migrate
```
6. 初期ユーザとしてSuperUserを作成する
```
$ pipenv run python manage.py createsuperuser
Enter admin user information.
```

### 開発時に使用する操作

* Djangoサーバーを起動
```
$ pipenv run server
```
* frontendサーバー起動
```
$ cd frontend
$ yarn serve
```
* frontendのコードを自動フォーマットする
```
$ cd frontend
$ yarn fix
```
* frontendにGraphQLの型定義を生成する
```
$ pipenv run update_gql
```
