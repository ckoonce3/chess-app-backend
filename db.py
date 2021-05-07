import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def connect():
    conn = sqlite3.connect('chess.db')
    conn.row_factory = sqlite3.Row
    return conn

def setupDB():
    with connect() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS User (
                username TEXT PRIMARY KEY,
                salt TEXT,
                password BINARY(16),
                loggedIn INTEGER,
                ip TEXT
        )''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS PracticeGame (
                id INTEGER PRIMARY KEY,
                user TEXT,
                log TEXT,
                FOREIGN KEY(user) REFERENCES User(username)
        )''')

def resetDB():
    with connect() as db:
        db.execute("DROP TABLE IF EXISTS User")
        db.execute("DROP TABLE IF EXISTS PracticeGame")
    setupDB()

