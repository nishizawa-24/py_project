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
    
    if db.login(name, password):
        session['user'] = True
        return redirect(url_for('mypage'))
    else:
        error = '名前またはパスワードが違います。'
        input_data = {'name':name, 'password':password}
        return render_template('user_login.html', error=error, data=input_data)
    
@app.route('/logout')
def logout():
    session.pop('user', None)
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
    if 'user' in session:
        return render_template('book_detail.html', book=book)
    else:
        return redirect(url_for('top'))

@app.route('/search', methods=['POST'])
def book_search():
    keyword = request.form.get('keyword')
    books = db.get_searched_books(keyword)
    msg = '図書が見つかりませんでした。'
    
    if 'user' in session:
        return redirect(url_for('top'))
    
    if books == []:
        return render_template('search_result.html', keyword=keyword, books=books, msg=msg)
    else:
        return render_template('search_result.html', keyword=keyword, books=books, msg=None)

    
if __name__ == '__main__':
    app.run(debug=True)