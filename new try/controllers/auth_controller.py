# controllers/auth_controller.py
import bcrypt

class AuthController:
    def __init__(self, db):
        self.db = db

    def login(self, email, password):
        self.db.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = self.db.cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            return True
        return False

    def register(self, email, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            self.db.cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
            self.db.conn.commit()
            return True
        except:
            return False