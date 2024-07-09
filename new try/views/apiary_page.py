# views/apiary_page.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controllers.apiary_controller import ApiaryController


class ApiaryPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.apiary_controller = ApiaryController(controller.db)

        self.create_layout()

    def create_layout(self):
        # Create left sidebar (similar to DashboardPage)
        sidebar = ttk.Frame(self, width=200)
        sidebar.pack(side="left", fill="y")

        dashboard_button = ttk.Button(sidebar, text="Dashboard", command=self.show_dashboard)
        dashboard_button.pack(pady=10)

        apiary_button = ttk.Button(sidebar, text="Apiary", command=self.show_apiary)
        apiary_button.pack(pady=10)

        prediction_button = ttk.Button(sidebar, text="Prediction", command=self.show_prediction)
        prediction_button.pack(pady=10)

        logout_button = ttk.Button(sidebar, text="Logout", command=self.logout)
        logout_button.pack(pady=10)

        # Create right content area
        self.content_area = ttk.Frame(self)
        self.content_area.pack(side="right", expand=True, fill="both")

        # Initially show apiary content
        self.show_apiary()

    def show_dashboard(self):
        self.controller.show_frame("DashboardPage")

    def show_apiary(self):
        self.clear_content()
        apiaries = self.apiary_controller.get_apiaries(self.controller.current_user_id)

        if apiaries:
            self.display_apiaries(apiaries)
        else:
            self.show_create_apiary_form()

    def show_prediction(self):
        # Placeholder for prediction page
        pass

    def logout(self):
        if tk.messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.controller.show_frame("HomePage")

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def display_apiaries(self, apiaries):
        for apiary in apiaries:
            frame = ttk.Frame(self.content_area)
            frame.pack(pady=10, padx=10, fill="x")

            name_label = ttk.Label(frame, text=f"Name: {apiary['name']}")
            name_label.pack(side="left", padx=5)

            location_label = ttk.Label(frame, text=f"Location: {apiary['location']}")
            location_label.pack(side="left", padx=5)

            hives_label = ttk.Label(frame, text=f"Hives: {apiary['num_hives']}")
            hives_label.pack(side="left", padx=5)

            edit_button = ttk.Button(frame, text="Edit", command=lambda a=apiary: self.edit_apiary(a))
            edit_button.pack(side="right", padx=5)

        create_button = ttk.Button(self.content_area, text="Create New Apiary", command=self.show_create_apiary_form)
        create_button.pack(pady=20)

    def show_create_apiary_form(self):
        self.clear_content()

        form_frame = ttk.Frame(self.content_area)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Apiary Name:").grid(row=0, column=0, sticky="e", pady=5)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Location:").grid(row=1, column=0, sticky="e", pady=5)
        self.location_entry = ttk.Entry(form_frame)
        self.location_entry.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Number of Hives:").grid(row=2, column=0, sticky="e", pady=5)
        self.num_hives_entry = ttk.Entry(form_frame)
        self.num_hives_entry.grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Establishment Date:").grid(row=3, column=0, sticky="e", pady=5)
        self.date_entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=3, column=1, pady=5)

        create_button = ttk.Button(form_frame, text="Create Apiary", command=self.create_apiary)
        create_button.grid(row=4, column=0, columnspan=2, pady=20)

    def create_apiary(self):
        name = self.name_entry.get()
        location = self.location_entry.get()
        num_hives = self.num_hives_entry.get()
        date = self.date_entry.get()

        if name and location and num_hives and date:
            success = self.apiary_controller.create_apiary(
                self.controller.current_user_id, name, location, num_hives, date
            )
            if success:
                messagebox.showinfo("Success", "Apiary created successfully")
                self.show_apiary()
            else:
                messagebox.showerror("Error", "Failed to create apiary")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def edit_apiary(self, apiary):
        # Placeholder for edit apiary functionality
        pass