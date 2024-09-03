# 著者記号管理システム

## 使用技術一覧
<img src="https://img.shields.io/badge/-django-ced5d2.svg?style=for-the-badge&logo=django&logoColor=%23092E20">
<img src="https://img.shields.io/badge/-python-ebf1f7.svg?style=for-the-badge&logo=python&logoColor=3776AB">
<img src="https://img.shields.io/badge/-redis-ffeceb.svg?style=for-the-badge&logo=redis&logoColor=FF4438">
<img src="https://img.shields.io/badge/-celery-ebf2ed.svg?style=for-the-badge&logo=celery&logoColor=37814A">
<img src="https://img.shields.io/badge/-postgresql-ecf0fc.svg?style=for-the-badge&logo=postgresql&logoColor=4169E1">
<img src="https://img.shields.io/badge/-javascript-312d06.svg?style=for-the-badge&logo=javascript&logoColor=F7DF1E">

## 概要
カッター・サンボーン著者記号に独自分類を付与した著者記号を管理するためのWEBシステムです。  
実行手順に従ってDocker環境を立ち上げると動作を確認できます。

ローカル環境でのテスト用コードとなっています。  
本番環境へのデプロイにはセキュリティ上等の問題があります。  

そのままサーバ上で実行することは行わないでください。  
適切なセキュリティ対策等を実施せずに稼働させたことにより生じた損害等の責任は負いません。

### 実行環境

macOS Sonoma 14.5 上の Docker v4.33.0 での動作を確認しています。

## 実行方法

全てのファイルをプロジェクトディレクトリに保存した後、ディレクトリに入って下記のコマンドを実行してください。

#### 1. コンテナの起動と実行

```docker compose -f docker-compose.development.yml up -d --build```

#### 2. 静的ファイルの集合配置（初回起動時のみ）

```docker compose -f docker-compose.development.yml exec -u _apt app python manage.py collectstatic --no-input --clear```

#### 3. 管理者ユーザーの作成（初回起動時のみ）

```docker compose -f docker-compose.development.yml exec app python manage.py createsuperuser```
