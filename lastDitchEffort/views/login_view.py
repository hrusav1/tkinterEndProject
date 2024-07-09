# views/login_view.py
import tkinter as tk
from tkinter import messagebox


class LoginView:
    def __init__(self, master):
        self.master = master
        self.master.title("Apiary Management System - Login")
        self.master.geometry("1280x1024")
        self.master.resizable(False, False)

        self.frame = tk.Frame(self.master, bg="#464646")
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.frame, text="Login Page", font=("Arial", 20), bg="#464646", fg="white").pack(pady=20)

        tk.Label(self.frame, text="E-mail:", bg="#464646", fg="white").pack()
        self.email_entry = tk.Entry(self.frame, width=30)
        self.email_entry.pack(pady=5)

        tk.Label(self.frame, text="Password:", bg="#464646", fg="white").pack()
        self.password_entry = tk.Entry(self.frame, width=30, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.frame, text="Login", bg="#666666", fg="white")
        self.login_button.pack(pady=20)

        self.home_button = tk.Button(self.frame, text="Home", bg="#666666", fg="white")
        self.home_button.pack()

    def show(self):
        print("LoginView.show() called")  # Debug print
        self.master.deiconify()
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def hide(self):
        print("LoginView.hide() called")  # Debug print
        self.frame.place_forget()

    def show_error(self, message):
        messagebox.showerror("Error", message)