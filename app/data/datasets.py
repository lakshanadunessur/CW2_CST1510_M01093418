import  sqlite3

conn = sqlite3.connect("intelligence_platform.db")
cur = conn.cursor()

#Create table user
cur.execute("""" CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
               role TEXT DEFAULT 'user')

            """)
#save changes
conn.commit()

#Adding data in user table
cur.execute(""" INSERT INTO users (username, password_hash, role)
             #VALUES (?, ?, ?)
             #""", ('alice', 'password_123', 'admin'))

conn.commit()

#Reading Values from user table
cur.execute("SELECT username FROM users WHERE role = ?""", ('admin',))
all_user = cur.fetchall()
#print(all_users)

#Updating existing data
cur.execute(""" UPDATE users SET role = ? WHERE username = ?""", ('admin','bob'))
cur.execute("SELECT * FROM users")