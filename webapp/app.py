from flask import Flask, render_template, session, request
from flaskext.mysql import MySQL
import json
#from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__,
            static_url_path='',
            static_folder='static')

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


@app.route("/login", methods=['POST'])
def login():
    _username = request.form['Username']
    _password = request.form['Password']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_login', (_username, _password))
    data = cursor.fetchall()
    return json.dumps({'error': str(data)})


@app.route("/createUser", methods=['POST'])
def createUser():
    conn = mysql.connect()
    _hashed_password = generate_password_hash(_password)
    return "You said: " + request.form['text']



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
