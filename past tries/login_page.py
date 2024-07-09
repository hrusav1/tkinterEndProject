# File: login_page.py

import tkinter as tk
from login_base import BaseApplication

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#252525")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Create the main rectangle at the center
        self.controller.create_rectangle(
            780.0, 113.0, 1137.0, 388.0,
            fill="#464646", outline=""
        )

        # Create "Login" text at the top of the rectangle
        self.controller.create_text(
            781.0, 90.0,
            anchor="nw",
            text="Login",
            fill="#FFFFFF",
            font=("Helvetica", 24, "bold")
        )

        # Username entry
        self.controller.create_entry(855.0, 179.63636779785156, 208.0, 19.0, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
        self.controller.create_text(856.0, 145.63636779785156, anchor="nw", text="Username:", fill="#FFFFFF", font=("Helvetica", 16))

        # Password entry
        self.controller.create_entry(856.0, 254.63636779785156, 208.0, 19.0, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
        self.controller.create_text(857.0, 220.63636779785156, anchor="nw", text="Password:", fill="#FFFFFF", font=("Helvetica", 16))

        # Create buttons
        self.controller.create_custom_button(910.0, 288.0, "Log In", lambda: print("Log In clicked"), 220, 30, bg="#767676", fg="#FFFFFF", hover_bg="#666666", hover_fg="#FFFFFF", font=("Helvetica", 12))
        self.controller.create_custom_button(910.0, 323.0, "Register", lambda: print("Register clicked"), 220, 30, bg="#767676", fg="#FFFFFF", hover_bg="#666666", hover_fg="#FFFFFF", font=("Helvetica", 12))
        self.controller.create_custom_button(909.0, 358.0, "Forgot Password", lambda: print("Forgot Password clicked"), 220, 30, bg="#767676", fg="#FFFFFF", hover_bg="#666666", hover_fg="#FFFFFF", font=("Helvetica", 12))

if __name__ == "__main__":
    app = BaseApplication("Login Application", "1920x1080")
    login_frame = LoginFrame(app, app)
    app.add_frame(login_frame, "LoginFrame")
    app.show_frame("LoginFrame")
    app.mainloop()
