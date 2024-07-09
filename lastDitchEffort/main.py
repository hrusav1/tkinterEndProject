# main.py
import tkinter as tk
from controllers.main_controller import MainController
from models.database_model import DatabaseModel
from views.main_view import MainView
from views.login_view import LoginView

if __name__ == "__main__":
    root = tk.Tk()
    db_model = DatabaseModel('apiary_data.db')
    login_view = LoginView(root)
    main_view = MainView(root)
    main_controller = MainController(db_model, login_view, main_view)

    main_controller.initialize_view()

    root.mainloop()