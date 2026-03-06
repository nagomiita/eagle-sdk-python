# eagle-sdk-python 実装計画

## フェーズ 1: プロジェクト基盤

### 1.1 プロジェクトセットアップ
- [ ] `pyproject.toml` を作成（メタデータ、依存関係、ビルド設定）
- [ ] `eagle_sdk/__init__.py` を作成
- [ ] `eagle_sdk/api/__init__.py` を作成
- [ ] `tests/__init__.py` を作成

### 1.2 例外クラス
- [ ] `eagle_sdk/exceptions.py` を作成
  - `EagleError`（基底）
  - `EagleConnectionError`（接続失敗）
  - `EagleApiError`（APIエラー応答）

### 1.3 HTTP通信層
- [ ] `eagle_sdk/http.py` を作成
  - `HttpClient` クラス（httpxラッパー）
  - GET/POST メソッド
  - ステータス検査・例外変換

## フェーズ 2: データモデル

### 2.1 モデル定義
- [ ] `eagle_sdk/models.py` を作成
  - `ApplicationInfo`
  - `Palette`, `ItemDetail`
  - `Folder`, `FolderListItem`
  - `LibraryInfo`
  - `AddItemFromUrlParam`, `AddItemFromPathParam`（TypedDict）
  - JSON → dataclass 変換ユーティリティ（camelCase → snake_case）

## フェーズ 3: APIクラス実装

### 3.1 ApplicationAPI
- [ ] `eagle_sdk/api/application.py` を作成
  - `info()` → `ApplicationInfo`

### 3.2 ItemAPI
- [ ] `eagle_sdk/api/item.py` を作成
  - `add_from_url()` — URLから画像追加
  - `add_from_urls()` — URL一括追加
  - `add_from_path()` — ローカルファイル追加
  - `add_from_paths()` — ローカルファイル一括追加
  - `add_bookmark()` — ブックマーク追加
  - `info()` — アイテム情報取得
  - `thumbnail()` — サムネイルパス取得
  - `update()` — アイテム更新
  - `list()` — アイテム一覧取得
  - `move_to_trash()` — ゴミ箱移動
  - `refresh_palette()` — カラーパレット再解析
  - `refresh_thumbnail()` — サムネイル再生成

### 3.3 FolderAPI
- [ ] `eagle_sdk/api/folder.py` を作成
  - `create()` — フォルダ作成
  - `rename()` — フォルダ名変更
  - `update()` — フォルダ情報更新
  - `list()` — フォルダ一覧取得
  - `list_recent()` — 最近使用フォルダ取得

### 3.4 LibraryAPI
- [ ] `eagle_sdk/api/library.py` を作成
  - `info()` — ライブラリ情報取得
  - `history()` — 履歴取得
  - `switch()` — ライブラリ切替
  - `icon()` — アイコン画像取得

## フェーズ 4: クライアント統合

### 4.1 EagleClient
- [ ] `eagle_sdk/client.py` を作成
  - コンストラクタ（base_url, timeout）
  - `application`, `item`, `folder`, `library` プロパティ
- [ ] `eagle_sdk/__init__.py` でエクスポート整理
  - `EagleClient`, 例外クラス, モデルクラス

## フェーズ 5: テスト

### 5.1 ユニットテスト
- [ ] `tests/test_client.py` — クライアント初期化テスト
- [ ] `tests/test_application.py` — ApplicationAPI テスト
- [ ] `tests/test_item.py` — ItemAPI テスト（全12メソッド）
- [ ] `tests/test_folder.py` — FolderAPI テスト（全5メソッド）
- [ ] `tests/test_library.py` — LibraryAPI テスト（全4メソッド）

テスト方針:
- `pytest-httpx` を使用してHTTPリクエストをモック
- 各メソッドについて正常系・異常系をテスト
- リクエストボディ/パラメータの正しさを検証

## フェーズ 6: 仕上げ

### 6.1 ドキュメント・配布準備
- [ ] README.md の使い方セクションが実装と整合していることを確認
- [ ] LICENSE ファイルを作成（MIT）
- [ ] .gitignore を作成

## 実装順序

```
フェーズ1 → フェーズ2 → フェーズ3 → フェーズ4 → フェーズ5 → フェーズ6
```

各フェーズは前のフェーズに依存する。フェーズ3のAPIクラス（3.1〜3.4）は互いに独立しているため並行実装可能。
