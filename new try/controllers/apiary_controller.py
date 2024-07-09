# controllers/apiary_controller.py

class ApiaryController:
    def __init__(self, db):
        self.db = db

    def get_apiaries(self, user_id):
        self.db.cursor.execute("""
            SELECT * FROM apiaries WHERE user_id = ?
        """, (user_id,))
        apiaries = self.db.cursor.fetchall()
        return [
            {
                'id': apiary[0],
                'name': apiary[2],
                'location': apiary[3],
                'num_hives': apiary[4],
                'establishment_date': apiary[5]
            }
            for apiary in apiaries
        ]

    def create_apiary(self, user_id, name, location, num_hives, establishment_date):
        try:
            self.db.cursor.execute("""
                INSERT INTO apiaries (user_id, name, location, num_hives, establishment_date)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, name, location, num_hives, establishment_date))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating apiary: {e}")
            return False

    def update_apiary(self, apiary_id, name, location, num_hives, establishment_date):
        try:
            self.db.cursor.execute("""
                UPDATE apiaries
                SET name = ?, location = ?, num_hives = ?, establishment_date = ?
                WHERE id = ?
            """, (name, location, num_hives, establishment_date, apiary_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating apiary: {e}")
            return False

    def delete_apiary(self, apiary_id):
        try:
            self.db.cursor.execute("DELETE FROM apiaries WHERE id = ?", (apiary_id,))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting apiary: {e}")
            return False