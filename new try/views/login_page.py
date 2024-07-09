# views/login_page.py
import tkinter as tk
from tkinter import ttk, messagebox
from utils.styling import create_centered_frame
from controllers.auth_controller import AuthController

class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.auth_controller = AuthController(controller.db)

        centered_frame = create_centered_frame(self, 400, 400)

        title_label = ttk.Label(centered_frame, text="Login Page", font=("TkDefaultFont", 24))
        title_label.pack(pady=20)

        email_label = ttk.Label(centered_frame, text="E-mail:")
        email_label.pack()
        self.email_entry = ttk.Entry(centered_frame)
        self.email_entry.pack(pady=5)

        password_label = ttk.Label(centered_frame, text="Password:")
        password_label.pack()
        self.password_entry = ttk.Entry(centered_frame, show="*")
        self.password_entry.pack(pady=5)

        login_button = ttk.Button(centered_frame, text="Login", command=self.login)
        login_button.pack(pady=20)

        home_button = ttk.Button(centered_frame, text="Home", command=self.go_to_home)
        home_button.pack()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if self.auth_controller.login(email, password):
            print("Login successful")
            messagebox.showinfo("Login", "Login successful")
            self.controller.show_frame("DashboardPage")
        else:
            print("Login failed")
            messagebox.showerror("Login", "Invalid email or password")

    def go_to_home(self):
        self.controller.show_frame("HomePage")