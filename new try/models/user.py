#/models/user.py
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, id, email, password_hash):
        self.id = id
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def create(email, password):
        conn = sqlite3.connect('beekeeping.db')
        cursor = conn.cursor()
        password_hash = generate_password_hash(password)
        cursor.execute('INSERT INTO users (email, password_hash) VALUES (?, ?)', (email, password_hash))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return User(user_id, email, password_hash)

    @staticmethod
    def get_by_email(email):
        conn = sqlite3.connect('beekeeping.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return User(user_data[0], user_data[1], user_data[2])
        return None

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)