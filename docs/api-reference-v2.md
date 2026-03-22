# Eagle API v2 リファレンス

公式ドキュメント: https://developer.eagle.cool/web-api

## 概要

Eagle Web API v2は、Eagle アプリが起動している間のみ利用可能なローカルAPIです。v1と比較して、全文検索、AIセマンティック検索、タグ・フォルダの包括的管理、自動ページネーションなど大幅に機能が拡張されています。

- **ベースURL:** `http://localhost:41595/api/v2/`
- **ポート:** 41595（デフォルト）
- **レスポンス形式:** JSON（JSend形式）
- **必要バージョン:** Eagle 4.0 Build 21 以降
- **呼び出し制限:** なし（ローカル通信のため）
- **ページネーション:** デフォルト50件、最大1000件

### 認証

- **ローカルアクセス:** localhost / 127.0.0.1 / 0.0.0.0 からのリクエストは認証不要
- **リモートアクセス:** APIトークンをクエリパラメータとして付与（`?token=...`）。トークンはEagleの開発者設定から取得可能

### レスポンス形式

**成功時:**
```json
{
    "status": "success",
    "data": { ... }
}
```

**エラー時:**
```json
{
    "status": "error",
    "message": "エラーメッセージ"
}
```

---

## 目次

- [App](#app)
  - [GET /api/v2/app/info](#get-apiv2appinfo)
- [Item](#item)
  - [GET /api/v2/item/get](#get-apiv2itemget)
  - [POST /api/v2/item/get](#post-apiv2itemget)
  - [POST /api/v2/item/query](#post-apiv2itemquery)
  - [GET /api/v2/item/countAll](#get-apiv2itemcountall)
  - [POST /api/v2/item/add](#post-apiv2itemadd)
  - [POST /api/v2/item/update](#post-apiv2itemupdate)
  - [POST /api/v2/item/setCustomThumbnail](#post-apiv2itemsetcustomthumbnail)
  - [POST /api/v2/item/refreshThumbnail](#post-apiv2itemrefreshthumbnail)
- [Folder](#folder)
  - [GET /api/v2/folder/get](#get-apiv2folderget)
  - [POST /api/v2/folder/get](#post-apiv2folderget)
  - [POST /api/v2/folder/create](#post-apiv2foldercreate)
  - [POST /api/v2/folder/update](#post-apiv2folderupdate)
- [Tag](#tag)
  - [GET /api/v2/tag/get](#get-apiv2tagget)
  - [POST /api/v2/tag/get](#post-apiv2tagget)
  - [GET /api/v2/tag/getRecentTags](#get-apiv2taggetrecenttags)
  - [GET /api/v2/tag/getStarredTags](#get-apiv2taggetstarredtags)
  - [POST /api/v2/tag/update](#post-apiv2tagupdate)
  - [POST /api/v2/tag/merge](#post-apiv2tagmerge)
- [Tag Group](#tag-group)
  - [GET /api/v2/tagGroup/get](#get-apiv2taggroupget)
  - [POST /api/v2/tagGroup/create](#post-apiv2taggroupcreate)
  - [POST /api/v2/tagGroup/update](#post-apiv2taggroupupdate)
  - [POST /api/v2/tagGroup/remove](#post-apiv2taggroupremove)
  - [POST /api/v2/tagGroup/addTags](#post-apiv2taggroupaddtags)
  - [POST /api/v2/tagGroup/removeTags](#post-apiv2taggroupremovetags)
- [Library](#library)
  - [GET /api/v2/library/info](#get-apiv2libraryinfo)
  - [GET /api/v2/library/history](#get-apiv2libraryhistory)
  - [POST /api/v2/library/switch](#post-apiv2libraryswitch)
  - [GET /api/v2/library/icon](#get-apiv2libraryicon)
- [AI Search](#ai-search)
  - [GET /api/v2/aiSearch/isInstalled](#get-apiv2aisearchisinstalled)
  - [GET /api/v2/aiSearch/isReady](#get-apiv2aisearchisready)
  - [GET /api/v2/aiSearch/isStarting](#get-apiv2aisearchisstarting)
  - [GET /api/v2/aiSearch/isSyncing](#get-apiv2aisearchissyncing)
  - [GET /api/v2/aiSearch/getSyncStatus](#get-apiv2aisearchgetsyncstatus)
  - [GET /api/v2/aiSearch/checkServiceHealth](#get-apiv2aisearchcheckservicehealth)
  - [POST /api/v2/aiSearch/searchByText](#post-apiv2aisearchsearchbytext)
  - [POST /api/v2/aiSearch/searchByBase64](#post-apiv2aisearchsearchbybase64)
  - [POST /api/v2/aiSearch/searchByItemId](#post-apiv2aisearchsearchbyitemid)

---

## App

### GET /api/v2/app/info

Eagle アプリの情報を取得します。バージョンやプラットフォーム情報の確認に使用します。

**パラメータ:** なし

**リクエスト例:**

```
GET http://localhost:41595/api/v2/app/info
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "version": "4.0.0",
        "prereleaseVersion": null,
        "buildVersion": "build12",
        "platform": "win32"
    }
}
```

| フィールド | 型 | 説明 |
|-----------|-----|------|
| version | string | アプリケーションバージョン（例: `"4.0.0"`） |
| prereleaseVersion | string\|null | プレリリースバージョン（正式版の場合はnull） |
| buildVersion | string\|null | ビルドバージョン（例: `"build12"`） |
| platform | string | OS識別子（`"win32"` または `"darwin"`） |

---

## Item

### GET /api/v2/item/get

条件に一致するアイテムの一覧を取得します。ページネーション付きの結果を返します。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string | No | 単一アイテムのID |
| ids | string | No | カンマ区切りのアイテムID |
| isSelected | boolean | No | 現在選択中のアイテムを取得 |
| isUntagged | boolean | No | タグなしのアイテムを取得 |
| isUnfiled | boolean | No | フォルダに属さないアイテムを取得 |
| keywords | string | No | カンマ区切りのキーワードフィルタ |
| tags | string | No | カンマ区切りのタグフィルタ |
| folders | string | No | カンマ区切りのフォルダIDフィルタ |
| ext | string | No | 拡張子フィルタ（例: `jpg`, `png`） |
| annotation | string | No | 注釈テキストフィルタ |
| rating | integer | No | 評価フィルタ（0-5） |
| url | string | No | 出典元URLフィルタ |
| shape | string | No | 画像形状フィルタ。`square`, `portrait`, `panoramic-portrait`, `landscape`, `panoramic-landscape` |
| fields | string | No | カンマ区切りの取得フィールド指定 |
| offset | integer | No | オフセット（デフォルト: 0） |
| limit | integer | No | 取得件数（デフォルト: 50、最大: 1000） |

**リクエスト例:**

```
GET http://localhost:41595/api/v2/item/get?tags=design,illustration&limit=20
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "data": [
            {
                "id": "M3QSGJNQTC2DG",
                "name": "sunset-photo",
                "ext": "jpg",
                "width": 1920,
                "height": 1080,
                "url": "https://example.com/photo.jpg",
                "tags": ["nature", "sunset"],
                "folders": ["FOLDER_ID_1"],
                "star": 4,
                "annotation": "Beautiful sunset at the beach",
                "modificationTime": 1700000000000
            }
        ],
        "total": 1250,
        "offset": 0,
        "limit": 50
    }
}
```

---

### POST /api/v2/item/get

GET版と同じ機能ですが、フィルタパラメータをJSONリクエストボディで受け取ります。配列を使った複雑なクエリに適しています。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string | No | アイテムID |
| ids | string[] | No | アイテムIDの配列 |
| isSelected | boolean | No | 現在選択中のアイテムを取得 |
| isUntagged | boolean | No | タグなしのアイテムを取得 |
| isUnfiled | boolean | No | フォルダに属さないアイテムを取得 |
| keywords | string[] | No | キーワードの配列 |
| tags | string[] | No | タグの配列 |
| folders | string[] | No | フォルダIDの配列 |
| ext | string | No | 拡張子フィルタ |
| annotation | string | No | 注釈テキストフィルタ |
| rating | integer | No | 評価フィルタ（0-5） |
| url | string | No | 出典元URLフィルタ |
| shape | string | No | 画像形状フィルタ |
| fields | string[] | No | 取得フィールドの配列 |
| offset | integer | No | オフセット（デフォルト: 0） |
| limit | integer | No | 取得件数（デフォルト: 50、最大: 1000） |

**リクエスト例:**

```json
{
    "tags": ["design", "inspiration"],
    "limit": 20
}
```

**レスポンス:** GET /api/v2/item/get と同じ形式

---

### POST /api/v2/item/query

アイテム名、タグ、注釈、URL、フォルダ名などを対象とした全文検索を実行します。高度なクエリ構文をサポートします。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| query | string | Yes | 検索クエリ文字列 |
| offset | integer | No | オフセット（デフォルト: 0） |
| limit | integer | No | 取得件数（デフォルト: 50、最大: 1000） |

**クエリ構文:**

| 構文 | 説明 |
|------|------|
| `word` | wordを含む |
| `a b` | aとb両方を含む（AND） |
| `a OR b` / `a \|\| b` | aまたはbを含む（OR） |
| `-word` | wordを含まない（NOT） |
| `"phrase"` | 完全一致フレーズ |
| `(a OR b) c` | グルーピング |

**リクエスト例:**

```json
{
    "query": "(cat OR dog) -cartoon",
    "limit": 20
}
```

**レスポンス:** GET /api/v2/item/get と同じ形式

---

### GET /api/v2/item/countAll

ライブラリ内のアイテム総数を取得します。

**パラメータ:** なし

**リクエスト例:**

```
GET http://localhost:41595/api/v2/item/countAll
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": 12500
}
```

---

### POST /api/v2/item/add

URL、Base64データ、ローカルファイルパス、またはブックマークからアイテムを追加します。単一追加とバッチ追加の両方に対応しています。

**リクエストボディ（単一追加）:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| url | string | いずれか1つ必須 | ダウンロードする画像のURL |
| base64 | string | いずれか1つ必須 | Base64エンコードされた画像データ |
| path | string | いずれか1つ必須 | ローカルファイルのパス |
| bookmarkURL | string | いずれか1つ必須 | ブックマークとして追加するURL |
| id | string | No | カスタムアイテムID |
| name | string | No | アイテム名 |
| tags | string[] | No | タグの配列 |
| folders | string[] | No | 保存先フォルダIDの配列 |
| annotation | string | No | 注釈 |
| website | string | No | 出典元URL |

**リクエストボディ（バッチ追加）:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| items | object[] | Yes | 追加するアイテムの配列（最大1000件）。各要素は単一追加と同じフィールド |

**リクエスト例（単一追加）:**

```json
{
    "url": "https://example.com/photo.jpg",
    "name": "Example Photo",
    "tags": ["downloaded", "example"],
    "folders": ["FOLDER_ID"]
}
```

**レスポンス例（単一追加）:**

```json
{
    "status": "success",
    "data": {
        "id": "M3QSGJNQTC2DG"
    }
}
```

**リクエスト例（バッチ追加）:**

```json
{
    "items": [
        {
            "url": "https://example.com/photo1.jpg",
            "name": "Photo 1"
        },
        {
            "path": "C:\\Users\\User\\Downloads\\design.png",
            "name": "Design"
        }
    ]
}
```

**レスポンス例（バッチ追加）:**

```json
{
    "status": "success",
    "data": {
        "ids": ["ITEM_ID_1", "ITEM_ID_2"]
    }
}
```

---

### POST /api/v2/item/update

アイテムのメタデータを更新します。指定したフィールドのみが変更されます。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string | Yes | 更新対象のアイテムID |
| name | string | No | 新しいアイテム名 |
| tags | string[] | No | タグ（置換） |
| folders | string[] | No | フォルダ割り当て（置換） |
| annotation | string | No | 注釈 |
| url | string | No | 出典元URL |
| star | integer | No | 評価（0-5） |
| modificationTime | integer | No | 変更日時タイムスタンプ |
| noThumbnail | boolean | No | サムネイルなしフラグ |
| noPreview | boolean | No | プレビュー無効フラグ |
| isDeleted | boolean | No | ゴミ箱への移動/復元 |

**リクエスト例:**

```json
{
    "id": "M3QSGJNQTC2DG",
    "name": "Updated Name",
    "tags": ["tag1", "tag2"],
    "star": 5
}
```

**レスポンス:** 更新後の完全なアイテムオブジェクトを返します。

---

### POST /api/v2/item/setCustomThumbnail

ローカルの画像ファイルからアイテムのカスタムサムネイルを設定します。

> **注意:** この操作は非同期です。サムネイル生成完了まで最大10秒間レスポンスを待機します。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| itemId | string | Yes | アイテムID |
| filePath | string | Yes | サムネイル画像のファイルパス |

**リクエスト例:**

```json
{
    "itemId": "M3QSGJNQTC2DG",
    "filePath": "C:\\Users\\User\\thumbnails\\custom.png"
}
```

**レスポンス例:**

```json
{
    "status": "success"
}
```

---

### POST /api/v2/item/refreshThumbnail

アイテムのサムネイルを再生成します。ファイルサイズ、寸法、カラーパレットも再計算されます。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| itemId | string | Yes | アイテムID |

**リクエスト例:**

```json
{
    "itemId": "M3QSGJNQTC2DG"
}
```

**レスポンス例:**

```json
{
    "status": "success"
}
```

---

### Item プロパティリファレンス

アイテムオブジェクトに含まれるプロパティ一覧:

| プロパティ | 型 | 説明 |
|-----------|-----|------|
| id | string | アイテムの一意識別子 |
| name | string | アイテム名 |
| ext | string | ファイル拡張子 |
| width | integer | 画像の幅（px） |
| height | integer | 画像の高さ（px） |
| url | string | 出典元URL |
| isDeleted | boolean | ゴミ箱に入っているかどうか |
| annotation | string | 注釈 |
| tags | string[] | タグ名の配列 |
| folders | string[] | フォルダIDの配列 |
| palettes | object[] | カラーパレット（RGB値と比率） |
| size | integer | ファイルサイズ（バイト） |
| star | integer | 評価（0-5） |
| modificationTime | integer | 最終更新日時タイムスタンプ |
| noThumbnail | boolean | サムネイルなしフラグ |
| noPreview | boolean | ダブルクリックプレビュー無効フラグ |

---

## Folder

### GET /api/v2/folder/get

条件に一致するフォルダの一覧を取得します。ページネーション付きの結果を返します。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string | No | 単一フォルダのID |
| ids | string | No | カンマ区切りのフォルダID |
| isSelected | boolean | No | 現在選択中のフォルダを取得 |
| isRecent | boolean | No | 最近使用したフォルダを取得 |
| offset | integer | No | オフセット（デフォルト: 0） |
| limit | integer | No | 取得件数（デフォルト: 50、最大: 1000） |

**リクエスト例:**

```
GET http://localhost:41595/api/v2/folder/get?id=LRK3AQGN7VCB1
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "data": [
            {
                "id": "LRK3AQGN7VCB1",
                "name": "Design References",
                "description": "UI/UX design references",
                "children": [],
                "modificationTime": 1700000000000,
                "tags": [],
                "iconColor": "blue",
                "imageCount": 42
            }
        ],
        "total": 25,
        "offset": 0,
        "limit": 50
    }
}
```

---

### POST /api/v2/folder/get

GET版と同じ機能ですが、フィルタパラメータをJSONリクエストボディで受け取ります。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string | No | フォルダID |
| ids | string[] | No | フォルダIDの配列 |
| isSelected | boolean | No | 現在選択中のフォルダを取得 |
| isRecent | boolean | No | 最近使用したフォルダを取得 |
| offset | integer | No | オフセット（デフォルト: 0） |
| limit | integer | No | 取得件数（デフォルト: 50、最大: 1000） |

**リクエスト例:**

```json
{
    "ids": ["FOLDER_ID_1", "FOLDER_ID_2"]
}
```

**レスポンス:** GET /api/v2/folder/get と同じ形式

---

### POST /api/v2/folder/create

ライブラリに新しいフォルダを作成します。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| name | string | Yes | フォルダ名 |
| description | string | No | フォルダの説明 |
| parent | string | No | 親フォルダのID。省略するとルートレベルに作成 |

**リクエスト例:**

```json
{
    "name": "My New Folder",
    "description": "A subfolder for organizing",
    "parent": "PARENT_FOLDER_ID"
}
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "id": "NEW_FOLDER_ID",
        "name": "My New Folder",
        "description": "",
        "children": [],
        "modificationTime": 1700000000000,
        "tags": []
    }
}
```

---

### POST /api/v2/folder/update

既存フォルダのメタデータを更新します。指定したフィールドのみが変更されます。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string | Yes | 更新対象のフォルダID |
| name | string | No | 新しいフォルダ名 |
| description | string | No | 新しい説明文 |
| tags | string[] | No | フォルダタグ（置換） |
| iconColor | string | No | アイコンの色。`red`, `orange`, `yellow`, `green`, `aqua`, `blue`, `purple`, `pink` のいずれか |
| parent | string\|null | No | 親フォルダの移動先。`null`を指定するとルートに移動 |

**リクエスト例:**

```json
{
    "id": "LRK3AQGN7VCB1",
    "name": "Renamed Folder",
    "iconColor": "green"
}
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "id": "LRK3AQGN7VCB1",
        "name": "Renamed Folder",
        "description": "UI/UX design references",
        "children": [],
        "modificationTime": 1700000000000,
        "tags": [],
        "iconColor": "green",
        "imageCount": 42
    }
}
```

---

### Folder プロパティリファレンス

| プロパティ | 型 | 説明 |
|-----------|-----|------|
| id | string | フォルダの一意識別子 |
| name | string | フォルダ名 |
| description | string | フォルダの説明 |
| children | object[] | 子フォルダの配列 |
| modificationTime | integer | 最終更新日時タイムスタンプ |
| tags | string[] | タグ名の配列 |
| iconColor | string | アイコンの色 |
| imageCount | integer | フォルダ内のアイテム数 |

---

## Tag

### GET /api/v2/tag/get

ライブラリ内の全タグを一覧取得します。ページネーション付きの結果を返します。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| name | string | No | タグ名フィルタ（部分一致） |
| offset | integer | No | オフセット（デフォルト: 0） |
| limit | integer | No | 取得件数（デフォルト: 50、最大: 1000） |

**リクエスト例:**

```
GET http://localhost:41595/api/v2/tag/get?name=design&offset=50&limit=100
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "data": [
            {
                "name": "design",
                "count": 150,
                "color": "",
                "groups": ["GROUP_ID_1"],
                "pinyin": "design"
            }
        ],
        "total": 340,
        "offset": 0,
        "limit": 50
    }
}
```

---

### POST /api/v2/tag/get

GET版と同じ機能ですが、フィルタパラメータをJSONリクエストボディで受け取ります。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| name | string | No | タグ名フィルタ（部分一致） |
| offset | integer | No | オフセット（デフォルト: 0） |
| limit | integer | No | 取得件数（デフォルト: 50、最大: 1000） |

**リクエスト例:**

```json
{
    "name": "design",
    "limit": 100
}
```

**レスポンス:** GET /api/v2/tag/get と同じ形式

---

### GET /api/v2/tag/getRecentTags

最近使用したタグを取得します。ページネーション付きの結果を返します。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| offset | integer | No | オフセット（デフォルト: 0） |
| limit | integer | No | 取得件数（デフォルト: 50、最大: 1000） |

**リクエスト例:**

```
GET http://localhost:41595/api/v2/tag/getRecentTags
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "data": [
            {
                "name": "ui-design",
                "count": 45,
                "color": "",
                "groups": [],
                "pinyin": "ui-design"
            }
        ],
        "total": 12,
        "offset": 0,
        "limit": 50
    }
}
```

---

### GET /api/v2/tag/getStarredTags

スター付き（ピン留め）タグを取得します。ページネーション付きの結果を返します。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| offset | integer | No | オフセット（デフォルト: 0） |
| limit | integer | No | 取得件数（デフォルト: 50、最大: 1000） |

**リクエスト例:**

```
GET http://localhost:41595/api/v2/tag/getStarredTags
```

**レスポンス:** GET /api/v2/tag/getRecentTags と同じ形式

---

### POST /api/v2/tag/update

既存のタグ名を変更します。このタグを使用している全アイテムが自動的に更新されます。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| originalName | string | Yes | 現在のタグ名 |
| name | string | Yes | 新しいタグ名 |

**リクエスト例:**

```json
{
    "originalName": "old-tag-name",
    "name": "new-tag-name"
}
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "name": "new-tag-name",
        "count": 45,
        "color": "",
        "groups": [],
        "pinyin": "new-tag-name"
    }
}
```

---

### POST /api/v2/tag/merge

ソースタグをターゲットタグにマージします。ソースタグを持つ全アイテムのタグがターゲットタグに置換され、ソースタグはマージ後に削除されます。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| source | string | Yes | マージ元のタグ名（削除される） |
| target | string | Yes | マージ先のタグ名（保持される） |

**リクエスト例:**

```json
{
    "source": "photograph",
    "target": "photography"
}
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "affectedItems": 25,
        "sourceRemoved": true
    }
}
```

---

### Tag プロパティリファレンス

| プロパティ | 型 | 説明 |
|-----------|-----|------|
| name | string | タグ名 |
| count | integer | このタグを使用しているアイテム数 |
| color | string | タグの色（未設定時は空文字列） |
| groups | string[] | タググループIDの配列 |
| pinyin | string | 名前のピンイン表記 |

---

## Tag Group

### GET /api/v2/tagGroup/get

全タググループを一覧取得します。ページネーション付きの結果を返します。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| offset | integer | No | オフセット（デフォルト: 0） |
| limit | integer | No | 取得件数（デフォルト: 50、最大: 1000） |

**リクエスト例:**

```
GET http://localhost:41595/api/v2/tagGroup/get
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "data": [
            {
                "id": "TG_001",
                "name": "Design Styles",
                "color": "blue",
                "tags": ["flat", "material", "skeuomorphic"],
                "description": "Visual design styles"
            }
        ],
        "total": 5,
        "offset": 0,
        "limit": 50
    }
}
```

---

### POST /api/v2/tagGroup/create

新しいタググループを作成します。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| name | string | Yes | グループ名 |
| tags | string[] | Yes | グループに含めるタグ名の配列 |
| color | string | No | グループの色 |
| description | string | No | グループの説明 |

**リクエスト例:**

```json
{
    "name": "Color Palette",
    "tags": ["warm", "cool", "neutral"],
    "description": "Tags for color palettes"
}
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "id": "NEW_GROUP_ID",
        "name": "Color Palette",
        "color": "",
        "tags": ["warm", "cool", "neutral"],
        "description": "Tags for color palettes"
    }
}
```

---

### POST /api/v2/tagGroup/update

既存のタググループを更新します。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string | Yes | 更新対象のタググループID |
| name | string | Yes | グループ名 |
| tags | string[] | Yes | タグ名の配列（既存のタグを置換） |
| color | string | No | グループの色 |
| description | string | No | グループの説明 |

**リクエスト例:**

```json
{
    "id": "TG_001",
    "name": "Updated Group Name",
    "tags": ["tag1", "tag2", "tag3"],
    "color": "green"
}
```

**レスポンス:** 更新後のタググループオブジェクトを返します。

---

### POST /api/v2/tagGroup/remove

タググループを削除します。グループのみが削除され、タグ自体は削除されません。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string | Yes | 削除対象のタググループID |

**リクエスト例:**

```json
{
    "id": "TG_001"
}
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": true
}
```

---

### POST /api/v2/tagGroup/addTags

既存のタググループにタグを追加します。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| groupId | string | Yes | タググループID |
| tags | string[] | Yes | 追加するタグ名の配列 |
| removeFromSource | boolean | No | `true`の場合、追加前に元のグループからタグを削除 |

**リクエスト例:**

```json
{
    "groupId": "TG_001",
    "tags": ["minimalist", "modern"]
}
```

**レスポンス:** 更新後のタググループオブジェクトを返します。

---

### POST /api/v2/tagGroup/removeTags

タググループからタグを削除します。タグ自体は削除されず、グループからの関連付けのみが解除されます。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| groupId | string | Yes | タググループID |
| tags | string[] | Yes | グループから削除するタグ名の配列 |

**リクエスト例:**

```json
{
    "groupId": "TG_001",
    "tags": ["outdated-tag"]
}
```

**レスポンス:** 更新後のタググループオブジェクトを返します。

---

### Tag Group プロパティリファレンス

| プロパティ | 型 | 説明 |
|-----------|-----|------|
| id | string | タググループの一意識別子 |
| name | string | グループ名 |
| color | string | グループの色 |
| tags | string[] | グループ内のタグ名の配列 |
| description | string | グループの説明 |

---

## Library

### GET /api/v2/library/info

現在開いているライブラリのメタデータを取得します。フォルダ、スマートフォルダ、タググループ、クイックアクセスなどの情報を含みます。

**パラメータ:** なし

**リクエスト例:**

```
GET http://localhost:41595/api/v2/library/info
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "name": "My Design Library",
        "path": "D:\\Eagle Libraries\\My Design Library.library",
        "modificationTime": 1700000000000,
        "applicationVersion": "4.0",
        "folders": [],
        "smartFolders": [],
        "quickAccess": [],
        "tagGroups": []
    }
}
```

| フィールド | 型 | 説明 |
|-----------|-----|------|
| name | string | ライブラリの表示名 |
| path | string | `.library`ディレクトリへのフルパス |
| modificationTime | integer | 最終更新日時タイムスタンプ |
| applicationVersion | string | ライブラリを作成したEagleバージョン |
| folders | object[] | トップレベルフォルダ構造 |
| smartFolders | object[] | スマートフォルダ設定 |
| quickAccess | object[] | クイックアクセス項目 |
| tagGroups | object[] | タググループ定義 |

---

### GET /api/v2/library/history

最近開いたライブラリの一覧を取得します。ページネーション付きの結果を返します。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| offset | integer | No | オフセット（デフォルト: 0） |
| limit | integer | No | 取得件数（デフォルト: 50、最大: 1000） |

**リクエスト例:**

```
GET http://localhost:41595/api/v2/library/history
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "data": [
            {
                "name": "My Design Library",
                "path": "D:\\Eagle Libraries\\My Design Library.library"
            }
        ],
        "total": 3,
        "offset": 0,
        "limit": 50
    }
}
```

| フィールド | 型 | 説明 |
|-----------|-----|------|
| data | object[] | ライブラリオブジェクトの配列（`name`と`path`を含む） |
| total | integer | ライブラリ総数 |
| offset | integer | 現在のオフセット |
| limit | integer | 現在のリミット |

---

### POST /api/v2/library/switch

開くライブラリを切り替えます。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| libraryPath | string | Yes | 切り替え先のライブラリパス |

**リクエスト例:**

```json
{
    "libraryPath": "D:\\Eagle Libraries\\My Design Library.library"
}
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": true
}
```

---

### GET /api/v2/library/icon

指定したライブラリのアイコン画像を取得します。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| libraryPath | string | Yes | ライブラリのパス（URLエンコードが必要） |

**リクエスト例:**

```
GET http://localhost:41595/api/v2/library/icon?libraryPath=D%3A%5CEagle%20Libraries%5CMy%20Design%20Library.library
```

**レスポンス:** ライブラリのアイコン画像データ（バイナリ）が返されます。

---

## AI Search

AI Searchプラグインによるセマンティック検索機能を提供します。テキスト、画像、既存アイテムをベースにした類似検索が可能です。

### GET /api/v2/aiSearch/isInstalled

AI Searchプラグインがインストールされているかどうかを確認します。

**パラメータ:** なし

**リクエスト例:**

```
GET http://localhost:41595/api/v2/aiSearch/isInstalled
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": true
}
```

---

### GET /api/v2/aiSearch/isReady

AI Searchが完全に初期化され、検索クエリを受け付ける準備ができているかを確認します。

**パラメータ:** なし

**リクエスト例:**

```
GET http://localhost:41595/api/v2/aiSearch/isReady
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": true
}
```

---

### GET /api/v2/aiSearch/isStarting

AI Searchサービスが初期化中かどうかを確認します。

**パラメータ:** なし

**リクエスト例:**

```
GET http://localhost:41595/api/v2/aiSearch/isStarting
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": false
}
```

---

### GET /api/v2/aiSearch/isSyncing

AI Searchがライブラリデータのインデックス作成中かどうかを確認します。

**パラメータ:** なし

**リクエスト例:**

```
GET http://localhost:41595/api/v2/aiSearch/isSyncing
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": false
}
```

---

### GET /api/v2/aiSearch/getSyncStatus

同期の詳細なステータスと進捗情報を取得します。

**パラメータ:** なし

**リクエスト例:**

```
GET http://localhost:41595/api/v2/aiSearch/getSyncStatus
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "isSyncing": false,
        "syncedCount": 12500,
        "totalCount": 12500,
        "progress": 1.0
    }
}
```

| フィールド | 型 | 説明 |
|-----------|-----|------|
| isSyncing | boolean | 現在同期中かどうか |
| syncedCount | integer | インデックス済みアイテム数 |
| totalCount | integer | インデックス対象の総アイテム数 |
| progress | decimal | 完了率（0.0-1.0） |

---

### GET /api/v2/aiSearch/checkServiceHealth

AI Searchサービスの診断チェックを実行します。

**パラメータ:** なし

**リクエスト例:**

```
GET http://localhost:41595/api/v2/aiSearch/checkServiceHealth
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "healthy": true
    }
}
```

---

### POST /api/v2/aiSearch/searchByText

自然言語テキストによるセマンティック検索を実行し、意味的に一致するアイテムを返します。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| query | string | Yes | 検索するテキスト説明 |
| options | object | No | 検索オプション |
| options.limit | integer | No | 最大結果件数 |

**リクエスト例:**

```json
{
    "query": "an orange cat sitting on a windowsill",
    "options": {
        "limit": 20
    }
}
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "results": [
            {
                "item": {
                    "id": "M3QSGJNQTC2DG",
                    "name": "sunset-beach",
                    "ext": "jpg",
                    "width": 1920,
                    "height": 1080,
                    "tags": ["nature", "sunset"],
                    "star": 4
                },
                "score": 0.892
            },
            {
                "item": {
                    "id": "K7XPWQBN9TC3F",
                    "name": "golden-hour",
                    "ext": "png",
                    "width": 2560,
                    "height": 1440,
                    "tags": ["photography"],
                    "star": 3
                },
                "score": 0.756
            }
        ]
    }
}
```

| フィールド | 型 | 説明 |
|-----------|-----|------|
| item.id | string | アイテムの一意識別子 |
| item.name | string | アイテム名 |
| item.ext | string | ファイル拡張子 |
| item.width | integer | 画像の幅（px） |
| item.height | integer | 画像の高さ（px） |
| item.tags | string[] | タグの配列 |
| item.star | integer | 評価 |
| score | decimal | 関連度スコア（0.0-1.0） |

---

### POST /api/v2/aiSearch/searchByBase64

Base64エンコードされた画像データを使った逆画像検索で、視覚的に類似したアイテムを検索します。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| base64 | string | Yes | Base64エンコードされた画像データ |
| options | object | No | 検索オプション |
| options.limit | integer | No | 最大結果件数 |

**リクエスト例:**

```json
{
    "base64": "/9j/4AAQSkZJRg...",
    "options": {
        "limit": 10
    }
}
```

**レスポンス:** POST /api/v2/aiSearch/searchByText と同じ形式（`{ item, score }` ペアの配列）

---

### POST /api/v2/aiSearch/searchByItemId

既存のライブラリアイテムを基準に、視覚的特徴が類似したアイテムを検索します。

**リクエストボディ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| itemId | string | Yes | 基準となるアイテムのID |
| options | object | No | 検索オプション |
| options.limit | integer | No | 最大結果件数 |

**リクエスト例:**

```json
{
    "itemId": "M3QSGJNQTC2DG",
    "options": {
        "limit": 10
    }
}
```

**レスポンス:** POST /api/v2/aiSearch/searchByText と同じ形式（`{ item, score }` ペアの配列）

---

## v1 からの変更点まとめ

| カテゴリ | v1 | v2 |
|---------|-----|-----|
| ベースパス | `/api/` | `/api/v2/` |
| アプリ情報 | `/api/application/info` | `/api/v2/app/info` |
| アイテム追加 | 個別エンドポイント（addFromURL, addFromPath等） | 統合エンドポイント `/api/v2/item/add` |
| アイテム一覧 | `/api/item/list` | `/api/v2/item/get`（GET/POST両対応） |
| 全文検索 | なし | `/api/v2/item/query` |
| アイテム総数 | なし | `/api/v2/item/countAll` |
| カスタムサムネイル | なし | `/api/v2/item/setCustomThumbnail` |
| フォルダ一覧 | `/api/folder/list` | `/api/v2/folder/get`（GET/POST両対応） |
| フォルダリネーム | `/api/folder/rename` | `/api/v2/folder/update` に統合 |
| 最近のフォルダ | `/api/folder/listRecent` | `/api/v2/folder/get?isRecent=true` |
| タグ管理 | なし | `/api/v2/tag/get`, `update`, `merge` |
| タググループ | なし | `/api/v2/tagGroup/*`（6エンドポイント） |
| AI検索 | なし | `/api/v2/aiSearch/*`（9エンドポイント） |
| ページネーション | `offset`/`limit` | 全リストエンドポイントで `total`, `offset`, `limit` を返却 |
| 認証 | なし | リモートアクセス時にAPIトークンが必要 |
