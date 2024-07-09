#/models/apiary.py
import sqlite3

class Apiary:
    def __init__(self, id, name, location, num_hives, establishment_date, user_id):
        self.id = id
        self.name = name
        self.location = location
        self.num_hives = num_hives
        self.establishment_date = establishment_date
        self.user_id = user_id

    @staticmethod
    def create(name, location, num_hives, establishment_date, user_id):
        conn = sqlite3.connect('beekeeping.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO apiaries (name, location, num_hives, establishment_date, user_id) VALUES (?, ?, ?, ?, ?)',
                       (name, location, num_hives, establishment_date, user_id))
        conn.commit()
        apiary_id = cursor.lastrowid
        conn.close()
        return Apiary(apiary_id, name, location, num_hives, establishment_date, user_id)

    @staticmethod
    def get_all_for_user(user_id):
        conn = sqlite3.connect('beekeeping.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM apiaries WHERE user_id = ?', (user_id,))
        apiaries = [Apiary(*row) for row in cursor.fetchall()]
        conn.close()
        return apiaries

    def update(self):
        conn = sqlite3.connect('beekeeping.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE apiaries SET name = ?, location = ?, num_hives = ?, establishment_date = ? WHERE id = ?',
                       (self.name, self.location, self.num_hives, self.establishment_date, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect('beekeeping.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM apiaries WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()