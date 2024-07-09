# controllers/hive_controller.py
from tkinter import messagebox, ttk


class HiveController:
    def __init__(self, db):
        self.hive_controller = None
        self.db = db

    def get_hives(self, apiary_id):
        self.db.cursor.execute("""
            SELECT * FROM hives WHERE apiary_id = ?
        """, (apiary_id,))
        hives = self.db.cursor.fetchall()
        return [
            {
                'id': hive[0],
                'name': hive[2],
                'type': hive[3],
                'num_frames': hive[4],
                'num_boxes': hive[5],
                'queen_breed': hive[6],
                'queen_age': hive[7],
                'last_inspection_date': hive[8],
                'frames_brood': hive[9],
                'frames_honey': hive[10],
                'frames_pollen': hive[11],
                'notes': hive[12]
            }
            for hive in hives
        ]

    def create_hive(self, apiary_id, name, hive_type, num_frames, num_boxes, queen_breed, queen_age, last_inspection_date, frames_brood, frames_honey, frames_pollen, notes):
        try:
            self.db.cursor.execute("""
                INSERT INTO hives (apiary_id, name, type, num_frames, num_boxes, queen_breed, queen_age, last_inspection_date, frames_brood, frames_honey, frames_pollen, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (apiary_id, name, hive_type, num_frames, num_boxes, queen_breed, queen_age, last_inspection_date, frames_brood, frames_honey, frames_pollen, notes))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating hive: {e}")
            return False

    def update_hive(self, hive_id, name, hive_type, num_frames, num_boxes, queen_breed, queen_age, last_inspection_date, frames_brood, frames_honey, frames_pollen, notes):
        try:
            self.db.cursor.execute("""
                UPDATE hives
                SET name = ?, type = ?, num_frames = ?, num_boxes = ?, queen_breed = ?, queen_age = ?, last_inspection_date = ?, frames_brood = ?, frames_honey = ?, frames_pollen = ?, notes = ?
                WHERE id = ?
            """, (name, hive_type, num_frames, num_boxes, queen_breed, queen_age, last_inspection_date, frames_brood, frames_honey, frames_pollen, notes, hive_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating hive: {e}")
            return False

    def delete_hive(self, hive_id):
        try:
            self.db.cursor.execute("DELETE FROM hives WHERE id = ?", (hive_id,))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting hive: {e}")
            return False

    def edit_hive(self, hive):
        # Placeholder for edit hive functionality
        self.clear_content()

        form_frame = ttk.Frame(self.content_area)
        form_frame.pack(pady=20)

        # Prepopulate the fields with current hive data
        ttk.Label(form_frame, text="Hive Name:").grid(row=0, column=0, sticky="e", pady=5)
        self.hive_name_entry = ttk.Entry(form_frame)
        self.hive_name_entry.grid(row=0, column=1, pady=5)
        self.hive_name_entry.insert(0, hive['name'])

        ttk.Label(form_frame, text="Hive Type:").grid(row=1, column=0, sticky="e", pady=5)
        self.hive_type_entry = ttk.Entry(form_frame)
        self.hive_type_entry.grid(row=1, column=1, pady=5)
        self.hive_type_entry.insert(0, hive['type'])

        # Add other fields similarly...

        save_button = ttk.Button(form_frame, text="Save Changes", command=lambda: self.save_hive_changes(hive['id']))
        save_button.grid(row=7, column=0, columnspan=2, pady=20)

    def save_hive_changes(self, hive_id):
        # Collect the data from the form
        name = self.hive_name_entry.get()
        hive_type = self.hive_type_entry.get()

        # Update the hive in the database
        success = self.hive_controller.update_hive(hive_id, name, hive_type, ...)

        if success:
            messagebox.showinfo("Success", "Hive updated successfully")
            self.get_hives({'id': apiary_id})
        else:
            messagebox.showerror("Error", "Failed to update hive")
