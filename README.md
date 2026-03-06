# eagle-sdk-python

PythonでEagle APIを呼び出すためのラッパーライブラリです。

[Eagle](https://eagle.cool/) は画像・デザイン素材を管理するためのデスクトップアプリケーションです。本ライブラリは Eagle が提供するローカル API をPythonから簡単に利用できるようにします。

## 前提条件

- Eagle アプリが起動していること（APIサーバーは Eagle 起動時に自動的に立ち上がります）
- Eagle 1.11 Build21 (2020/06/17) 以降
- デフォルトのAPIエンドポイント: `http://localhost:41595`

## インストール

```bash
pip install eagle-sdk-python
```

## 使い方

```python
from eagle_sdk import EagleClient

client = EagleClient()  # デフォルト: http://localhost:41595

# アプリケーション情報を取得
info = client.application.info()

# ライブラリ情報を取得
library = client.library.info()

# URLから画像を追加
client.item.add_from_url(
    url="https://example.com/image.png",
    name="Sample Image",
    tags=["design", "sample"]
)

# アイテム一覧を取得
items = client.item.list(limit=50, tags="design")
```

## API リファレンス

公式APIドキュメント: https://api.eagle.cool/

### Application

| メソッド | APIエンドポイント | 説明 |
|---------|-----------------|------|
| `application.info()` | `GET /api/application/info` | Eagleアプリの情報を取得（バージョン、プラットフォーム等） |

### Item

| メソッド | APIエンドポイント | 説明 |
|---------|-----------------|------|
| `item.add_from_url()` | `POST /api/item/addFromURL` | URLから画像を追加 |
| `item.add_from_urls()` | `POST /api/item/addFromURLs` | URLから複数画像を一括追加 |
| `item.add_from_path()` | `POST /api/item/addFromPath` | ローカルファイルを追加 |
| `item.add_from_paths()` | `POST /api/item/addFromPaths` | ローカルファイルを一括追加 |
| `item.add_bookmark()` | `POST /api/item/addBookmark` | ブックマークを追加 |
| `item.info()` | `GET /api/item/info` | アイテムの詳細情報を取得 |
| `item.thumbnail()` | `GET /api/item/thumbnail` | サムネイル画像のパスを取得 |
| `item.update()` | `POST /api/item/update` | アイテム情報を更新 |
| `item.list()` | `GET /api/item/list` | アイテム一覧を取得（フィルタ対応） |
| `item.move_to_trash()` | `POST /api/item/moveToTrash` | アイテムをゴミ箱に移動 |
| `item.refresh_palette()` | `POST /api/item/refreshPalette` | カラーパレットを再解析 |
| `item.refresh_thumbnail()` | `POST /api/item/refreshThumbnail` | サムネイルを再生成 |

### Folder

| メソッド | APIエンドポイント | 説明 |
|---------|-----------------|------|
| `folder.create()` | `POST /api/folder/create` | フォルダを作成 |
| `folder.rename()` | `POST /api/folder/rename` | フォルダ名を変更 |
| `folder.update()` | `POST /api/folder/update` | フォルダ情報を更新（名前・説明・色） |
| `folder.list()` | `GET /api/folder/list` | フォルダ一覧を取得 |
| `folder.list_recent()` | `GET /api/folder/listRecent` | 最近使用したフォルダ一覧を取得 |

### Library

| メソッド | APIエンドポイント | 説明 |
|---------|-----------------|------|
| `library.info()` | `GET /api/library/info` | 現在のライブラリ情報を取得 |
| `library.history()` | `GET /api/library/history` | 最近開いたライブラリ一覧を取得 |
| `library.switch()` | `POST /api/library/switch` | ライブラリを切り替え |
| `library.icon()` | `GET /api/library/icon` | ライブラリのアイコン画像を取得 |

## 主要パラメータ

### item.add_from_url()

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `url` | str | Yes | 画像URL（http/https/base64対応） |
| `name` | str | Yes | 表示名 |
| `website` | str | No | 元のWebページURL |
| `tags` | list | No | タグ |
| `star` | int | No | 評価 |
| `annotation` | str | No | 注釈 |
| `modification_time` | int | No | 変更日時（タイムスタンプ） |
| `folder_id` | str | No | 保存先フォルダID |
| `headers` | dict | No | カスタムHTTPヘッダー |

### item.list()

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `limit` | int | No | 取得件数（デフォルト: 200） |
| `offset` | int | No | オフセット（デフォルト: 0） |
| `order_by` | str | No | ソート順（CREATEDATE, FILESIZE, NAME, RESOLUTION） |
| `keyword` | str | No | キーワード検索 |
| `ext` | str | No | 拡張子フィルタ（jpg, png等） |
| `tags` | str | No | タグフィルタ（カンマ区切り） |
| `folders` | str | No | フォルダフィルタ（カンマ区切り） |

## 開発環境セットアップ

本プロジェクトはパッケージマネージャーに [uv](https://docs.astral.sh/uv/) を使用しています。

```bash
# リポジトリのクローン
git clone https://github.com/your-username/eagle-sdk-python.git
cd eagle-sdk-python

# 依存関係のインストール（仮想環境の作成も自動で行われます）
uv sync

# テストの実行
uv run pytest

# パッケージのビルド
uv build
```

### 依存パッケージの追加

```bash
# ランタイム依存
uv add <package-name>

# 開発用依存
uv add --dev <package-name>
```

## ライセンス

MIT License
