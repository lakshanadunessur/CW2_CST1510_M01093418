import pandas as pd
from app.data.db import connect_database


# INSERT TICKET

def insert_ticket( title, priority, status):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets (title, priority, status)
        VALUES (?, ?, ?)
    """, (title, priority, status))
    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()
    return ticket_id

# GET ALL TICKETS
def get_all_tickets(conn):
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM tickets ORDER BY ticket_id DESC",
        conn
    )
    conn.close()
    return df

# UPDATE TICKET
def update_ticket(conn, ticket_id, new_status):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tickets
        SET status = ?
        WHERE id = ?
    """, (new_status, ticket_id))
    conn.commit()
    rows = cursor.rowcount
    conn.close()
    return rows

# DELETE TICKET

def delete_ticket(conn, ticket_id):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM tickets
        WHERE id = ?
    """, (ticket_id,))
    conn.commit()
    rows = cursor.rowcount
    conn.close()
    return rows
if __name__ == "__main__":
 conn = connect_database()