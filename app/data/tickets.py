import pandas as pd
from app.data.db import connect_database
def insert_tickets(date, incident_type, severity, status, description, reported_by=None):
    """Insert new incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    tickets_id = cursor.lastrowid
    conn.close()
    return tickets_id

def get_all_incidents(conn):
  query = "SELECT * FROM cyber_incidents"
  df = pd.read_sql_query(query, conn)
  return df

def update_tickets(conn, tickets_id, new_status):
    cursor = conn.cursor()
    query = "UPDATE cyber_incidents SET status = ? WHERE id = ?"
    values = (new_status, tickets_id)
    cursor.execute(query, values)
    conn.commit()
    return cursor.rowcount


def delete_tickets(conn, tickets_id):
  cursor = conn.cursor()
  query = "DELETE FROM cyber_incidents WHERE id = ?"
  values = (tickets_id,)
  cursor.execute(query, values)
  conn.commit()
  return cursor.rowcount