# models/database_model.py
import sqlite3
from datetime import datetime, timedelta
import random
import bcrypt
import requests


class DatabaseModel:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        self.generate_test_data()
        self.create_admin_user()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            data_type TEXT,
            value REAL
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            prediction_type TEXT,
            value TEXT
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            is_active INTEGER,
            last_login TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            password TEXT,
            location TEXT
        )
        ''')
        self.conn.commit()

    def get_honey_production_prediction(self, user_id):
        location = self.get_user_location(user_id)
        if not location:
            return "Please set a valid location to get a honey production prediction."

        api_key = "333a1b6b1304b37578bd5ca75a11fbaa"
        url = f"http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            weather_data = response.json()

            good_days = 0
            start_date = datetime.now().date()
            end_date = start_date + timedelta(days=5)

            for item in weather_data['list']:
                forecast_date = datetime.fromtimestamp(item['dt']).date()
                if start_date <= forecast_date < end_date:
                    if item['weather'][0]['main'] != 'Rain' and item['main']['temp'] > 18:
                        good_days += 1

            if good_days >= 3:
                return (f"Based on the weather forecast for {location} over the next 5 days, "
                        f"we expect {good_days} days of favorable conditions (no rain and temperature above 18°C). "
                        "This suggests moderate to good nectar flow availability in the area. "
                        "Bees are likely to be active, which could lead to increased honey production.")
            else:
                return (f"Based on the weather forecast for {location} over the next 5 days, "
                        f"we only expect {good_days} days of favorable conditions (no rain and temperature above 18°C). "
                        "This suggests that nectar flow may be limited. "
                        "Honey production might be lower than optimal during this period.")

        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return "Unable to fetch weather data. Please try again later."

    def save_user_location(self, user_id, location):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET location = ? WHERE id = ?", (location, user_id))
        self.conn.commit()

    def get_user_location(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT location FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None

    def verify_location(self, location):
        # Use a more lenient verification using OpenStreetMap Nominatim API
        url = f"https://nominatim.openstreetmap.org/search"
        params = {
            "q": location,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "ApairyManagementSystem/1.0"
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise an exception for bad responses
            results = response.json()
            return len(results) > 0
        except requests.RequestException as e:
            print(f"Error verifying location: {e}")
            return False

    def create_admin_user(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = 'admin'")
        if cursor.fetchone() is None:
            hashed_password = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)",
                           ('admin', hashed_password))
            self.conn.commit()

    def verify_user(self, email, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        if result:
            user_id, hashed_password = result
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                print(f"User verified: {user_id}")  # Debug print
                return user_id
        print("User verification failed")  # Debug print
        return None

    def insert_sensor_data(self, timestamp, data_type, value):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO sensor_data (timestamp, data_type, value) VALUES (?, ?, ?)",
                       (timestamp, data_type, value))
        self.conn.commit()

    def insert_prediction(self, timestamp, prediction_type, value):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO predictions (timestamp, prediction_type, value) VALUES (?, ?, ?)",
                       (timestamp, prediction_type, value))
        self.conn.commit()

    def update_sensor_data(self, id, timestamp, data_type, value):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE sensor_data SET timestamp = ?, data_type = ?, value = ? WHERE id = ?",
                       (timestamp, data_type, value, id))
        self.conn.commit()

    def delete_sensor_data(self, id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM sensor_data WHERE id = ?", (id,))
        self.conn.commit()

    def get_sensor_data(self, data_type):
        cursor = self.conn.cursor()
        cursor.execute("SELECT timestamp, value FROM sensor_data WHERE data_type = ? ORDER BY timestamp", (data_type,))
        return cursor.fetchall()

    def generate_test_data(self):
        data_types = ['temperature', 'humidity', 'weight']
        ranges = {
            'temperature': (-10, 45),
            'humidity': (10, 100),
            'weight': (15, 150)
        }

        for _ in range(100):  # Generate 100 data points for each type
            for data_type in data_types:
                timestamp = datetime.now() - timedelta(days=random.randint(0, 30))
                value = random.uniform(*ranges[data_type])
                self.insert_sensor_data(timestamp.isoformat(), data_type, value)

    def create_user_session(self, user_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM user_sessions WHERE user_id = ?", (user_id,))
            cursor.execute("INSERT INTO user_sessions (user_id, is_active, last_login) VALUES (?, 1, ?)",
                           (user_id, datetime.now().isoformat()))
            self.conn.commit()
            print(f"Session created for user_id: {user_id}")  # Debug print
            # Verify the session was created
            cursor.execute("SELECT is_active FROM user_sessions WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            print(f"Verified session active status: {result[0] if result else None}")  # Debug print
            return result[0] == 1 if result else False
        except sqlite3.Error as e:
            print(f"Database error: {e}")  # Debug print
            self.conn.rollback()
            return False

    def end_user_session(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE user_sessions SET is_active = 0 WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def is_session_active(self, user_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT is_active FROM user_sessions WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            is_active = result is not None and result[0] == 1
            print(f"Checking session for user_id: {user_id}. Result: {result}, Is active: {is_active}")  # Debug print
            return is_active
        except sqlite3.Error as e:
            print(f"Database error: {e}")  # Debug print
            return False

    def get_user_id(self, email):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        return result[0] if result else None
