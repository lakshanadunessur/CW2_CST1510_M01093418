import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """Connect to SQLite database."""
    return sqlite3.connect(str(db_path))



