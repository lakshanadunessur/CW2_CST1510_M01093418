import pandas as pd
from app.data.db import connect_database
from app.data.db import initialize_tables


def insert_datasets(name, rows, columns, uploaded_by, upload_date):

    """Insert new incident."""
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO datasets_metadata (name, rows, columns, uploaded_by, upload_date) 
        VALUES (?, ?, ?, ?, ?, ?)
    """,(name,rows,columns,uploaded_by,upload_date))
    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()
    return dataset_id

def get_all_datasets(conn):
    conn= connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY dataset_id",
        conn
    )
    conn.close()
    return df

def update_dataset_name(conn , dataset_id, new_name):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE datasets_metadata 
        SET name = ?
        WHERE dataset_id = ?
    """,(new_name,dataset_id))
    conn.commit()
    rows = cursor.rowcount
    conn.close()
    return rows


def delete_dataset(dataset_id):
  conn = connect_database()
  cursor = conn.cursor()

  cursor.execute("DELETE FROM datasets_metadata WHERE dataset_id = ?",(dataset_id,))
  conn.commit()
  rows = cursor.rowcount
  conn.close()
  return rows

if __name__ == "__main__":
 conn = connect_database()