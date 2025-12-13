import pandas as pd
from app.data.db import connect_database
from app.data.db import initialize_tables

#Function insert ticket
def insert_ticket(priority, description, status, assigned_to, created_at, resolution_time_hours):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets (priority, description, status, assigned_to, created_at, resolution_time_hours)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (priority, description, status, assigned_to, created_at, resolution_time_hours))

    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()
    return ticket_id

#Function get all tickets
def get_all_tickets(conn):
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM tickets ORDER BY ticket_id",
        conn
    )
    conn.close()
    return df

#Function update ticket status
def update_ticket_status(conn, ticket_id, new_status):
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tickets
        SET status = ?
        WHERE ticket_id = ?
    """, (new_status, ticket_id))

    conn.commit()
    rows = cursor.rowcount
    conn.close()
    return rows

#Function delete ticket
def delete_ticket(ticket_id):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tickets WHERE ticket_id = ?
    """, (ticket_id,))

    conn.commit()
    rows = cursor.rowcount
    conn.close()
    return rows

if __name__ == '__main__':
    conn = connect_database()