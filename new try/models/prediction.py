#/models/prediction.py

import sqlite3

class Prediction:
    def __init__(self, id, hive_id, prediction_type, value, timestamp):
        self.id = id
        self.hive_id = hive_id
        self.prediction_type = prediction_type
        self.value = value
        self.timestamp = timestamp

    @staticmethod
    def create(hive_id, prediction_type, value, timestamp):
        conn = sqlite3.connect('beekeeping.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO predictions (hive_id, prediction_type, value, timestamp) VALUES (?, ?, ?, ?)',
                       (hive_id, prediction_type, value, timestamp))
        conn.commit()
        prediction_id = cursor.lastrowid
        conn.close()
        return Prediction(prediction_id, hive_id, prediction_type, value, timestamp)

    @staticmethod
    def get_latest_for_hive(hive_id, prediction_type):
        conn = sqlite3.connect('beekeeping.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM predictions WHERE hive_id = ? AND prediction_type = ? ORDER BY timestamp DESC LIMIT 1',
                       (hive_id, prediction_type))
        prediction_data = cursor.fetchone()
        conn.close()
        if prediction_data:
            return Prediction(*prediction_data)
        return None