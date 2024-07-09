#/models/database.py
import sqlite3
import os
from datetime import datetime

DATABASE_NAME = 'beekeeping.db'

class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(DATABASE_NAME)
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create Apiaries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS apiaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                location TEXT,
                num_hives INTEGER,
                established_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Create Hives table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                apiary_id INTEGER,
                name TEXT,
                hive_type TEXT,
                num_frames INTEGER,
                num_boxes INTEGER,
                queen_breed TEXT,
                queen_date DATE,
                last_inspection_date DATE,
                frames_brood INTEGER,
                frames_honey INTEGER,
                frames_pollen INTEGER,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (apiary_id) REFERENCES apiaries (id)
            )
        ''')

        # Create SensorData table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hive_id INTEGER,
                data_type TEXT,
                value REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (hive_id) REFERENCES hives (id)
            )
        ''')

        # Create Predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hive_id INTEGER,
                prediction_type TEXT,
                value TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (hive_id) REFERENCES hives (id)
            )
        ''')

        conn.commit()

    def insert_admin_user(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = 'admin'")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", ('admin', 'admin'))
            conn.commit()

db = Database()
db.create_tables()
db.insert_admin_user()