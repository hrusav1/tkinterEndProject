# controllers/hive_controller.py

class HiveController:
    def __init__(self, db):
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