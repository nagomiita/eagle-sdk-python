# Eagle API リファレンス

公式ドキュメント: https://api.eagle.cool/

## 概要

Eagle APIは、Eagle アプリが起動している間のみ利用可能なローカルAPIです。

- **ベースURL:** `http://localhost:41595`
- **レスポンス形式:** JSON
- **必要バージョン:** Eagle 1.11 Build21 (2020/06/17) 以降
- **呼び出し制限:** なし（ローカル通信のため）

---

## 目次

- [Application](#application)
  - [GET /api/application/info](#get-apiapplicationinfo)
- [Item](#item)
  - [POST /api/item/addFromURL](#post-apiitemaddfromurl)
  - [POST /api/item/addFromURLs](#post-apiitemaddfromurls)
  - [POST /api/item/addFromPath](#post-apiitemaddfrompath)
  - [POST /api/item/addFromPaths](#post-apiitemaddfrompaths)
  - [POST /api/item/addBookmark](#post-apiitemaddbookmark)
  - [GET /api/item/info](#get-apiiteminfo)
  - [GET /api/item/thumbnail](#get-apiitemthumbnail)
  - [POST /api/item/update](#post-apiitemupdate)
  - [GET /api/item/list](#get-apiitemlist)
  - [POST /api/item/moveToTrash](#post-apiitemmovetotrash)
  - [POST /api/item/refreshPalette](#post-apiitemrefreshpalette)
  - [POST /api/item/refreshThumbnail](#post-apiitemrefreshthumbnail)
- [Folder](#folder)
  - [POST /api/folder/create](#post-apifoldercreate)
  - [POST /api/folder/rename](#post-apifolderrename)
  - [POST /api/folder/update](#post-apifolderupdate)
  - [GET /api/folder/list](#get-apifolderlist)
  - [GET /api/folder/listRecent](#get-apifolderlistrecent)
- [Library](#library)
  - [GET /api/library/info](#get-apilibraryinfo)
  - [GET /api/library/history](#get-apilibraryhistory)
  - [POST /api/library/switch](#post-apilibraryswitch)
  - [GET /api/library/icon](#get-apilibraryicon)

---

## Application

### GET /api/application/info

Eagle アプリの情報を取得します。ユーザーのデバイスで特定の機能が利用可能かどうかを判定するために使用できます。

**パラメータ:** なし

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "version": "1.11.0",
        "prereleaseVersion": null,
        "buildVersion": "20200612",
        "execPath": "/Users/augus/Projects/Eagle App/node_modules/electron/dist/Electron.app/Contents/Frameworks/Electron Helper (Renderer).app/Contents/MacOS/Electron Helper (Renderer)",
        "platform": "darwin"
    }
}
```

| フィールド | 型 | 説明 |
|-----------|-----|------|
| version | string | アプリケーションバージョン |
| prereleaseVersion | string\|null | プレリリースバージョン（正式版の場合はnull） |
| buildVersion | string | ビルドバージョン |
| execPath | string | 実行ファイルのパス |
| platform | string | OS識別子（darwin, win32 等） |

---

## Item

### POST /api/item/addFromURL

URLから画像をEagleに追加します。複数の画像を追加する場合は `/api/item/addFromURLs` を使用してください。

**パラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| url | string | Yes | 画像のURL。`http`、`https`、`base64` をサポート |
| name | string | Yes | 追加する画像の名前 |
| website | string | No | 画像の出典元URL |
| tags | string[] | No | 画像のタグ |
| star | number | No | 画像の評価 |
| annotation | string | No | 画像の注釈 |
| modificationTime | number | No | 画像の作成日時（タイムスタンプ）。ソート順に影響する |
| folderId | string | No | 保存先フォルダのID |
| headers | object | No | カスタムHTTPヘッダー。特定のWebサイトのセキュリティを回避するために使用 |

**リクエスト例:**

```json
{
    "url": "https://cdn.dribbble.com/users/674925/screenshots/12020761/media/6420a7ec85751c11e5254282d6124950.png",
    "name": "Work",
    "website": "https://dribbble.com/shots/12020761-Work",
    "tags": ["Illustration", "Design"],
    "modificationTime": 1591325171766,
    "headers": {
        "referer": "dribbble.com"
    }
}
```

**レスポンス例:**

```json
{
    "status": "success"
}
```

---

### POST /api/item/addFromURLs

複数の画像をURLから一括でEagleに追加します。

**パラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| items | object[] | Yes | 追加するアイテムの配列 |
| items[].url | string | Yes | 画像のURL。`http`、`https`、`base64` をサポート |
| items[].name | string | Yes | 画像の名前 |
| items[].website | string | No | 画像の出典元URL |
| items[].annotation | string | No | 画像の注釈 |
| items[].tags | string[] | No | 画像のタグ |
| items[].modificationTime | number | No | 作成日時（タイムスタンプ）。ソート順に影響する |
| items[].headers | object | No | カスタムHTTPヘッダー |
| folderId | string | No | 保存先フォルダのID |

**リクエスト例:**

```json
{
    "items": [
        {
            "url": "https://cdn.dribbble.com/users/674925/screenshots/12020761/media/6420a7ec85751c11e5254282d6124950.png",
            "name": "Work",
            "website": "https://dribbble.com/shots/12020761-Work",
            "tags": ["Illustration", "Design"],
            "modificationTime": 1591325171767,
            "headers": {
                "referer": "dribbble.com"
            }
        }
    ],
    "folderId": "KAY6NTU6UYI5Qa"
}
```

**レスポンス例:**

```json
{
    "status": "success"
}
```

---

### POST /api/item/addFromPath

ローカルファイルをEagleに追加します。複数のファイルを追加する場合は `/api/item/addFromPaths` を使用してください。

**パラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| path | string | Yes | ローカルファイルのパス |
| name | string | Yes | 追加する画像の名前 |
| website | string | No | 画像の出典元URL |
| annotation | string | No | 画像の注釈 |
| tags | string[] | No | 画像のタグ |
| folderId | string | No | 保存先フォルダのID |

**リクエスト例:**

```json
{
    "path": "C://Users/User/Downloads/test.jpg",
    "name": "アルトリア･キャスター",
    "website": "https://www.pixiv.net/artworks/83585181",
    "tags": ["FGO", "アルトリア・キャスター"],
    "annotation": "久坂んむり",
    "folderId": "KEHB8I2C9F23H"
}
```

**レスポンス例:**

```json
{
    "status": "success"
}
```

---

### POST /api/item/addFromPaths

複数のローカルファイルを一括でEagleに追加します。

**パラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| items | object[] | Yes | 追加するアイテムの配列 |
| items[].path | string | Yes | ローカルファイルのパス |
| items[].name | string | Yes | 画像の名前 |
| items[].website | string | No | 画像の出典元URL |
| items[].annotation | string | No | 画像の注釈 |
| items[].tags | string[] | No | 画像のタグ |
| folderId | string | No | 保存先フォルダのID |

**リクエスト例:**

```json
{
    "items": [
        {
            "path": "C://Users/User/Downloads/test.jpg",
            "name": "アルトリア･キャスター",
            "website": "https://www.pixiv.net/artworks/83585181",
            "tags": ["FGO", "アルトリア・キャスター"],
            "annotation": "久坂んむり"
        },
        {
            "path": "C://Users/User/Downloads/test2.jpg",
            "name": "アルトリア･キャスター",
            "website": "https://www.pixiv.net/artworks/83585181",
            "tags": ["FGO", "アルトリア・キャスター"],
            "annotation": "久坂んむり"
        }
    ],
    "folderId": "KEHB8I2C9F23H"
}
```

**レスポンス例:**

```json
{
    "status": "success"
}
```

---

### POST /api/item/addBookmark

ブックマーク（リンク）をEagleに保存します。

**パラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| url | string | Yes | 保存するリンクのURL。`http`、`https`、`base64` をサポート |
| name | string | Yes | ブックマークの名前 |
| base64 | string | No | サムネイル画像（base64形式） |
| tags | string[] | No | タグ |
| modificationTime | number | No | 作成日時（タイムスタンプ）。ソート順に影響する |
| folderId | string | No | 保存先フォルダのID |

**リクエスト例:**

```json
{
    "url": "https://www.pixiv.net/artworks/83585181",
    "name": "アルトリア･キャスター",
    "tags": ["FGO", "アルトリア・キャスター"],
    "base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA..."
}
```

**レスポンス例:**

```json
{
    "status": "success"
}
```

---

### GET /api/item/info

指定したアイテムの詳細情報（ファイル名、タグ、フォルダ、サイズ、カラーパレット等）を取得します。

**パラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string | Yes | アイテムのID（クエリパラメータ） |

**リクエスト例:**

```
GET http://localhost:41595/api/item/info?id=KBHG6KA0Y5S9W
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "id": "KBHG6KA0Y5S9W",
        "name": "Work",
        "size": 45231,
        "ext": "png",
        "tags": ["Illustration", "Design"],
        "folders": [],
        "isDeleted": false,
        "url": "https://dribbble.com/shots/12020761-Work",
        "annotation": "",
        "modificationTime": 1591325171766,
        "width": 623,
        "height": 623,
        "noThumbnail": false,
        "lastModified": 1591325171766,
        "palettes": [
            {
                "color": [232, 198, 159],
                "ratio": 34.05
            },
            {
                "color": [77, 54, 45],
                "ratio": 21.13
            }
        ]
    }
}
```

| フィールド | 型 | 説明 |
|-----------|-----|------|
| id | string | アイテムID |
| name | string | アイテム名 |
| size | number | ファイルサイズ（バイト） |
| ext | string | ファイル拡張子 |
| tags | string[] | タグ一覧 |
| folders | string[] | 所属フォルダID一覧 |
| isDeleted | boolean | 削除済みかどうか |
| url | string | 出典元URL |
| annotation | string | 注釈 |
| modificationTime | number | 変更日時（タイムスタンプ） |
| width | number | 画像の幅（px） |
| height | number | 画像の高さ（px） |
| noThumbnail | boolean | サムネイルなしフラグ |
| lastModified | number | 最終更新日時 |
| palettes | object[] | カラーパレット（RGB値と比率） |

---

### GET /api/item/thumbnail

指定したアイテムのサムネイル画像のファイルパスを取得します。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string | Yes | アイテムのID |

**リクエスト例:**

```
GET http://localhost:41595/api/item/thumbnail?id=KBHG6KA0Y5S9W
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": "/Users/augus/Pictures/test.library/images/KBKE04XSTXR7I.info/Rosto.jpg"
}
```

| フィールド | 型 | 説明 |
|-----------|-----|------|
| data | string | サムネイル画像のファイルパス |

> **ヒント:** 大量のアイテムを処理する場合は、ライブラリのパスとアイテムIDを組み合わせてパスを構築する方が効率的です。

---

### POST /api/item/update

アイテムのメタデータを更新します。OCRの結果やオブジェクト検出の結果をタグや注釈として統合するのに便利です。

**パラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string | Yes | 更新対象のアイテムID |
| tags | string[] | No | タグ |
| annotation | string | No | 注釈 |
| url | string | No | 出典元URL |
| star | number | No | 評価 |

**リクエスト例:**

```json
{
    "id": "KBN1X9NHDZ99F",
    "tags": ["Design1", "Design2"],
    "annotation": "Awesome",
    "url": "https://dribbble.com",
    "star": 4
}
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "id": "KBN1X9NHDZ99F",
        "name": "Work",
        "size": 45231,
        "ext": "png",
        "tags": ["Design1", "Design2"],
        "folders": [],
        "isDeleted": false,
        "url": "https://dribbble.com",
        "annotation": "Awesome",
        "star": 4,
        "modificationTime": 1591325171766,
        "width": 623,
        "height": 623,
        "palettes": []
    }
}
```

---

### GET /api/item/list

条件に一致するアイテムの一覧を取得します。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| limit | number | No | 取得件数（デフォルト: 200） |
| offset | number | No | オフセット（デフォルト: 0） |
| orderBy | string | No | ソート順。`CREATEDATE`, `FILESIZE`, `NAME`, `RESOLUTION`。先頭に `-` を付けると降順 |
| keyword | string | No | キーワード検索 |
| ext | string | No | 拡張子フィルタ（例: `jpg`, `png`, `svg`） |
| tags | string | No | タグフィルタ（カンマ区切り。例: `Design,Poster`） |
| folders | string | No | フォルダフィルタ（カンマ区切りのフォルダID。例: `KAY6NTU6UYI5Q,KBJ8Z60O88VMG`） |

**リクエスト例:**

```
GET http://localhost:41595/api/item/list?orderBy=-RESOLUTION&limit=10&ext=svg&tags=test,test2
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": [
        {
            "id": "KBHG6KA0Y5S9W",
            "name": "Work",
            "size": 45231,
            "ext": "png",
            "tags": ["Design"],
            "folders": [],
            "isDeleted": false,
            "url": "",
            "annotation": "",
            "modificationTime": 1591325171766,
            "width": 623,
            "height": 623,
            "lastModified": 1591325171766,
            "palettes": [
                {
                    "color": [232, 198, 159],
                    "ratio": 34.05
                }
            ]
        }
    ]
}
```

---

### POST /api/item/moveToTrash

指定したアイテムをゴミ箱に移動します。

**パラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| itemIds | string[] | Yes | ゴミ箱に移動するアイテムIDの配列 |

**リクエスト例:**

```json
{
    "itemIds": ["KWLKGQW2HTHC7", "KWLOGLTX0FGHF"]
}
```

**レスポンス例:**

```json
{
    "status": "success"
}
```

---

### POST /api/item/refreshPalette

アイテムのカラーパレット（色解析結果）を再生成します。元ファイルが変更された場合に使用します。

**パラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string | Yes | アイテムのID |

**リクエスト例:**

```json
{
    "id": "KBKE02W8V0YWD"
}
```

**レスポンス例:**

```json
{
    "status": "success"
}
```

---

### POST /api/item/refreshThumbnail

アイテムのサムネイルを再生成します。同時にカラーパレットの再解析も行われます。元ファイルが変更された場合に使用します。

**パラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string | Yes | アイテムのID |

**リクエスト例:**

```json
{
    "id": "KBKE02W8V0YWD"
}
```

**レスポンス例:**

```json
{
    "status": "success"
}
```

---

## Folder

### POST /api/folder/create

現在のライブラリに新しいフォルダを作成します。作成されたフォルダはフォルダリストの最下部に表示されます。

**パラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| folderName | string | Yes | フォルダ名 |
| parent | string | No | 親フォルダのID |

**リクエスト例:**

```json
{
    "folderName": "The Folder Name"
}
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "id": "KBJJSMMVF9WYL",
        "name": "The Folder Name",
        "images": [],
        "folders": [],
        "modificationTime": 1592409993367,
        "imagesMappings": {},
        "tags": [],
        "children": [],
        "isExpand": true
    }
}
```

---

### POST /api/folder/rename

フォルダ名を変更します。

**パラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| folderId | string | Yes | フォルダのID |
| newName | string | Yes | 新しいフォルダ名 |

**リクエスト例:**

```json
{
    "folderId": "KBHOIWCUO6U9I",
    "newName": "New Folder Name"
}
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "id": "KBJJSMMVF9WYL",
        "name": "New Folder Name",
        "images": [],
        "folders": [],
        "modificationTime": 1592409993367,
        "imagesMappings": {},
        "tags": [],
        "children": [],
        "isExpand": true,
        "size": 30,
        "vstype": "folder",
        "styles": {
            "depth": 0,
            "first": false,
            "last": false
        },
        "isVisible": true,
        "editable": false,
        "pinyin": "New Folder Name"
    }
}
```

---

### POST /api/folder/update

フォルダの情報（名前・説明・色）を更新します。

**パラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| folderId | string | Yes | フォルダのID |
| newName | string | No | 新しいフォルダ名 |
| newDescription | string | No | 新しい説明文 |
| newColor | string | No | 新しい色。`red`, `orange`, `green`, `yellow`, `aqua`, `blue`, `purple`, `pink` のいずれか |

**リクエスト例:**

```json
{
    "folderId": "KMUFMKTBHINM4",
    "newName": "New Name",
    "newDescription": "New Description",
    "newColor": "red"
}
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "id": "KMUFMKTBHINM4",
        "name": "New Name",
        "description": "New Description",
        "images": [],
        "folders": [],
        "modificationTime": 1592409993367,
        "imagesMappings": {},
        "tags": [],
        "children": [],
        "isExpand": true,
        "size": 30,
        "vstype": "folder",
        "styles": {
            "depth": 0,
            "first": false,
            "last": false
        },
        "isVisible": true,
        "editable": false
    }
}
```

---

### GET /api/folder/list

現在のライブラリのフォルダ一覧を取得します。

**パラメータ:** なし

**リクエスト例:**

```
GET http://localhost:41595/api/folder/list
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": [
        {
            "id": "KBJJSMMVF9WYL",
            "name": "Design",
            "description": "",
            "children": [],
            "modificationTime": 1592409993367,
            "tags": [],
            "imageCount": 30,
            "descendantImageCount": 45,
            "pinyin": "Design",
            "extendTags": []
        }
    ]
}
```

| フィールド | 型 | 説明 |
|-----------|-----|------|
| id | string | フォルダID |
| name | string | フォルダ名 |
| description | string | 説明 |
| children | object[] | 子フォルダ |
| modificationTime | number | 最終更新日時 |
| tags | string[] | タグ |
| imageCount | number | 直下の画像数 |
| descendantImageCount | number | 子孫を含む画像数 |
| pinyin | string | ピンイン表記 |
| extendTags | string[] | 拡張タグ |

---

### GET /api/folder/listRecent

最近使用したフォルダの一覧を取得します。

**パラメータ:** なし

**リクエスト例:**

```
GET http://localhost:41595/api/folder/listRecent
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": [
        {
            "id": "KBJJSMMVF9WYL",
            "name": "Industrial",
            "description": "",
            "children": [],
            "modificationTime": 1592409993367,
            "tags": [],
            "password": "",
            "passwordTips": "",
            "images": [],
            "isExpand": true,
            "newFolderName": "",
            "imagesMappings": {},
            "imageCount": 11,
            "descendantImageCount": 11,
            "pinyin": "Industrial",
            "extendTags": []
        }
    ]
}
```

---

## Library

### GET /api/library/info

現在開いているライブラリの情報を取得します。フォルダ、スマートフォルダ、タググループ、クイックアクセスなどの情報を含みます。

**パラメータ:** なし

**リクエスト例:**

```
GET http://localhost:41595/api/library/info
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": {
        "folders": [
            {
                "id": "KBJJSMMVF9WYL",
                "name": "Design",
                "description": "",
                "children": [],
                "modificationTime": 1592409993367,
                "tags": [],
                "iconColor": "",
                "password": "",
                "passwordTips": "",
                "coverId": "",
                "orderBy": "MANUAL",
                "sortIncrease": true,
                "icon": ""
            }
        ],
        "smartFolders": [
            {
                "id": "KBJJSMMVF9WYM",
                "icon": "",
                "name": "High Resolution",
                "description": "",
                "modificationTime": 1592409993367,
                "conditions": [
                    {
                        "match": "OR",
                        "rules": [
                            {
                                "method": "within",
                                "property": "resolution",
                                "value": [1920, 9999]
                            }
                        ]
                    }
                ],
                "orderBy": "FILESIZE",
                "sortIncrease": false
            }
        ],
        "quickAccess": [
            {
                "type": "smartFolder",
                "id": "KBJJSMMVF9WYM"
            }
        ],
        "tagsGroups": [
            {
                "id": "KBJJSMMVF9WYN",
                "name": "Style",
                "tags": ["Modern", "Classic"],
                "color": "blue"
            }
        ],
        "modificationTime": 1592409993367,
        "applicationVersion": "1.11.0"
    }
}
```

| フィールド | 型 | 説明 |
|-----------|-----|------|
| folders | object[] | フォルダ一覧 |
| smartFolders | object[] | スマートフォルダ一覧（条件付きフォルダ） |
| quickAccess | object[] | クイックアクセスのショートカット |
| tagsGroups | object[] | タググループ |
| modificationTime | number | 最終更新日時 |
| applicationVersion | string | アプリケーションバージョン |

---

### GET /api/library/history

最近開いたライブラリの一覧を取得します。

**パラメータ:** なし

**リクエスト例:**

```
GET http://localhost:41595/api/library/history
```

**レスポンス例:**

```json
{
    "status": "success",
    "data": [
        "/Users/augus/Google Drive/Design fields.library",
        "/Users/augus/Google Drive/Office Style.library",
        "/Users/augus/Google Drive/Design Assets.library"
    ]
}
```

---

### POST /api/library/switch

開くライブラリを切り替えます。

**パラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| libraryPath | string | Yes | ライブラリファイルのパス |

**リクエスト例:**

```json
{
    "libraryPath": "/Users/augus/Pictures/Design.library"
}
```

**レスポンス例:**

```json
{
    "status": "success"
}
```

---

### GET /api/library/icon

指定したライブラリのアイコン画像を取得します。

**クエリパラメータ:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| libraryPath | string | Yes | ライブラリのパス（URLエンコードが必要） |

**リクエスト例:**

```
GET http://localhost:41595/api/library/icon?libraryPath=%2FUsers%2Faugus%2FPictures%2FDesign.library
```

**レスポンス:** ライブラリのアイコン画像データが返されます。
