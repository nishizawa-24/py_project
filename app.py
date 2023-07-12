# coding: utf-8
from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['GET'])
def top():
    return render_template('index.html')

@app.route('/register')
def user_register_form():
    return render_template('user_register.html')

@app.route('/register_exe', methods=['POST'])
def user_register_exe():
    name = request.form.get('name')
    password = request.form.get('password')
    birth = request.form.get('birth')
    
    count = db.insert_user(name, password, birth)
    
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('user_login_index', msg=msg))
    
    else:
        error = '登録に失敗しました。'
        return render_template('user_register.html', error=error)

@app.route('/login')
def user_login_index():    
    msg = request.args.get('msg')
    if msg == None:
        return render_template('user_login.html')
    else:
        return render_template('user_login.html', msg=msg)

@app.route('/login', methods=['POST'])
def user_login():
    name = request.form.get('name')
    password = request.form.get('password')
    
    if db.login(name, password)[0]:
        session['user'] = True
        session['user_info'] = db.login(name, password)[1]
        return redirect(url_for('mypage'))
    else:
        error = '名前またはパスワードが違います。'
        input_data = {'name':name, 'password':password}
        return render_template('user_login.html', error=error, data=input_data)
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_info', None)
    return redirect(url_for('top'))
    
@app.route('/top', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else:
        return redirect(url_for('top'))

@app.route('/list', methods=['GET'])
def show_all_book():
    book_list = db.get_all_books()
    if 'user' in session:
        return render_template('book_list.html', book_list=book_list)
    else:
        return redirect(url_for('top'))
    
@app.route('/detail', methods=['POST'])
def book_detail():
    book_id = request.form.get('book_id')
    book = db.get_book(book_id)
    if request.form.get('return_book') == 'True':
        return_book = True
    else:
        return_book = False
    if 'user' in session:
        return render_template('book_detail.html', book=book, return_book=return_book)
    else:
        return redirect(url_for('top'))

@app.route('/search', methods=['POST'])
def book_search():
    keyword = request.form.get('keyword')
    books = db.get_searched_books(keyword)
    msg = '図書が見つかりませんでした。'
    
    if 'user' not in session:
        return redirect(url_for('top'))    
    elif books == []:
        return render_template('search_result.html', keyword=keyword, books=books, msg=msg)
    else:
        return render_template('search_result.html', keyword=keyword, books=books, msg=None)

@app.route('/borrow_confirm', methods=['POST'])
def book_borrow_confirm():
    book_id = request.form.get('book_id')
    book = db.get_book(book_id)
    if 'user' in session and db.borrow_confirm_book_pass(book_id):
        msg = 'この図書を借りますか？'
        flg = 'yes'
        return render_template('book_borrow.html', book=book, msg=msg, flg=flg)
    elif 'user' in session and db.borrow_confirm_user(session['user_info']) and db.borrow_confirm_book(book_id):
        msg = 'この図書を借りますか？'
        flg = 'yes'
        return render_template('book_borrow.html', book=book, msg=msg, flg=flg)
    elif 'user' in session:
        msg = '現在この図書を借りることはできません。'
        flg = 'no'
        return render_template('book_borrow.html', book=book, msg=msg, flg=flg)
    else:
        return redirect(url_for('top'))
    
@app.route('/borrow', methods=['POST'])
def book_borrow():
    book_id = request.form.get('book_id')
    book = db.get_book(book_id)
    if 'user' in session and db.borrow_book(session['user_info'], book_id) == 1 and db.update_current_books_borrowed(session['user_info']) == 1:
        msg = 'この図書を借りました。'
        flg = 'success'
        return render_template('book_borrow.html', book=book, msg=msg, flg=flg)
    elif 'user' in session:
        msg = 'この図書を借りることができませんでした。'
        flg = 'no'
        return render_template('book_borrow.html', book=book, msg=msg, flg=flg)
    else:
        return redirect(url_for('top'))
    
@app.route('/list_borrowed', methods=['GET'])
def book_list_borrowed():
    user_id = session['user_info']
    book_id_list = db.borrowed_book_id_list(user_id)
    book_list = []
    return_book = True
    for num in book_id_list:
        row = db.get_book([num][0])
        book_list.append(row)
    if 'user' in session:
        return render_template('book_list.html', book_list=book_list, return_book=return_book)
    else:
        return redirect(url_for('top'))

if __name__ == '__main__':
    app.run(debug=True)