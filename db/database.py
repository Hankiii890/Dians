import sqlite3
from contextlib import contextmanager
import hashlib


class Database:
    def __init__(self, db_name="events.db"):
        self.db_name = db_name
        self._initialized = False
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init_db(self):
        if self._initialized:
            return
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Programs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS programs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price INTEGER NOT NULL
                )
            """)
            # Add-ons table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS addons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price INTEGER NOT NULL
                )
            """)
            # Masterclasses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS masterclasses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price_per_child INTEGER NOT NULL
                )
            """)
            # Bookings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    guest_count INTEGER NOT NULL,
                    phone TEXT NOT NULL,
                    child_name TEXT NOT NULL,
                    program_id INTEGER,
                    addon_ids TEXT,
                    masterclass_ids TEXT,
                    total_price INTEGER NOT NULL,
                    completed INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (program_id) REFERENCES programs(id)
                )
            """)
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
                )
            """)
            # Add completed column if not exists
            cursor.execute("PRAGMA table_info(bookings)")
            columns = [col[1] for col in cursor.fetchall()]
            if "completed" not in columns:
                cursor.execute("ALTER TABLE bookings ADD COLUMN completed INTEGER NOT NULL DEFAULT 0")
            # Check if default admin exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
            if cursor.fetchone()[0] == 0:
                # Default admin: username='admin', password='admin123'
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                              ("admin", hashlib.sha256("admin123".encode()).hexdigest(), "admin"))
            # Insert default data for programs
            cursor.execute("SELECT COUNT(*) FROM programs")
            if cursor.fetchone()[0] == 0:
                programs = [
                    ("Transformers", 8000),
                    ("Lady Bug", 8000),
                    ("Disney", 8000),
                    ("Super Heroes", 8000)
                ]
                cursor.executemany("INSERT INTO programs (name, price) VALUES (?, ?)", programs)
            # Insert default data for addons
            cursor.execute("SELECT COUNT(*) FROM addons")
            if cursor.fetchone()[0] == 0:
                addons = [
                    ("Soap Show", 2000),
                    ("Magic Disco", 2000),
                    ("Magician", 3000)
                ]
                cursor.executemany("INSERT INTO addons (name, price) VALUES (?, ?)", addons)
            # Insert default data for masterclasses
            cursor.execute("SELECT COUNT(*) FROM masterclasses")
            if cursor.fetchone()[0] == 0:
                masterclasses = [
                    ("Young Confectioner", 350),
                    ("Young Artist", 250),
                    ("Slime Lab", 300)
                ]
                cursor.executemany("INSERT INTO masterclasses (name, price_per_child) VALUES (?, ?)", masterclasses)
            self._initialized = True