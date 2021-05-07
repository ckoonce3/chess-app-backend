from flask import Flask, request, abort
from flask_cors import CORS
from db import create_connection, setupDB, resetDB, connect
from user import User

app = Flask(__name__)
CORS(app)

# Setup the database
create_connection('chess.db')
# Setup the database tables
resetDB()

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
    return {'username': row['username'], 'salt': row['salt'], 'password': row['password']}

@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        body = request.get_json(force=True)
        username = body['username']
        password = body['password']
        ip = request.headers['Origin']
        try:
            User.logIn(username, password, ip)
        except Exception as error:
            abort(400)
            return str(error)
        row = User.findUser(username)
        return {'loggedIn': row['loggedIn'], 'ip': row['ip']}

