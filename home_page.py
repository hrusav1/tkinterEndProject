# File: home_page.py

import tkinter as tk
from login_base import BaseApplication

class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#252525")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Create the main rectangle at the center
        self.controller.create_rectangle(
            781.0, 113.0, 1138.0, 483.0,
            fill="#464646", outline=""
        )

        # Create "Home" text at the top of the rectangle
        self.controller.create_text(
            781.0, 90.0,
            anchor="nw",
            text="Home",
            fill="#FFFFFF",
            font=("Helvetica", 24, "bold")
        )

        # Create buttons
        self.controller.create_custom_button(
            811.0, 169.0,
            text="Already a User",
            command=lambda: self.controller.show_frame("LoginFrame"),
            width=200, height=50,
            bg="#767676", fg="#FFFFFF",
            hover_bg="#666666", hover_fg="#FFFFFF",
            font=("Helvetica", 16, "bold")
        )
        self.controller.create_custom_button(
            978.0, 171.0,
            text="Register",
            command=lambda: print("Register clicked"),
            width=200, height=50,
            bg="#767676", fg="#FFFFFF",
            hover_bg="#666666", hover_fg="#FFFFFF",
            font=("Helvetica", 16, "bold")
        )

if __name__ == "__main__":
    app = BaseApplication("Home Application", "1920x1080")
    home_frame = HomeFrame(app, app)
    app.add_frame(home_frame, "HomeFrame")
    app.show_frame("HomeFrame")
    app.mainloop()
