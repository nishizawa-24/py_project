from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def top():
    return render_template('index.html')

@app.route('/register')
def user_register():
    return render_template('user_register.html')


if __name__ == '__main__':
    app.run(debug=True)