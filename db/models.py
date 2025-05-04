import sqlite3
from db.database import Database
import json
import hashlib


class BookingModel:
    def __init__(self, db: Database):
        self.db = db
        # Database is already initialized by Database class

    def create_user(self, username, password, role="user"):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            try:
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                              (username, hashed_password, role))
                return True
            except sqlite3.IntegrityError:
                return False

    def authenticate_user(self, username, password):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, hashed_password))
            result = cursor.fetchone()
            return result[0] if result else None

    def create_booking(self, date, event_type, guest_count, phone, child_name, program_id, addon_ids, masterclass_ids, total_price):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bookings (date, event_type, guest_count, phone, child_name, program_id, addon_ids, masterclass_ids, total_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (date, event_type, guest_count, phone, child_name, program_id, json.dumps(addon_ids), json.dumps(masterclass_ids), total_price))
            return cursor.lastrowid

    def get_all_bookings(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bookings")
            return [dict(row) for row in cursor.fetchall()]

    def delete_booking(self, booking_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))

    def get_programs(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM programs")
            return [dict(row) for row in cursor.fetchall()]

    def get_addons(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM addons")
            return [dict(row) for row in cursor.fetchall()]

    def get_masterclasses(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM masterclasses")
            return [dict(row) for row in cursor.fetchall()]

    def add_program(self, name, price):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO programs (name, price) VALUES (?, ?)", (name, price))
            return cursor.lastrowid

    def add_addon(self, name, price):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO addons (name, price) VALUES (?, ?)", (name, price))
            return cursor.lastrowid

    def add_masterclass(self, name, price_per_child):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO masterclasses (name, price_per_child) VALUES (?, ?)", (name, price_per_child))
            return cursor.lastrowid

    def delete_program(self, program_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM programs WHERE id = ?", (program_id,))

    def delete_addon(self, addon_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM addons WHERE id = ?", (addon_id,))

    def delete_masterclass(self, masterclass_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM masterclasses WHERE id = ?", (masterclass_id,))