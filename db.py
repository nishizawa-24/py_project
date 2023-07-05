# coding: utf-8
import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def insert_user(name, password, birth):
    sql = 'INSERT INTO users VALUES (default, %s, %s, %s, %s, 0)'
    
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (name, birth, hashed_password, salt))
        count = cursor.rowcount
        connection.commit()
        
    except psycopg2.DatabaseError:
        count = 0
        
    finally:
        cursor.close()
        connection.close()
        
    return count

# ログイン判定
def login(name, password):
    sql = 'SELECT hashed_password, salt FROM users WHERE name = %s'
    flg = False
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (name,))
        user = cursor.fetchone()
        if user != None:
            salt = user[1]
            hashed_password = get_hash(password, salt)
            if hashed_password == user[0]:
                flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()
    return flg
            
# ソルト生成
def get_salt():
    charset = string.ascii_letters + string.digits
    salt = ''.join(random.choices(charset, k=30))
    return salt

# ハッシュ化されたpw生成
def get_hash(password, salt):
    b_pw = bytes(password, "utf-8")
    b_salt = bytes(salt, "utf-8")
    hashed_password = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1000).hex()
    return hashed_password

# 全ての図書を取得
def get_all_books():
    sql = 'SELECT * FROM books'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        book_list = []
        for row in rows:
            book_list.append(row)
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()    
    return book_list

# book_idで図書を取得
def get_book(book_id):
    sql = 'SELECT * FROM books WHERE book_id = %s'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(book_id,))
        book = cursor.fetchone()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()    
    return book

# キーワード検索
def get_searched_books(keyword):
    sql = 'SELECT * FROM books WHERE title LIKE %s or author LIKE %s or publisher LIKE %s'
    keyword = '%' + keyword + '%'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(keyword,keyword,keyword,))
        rows = cursor.fetchall()
        book_list = []
        for row in rows:
            book_list.append(row)
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()    
    return book_list