# py_project
pythonの最終課題

<a target="_blank" href="https://xd.adobe.com/view/e44c6bd4-8b96-472d-8b65-f82c0044b3ba-b11f/">画面設計</a>
(新しいタブで開きます)

<details>
<summary>進捗</summary>

### 07/05
* 一覧機能完成
* 部分一致検索作成
* 図書の詳細情報の表示画面作成

### 07/03
* booksテーブルとuesr_bookテーブルのsql文作成
* ログイン後のトップ画面作成
* 一覧機能作成開始

<details>
<summary>6月までの進捗</summary>

### 06/29
* usersテーブルのsql文作成
* 新規登録画面の調整
* ログイン画面作成
* 新規登録・ログイン完成(?)
* 画面設計(XD)の調整

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
</details>

<details>
<summary>データベース設計</summary>

### テーブル

---

#### users

ユーザの登録、参照

|カラム名|データ型|
|----|----|
|user_id|SERIAL|
|name|VARCHAR(256)|
|birth|VARCHER(8)|
|hashed_password|VARCHAR(64)|
|salt|VARCHAR(30)|
|current_books_borrowed|INTEGER|

※パスワードはハッシュ化済み

<details>
<summary>sql文</summary>

CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  name VARCHAR(256),
  birth VARCHAR(8),
  hashed_password VARCHAR(64),
  salt VARCHAR(30),
  current_books_borrowed INTEGER
);
</details>

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

<details>
<summary>sql文</summary>

CREATE TABLE books (
  book_id SERIAL PRIMARY KEY,
  isbn INTEGER,
  title VARCHAR(256),
  author VARCHAR(256),
  publisher VARCHAR(256)
);
</details>

---

#### user_book

ユーザ図書関連

|カラム名|データ型|
|----|----|
|user_book_id|SERIAL|
|user_id|INTEGER|
|book_id|INTEGER|
|borrowed_time|TIMESTAMP|
|returned_time|TIMESTAMP|
|review|VARCHAR(256)|

<details>
<summary>sql文</summary>

CREATE TABLE user_book (
  user_book_id SERIAL PRIMARY KEY,
  user_id INTEGER,
  book_id INTEGER,
  borrowed_time TIMESTAMP,
  returned_time TIMESTAMP,
  review VARCHAR(256)
);
</details>

---

<details>
<summary>メモ</summary>

##### ユーザ登録・ログイン
授業資料参照。

##### 借りる
`user_bookテーブル`からbook_idで検索し、borrowed_timeが最新のデータを抽出する。
以下の条件を満たすときに、本を借りることができる。
* returned_timeに値が入っている
* `usersテーブル`のcurrent_books_borrowedが5未満

###### 操作
* user_bookテーブル
borrowed_timeにtimestampを入れ、returned_timeはnullでレコード追加

* usersテーブル
current_books_borrowedを+1する。

##### 返す
`user_bookテーブル`からuser_id,book_idで検索し、borrowed_timeが最新のデータを抽出する。
returned_timeに値が入っていないときにその本を返すことができる。

##### 操作

* user_bookテーブル
returned_timeにtimestampを入れてレコード更新

* usersテーブル
current_books_borrowedを-1する。

##### キーワード検索
`bookテーブル`からtitleを部分検索する。
</details>


</details>