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
    sql = 'SELECT user_id, hashed_password, salt FROM users WHERE name = %s'
    flg = False
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (name,))
        user = cursor.fetchone()
        if user != None:
            salt = user[2]
            hashed_password = get_hash(password, salt)
            if hashed_password == user[1]:
                flg = True
                user_info = user[0]
    except psycopg2.DatabaseError:
        flg = False
        user_info = None
    finally:
        cursor.close()
        connection.close()
    return [flg, user_info]
            
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

# ユーザーは本を借りられるのか判別する
def borrow_confirm_user(user_id):
    sql = 'SELECT current_books_borrowed FROM users WHERE user_id = %s'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_id,))
        row = cursor.fetchone()
        print("borrow_confirm_user/row:{}".format(row))
        if row[0] < 5:
            flg = True
        else:
            flg = False
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()    
    print("ユーザは本を借りられる:{}".format(flg))
    return flg

# 過去に図書が借りられているか判別する
def borrow_confirm_book_pass(book_id):
    sql = 'SELECT EXISTS (SELECT * FROM user_book WHERE book_id = %s)'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(book_id,))
        row = cursor.fetchone()
        print("borrow_confirm_book_pass/row:{}".format(row))
        # row[0]=>trueは借りられている、falseは借りられていない
        if row[0] == 'False':
            flg = True
        else:
            flg = False
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()
    # flg=>trueは借りられる、falseは次の判別へ
    print("過去に図書が借りられていない:{}".format(flg))  
    return flg

# 本は借りられる状態なのか判別する
def borrow_confirm_book(book_id):
    sql = 'SELECT returned_time FROM user_book WHERE book_id = %s and borrowed_time = (SELECT MAX(borrowed_time) FROM user_book)'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(book_id,))
        row = cursor.fetchone()
        print("borrow_confirm_book/row:{}".format(row))
        # returned_timeに値が入っていれば借りられる
        if row != 'None':
            flg = True
        else:
            flg = False
        # if row != None and row[1] == None:
        #     flg = False
        # elif row[0] != None and row[1] != None:
        #     flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()  
    print("本は借りられるか：{}".format(flg))  
    return flg
    
# 借りる(user_bookにレコード追加)
def borrow_book(user_id, book_id):
    sql = 'INSERT INTO user_book VALUES (default, %s, %s, CURRENT_TIMESTAMP, null, null)'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (user_id, book_id))
        count = cursor.rowcount
        connection.commit()     
    except psycopg2.DatabaseError:
        count = 0  
    finally:
        cursor.close()
        connection.close()
    return count

# 借りる(ユーザの借りている本の冊数を更新)
def update_current_books_borrowed(user_id):
    sql = 'UPDATE users SET current_books_borrowed = current_books_borrowed + 1 WHERE user_id = %s'
    try:
        connection = get_connection()
        cursor = connection.cursor()    
        cursor.execute(sql, (user_id,))
        count = cursor.rowcount
        connection.commit()     
    except psycopg2.DatabaseError:
        count = 0  
    finally:
        cursor.close()
        connection.close()
    return count

# ユーザが借りている図書のbook_idを取得
def borrowed_book_id_list(user_id):
    sql = 'SELECT book_id FROM user_book WHERE user_id = %s and returned_time IS NULL'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(user_id,))
        rows = cursor.fetchall()
        book_id_list = []
        for row in rows:
            book_id_list.append(row)
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    print(book_id_list)
    return book_id_list   