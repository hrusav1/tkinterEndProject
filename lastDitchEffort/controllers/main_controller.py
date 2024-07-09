# controllers/main_controller.py
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


class MainController:
    def __init__(self, model, login_view, main_view):
        self.model = model
        self.login_view = login_view
        self.main_view = main_view
        self.current_user_id = None
        self.setup_login_button_commands()
        self.setup_main_button_commands()

    def setup_login_button_commands(self):
        self.login_view.login_button.config(command=self.login)
        self.login_view.home_button.config(command=self.show_login_view)

    def setup_main_button_commands(self):
        self.main_view.buttons["Dashboard"].config(command=self.show_dashboard)
        self.main_view.buttons["Prediction"].config(command=self.show_prediction)
        self.main_view.buttons["Apiary"].config(command=self.placeholder_click)
        self.main_view.buttons["Logout"].config(command=self.logout)

    def login(self):
        print("Login method called")  # Debug print
        email = self.login_view.email_entry.get()
        password = self.login_view.password_entry.get()
        print(f"Attempting login with email: {email}")  # Debug print
        user_id = self.model.verify_user(email, password)
        if user_id:
            print(f"Login successful for user_id: {user_id}")  # Debug print
            self.current_user_id = user_id
            session_created = self.model.create_user_session(user_id)
            print(f"Session created: {session_created}")  # Debug print
            print(f"self.current_user_id set to: {self.current_user_id}")  # Debug print
            # Double-check session is active
            is_active = self.model.is_session_active(user_id)
            print(f"Double-checked session active status: {is_active}")  # Debug print
            if is_active:
                print("Calling show_main_view()")  # Debug print
                self.show_main_view()
            else:
                print("Session creation failed, showing error")  # Debug print
                self.login_view.show_error("Failed to create session. Please try again.")
        else:
            print("Login failed")  # Debug print
            self.login_view.show_error("Invalid email or password")

    def logout(self):
        if self.current_user_id:
            self.model.end_user_session(self.current_user_id)
        self.current_user_id = None
        self.show_login_view()

    def show_login_view(self):
        self.main_view.hide()
        self.login_view.show()

    def show_main_view(self):
        print("show_main_view called")  # Debug print
        self.login_view.hide()
        self.main_view.show()
        print("Calling show_dashboard()")  # Debug print
        self.show_dashboard()

    def show_login(self):
        self.main_view.hide()
        self.login_view.show()

    def show_dashboard(self):
        print("show_dashboard called")  # Debug print
        if self.current_user_id and self.model.is_session_active(self.current_user_id):
            print(f"Showing dashboard for user_id: {self.current_user_id}")  # Debug print
            data = {}
            for data_type in ['temperature', 'humidity', 'weight']:
                raw_data = self.model.get_sensor_data(data_type)
                data[data_type] = [(datetime.fromisoformat(row[0]), row[1]) for row in raw_data]
            self.main_view.show_dashboard(data)
        else:
            print(f"No active session. current_user_id: {self.current_user_id}")  # Debug print
            self.show_login_view()

    def initialize_view(self):
        active_user = self.model.get_user_id('admin')  # change this to the last logged-in user
        if active_user and self.model.is_session_active(active_user):
            self.current_user_id = active_user
            self.show_main_view()
        else:
            self.show_login_view()

    def show_prediction(self):
        honey_prediction = self.model.get_honey_production_prediction(self.current_user_id)
        health_prediction = "Hive health status: Good\nNo immediate concerns detected. Regular inspection recommended."
        current_location = self.model.get_user_location(self.current_user_id)
        self.main_view.show_prediction(honey_prediction, health_prediction, current_location)
        self.main_view.location_submit.config(command=self.submit_location)

    def placeholder_click(self):
        print("Button clicked")

    def submit_location(self):
        location = self.main_view.location_entry.get()
        if self.model.verify_location(location):
            self.model.save_user_location(self.current_user_id, location)
            tk.messagebox.showinfo("Success", f"Location '{location}' has been saved.")
            self.show_prediction()
        else:
            tk.messagebox.showerror("Error", f"'{location}' is not a valid location. Please try again.")
