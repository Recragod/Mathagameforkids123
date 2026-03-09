#Programmer name: Joe Shikagishi

#libraries
import sqlite3

#Connect to the database (creates users.db if it doesn't)
conn = sqlite3.connect("users.db")

#Cursor alows us to execute SQL commands
cursor = conn.cursor()

#Create a table called "users"
cursor.execute("""
CREATE TABLE IF NOT EXIST users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
               
)
""")

#Insert a test user for login testing
cursor.execute("""
INSERT INTO users (username, password)
VALUES ('admin', '1234')
""")

#Save the changes
conn.commit()

#Close database connection
conn.close()

#lines prints in your terminal
print("Database created successfully")