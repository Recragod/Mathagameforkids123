#Programmer name: Joe Shikagishi

import sqlite3 #libraries

conn = sqlite3.connect("users.db") #Connect to the database (creates users.db if it doesn't)

cursor = conn.cursor() #Cursor alows us to execute SQL commands

#Create a table called "users"
cursor.execute(""" 
CREATE TABLE IF NOT EXISTS users (

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

conn.commit() #Save the changes

conn.close() #Close database connection

print("Database created successfully") #lines prints in your terminal