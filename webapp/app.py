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

@app.route("/boxOffice", methods=['GET'])
def boxOffice():
    # directorf = request.form['Director1']
    # directorl = request.form['Director2']
    # actorf = request.form['Actor1']
    # actorl = request.form['Actor2']
    # conn = mysql.connect()
    # cursor = conn.cursor()
    # cursor.callproc('sp_boxOffice', (directorf, directorl, actorf, actorl))
    # data = cursor.fetchall()
    # if data:
    #     session['prediction'] = data
    return render_template('predict.html')

@app.route("/predictBox", methods=['GET', 'POST'])
def predictBox():
    directorf = request.form['DirectorF']
    directorl = request.form['DirectorL']
    actor1f = request.form['Actor1F']
    actor1l = request.form['Actor1L']
    actor2f = request.form['Actor2F']
    actor2l = request.form['Actor2L']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_boxOffice', (directorf, directorl, actor1f, actor1l, actor2f, actor2l))
    data = cursor.fetchall()
    if data:
        session['prediction'] = data
        return json.dumps({'Prediction' : data})
    else:
        return json.dumps({'Prediction' : 'unsuccessful'})



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

@app.route("/GetDirectors")
def getDirectors():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM directors")
    data = cursor.fetchall()
    if data:
        return render_template('directors.html', x=data)

@app.route("/FavActors", methods=['POST'])
def FavActors():
    actorID = request.form['actorID']
    print(actorID)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_addFavActor', (actorID, session['user_id']))
    data = cursor.fetchall()
    if data:
        print(data)
        conn.commit()
        return json.dumps({'success': 'Favorited Actor'})
    return json.dumps({'Error': 'Unknonwn'})


@app.route("/getProfile")
def getProfile():
    userID = session['user_id']

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_getUserFavMovies', (userID,))
    favMovie = cursor.fetchall()
    ftitle = favMovie[0][0]
    frelease = favMovie[0][1]
    frating = favMovie[0][2]

    cursor.callproc('sp_getUserFavActors', (userID,))
    totalName = cursor.fetchall()
    fName = totalName[0][0]
    lName = totalName[0][1]
    favActor = fName + ' ' + lName

    cursor.callproc('sp_getUserRec', (userID,))
    rMovie = cursor.fetchall()
    rMovie = rMovie[0][0]

    return render_template('profile.html', username=session['username'], title = ftitle, rYear = frelease, rating = frating, actor=favActor,recMovie = rMovie)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
