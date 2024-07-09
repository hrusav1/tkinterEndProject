#updated versioon of apiary_page.py
# views/apiary_page.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controllers.apiary_controller import ApiaryController
from controllers.hive_controller import HiveController

class ApiaryPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.apiary_controller = ApiaryController(controller.db)
        self.hive_controller = HiveController(controller.db)

        self.create_layout()

    def create_layout(self):
        # ... (previous sidebar code remains the same)

        # Create right content area
        self.content_area = ttk.Frame(self)
        self.content_area.pack(side="right", expand=True, fill="both")

        # Initially show apiary content
        self.show_apiary()

    # ... (previous methods remain the same)

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

            view_hives_button = ttk.Button(frame, text="View Hives", command=lambda a=apiary: self.view_hives(a))
            view_hives_button.pack(side="right", padx=5)

        create_button = ttk.Button(self.content_area, text="Create New Apiary", command=self.show_create_apiary_form)
        create_button.pack(pady=20)

    def view_hives(self, apiary):
        self.clear_content()

        hives = self.hive_controller.get_hives(apiary['id'])

        for hive in hives:
            frame = ttk.Frame(self.content_area)
            frame.pack(pady=10, padx=10, fill="x")

            name_label = ttk.Label(frame, text=f"Name: {hive['name']}")
            name_label.pack(side="left", padx=5)

            type_label = ttk.Label(frame, text=f"Type: {hive['type']}")
            type_label.pack(side="left", padx=5)

            frames_label = ttk.Label(frame, text=f"Frames: {hive['num_frames']}")
            frames_label.pack(side="left", padx=5)

            edit_button = ttk.Button(frame, text="Edit", command=lambda h=hive: self.edit_hive(h))
            edit_button.pack(side="right", padx=5)

        create_hive_button = ttk.Button(self.content_area, text="Add New Hive", command=lambda: self.show_create_hive_form(apiary['id']))
        create_hive_button.pack(pady=20)

        back_button = ttk.Button(self.content_area, text="Back to Apiaries", command=self.show_apiary)
        back_button.pack(pady=10)

    def show_create_hive_form(self, apiary_id):
        self.clear_content()

        form_frame = ttk.Frame(self.content_area)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Hive Name:").grid(row=0, column=0, sticky="e", pady=5)
        self.hive_name_entry = ttk.Entry(form_frame)
        self.hive_name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Hive Type:").grid(row=1, column=0, sticky="e", pady=5)
        self.hive_type_entry = ttk.Entry(form_frame)
        self.hive_type_entry.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Number of Frames:").grid(row=2, column=0, sticky="e", pady=5)
        self.num_frames_entry = ttk.Entry(form_frame)
        self.num_frames_entry.grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Number of Boxes:").grid(row=3, column=0, sticky="e", pady=5)
        self.num_boxes_entry = ttk.Entry(form_frame)
        self.num_boxes_entry.grid(row=3, column=1, pady=5)

        ttk.Label(form_frame, text="Queen Breed:").grid(row=4, column=0, sticky="e", pady=5)
        self.queen_breed_entry = ttk.Entry(form_frame)
        self.queen_breed_entry.grid(row=4, column=1, pady=5)

        ttk.Label(form_frame, text="Queen Age:").grid(row=5, column=0, sticky="e", pady=5)
        self.queen_age_entry = ttk.Entry(form_frame)
        self.queen_age_entry.grid(row=5, column=1, pady=5)

        ttk.Label(form_frame, text="Last Inspection Date:").grid(row=6, column=0, sticky="e", pady=5)
        self.last_inspection_date_entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.last_inspection_date_entry.grid(row=6, column=1, pady=5)

        create_button = ttk.Button(form_frame, text="Create Hive", command=lambda: self.create_hive(apiary_id))
        create_button.grid(row=7, column=0, columnspan=2, pady=20)

    def create_hive(self, apiary_id):
        name = self.hive_name_entry.get()
        hive_type = self.hive_type_entry.get()
        num_frames = self.num_frames_entry.get()
        num_boxes = self.num_boxes_entry.get()
        queen_breed = self.queen_breed_entry.get()
        queen_age = self.queen_age_entry.get()
        last_inspection_date = self.last_inspection_date_entry.get()

        if all([name, hive_type, num_frames, num_boxes, queen_breed, queen_age, last_inspection_date]):
            success = self.hive_controller.create_hive(
                apiary_id, name, hive_type, num_frames, num_boxes, queen_breed, queen_age, last_inspection_date, 0, 0, 0, ""
            )
            if success:
                messagebox.showinfo("Success", "Hive created successfully")
                self.view_hives({'id': apiary_id})
            else:
                messagebox.showerror("Error", "Failed to create hive")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def edit_hive(self, hive):
        # Placeholder for edit hive functionality
        pass