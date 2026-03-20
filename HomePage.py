#Programmer: Joe Shikagishi
#Importing Flask class & functions for HTML
#FLASK LOGIN AND SIGNUP APPLICAION (NO PASSWORD CHECK)
#------------------------------------------------------------------------

from flask import Flask, render_template, request, redirect, url_for
import sqlite3  # Allows you to use the SQL commands on Python
import os       # Module that creates a connection between your operating system & Python

#CREATE THE FLASK APPLICATION
#------------------------------------------------------------------------

app = Flask(__name__)

# DATABASE SETUP
#------------------------------------------------------------------------
DB_NAME = "users.db"

def init_db(): #Creates the take for us in the database
    """
    Initialise the database and create the users table if it doesn't exist
    """
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL   
            )             
        """)
        conn.commit()
        conn.close()

#Initialise the database
init_db()  #Use this function everytime we recall the table

#HOME PAGE ROUTE
#------------------------------------------------------------------------

#variables for login details
#USERNAME = "admin"
#PASSWORD = "1234"

#This route runs when the user goes to the login page
@app.route("/")

#name of function called home
def home():
#this shows the login.html page to the user
    return render_template("login.html")

@app.route("/learn")
def learn():
    return render_template("learn.html")



#This route runs when the login form is submitted
#it only accepts POST requests - because the form uses POST in HTML
@app.route("/login", methods=["POST"])

#name of function called login to accept data the user types
def login():
    #Get the username typed in the form on the login screen
    username=request.form["username"]
    #Get the password typed in the form on the login screen
    password=request.form["password"]

    conn = sqlite3.connect(DB_NAME) # connecting to the database
    cursor = conn.cursor() #creating a obj(var) called cursor
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)) #Selects ALL the username from the users table WHERE the username and password is equal to what the user has entered
    user = cursor.fetchone()
    conn.close()

    #Check if the username and password entered is a match to whats saved
    if user:
        #if the correct details are entered, show success message
        return render_template("home.html")
    
    if username == USERNAME and password == PASSWORD:
        return render_template("home.html")
     #if the incorrect details are entered, show invalid message
    else:
        return "Invalid username or password"
    
@app.route("/success")
def success():
    return "Login Successful!"

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username=request.form["username"]
        password=request.form["password"]

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute( 
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()

        return """
        <h3>User created successfully!</h3>
        <button onclick='window.close()'>Close Window</button>
        """

    # GET request: show signup form
    return """
    <html>
    <head><title>Sign Up</title></head>
    <body>
        <h2>Create New User</h2>
        <form method='POST'>
            <input type='text' name='username' placeholder='Username' required><br><br>
            <input type='password' name='password' placeholder='Password' required><br><br>
            <button type='submit'>Sign Up</button>
        </form>
    </body>
    </html>
    """

#This makes sure that the program runs only when this file is executed directly
if __name__ == "__main__":
    app.run(debug=True, port=4000)
