# views/home_page.py
import tkinter as tk
from tkinter import ttk
from utils.styling import create_centered_frame

class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        centered_frame = create_centered_frame(self, 400, 300)

        title_label = ttk.Label(centered_frame, text="Home", font=("TkDefaultFont", 24))
        title_label.pack(pady=20)

        button_frame = ttk.Frame(centered_frame)
        button_frame.pack(pady=20)

        login_button = ttk.Button(button_frame, text="Already a user", command=self.go_to_login)
        login_button.pack(side="left", padx=10)

        register_button = ttk.Button(button_frame, text="Register", command=self.register)
        register_button.pack(side="left", padx=10)

    def go_to_login(self):
        self.controller.show_frame("LoginPage")

    def register(self):
        print("Register clicked")