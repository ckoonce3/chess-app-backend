from flask import Flask, request, abort
from flask_cors import CORS
from db import create_connection, setupDB, resetDB, connect
from user import User
from game import Game
import json

# Setup Flask
app = Flask(__name__)
CORS(app)

# Setup the database
create_connection('chess.db')
# Setup the database tables
setupDB()

@app.route("/")
def hello():
    return {'id': "Hello world"}

@app.route("/signup")
def sign_up():
    username = request.args.get('username')
    password = request.args.get('password')
    confirm = request.args.get('confirm')
    print(username, password, confirm)
    if password != confirm:
        abort(400)
        return "Confirm password does not match"
    try:
        User.addUser(username, password)
    except Exception as error:
        abort(400)
        return str(error)
    row = User.findUser(username)
    return {'username': row['username']}

@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        body = request.get_json(force=True)
        username = body['username']
        password = body['password']
        try:
            User.logIn(username, password)
        except Exception as error:
            abort(400)
            return str(error)
        row = User.findUser(username)
        return {'loggedIn': row['loggedIn']}

@app.route("/logout")
def logout():
    username = request.args.get('username')
    row = User.findUser(username)
    if row is None:
        abort(404)
        return 'Username not found'
    if row['loggedIn'] == 0:
        abort(400)
        return 'User is not logged in'
    User.logOut(username)
    row = User.findUser(username)
    return {'loggedIn': row['loggedIn']}

@app.route("/save", methods = ['POST'])
def save():
    body = request.get_json(force=True)
    username = body['username']
    row = User.findUser(username)
    if row['loggedIn'] == 0:
        abort(400)
        return 'User is not logged in'
    color = body['color']
    date = body['date']
    log = body['log']
    row = Game.saveGame(username,color,date,log)
    return {
        'id': row['id'],
        'user': row['user'], 
        'color': row['color'],
        'date': row['date'],
        'log': row['log']}

@app.route("/load")
def load():
    user = request.args.get('username')
    row = User.findUser(user)
    if row is None:
        abort(404)
        return {'error': 'Username not found'}
    return json.dumps(Game.loadGames(user))
