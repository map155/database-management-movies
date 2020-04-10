from flask import Flask, render_template, session, request, redirect
from flaskext.mysql import MySQL
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,
            static_url_path='',
            static_folder='static')
app.secret_key = b'\x8b3\xbal3/-1\xb6s\x9a\xef\x03\xf1\xf0\xd4'
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'DBMMoviesAdmin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'DBMMov1es'
app.config['MYSQL_DATABASE_DB'] = 'dbmmovies'
app.config['MYSQL_DATABASE_HOST'] = '25.9.255.51'
mysql.init_app(app)


@app.route('/')
def index():
    if 'username' not in session:
        return render_template('login.html')
    else:
        return render_template('index.html', username=session['username'])


@app.route("/logout")
def logout():
    session.pop('username')
    return redirect("/")


@app.route("/login", methods=['POST'])
def login():
    _username = request.form['Username']
    _password = request.form['Password']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_login', (_username,))
    data = cursor.fetchall()
    if data:
        print(data)
        if check_password_hash(data[0][0], _password):
            session['username'] = _username
    return redirect("/")


@app.route("/createUser", methods=['POST'])
def createUser():
    _username = request.form['Username']
    _password = request.form['Password']
    conn = mysql.connect()
    cursor = conn.cursor()
    _hashed_password = generate_password_hash(_password)
    cursor.callproc('sp_TestReturn', (_username, _hashed_password))
    data = cursor.fetchall()
    print(data)
    if data:
        if data[0][0] == 1:
            conn.commit()
            return json.dumps({'success': 'User Created'})
        else:
            return json.dumps({'error': 'User Already Exists'})
    else:
        return json.dumps({'error': 'No Response From Database'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
