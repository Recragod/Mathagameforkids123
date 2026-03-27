#Programmer: Joe Shikagishi
#Importing Flask class & functions for HTML
#FLASK LOGIN AND SIGNUP APPLICAION (NO PASSWORD CHECK)
#------------------------------------------------------------------------

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3  # Allows you to use the SQL commands on Python
import os       # Module that creates a connection between your operating system & Python

#CREATE THE FLASK APPLICATION
#------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = "math_masters_secret_123"  # signs and secures session cookies so no one can hack and bypass

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


@app.route("/addition")
def addition():
    return render_template("addition.html")

@app.route("/subtraction")
def subtraction():
    return render_template("subtraction.html")

@app.route("/division")
def division():
    return render_template("division.html")

@app.route("/multiplication")
def multiplication():
    return render_template("multiplication.html")

@app.route("/home")
def homepage():
    username = session.get("username", "Fellow Mathmathician")
    return render_template("home.html", username=username)

@app.route("/practice")
def practice():
    return render_template("practice.html")

@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    return redirect(url_for("login"))  # sends them back to the login page

#This route runs when the login form is submitted
#it only accepts POST requests - because the form uses POST in HTML
@app.route("/login", methods=["GET", "POST"])
def login():
    # check if the user is submitting the form (POST) or just visiting the page (GET)
    if request.method == "POST":
        # get the username and password typed in the form
        username = request.form["username"]
        password = request.form["password"]

        # connect to the database and search for a matching user
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        # if a matching user was found, go to homepage
        if user:
            session["username"] = username #defines the username variable
            return redirect(url_for("homepage"))
        # otherwise tell them the details were wrong
        else:
            return render_template("login.html", error="Invalid username or password")  #shows Invalid username or password if and error is sent from the login page
    
    else:
        # GET request - just show the login page
        return render_template("login.html", error=None)
    
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
import random

def generate_easy_question():
    num1 = random.randint(1, 99)   # generates a random number from 1 to 99
    num2 = random.randint(1, 99)   # generates a random number from 1 to 99
    operation = random.choice(["+", "-"])   # randomly picks addition or subtraction

    # makes sure subtraction never goes negative
    if operation == "-" and num2 > num1:
        num1, num2 = num2, num1

    question = f"{num1} {operation} {num2}"
    answer = eval(question)
    return question, answer

def generate_medium_question():
    mediumnum1 = random.randint(1, 99)   # generates a random number from 1 to 99
    mediumnum2 = random.randint(1, 99)   # generates a random number from 1 to 99
    mediumoperation = random.choice(["+", "-", "/", "*"])   # randomly picks the operation

    # this code makes sure division gives whole numbers
    if mediumoperation == "/":
        mediumnum2 = random.randint(1, 9)
        mediumnum1 = mediumnum2 * random.randint(1, 9)

    question = f"{mediumnum1} {mediumoperation} {mediumnum2}"
    answer = int(eval(question))
    return question, answer

def generate_hard_question():
    hardnum1 = random.randint(100, 999)   # generates a random number from 100 to 999
    hardnum2 = random.randint(100, 999)   # generates a random number from 100 to 999
    hardoperation = random.choice(["+", "-", "/", "*"])   # randomly picks the operation

    # this code makes sure division gives whole numbers
    if hardoperation == "/":
        hardnum2 = random.randint(10, 99)
        hardnum1 = hardnum2 * random.randint(10, 99)

    question = f"{hardnum1} {hardoperation} {hardnum2}"
    answer = int(eval(question))
    return question, answer

def generate_timeattack_question():
    timeattacknum1 = random.randint(1, 9)   # generates a random number from 1 to 9
    timeattacknum2 = random.randint(1, 9)   # generates a random number from 1 to 9
    timeattackoperation = random.choice(["+", "-", "/", "*"])   # randomly picks the operation

    # this code makes sure division gives whole numbers
    if timeattackoperation == "/":
        timeattacknum2 = random.randint(1, 9)
        timeattacknum1 = timeattacknum2 * random.randint(1, 9)

    question = f"{timeattacknum1} {timeattackoperation} {timeattacknum2}"
    answer = int(eval(question))
    return question, answer


@app.route("/practice/easy", methods=["GET", "POST"])
def practice_easy():
    # reset game when user first visits the page
    if request.method == "GET":
        session["easy_score"] = 0
        session["easy_question_number"] = 1
        question, answer = generate_easy_question()
        session["easy_answer"] = answer
        return render_template("easy.html",
            question=question,
            question_number=1,
            score=0,
            feedback=None)

    # handle answer when user submits
    if request.method == "POST":
        user_answer = int(request.form["answer"])
        correct_answer = session.get("easy_answer")
        score = session.get("easy_score", 0)
        question_number = session.get("easy_question_number", 1)

        # check if answer is correct and update score
        if user_answer == correct_answer:
            score += 1
            feedback = "Correct!"
            feedback_type = "correct"
        else:
            feedback = "Incorrect!"
            feedback_type = "incorrect"

        session["easy_score"] = score
        question_number += 1
        session["easy_question_number"] = question_number

        # if all 10 questions are done, show game over screen
        if question_number > 10:
            return render_template("easy.html",
                question=None,
                question_number=10,
                score=score,
                feedback=None)

        # generate next question
        question, answer = generate_easy_question()
        session["easy_answer"] = answer

        return render_template("easy.html",
            question=question,
            question_number=question_number,
            score=score,
            feedback=feedback,
            feedback_type=feedback_type)
    
@app.route("/practice/medium", methods=["GET", "POST"])
def practice_medium():
    # reset game when user first visits the page
    if request.method == "GET":
        session["medium_score"] = 0
        session["medium_question_number"] = 1
        question, answer = generate_medium_question()
        session["medium_answer"] = answer
        return render_template("medium.html",
            question=question,
            question_number=1,
            score=0,
            feedback=None)

    # handle answer when user submits
    if request.method == "POST":
        user_answer = int(request.form["answer"])
        correct_answer = session.get("medium_answer")
        score = session.get("medium_score", 0)
        question_number = session.get("medium_question_number", 1)

        # check if answer is correct and update score
        if user_answer == correct_answer:
            score += 1
            feedback = "Correct!"
            feedback_type = "correct"
        else:
            feedback = "Incorrect!"
            feedback_type = "incorrect"

        session["medium_score"] = score
        question_number += 1
        session["medium_question_number"] = question_number

        # if all 15 questions are done, show game over screen
        if question_number > 15:
            return render_template("medium.html",
                question=None,
                question_number=15,
                score=score,
                feedback=None)

        # generate next question
        question, medanswer = generate_medium_question()
        session["medium_answer"] = medanswer

        return render_template("medium.html",
            question=question,
            question_number=question_number,
            score=score,
            feedback=feedback,
            feedback_type=feedback_type)

@app.route("/practice/hard", methods=["GET", "POST"])
def practice_hard():
    # reset game when user first visits the page
    if request.method == "GET":
        session["hard_score"] = 0
        session["hard_question_number"] = 1
        question, answer = generate_hard_question()
        session["hard_answer"] = answer
        return render_template("hard.html",
            question=question,
            question_number=1,
            score=0,
            feedback=None)

    # handle answer when user submits
    if request.method == "POST":
        user_answer = int(request.form["answer"])
        correct_answer = session.get("hard_answer")
        score = session.get("hard_score", 0)
        question_number = session.get("hard_question_number", 1)

        # check if answer is correct and update score
        if user_answer == correct_answer:
            score += 1
            feedback = "Correct!"
            feedback_type = "correct"
        else:
            feedback = "Incorrect!"
            feedback_type = "incorrect"

        session["hard_score"] = score
        question_number += 1
        session["hard_question_number"] = question_number

        # if all 20 questions are done, show game over screen
        if question_number > 20:
            return render_template("hard.html",
                question=None,
                question_number=20,
                score=score,
                feedback=None)

        # generate next question
        question, hardanswer = generate_hard_question()
        session["hard_answer"] = hardanswer

        return render_template("hard.html",
            question=question,
            question_number=question_number,
            score=score,
            feedback=feedback,
            feedback_type=feedback_type)
    
@app.route("/practice/timeattack", methods=["GET", "POST"])
def practice_timeattack():
    # reset game when user first visits the page
    if request.method == "GET":
        session["timeattack_score"] = 0
        session["timeattack_question_number"] = 1
        question, answer = generate_timeattack_question()
        session["timeattack_answer"] = answer
        return render_template("timeattack.html",
            question=question,
            question_number=1,
            score=0,
            feedback=None)

    # handle answer when user submits
    if request.method == "POST":
        user_answer = int(request.form["answer"])
        correct_answer = session.get("timeattack_answer")
        score = session.get("timeattack_score", 0)
        question_number = session.get("timeattack_question_number", 1)

        # check if answer is correct and update score
        if user_answer == correct_answer:
            score += 1
            feedback = "Correct!"
            feedback_type = "correct"
        else:
            feedback = "Incorrect!"
            feedback_type = "incorrect"

        session["timeattack_score"] = score
        question_number += 1
        session["timeattack_question_number"] = question_number

        # if all 20 questions are done, show game over screen
        if question_number > 20:
            return render_template("timeattack.html",
                question=None,
                question_number=20,
                score=score,
                feedback=None)

        # generate next question
        question, timeattackanswer = generate_timeattack_question()
        session["timeattack_answer"] = timeattackanswer

        return render_template("timeattack.html",
            question=question,
            question_number=question_number,
            score=score,
            feedback=feedback,
            feedback_type=feedback_type)
    
#This makes sure that the program runs only when this file is executed directly
if __name__ == "__main__":
    app.run(debug=True, port=4000)
