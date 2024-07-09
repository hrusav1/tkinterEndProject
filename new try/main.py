# main.py
import tkinter as tk
from tkinter import ttk
from views.home_page import HomePage
from views.login_page import LoginPage
from views.dashboard_page import DashboardPage
from views.apiary_page import ApiaryPage
from models.database import Database

class BeekeepingApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Beekeeping Management System")
        self.geometry("1280x1024")
        self.resizable(False, False)

        self.db = Database()
        self.db.setup()

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, LoginPage, DashboardPage, ApiaryPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    app = BeekeepingApp()
    app.mainloop()

# models/database.py
import sqlite3
import bcrypt

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('beekeeping.db')
        self.cursor = self.conn.cursor()

    def setup(self):
        self.create_users_table()
        self.create_apiaries_table()
        self.create_hives_table()
        self.create_sensor_data_table()
        self.create_predictions_table()
        self.insert_admin_user()

    def create_users_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def create_apiaries_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS apiaries (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            num_hives INTEGER NOT NULL,
            establishment_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        self.conn.commit()

    def create_hives_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS hives (
            id INTEGER PRIMARY KEY,
            apiary_id INTEGER,
            name TEXT,
            type TEXT,
            num_frames INTEGER,
            num_boxes INTEGER,
            queen_breed TEXT,
            queen_age INTEGER,
            last_inspection_date TEXT,
            frames_brood INTEGER,
            frames_honey INTEGER,
            frames_pollen INTEGER,
            notes TEXT,
            FOREIGN KEY (apiary_id) REFERENCES apiaries (id)
        )
        ''')
        self.conn.commit()

    def create_sensor_data_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY,
            hive_id INTEGER,
            data_type TEXT NOT NULL,
            value REAL NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (hive_id) REFERENCES hives (id)
        )
        ''')
        self.conn.commit()

    def create_predictions_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY,
            hive_id INTEGER,
            honey_production REAL,
            hive_health TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (hive_id) REFERENCES hives (id)
        )
        ''')
        self.conn.commit()

    def insert_admin_user(self):
        hashed_password = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute('''
        INSERT OR IGNORE INTO users (email, password) VALUES (?, ?)
        ''', ('admin', hashed_password))
        self.conn.commit()

    def close(self):
        self.conn.close()