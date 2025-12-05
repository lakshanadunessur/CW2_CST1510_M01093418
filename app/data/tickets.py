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
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents(conn):
  query = "SELECT * FROM cyber_incidents"
  df = pd.read_sql_query(query, conn)
  return df

def update_incident_status(conn, incident_id, new_status):
    cursor = conn.cursor()
    query = "UPDATE cyber_incidents SET status = ? WHERE id = ?"
    values = (new_status, incident_id)
    cursor.execute(query, values)
    conn.commit()
    return cursor.rowcount


def delete_incident(conn, incident_id):
  cursor = conn.cursor()
  query = "DELETE FROM cyber_incidents WHERE id = ?"
  values = (incident_id,)
  cursor.execute(query, values)
  conn.commit()
  return cursor.rowcount