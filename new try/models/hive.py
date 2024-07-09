#/models/hive.py
import sqlite3

class Hive:
    def __init__(self, id, apiary_id, name, type, num_frames, queen_age, last_inspection_date):
        self.id = id
        self.apiary_id = apiary_id
        self.name = name
        self.type = type
        self.num_frames = num_frames
        self.queen_age = queen_age
        self.last_inspection_date = last_inspection_date

    @staticmethod
    def create(apiary_id, name, type, num_frames, queen_age, last_inspection_date):
        conn = sqlite3.connect('beekeeping.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO hives (apiary_id, name, type, num_frames, queen_age, last_inspection_date) VALUES (?, ?, ?, ?, ?, ?)',
                       (apiary_id, name, type, num_frames, queen_age, last_inspection_date))
        conn.commit()
        hive_id = cursor.lastrowid
        conn.close()
        return Hive(hive_id, apiary_id, name, type, num_frames, queen_age, last_inspection_date)

    @staticmethod
    def get_all_for_apiary(apiary_id):
        conn = sqlite3.connect('beekeeping.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM hives WHERE apiary_id = ?', (apiary_id,))
        hives = [Hive(*row) for row in cursor.fetchall()]
        conn.close()
        return hives

    def update(self):
        conn = sqlite3.connect('beekeeping.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE hives SET name = ?, type = ?, num_frames = ?, queen_age = ?, last_inspection_date = ? WHERE id = ?',
                       (self.name, self.type, self.num_frames, self.queen_age, self.last_inspection_date, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect('beekeeping.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM hives WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()