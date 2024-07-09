# File: main.py

from login_base import BaseApplication
from home_page import HomeFrame
from login_page import LoginFrame

if __name__ == "__main__":
    app = BaseApplication("Main Application", "1920x1080")

    home_frame = HomeFrame(app, app)
    login_frame = LoginFrame(app, app)

    app.add_frame(home_frame, "HomeFrame")
    app.add_frame(login_frame, "LoginFrame")

    app.show_frame("HomeFrame")  # Show the home frame first

    app.mainloop()
