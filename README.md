# py_project
pythonの最終課題

[画面設計](https://xd.adobe.com/view/e44c6bd4-8b96-472d-8b65-f82c0044b3ba-b11f/)

<details>
<summary>進捗</summary>

### 06/28
* トップ画面作成
* 新規登録画面作成
* データベース設計開始

### 06/22
* ログイン後の画面設計
  * トップ画面
  * 図書一覧画面
  * キーワード検索

### 06/21
* 空ファイルのpush
* ログインと新規登録の画面設計

### 06/13
* リポジトリの作成
* 画面設計開始(XD)
</details>

<details>
<summary>データベース</summary>

#### users

ユーザの登録、参照

|カラム名|データ型|
|----|----|
|user_id|SERIAL|
|name|VARCHAR(256)|
|birth|INTEGER|
|hashed_password|VARCHAR(64)|
|salt|VARCHAR(30)|

※パスワードはハッシュ化済み

---

#### books

図書の登録、参照

|カラム名|データ型|
|----|----|
|book_id|SERIAL|
|isbn|INTEGER|
|title|VARCHAR(256)|
|author|VARCHAR(256)|
|publisher|VARCHAR(256)|

---

#### user_books

ユーザ図書関連

|カラム名|データ型|
|----|----|
|history|SERIAL|
|user_id|INTEGER|
|book_id|INTEGER|
|borrowed_time|TIMESTAMP|
|returned_time|TIMESTAMP|
</details>