from user import User
import sqlite3

DB_NAME = 'database.db'

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Users(username text, '
          'seed_password text, salt text, last_token_used text)')
conn.commit()
conn.close()

class UserPersistence:
    @classmethod
    def create(cls, user):
        conn = sqlite3.connect(DB_NAME)

        cur = conn.cursor()
        cur.execute('SELECT * FROM Users WHERE username=?', [user.username])
        user_row = cur.fetchone()

        user_exists = user_row is not None

        if not user_exists:
            # Persiste o novo usuário
            cur.execute('INSERT INTO Users VALUES (?, ?, ?, ?)',
                [user.username, user.seed_password, user.salt, None]
            )

            user_created = True
        else:
            # Seria um update, mas nesse caso não queremos fazer isso
            user_created = False
        
        conn.commit()
        conn.close()

        return user_created

    @classmethod
    def find_by_username(cls, username):
        conn = sqlite3.connect(DB_NAME)

        cur = conn.cursor()
        cur.execute('SELECT * FROM Users WHERE username=? LIMIT 1', [username])
        user_row = cur.fetchone()

        user_exists = user_row is not None

        if user_exists:
            user = User(
                username=user_row[0],
                seed_password=user_row[1],
                salt=user_row[2],
                last_token_used=user_row[3],
                existing_user=True
            )
        else:
            user = None
        
        conn.commit()
        conn.close()

        return user

    @classmethod
    def update_token_info(cls, user):
        conn = sqlite3.connect(DB_NAME)

        cur = conn.cursor()
        cur.execute('UPDATE Users SET last_token_used=? WHERE username=?',
                  [user.last_token_used, user.username]
        )
    
        conn.commit()
        conn.close()