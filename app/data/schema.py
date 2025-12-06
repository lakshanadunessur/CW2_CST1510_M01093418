import sqlite3
from pathlib import Path
import os
import pandas as pd

def create_users_table(conn):
    """Create users table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()
def create_cyber_incidents_table(conn):
  cursor = conn.cursor()
  create_table_sql = """
  CREATE TABLE IF NOT EXISTS cyber_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    description TEXT NOT NULL,
    reported_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
  cursor.execute(create_table_sql)
  conn.commit()
  print("Cyber incidents table created successfully!")
  pass

def create_datasets_metadata_table(conn):
    cursor = conn.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS datasets_metadata (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      dataset_name TEXT NOT NULL,
      category TEXT NOT NULL,
      source TEXT NOT NULL,
      last_updated TEXT NOT NULL,
      record_count INTEGER NOT NULL,
      file_size_mb REAL NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
      """
    cursor.execute(create_table_sql)
    conn.commit()
    print("Datasets metadata table created successfully!")
    pass

def create_it_tickets_table(conn):
      cursor = conn.cursor()
      create_table_sql = """
      CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT NOT NULL UNIQUE,
        priority TEXT NOT NULL,
        status TEXT NOT NULL,
        category TEXT NOT NULL,
        subject TEXT NOT NULL,
        description TEXT
        created_date TEXT
        resolved_date TEXT,
        assigned_to TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
      cursor.execute(create_table_sql)
      conn.commit()
      print("IT tickets table created successfully!")
      pass

def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)

def load_csv_to_table(conn, csv_path, table_name):
    # 1. Check if file exists
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return 0

    # 2. Load CSV into DataFrame
    df = pd.read_csv(csv_path)

    # 3. Insert data into SQL table
    df.to_sql(name=table_name, con=conn, if_exists='append', index=False)

    # 4. Show result
    row_count = len(df)
    print(f"Loaded {row_count} rows into '{table_name}'")

    return row_count

def load_all_csv_data(conn):
    """
    Loads every domain CSV required by the platform.
    Update the paths to match your folder structure.
    """
    total_rows = 0

    csv_files = {
        "cyber_incidents": "DATA/cyber_incidents.csv",
        "datasets_metadata": "DATA/datasets_metadata.csv",
        "it_tickets": "DATA/it_tickets.csv"
    }

    for table, path in csv_files.items():
        print(f" - Loading {path} into {table}")
        total_rows += load_csv_to_table(conn, path, table)

    print(f"\nTotal CSV rows loaded: {total_rows}")
    return total_rows