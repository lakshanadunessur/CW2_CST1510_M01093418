import sqlite3
from pathlib import Path
from app.data.schema import create_all_tables, load_all_csv_data

DB_PATH = Path(__file__).resolve().parent.parent.parent / "DATA" / "intelligence_platform.db"


def connect_database(db_path=DB_PATH):
    """Connect to SQLite database."""
    return sqlite3.connect(str(db_path))

def initialize_tables():
    """Connect to the SQLite database (creates file if not exist)"""

    conn =connect_database()
    create_all_tables(conn)
    load_all_csv_data(conn)
    conn.close()

