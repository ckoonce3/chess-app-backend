import hashlib
import random
import string
from db import connect

class User:

    @staticmethod
    def addUser(username, password):
        # Make sure that the username does not previously exist
        user_row = User.findUser(username)
        if user_row is None:
            salt = getSalt(4)
            h = hashlib.md5((password+salt).encode()).hexdigest()
            print(h)
            with connect() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO User (username, salt, password, loggedIn) VALUES (?, ?, ?, ?)", 
                    (username,salt,h,0))
                conn.commit()
                print('success')
        else:
            raise Exception('Username already exists')

    @staticmethod
    def logIn(username, password):
        # Retrieve the row corresponding to the username
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
            row = cursor.fetchone()
            # Make sure that the user exists
            if row is None:
                raise Exception('Username not found')
            # Make sure that the password is correct
            h = hashlib.md5((password+row['salt']).encode()).hexdigest()
            if h != row['password']:
                raise Exception('Incorrect password')
            # Set the loggedin and ip variables of the user
            cursor.execute("UPDATE User SET loggedIn = 1 WHERE username = ?", (username,))
            conn.commit()          


    @staticmethod
    def findUser(username):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
            row = cursor.fetchone()
            return row

    @staticmethod
    def logOut(username):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE User SET loggedIn = 0 WHERE username = ?", (username,))
            conn.commit()


def getSalt(length):
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


