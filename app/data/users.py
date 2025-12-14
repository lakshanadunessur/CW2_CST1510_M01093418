from app.data.db import connect_database
import sqlite3
from app.data.schema import create_users_table
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "DATA"

#Function to get user by username
def get_user_by_username(username):
    """Retrieve user by username."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
    user = cursor.fetchone()
    conn.close()
    return user

#Function to insert user
def insert_user(username, password_hash, role='user'):
    """Insert new user."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()

