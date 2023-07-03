# coding: utf-8
from flask import Flask, render_template, request, redirect, url_for
import db

app = Flask(__name__)

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
        return redirect(url_for('mypage'))
    else:
        error = '名前またはパスワードが違います。'
        input_data = {'name':name, 'password':password}
        return render_template('user_login.html', error=error, data=input_data)
    
@app.route('/top', methods=['GET'])
def mypage():
    return render_template('mypage.html')

@app.route('/list', methods=['GET'])
def show_all_book():
    book_list = db.get_all_books()
    return book_list
    
if __name__ == '__main__':
    app.run(debug=True)