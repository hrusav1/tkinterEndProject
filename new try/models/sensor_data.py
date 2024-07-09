#models/sensor_data.py
import sqlite3

class SensorData:
    def __init__(self, id, hive_id, data_type, value, timestamp):
        self.id = id
        self.hive_id = hive_id
        self.data_type = data_type
        self.value = value
        self.timestamp = timestamp

    @staticmethod
    def create(hive_id, data_type, value, timestamp):
        conn = sqlite3.connect('beekeeping.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sensor_data (hive_id, data_type, value, timestamp) VALUES (?, ?, ?, ?)',
                       (hive_id, data_type, value, timestamp))
        conn.commit()
        data_id = cursor.lastrowid
        conn.close()
        return SensorData(data_id, hive_id, data_type, value, timestamp)

    @staticmethod
    def get_for_hive(hive_id, data_type=None, start_date=None, end_date=None):
        conn = sqlite3.connect('beekeeping.db')
        cursor = conn.cursor()
        query = 'SELECT * FROM sensor_data WHERE hive_id = ?'
        params = [hive_id]
        if data_type:
            query += ' AND data_type = ?'
            params.append(data_type)
        if start_date:
            query += ' AND timestamp >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND timestamp <= ?'
            params.append(end_date)
        query += ' ORDER BY timestamp'
        cursor.execute(query, params)
        sensor_data = [SensorData(*row) for row in cursor.fetchall()]
        conn.close()
        return sensor_data