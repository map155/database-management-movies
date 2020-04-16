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
    session.pop('user_id')
    return redirect("/")


@app.route("/DeleteUser")
def deleteUser():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_deleteUser', (session['username'],))
    conn.commit()
    session.pop('username')
    session.pop('user_id')
    return redirect("/")


@app.route("/FavMovies", methods=['POST'])
def favMovies():
    movieID = request.form['movieID']
    print(movieID)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_addFavMovie', (movieID, session['user_id']))
    data = cursor.fetchall()
    if data:
        print(data)
        conn.commit()
        return json.dumps({'success': 'Favorited Movie'})
    return json.dumps({'Error': 'Unknonwn'})


@app.route("/login", methods=['POST'])
def login():
    _username = request.form['Username']
    _password = request.form['Password']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_Login', (_username,))
    data = cursor.fetchall()
    if data:
        print(data)
        if check_password_hash(data[0][0], _password):
            session['username'] = _username
            session['user_id'] = data[0][1]
    return redirect("/")


@app.route("/createUser", methods=['POST'])
def createUser():
    _username = request.form['Username']
    _password = request.form['Password']
    conn = mysql.connect()
    cursor = conn.cursor()
    _hashed_password = generate_password_hash(_password)
    cursor.callproc('sp_CreateUser', (_username, _hashed_password))
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


@app.route("/GetMovies")
def getMovies():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    data = cursor.fetchall()
    if data:
        return render_template('movies.html', x=data)

@app.route("/GetActors")
def getActors():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM actors")
    data = cursor.fetchall()
    if data:
        return render_template('actors.html', x=data)

@app.route("/FavActors", methods=['POST'])
def FavActors():
    actorID = request.form['actorID']
    print(actorID)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_addFavActor', (movieID, session['user_id']))
    data = cursor.fetchall()
    if data:
        print(data)
        conn.commit()
        return json.dumps({'success': 'Favorited Actor'})
    return json.dumps({'Error': 'Unknonwn'})


@app.route("/getProfile")
def getProfile():
    # _username = session['username']
    # selectStatement = "SELECT username FROM users WHERE username = %(user)"
    # conn = mysql.connect()
    # cursor = conn.cursor()
    # cursor.execute(selecStatement, {'user' : _username})
    # data = cursor.fetchall()
    # if data:
    # return render_template('profile.html', x = data)
    return render_template('profile.html', username=session['username'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
