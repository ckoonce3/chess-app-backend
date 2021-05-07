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
                print('success')
        else:
            raise Exception('Username already exists')

    @staticmethod
    def logIn(username, password, ip):
        print(username,password,ip)
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
            # Make sure that the user is not already logged in
            if row['loggedIn'] == 1:
                raise Exception('User is already logged in')
            # Set the loggedin and ip variables of the user
            cursor.execute("UPDATE User SET loggedIn = 1, ip = ? WHERE username = ?", (ip,username))           


    @staticmethod
    def findUser(username):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
            row = cursor.fetchone()
            return row


def getSalt(length):
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


