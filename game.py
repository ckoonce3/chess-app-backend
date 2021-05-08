from db import connect

class Game:

    @staticmethod
    def saveGame(user, color, date, log):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO PracticeGame (user, color, date, log) VALUES (?,?,?,?)", 
                (user,color,date,log))
            conn.commit()
            new_id = cursor.lastrowid
            return Game.findGame(new_id)

    @staticmethod
    def findGame(id):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PracticeGame WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row is None:
                raise Exception("Game not found")
            return row

    @staticmethod
    def loadGames(user):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PracticeGame WHERE user = ?", (user,))
            return [{
                'id': row['id'],
                'user': row['user'],
                'color': row['color'],
                'date': row['date'],
                'log': row['log']
                } for row in cursor.fetchall()]