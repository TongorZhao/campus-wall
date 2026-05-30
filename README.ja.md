# Campus Wall - キャンパスウォール

[中文](README.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | 日本語 | [한국어](README.ko.md) | [Русский](README.ru.md) | [العربية](README.ar.md) | [Português](README.pt.md)

Djangoベースのキャンパス匿名/公開フォーラムシステム。

## 機能

- ユーザー登録、ログイン、プロフィール管理
- 投稿（画像アップロード、匿名投稿対応）
- コメント、返信、いいね
- 投稿の保存
- カテゴリー・タグシステム
- 全文検索
- メッセージ機能
- 通知システム
- 通報機能
- フォロー/フォロワーシステム
- 管理画面

## 技術スタック

- **バックエンド**: Django 4.2 + PostgreSQL
- **フロントエンド**: Bootstrap 5 + Bootstrap Icons
- **リアルタイム**: Django Channels + Redis

## インストール

### 必要要件

- Python 3.10+
- PostgreSQL 12+
- Redis（WebSocket用）

### セットアップ

```bash
# プロジェクトをクローン
git clone https://github.com/TongorZhao/campus-wall.git
cd campus-wall

# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または venv\Scripts\activate  # Windows

# 依存関係をインストール
pip install -r requirements.txt

# 環境変数を設定
cp .env.example .env
# .envファイルを編集して設定を入力

# データベースマイグレーション
python manage.py makemigrations accounts posts notifications messages_app
python manage.py migrate

# スーパーユーザーを作成
python manage.py createsuperuser

# カテゴリーを初期化
python manage.py init_categories

# スタティックファイルを収集
python manage.py collectstatic

# 開発サーバーを起動
python manage.py runserver
```

### 本番環境

```bash
# Gunicornを使用
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4

# Daphneを使用（WebSocketサポート）
daphne -b 127.0.0.1 -p 8000 config.asgi:application

# Nginxを設定（nginx.conf.exampleを参照）
```

## プロジェクト構造

```
campus-wall/
├── config/                 # プロジェクト設定
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                   # アプリケーション
│   ├── accounts/           # ユーザー管理
│   ├── posts/              # 投稿管理
│   ├── messages_app/       # メッセージ機能
│   └── notifications/      # 通知システム
├── templates/              # テンプレートファイル
├── static/                 # スタティックファイル
├── media/                  # ユーザーアップロード
├── manage.py
└── requirements.txt
```

## デフォルトカテゴリー

- 告白の壁
- 落とし物・拾い物
- フリマーケット
- 不満発泄
- 学習交流
- サークル活動
- キャンパスニュース
- その他

## 注意事項

1. 本番環境では`DJANGO_SECRET_KEY`を変更してください
2. 本番環境では`DJANGO_DEBUG=False`を設定してください
3. PostgreSQLとRedisが正常に動作していることを確認してください
4. 定期的にデータベースをバックアップしてください
5. 適切なCORSとセキュリティポリシーを設定してください
